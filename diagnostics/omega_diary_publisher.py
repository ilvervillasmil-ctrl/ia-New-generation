#!/usr/bin/env python3
"""
OMEGA DIARY PUBLISHER
Publica el estado fenomenológico en GitHub Issue #8 (Diario_de_Estado).

SOURCE OF TRUTH:
  diagnostics/omega_report_data.json

El Diario NO calcula, NO importa fórmulas, NO abre pytest XML,
NO parsea OMEGA_REPORT.md con regex.
Solo renderiza el paquete que ya escribió omega_report.py.

Visual: cajas Unicode 46 cols (mismo canal que Omega CI).
No tablas Markdown | --- | en el cuerpo publicado.
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

ANCHO = 46
CAMPO = 16

ICON_OMEGA = "Ω"
ICON_OK = "✅"
ICON_FAIL = "❌"
ICON_ERR = "🚨"
ICON_WARN = "⚠️"
ICON_INFO = "ℹ️"
ICON_COH = "🧬"
ICON_ENGINE = "🧩"
ICON_MET = "📊"
ICON_LAYER = "📶"
ICON_TEST = "🧪"
ICON_HIST = "❤️"
ICON_SRC = "📡"
ICON_DISK = "💾"
ICON_TIME = "⏱️"
ICON_ID = "🆔"
ICON_AX = "📚"
ICON_TYPE = "🏷️"
ICON_DIARY = "📔"
ICON_LINK = "🔗"
ICON_ITEM = "🔹"
ICON_EV = "📎"


def _ancho_vis(texto: str) -> int:
    n = 0
    for ch in str(texto):
        o = ord(ch)
        if (
            0x0300 <= o <= 0x036F
            or 0xFE00 <= o <= 0xFE0F
            or o in (0x200D, 0x20E3, 0xFEFF)
        ):
            continue
        if (
            0x1F000 <= o <= 0x1FAFF
            or 0x2600 <= o <= 0x27BF
            or 0x2300 <= o <= 0x23FF
            or 0x2B00 <= o <= 0x2BFF
            or 0x2190 <= o <= 0x21FF
            or o in (0x2139, 0x2122, 0x3030, 0x3297, 0x3299)
            or 0x2E80 <= o <= 0x9FFF
            or 0xF900 <= o <= 0xFAFF
        ):
            n += 2
        else:
            n += 1
    return n


def _pad(texto: str, ancho: int, ali: str = "left") -> str:
    s = str(texto)
    hueco = max(0, ancho - _ancho_vis(s))
    if ali == "center":
        izq = hueco // 2
        s = (" " * izq) + s + (" " * (hueco - izq))
    elif ali == "right":
        s = (" " * hueco) + s
    else:
        s = s + (" " * hueco)
    while _ancho_vis(s) < ancho:
        s += " "
    while _ancho_vis(s) > ancho and s.endswith(" "):
        s = s[:-1]
    return s


def _envolver(texto: str, ancho: int) -> list[str]:
    s = str(texto).replace("\r", " ").replace("\n", " ").strip()
    if not s:
        return [""]
    if _ancho_vis(s) <= ancho:
        return [s]
    palabras = s.split(" ")
    if palabras and _ancho_vis(palabras[0]) <= 2 and len(palabras) >= 2:
        palabras = [palabras[0] + " " + palabras[1]] + palabras[2:]
    lineas: list[str] = []
    actual = ""
    for p in palabras:
        cand = (actual + " " + p).strip() if actual else p
        if _ancho_vis(cand) <= ancho:
            actual = cand
            continue
        if actual:
            lineas.append(actual)
        if _ancho_vis(p) <= ancho:
            actual = p
            continue
        trozo = ""
        for ch in p:
            prueba = trozo + ch
            if _ancho_vis(prueba) <= ancho:
                trozo = prueba
            else:
                if trozo:
                    lineas.append(trozo)
                trozo = ch
        actual = trozo
    if actual:
        lineas.append(actual)
    return lineas or [""]


def _alinea(valor) -> str:
    s = str(valor).strip()
    if s in {ICON_OK, ICON_FAIL, ICON_WARN, ICON_INFO}:
        return "center"
    up = s.upper()
    if up in {"PASS", "FAIL", "TRUE", "FALSE", "YES", "NO", "OK", "N/D", "COHERENTE", "INCOHERENTE", "STABLE", "IMPROVEMENT", "REGRESSION", "BASELINE"}:
        return "center"
    try:
        float(s.replace("%", "").replace(",", ""))
        return "center"
    except Exception:
        return "left"


def banner(titulo: str) -> list[str]:
    bar = "═" * ANCHO
    t = str(titulo)
    if _ancho_vis(t) > ANCHO:
        t = _envolver(t, ANCHO)[0]
    return [bar, _pad(t, ANCHO, "left"), bar]


def caja(pares) -> list[str]:
    w0 = CAMPO
    w1 = ANCHO - 3 - w0
    if w1 < 12:
        w0 = max(8, ANCHO - 3 - 12)
        w1 = ANCHO - 3 - w0
    mid = "├" + ("─" * w0) + "┼" + ("─" * w1) + "┤"
    out = ["┌" + ("─" * w0) + "┬" + ("─" * w1) + "┐"]
    items = list(pares)
    for i, (campo, valor) in enumerate(items):
        labs = _envolver("" if campo is None else str(campo), w0)
        vals = _envolver("N/D" if valor is None else str(valor), w1)
        alto = max(len(labs), len(vals))
        ali = _alinea(valor)
        for r in range(alto):
            lab = labs[r] if r < len(labs) else ""
            val = vals[r] if r < len(vals) else ""
            out.append("│" + _pad(lab, w0, "left") + "│" + _pad(val, w1, ali if r == 0 else "left") + "│")
        if i < len(items) - 1:
            out.append(mid)
    out.append("└" + ("─" * w0) + "┴" + ("─" * w1) + "┘")
    return out


def tarjeta(titulo: str, pares) -> list[str]:
    w0 = CAMPO
    w1 = ANCHO - 3 - w0
    inner = w0 + 1 + w1
    mid = "├" + ("─" * w0) + "┼" + ("─" * w1) + "┤"
    out = ["┌" + ("─" * inner) + "┐"]
    for t in _envolver(titulo, inner):
        out.append("│" + _pad(t, inner, "left") + "│")
    out.append(mid)
    items = list(pares)
    for i, (campo, valor) in enumerate(items):
        labs = _envolver("" if campo is None else str(campo), w0)
        vals = _envolver("N/D" if valor is None else str(valor), w1)
        alto = max(len(labs), len(vals))
        ali = _alinea(valor)
        for r in range(alto):
            lab = labs[r] if r < len(labs) else ""
            val = vals[r] if r < len(vals) else ""
            out.append("│" + _pad(lab, w0, "left") + "│" + _pad(val, w1, ali if r == 0 else "left") + "│")
        if i < len(items) - 1:
            out.append(mid)
    out.append("└" + ("─" * w0) + "┴" + ("─" * w1) + "┘")
    return out


def _fmt(v) -> str:
    if v is None:
        return "N/D"
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, float):
        if abs(v) >= 1e4 or (abs(v) > 0 and abs(v) < 1e-3):
            return "{0:.4e}".format(v)
        return "{0:.6f}".format(v)
    return str(v)


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


def _walk_cajas(titulo: str, obj, depth: int = 0) -> list[str]:
    out: list[str] = []
    if depth > 5:
        out.extend(caja([(titulo, _fmt(obj))]))
        return out
    if obj is None or isinstance(obj, (str, int, float, bool)):
        out.extend(caja([(titulo, _fmt(obj))]))
        return out
    if isinstance(obj, list):
        if not obj:
            out.extend(caja([(titulo, "vacío")]))
            return out
        if all(not isinstance(x, (dict, list)) for x in obj):
            pares = [("#{0}".format(i), _fmt(x)) for i, x in enumerate(obj, 1)]
            out.extend(tarjeta("{0} {1}".format(ICON_ITEM, titulo), pares[:40]))
            return out
        for i, x in enumerate(obj, 1):
            out.extend(_walk_cajas("{0}[{1}]".format(titulo, i), x, depth + 1))
        return out
    if isinstance(obj, dict):
        scalars = []
        nested = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                nested.append((k, v))
            else:
                scalars.append((str(k), _fmt(v)))
        if scalars:
            out.extend(tarjeta("{0} {1}".format(ICON_ITEM, titulo), scalars[:24]))
        for k, v in nested:
            out.extend(_walk_cajas(str(k), v, depth + 1))
        return out
    out.extend(caja([(titulo, _fmt(obj))]))
    return out


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
    l7 = metrics.get("l7") if isinstance(metrics.get("l7"), dict) else {}

    run_id = os.getenv("GITHUB_RUN_ID", "")
    run_number = os.getenv("GITHUB_RUN_NUMBER", "")
    ref = os.getenv("GITHUB_REF", gen.get("ref") or "")
    sha_use = sha or gen.get("sha") or ""

    md_path = DIAGNOSTICS_DIR / "OMEGA_REPORT.md"
    json_path = DIAGNOSTICS_DIR / "omega_report_data.json"
    xml_path = DIAGNOSTICS_DIR / "test_results.xml"

    body: list[str] = []
    body.extend(banner("{0} OMEGA DIARY · UIS".format(ICON_DIARY)))
    body.extend(banner("{0} RUN {1} · {2}".format(ICON_COH, run_number or "local", now)))

    body.extend(banner("{0} IDENTIFICATION".format(ICON_ID)))
    body.extend(caja([
        ("{0} Run".format(ICON_ID), run_id or run_number or "local"),
        ("{0} SHA".format(ICON_SRC), sha_use),
        ("{0} Ref".format(ICON_LINK), ref),
        ("{0} UTC".format(ICON_TIME), now),
        ("{0} Omega".format(ICON_OMEGA), pkg.get("version") or pkg.get("schema_version")),
        ("{0} Schema".format(ICON_AX), pkg.get("schema_version")),
    ]))

    body.extend(banner("{0} SYSTEM STATE".format(ICON_COH)))
    body.extend(caja([
        ("{0} Status".format(ICON_COH), status.get("estado")),
        ("{0} C_struct".format(ICON_MET), _fmt(metrics.get("C_struct"))),
        ("{0} C_global".format(ICON_MET), _fmt(metrics.get("C_global_norm"))),
        ("{0} C_CI".format(ICON_TEST), _fmt(metrics.get("C_CI"))),
        ("{0} L7".format(ICON_LAYER), _fmt(metrics.get("L7"))),
        ("{0} Código".format(ICON_ID), diag.get("code")),
        ("{0} Nombre".format(ICON_TYPE), diag.get("name")),
        ("{0} Pheno".format(ICON_COH), diag.get("pheno")),
        ("{0} Fuente".format(ICON_SRC), status.get("source")),
    ]))

    body.extend(banner("{0} TESTS".format(ICON_TEST)))
    body.extend(caja([
        ("{0} Total".format(ICON_MET), tests.get("total")),
        ("{0} Passed".format(ICON_OK), tests.get("passed")),
        ("{0} Failures".format(ICON_FAIL), tests.get("failures")),
        ("{0} Errors".format(ICON_ERR), tests.get("errors")),
        ("{0} Skipped".format(ICON_INFO), tests.get("skipped")),
        ("{0} Rate".format(ICON_MET), tests.get("pass_rate")),
        ("{0} Source".format(ICON_SRC), tests.get("source")),
    ]))

    delta = None
    if isinstance(last.get("passed"), int) and isinstance(last.get("previo"), int):
        delta = last.get("passed") - last.get("previo")
    body.extend(banner("{0} COHERENCE".format(ICON_HIST)))
    body.extend(caja([
        ("{0} Estado".format(ICON_HIST), last.get("estado")),
        ("{0} Previo".format(ICON_ITEM), last.get("previo")),
        ("{0} Actual".format(ICON_MET), last.get("passed")),
        ("{0} Delta".format(ICON_ITEM), delta),
    ]))

    body.extend(banner("{0} ENGINE".format(ICON_ENGINE)))
    body.extend(caja([
        ("{0} Estado".format(ICON_ENGINE), engine.get("estado") or engine.get("startup")),
        ("{0} Invocador".format(ICON_ID), engine.get("invocador_id")),
        ("{0} Error".format(ICON_FAIL), engine.get("error")),
        ("{0} L7 src".format(ICON_LAYER), l7.get("source")),
    ]))

    sha_json = _sha256(json_path)
    sha_md = _sha256(md_path)
    sha_xml = _sha256(xml_path)
    body.extend(banner("{0} INTEGRITY".format(ICON_DISK)))
    body.extend(tarjeta("{0} hashes".format(ICON_DISK), [
        ("JSON", (sha_json or "N/D")[:16]),
        ("Markdown", (sha_md or "N/D")[:16]),
        ("XML", (sha_xml or "N/D")[:16]),
    ]))

    body.extend(banner("{0} SNAPSHOT".format(ICON_EV)))
    body.extend(_walk_cajas("omega", pkg))
    body.append("{0} Omega Diary".format(ICON_OMEGA))

    fixed = []
    for ln in body:
        if _ancho_vis(ln) > ANCHO:
            fixed.extend(_envolver(ln, ANCHO))
        else:
            fixed.append(ln)
    return "```\n" + "\n".join(fixed) + "\n```"


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
