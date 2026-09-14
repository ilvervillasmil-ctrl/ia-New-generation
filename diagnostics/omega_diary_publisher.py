#!/usr/bin/env python3
"""
OMEGA DIARY PUBLISHER
Publica el estado fenomenológico en GitHub Issue #8 (Diario_de_Estado).

SOURCE OF TRUTH:
  diagnostics/omega_report_data.json

El Diario NO calcula, NO importa fórmulas, NO abre pytest XML,
NO parsea OMEGA_REPORT.md con regex.
Solo renderiza el paquete que ya escribió omega_report.py.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
import urllib.error


ISSUE_NUMBER = 8
REPO_OWNER = "ilvervillasmil-ctrl"
REPO_NAME = "Universal-Integration-System"

CURRENT_FILE = Path(__file__).resolve()
DIAGNOSTICS_DIR = CURRENT_FILE.parent


def _sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_omega_package() -> dict | None:
    json_path = DIAGNOSTICS_DIR / "omega_report_data.json"
    if not json_path.exists():
        print("ERROR: diagnostics/omega_report_data.json no existe.")
        print("       Corre omega_report.py primero.")
        return None
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        print("INFO: Loaded omega_report_data.json")
        return data if isinstance(data, dict) else {"value": data}
    except Exception as exc:
        print("ERROR: no se pudo leer omega_report_data.json — {0}".format(exc))
        return None


def _cell(v) -> str:
    if v is None:
        return "N/D"
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, float):
        if abs(v) >= 1e4 or (abs(v) > 0 and abs(v) < 1e-3):
            return "{0:.4e}".format(v)
        return "{0:.6f}".format(v)
    text = str(v).replace("\n", " ").replace("|", "\\|")
    return text


def _md_table(headers, rows) -> list[str]:
    out = [
        "| " + " | ".join(str(h) for h in headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        cells = list(row) + [""] * (len(headers) - len(row))
        out.append("| " + " | ".join(_cell(c) for c in cells[: len(headers)]) + " |")
    return out


def _walk(title: str, obj, depth: int = 0) -> list[str]:
    lines: list[str] = []
    if depth > 6:
        lines.append(_cell(obj))
        return lines
    if obj is None or isinstance(obj, (str, int, float, bool)):
        lines.extend(_md_table(["Campo", "Valor"], [[title, obj]]))
        return lines
    if isinstance(obj, list):
        if not obj:
            lines.append("_{0}: vacío_".format(title))
            return lines
        if all(not isinstance(x, (dict, list)) for x in obj):
            lines.extend(_md_table(["#", title], [[i + 1, x] for i, x in enumerate(obj)]))
            return lines
        if all(isinstance(x, dict) for x in obj):
            keys = []
            for x in obj:
                for k in x.keys():
                    if k not in keys:
                        keys.append(k)
            keys = keys[:8]
            rows = []
            for i, x in enumerate(obj, 1):
                rows.append([i] + [x.get(k) for k in keys])
            lines.extend(_md_table(["#"] + [str(k) for k in keys], rows))
            return lines
        for i, x in enumerate(obj, 1):
            lines.append("#### {0}[{1}]".format(title, i))
            lines.extend(_walk("{0}[{1}]".format(title, i), x, depth + 1))
        return lines
    if isinstance(obj, dict):
        scalars = []
        nested = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                nested.append((k, v))
            else:
                scalars.append([k, v])
        if scalars:
            lines.extend(_md_table(["Campo", "Valor"], scalars))
        for k, v in nested:
            lines.append("")
            lines.append("#### {0}".format(k))
            lines.extend(_walk(str(k), v, depth + 1))
        return lines
    lines.append(_cell(obj))
    return lines


def format_diary_entry(pkg: dict, sha: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    gen = pkg.get("generated") if isinstance(pkg.get("generated"), dict) else {}
    metrics = pkg.get("metrics") if isinstance(pkg.get("metrics"), dict) else {}
    diag = pkg.get("diagnostic") if isinstance(pkg.get("diagnostic"), dict) else {}
    tests = pkg.get("tests") if isinstance(pkg.get("tests"), dict) else {}
    engine = pkg.get("engine") if isinstance(pkg.get("engine"), dict) else {}
    status = pkg.get("system_status") if isinstance(pkg.get("system_status"), dict) else {}
    hist = pkg.get("history") if isinstance(pkg.get("history"), list) else []
    last = hist[-1] if hist and isinstance(hist[-1], dict) else {}

    run_id = os.getenv("GITHUB_RUN_ID", "")
    run_number = os.getenv("GITHUB_RUN_NUMBER", "")
    ref = os.getenv("GITHUB_REF", gen.get("ref") or "")
    sha_use = sha or gen.get("sha") or ""

    md_path = DIAGNOSTICS_DIR / "OMEGA_REPORT.md"
    json_path = DIAGNOSTICS_DIR / "omega_report_data.json"
    xml_path = DIAGNOSTICS_DIR / "test_results.xml"

    lines = [
        "# 📔 OMEGA DIARY — Universal Integration System",
        "",
        "## 🧬 Run {0} · {1}".format(run_number or "local", now),
        "",
        "### 🆔 Identification",
        "",
    ]
    lines.extend(_md_table(
        ["Campo", "Valor"],
        [
            ["🆔 Run", run_id or run_number or "local"],
            ["📡 SHA", sha_use],
            ["🔗 Ref", ref],
            ["⏱️ UTC", now],
            ["Ω Omega", pkg.get("version") or pkg.get("schema_version")],
            ["📚 Schema", pkg.get("schema_version")],
        ],
    ))
    lines += ["", "### 🧬 System State", ""]
    lines.extend(_md_table(
        ["Métrica", "Valor", "Fuente"],
        [
            ["🧬 System status", status.get("estado"), status.get("source")],
            ["📊 C_struct", metrics.get("C_struct"), metrics.get("coherence_source")],
            ["📊 C_global", metrics.get("C_global_norm"), metrics.get("coherence_source")],
            ["🧪 C_CI", metrics.get("C_CI"), tests.get("source")],
            ["📶 L7", metrics.get("L7"), (metrics.get("l7") or {}).get("source") if isinstance(metrics.get("l7"), dict) else None],
            ["🆔 Código", diag.get("code"), "omega_report"],
            ["🏷️ Estado", diag.get("name"), "omega_report"],
            ["🧬 Pheno", diag.get("pheno"), "omega_report"],
        ],
    ))
    lines += ["", "### 🧪 Tests", ""]
    lines.extend(_md_table(
        ["Total", "Passed", "Failures", "Errors", "Skipped", "Rate"],
        [[
            tests.get("total"),
            tests.get("passed"),
            tests.get("failures"),
            tests.get("errors"),
            tests.get("skipped"),
            tests.get("pass_rate"),
        ]],
    ))
    lines += ["", "### ❤️ Coherence", ""]
    lines.extend(_md_table(
        ["Estado", "Previo", "Actual", "Delta"],
        [[
            last.get("estado"),
            last.get("previo"),
            last.get("passed"),
            (last.get("passed") - last.get("previo")) if isinstance(last.get("passed"), int) and isinstance(last.get("previo"), int) else None,
        ]],
    ))
    lines += ["", "### 🧩 Engine", ""]
    lines.extend(_md_table(
        ["Campo", "Valor"],
        [
            ["Estado", engine.get("estado") or engine.get("startup")],
            ["Invocador", engine.get("invocador_id")],
            ["Error", engine.get("error")],
        ],
    ))
    lines += ["", "### 💾 Integrity", ""]
    lines.extend(_md_table(
        ["Artefacto", "SHA-256"],
        [
            ["omega_report_data.json", _sha256(json_path)],
            ["OMEGA_REPORT.md", _sha256(md_path)],
            ["test_results.xml", _sha256(xml_path)],
        ],
    ))
    lines += [
        "",
        "<details>",
        "<summary>📎 Snapshot completo del run</summary>",
        "",
    ]
    lines.extend(_walk("omega", pkg))
    lines += [
        "",
        "</details>",
        "",
        "---",
        "*Publicado por Omega Diary — renderer puro, sin cálculos propios.*",
    ]
    return "\n".join(lines)


def publish_to_github(body: str) -> bool:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("WARNING: GITHUB_TOKEN not set — skipping publication (non-fatal).")
        return False

    url = (
        "https://api.github.com/repos/"
        + REPO_OWNER + "/" + REPO_NAME
        + "/issues/" + str(ISSUE_NUMBER) + "/comments"
    )
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "Omega-CI",
    }
    data = json.dumps({"body": body}).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print("✓ Diario_de_Estado updated — " + result.get("html_url", "N/A"))
            return True
    except urllib.error.HTTPError as exc:
        body_err = exc.read().decode("utf-8", errors="replace")
        print("WARNING: HTTP " + str(exc.code) + " — " + exc.reason)
        print("  Response: " + body_err)
        return False
    except Exception as exc:
        print("WARNING: Could not publish — " + str(exc))
        return False


def main() -> None:
    print()
    print("=" * 60)
    print("OMEGA DIARY PUBLISHER  [renderer — no calculator]")
    print("=" * 60)

    sha = os.getenv("GITHUB_SHA", "local")[:12]
    report = load_omega_package()
    if report is None:
        print("ERROR: Could not load Omega package — skipping diary.")
        sys.exit(0)

    print("INFO: version  = " + str(report.get("version")))
    print("INFO: schema   = " + str(report.get("schema_version")))
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    print("INFO: C_struct = " + str(metrics.get("C_struct")))
    print("INFO: L7       = " + str(metrics.get("L7")))

    entry = format_diary_entry(report, sha)
    print()
    print(entry)
    print()

    success = publish_to_github(entry)
    if success:
        print("✓ Omega Diary published successfully.")
    else:
        print("⚠ Diary publication skipped or failed (non-fatal).")
    sys.exit(0)


if __name__ == "__main__":
    main()
