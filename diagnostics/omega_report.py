#!/usr/bin/env python3
"""
OMEGA REPORT — Extreme Audit Renderer
Universal Integration System

paquete → JSON + Markdown + stdout CI
Nunca Markdown → regex → JSON.
Omega no inventa coherencia, módulos, capas ni APIs.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import platform
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CURRENT_FILE = Path(__file__).resolve()
DIAGNOSTICS_DIR = CURRENT_FILE.parent
REPO_ROOT = DIAGNOSTICS_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

OMEGA_VERSION = "3.1-uis-extreme"
SCHEMA_VERSION = "omega.uis.1"

SKIP_DIR_NAMES = {
    ".git", ".hg", ".svn", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".venv", "venv", "node_modules", ".tox",
}
SECRET_MARKERS = (
    "TOKEN", "SECRET", "PASSWORD", "PASSWD", "APIKEY", "API_KEY",
    "PRIVATE_KEY", "CREDENTIAL", "AWS_SECRET", "AUTHORIZATION",
)
CI_JSON_ARTIFACTS = (
    ("axioms", "axioms_report.json"),
    ("generatividad", "generatividad_report.json"),
    ("contratos", "contratos_report.json"),
    ("evaluaciones", "evaluaciones.json"),
)

ICON_OMEGA = "Ω"
ICON_OK = "✅"
ICON_FAIL = "❌"
ICON_WARN = "⚠️"
ICON_ERR = "🚨"
ICON_INFO = "ℹ️"
ICON_SKIP = "⏭️"
ICON_COH = "🧬"
ICON_ENGINE = "🧩"
ICON_PKG = "📦"
ICON_REPO = "🗂️"
ICON_DIR = "📁"
ICON_FILE = "📄"
ICON_PY = "🐍"
ICON_CONTRACT = "📜"
ICON_FN = "⚙️"
ICON_NUM = "🔢"
ICON_MET = "📊"
ICON_FORM = "📐"
ICON_LAYER = "📶"
ICON_GEN = "🧠"
ICON_AX = "📚"
ICON_TEST = "🧪"
ICON_HIST = "❤️"
ICON_DEP = "🔗"
ICON_GRAPH = "🕸️"
ICON_SRC = "📡"
ICON_EV = "📎"
ICON_DISK = "💾"
ICON_LOCK = "🔐"
ICON_AUDIT = "🔎"
ICON_TYPE = "🏷️"
ICON_TIME = "⏱️"
ICON_ID = "🆔"
ICON_DER = "🔄"
ICON_RES = "🎯"
ICON_BAN = "🚫"
ICON_ITEM = "🔹"

W = "════════════════════════════════════════════"
S = "────────────────────────────────────────────"

FINDINGS: list[dict[str, Any]] = []
RENDERED_PATHS: set[str] = set()


def finding(severity: str, category: str, component: str, message: str, source: str = "omega") -> None:
    FINDINGS.append({
        "severity": severity,
        "category": category,
        "component": component,
        "source": source,
        "message": message,
    })


def _is_secret_name(name: str) -> bool:
    up = (name or "").upper()
    return any(m in up for m in SECRET_MARKERS)


def _sorted_set(values: Any) -> list[Any]:
    try:
        return sorted(values, key=lambda x: repr(x))
    except Exception:
        return list(values)


def _json_ready(obj: Any, field_name: str = "") -> Any:
    if _is_secret_name(field_name):
        return "[REDACTED]"
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, set):
        return {"__type__": "set", "items": [_json_ready(x) for x in _sorted_set(obj)]}
    if isinstance(obj, dict):
        return {str(k): _json_ready(v, str(k)) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_ready(x) for x in obj]
    try:
        json.dumps(obj, default=str)
        return obj
    except Exception:
        return {"type": type(obj).__name__, "repr": repr(obj)}


def iter_leaf_paths(obj: Any, prefix: str = "") -> list[str]:
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return [prefix or "$"]
    if isinstance(obj, dict):
        if not obj:
            return [prefix or "$"]
        out: list[str] = []
        for k, v in obj.items():
            path = "{0}.{1}".format(prefix, k) if prefix else str(k)
            out.extend(iter_leaf_paths(v, path))
        return out
    if isinstance(obj, (list, tuple)):
        if not obj:
            return [prefix or "$"]
        out = []
        for i, v in enumerate(obj):
            path = "{0}[{1}]".format(prefix, i) if prefix else "[{0}]".format(i)
            out.extend(iter_leaf_paths(v, path))
        return out
    return [prefix or "$"]


def _ext_bucket(path: Path) -> str:
    ext = path.suffix.lower()
    mapping = {
        ".py": "python", ".md": "markdown", ".json": "json",
        ".yml": "yaml", ".yaml": "yaml", ".toml": "toml",
        ".txt": "txt", ".ini": "ini", ".cfg": "ini", ".xml": "xml",
    }
    if ext in mapping:
        return mapping[ext]
    if ext in {".so", ".bin", ".exe", ".dll", ".dylib", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf"}:
        return "binary"
    return "other"


def _sha256(path: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        finding("WARNING", "hash", str(path), str(e))
        return None


def _literal(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.List):
        return [_literal(x) for x in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(_literal(x) for x in node.elts)
    if isinstance(node, ast.Set):
        return {"__type__": "set", "items": [_literal(x) for x in node.elts]}
    if isinstance(node, ast.Dict):
        out = {}
        for k, v in zip(node.keys, node.values):
            if k is None:
                continue
            out[str(_literal(k))] = _literal(v)
        return out
    return None


def _parse_python(path: Path, rel: str) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "path": rel,
        "lines": 0,
        "parse_ok": False,
        "parse_error": None,
        "classes": [],
        "functions": [],
        "assigns": [],
        "imports": [],
    }
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        rec["parse_error"] = str(e)
        finding("ERROR", "read", rel, str(e))
        return rec
    rec["lines"] = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
    try:
        tree = ast.parse(text)
        rec["parse_ok"] = True
    except SyntaxError as e:
        rec["parse_error"] = "SyntaxError: {0}".format(e)
        finding("ERROR", "parse", rel, rec["parse_error"])
        return rec

    def decos(node: ast.AST) -> list[str]:
        raw = getattr(node, "decorator_list", []) or []
        out = []
        for d in raw:
            try:
                out.append(ast.unparse(d) if hasattr(ast, "unparse") else ast.dump(d))
            except Exception:
                out.append("?")
        return out

    for node in tree.body:
        if isinstance(node, ast.Import):
            for a in node.names:
                rec["imports"].append({"kind": "import", "name": a.name, "asname": a.asname, "relative": 0})
        elif isinstance(node, ast.ImportFrom):
            rec["imports"].append({
                "kind": "from",
                "module": node.module,
                "names": [a.name for a in node.names],
                "relative": node.level or 0,
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            rec["functions"].append({
                "name": node.name,
                "async": isinstance(node, ast.AsyncFunctionDef),
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", None),
                "args": [a.arg for a in node.args.args],
                "decorators": decos(node),
                "public": not node.name.startswith("_"),
                "doc": ast.get_docstring(node) or "",
            })
        elif isinstance(node, ast.ClassDef):
            methods_pub = []
            methods_priv_n = 0
            for n in node.body:
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if n.name.startswith("_"):
                        methods_priv_n += 1
                    else:
                        methods_pub.append(n.name)
            rec["classes"].append({
                "name": node.name,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", None),
                "bases": [
                    ast.unparse(b) if hasattr(ast, "unparse") else getattr(b, "id", "?")
                    for b in node.bases
                ],
                "decorators": decos(node),
                "methods_public": methods_pub,
                "methods_private_n": methods_priv_n,
                "doc": ast.get_docstring(node) or "",
            })
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and not t.id.startswith("_"):
                    rec["assigns"].append({
                        "name": t.id,
                        "line": node.lineno,
                        "annotation": None,
                        "literal": _literal(node.value),
                    })
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if not node.target.id.startswith("_"):
                ann = None
                try:
                    ann = ast.unparse(node.annotation) if hasattr(ast, "unparse") else None
                except Exception:
                    ann = None
                rec["assigns"].append({
                    "name": node.target.id,
                    "line": node.lineno,
                    "annotation": ann,
                    "literal": _literal(node.value) if node.value is not None else None,
                })
    return rec


def build_repository_inventory() -> dict[str, Any]:
    files_out: list[dict[str, Any]] = []
    dirs_out: list[dict[str, Any]] = []
    python_out: list[dict[str, Any]] = []
    summary = {
        "files": 0, "directories": 0, "python": 0, "markdown": 0, "json": 0,
        "yaml": 0, "toml": 0, "txt": 0, "ini": 0, "xml": 0, "binary": 0,
        "other": 0, "bytes": 0, "hashed": 0, "unreadable": 0, "symlinks": 0,
    }
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIR_NAMES)
        base = Path(dirpath)
        try:
            rel_dir = str(base.relative_to(REPO_ROOT))
        except ValueError:
            continue
        dirs_out.append({"path": rel_dir, "type": "directory"})
        summary["directories"] += 1
        for name in sorted(filenames):
            path = base / name
            try:
                rel = str(path.relative_to(REPO_ROOT))
            except ValueError:
                continue
            is_link = path.is_symlink()
            target = None
            if is_link:
                summary["symlinks"] += 1
                try:
                    target = os.readlink(path)
                except Exception as e:
                    finding("WARNING", "symlink", rel, str(e))
            bucket = _ext_bucket(path)
            readable = True
            try:
                size = path.stat().st_size
            except Exception as e:
                size = None
                readable = False
                summary["unreadable"] += 1
                finding("WARNING", "stat", rel, str(e))
            summary["files"] += 1
            summary["bytes"] += size or 0
            summary[bucket] = summary.get(bucket, 0) + 1
            digest = None
            if readable and bucket in {"python", "json", "yaml", "toml", "ini", "xml", "markdown", "txt"}:
                digest = _sha256(path)
                if digest:
                    summary["hashed"] += 1
            files_out.append({
                "path": rel, "type": bucket, "bytes": size, "sha256": digest,
                "symlink": is_link, "target": target, "readable": readable,
            })
            if bucket == "python":
                python_out.append(_parse_python(path, rel))
    return {"summary": summary, "directories": dirs_out, "files": files_out, "python": python_out}


def _public_state(obj: Any) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if obj is None:
        return out
    names = []
    data = getattr(obj, "__dict__", None)
    if isinstance(data, dict):
        names.extend(data.keys())
    names.extend(n for n in dir(obj) if not n.startswith("_"))
    seen = set()
    for name in names:
        if name in seen or name.startswith("_"):
            continue
        seen.add(name)
        try:
            val = getattr(obj, name)
        except Exception as e:
            finding("WARNING", "engine_attr", name, str(e))
            continue
        if callable(val):
            continue
        out[name] = _json_ready(val, name)
    return out


def collect_engine() -> dict[str, Any]:
    state: dict[str, Any] = {
        "available": False,
        "startup": "UNAVAILABLE",
        "class": "Engine",
        "constructor": "Engine(REPO_ROOT/modules, invocador_id='omega', strict=True)",
        "estado": None,
        "invocador_id": None,
        "error_type": None,
        "error": None,
        "paquete_from_engine": False,
        "package": None,
        "public": {},
        "census": None,
        "containers": [],
    }
    try:
        from core.engine import Engine, ArranqueError  # noqa: F401
    except Exception as e:
        state["error_type"] = type(e).__name__
        state["error"] = str(e)
        state["startup"] = "ERROR"
        finding("ERROR", "engine_import", "core.engine", "{0}: {1}".format(type(e).__name__, e))
        return state
    try:
        from core.engine import Engine
        eng = Engine(REPO_ROOT / "modules", invocador_id="omega", strict=True)
    except Exception as e:
        state["error_type"] = type(e).__name__
        state["error"] = str(e)
        state["startup"] = "ERROR"
        finding("ERROR", "engine_start", "core.engine.Engine", "{0}: {1}".format(type(e).__name__, e))
        return state

    state["available"] = True
    state["startup"] = "OK"
    state["estado"] = getattr(eng, "estado", None)
    state["invocador_id"] = getattr(eng, "invocador_id", None)
    state["public"] = _public_state(eng)

    if hasattr(eng, "censar") and callable(eng.censar):
        try:
            state["census"] = _json_ready(eng.censar(), "census")
        except Exception as e:
            finding("ERROR", "engine_census", "Engine.censar", str(e))
            state["census_error"] = str(e)

    registro = getattr(eng, "registro", None)
    raw_list = None
    if registro is not None:
        for attr in ("contenedores", "items", "todos"):
            cand = getattr(registro, attr, None)
            if cand is None:
                continue
            try:
                raw_list = list(cand() if callable(cand) else cand)
                break
            except Exception:
                continue
        if raw_list is None and hasattr(registro, "primero"):
            roles = []
            census = state.get("census") or {}
            if isinstance(census, dict):
                roles = list((census.get("roles") or {}).keys())
            raw_list = []
            for rol in roles:
                try:
                    raw_list.append(registro.primero(rol))
                except Exception as e:
                    finding("WARNING", "registro", str(rol), str(e))
        state["containers"] = [_public_state(c) for c in (raw_list or []) if c is not None]

    if hasattr(eng, "paquete_omega") and callable(eng.paquete_omega):
        try:
            pkg = eng.paquete_omega()
            if isinstance(pkg, dict):
                state["paquete_from_engine"] = True
                state["package"] = _json_ready(pkg)
        except Exception as e:
            finding("ERROR", "paquete_omega", "Engine.paquete_omega", str(e))
            state["package_error"] = str(e)
    return state


def _read_json_artifact(filename: str) -> dict[str, Any]:
    path = DIAGNOSTICS_DIR / filename
    rec = {
        "path": "diagnostics/{0}".format(filename),
        "present": path.exists(),
        "bytes": None,
        "read_ok": False,
        "error": None,
        "data": None,
    }
    if not path.exists():
        finding("INFO", "artifact", rec["path"], "ausente")
        return rec
    try:
        rec["bytes"] = path.stat().st_size
    except Exception as e:
        rec["error"] = str(e)
        finding("WARNING", "artifact", rec["path"], str(e))
        return rec
    try:
        rec["data"] = json.loads(path.read_text(encoding="utf-8"))
        rec["read_ok"] = True
    except Exception as e:
        rec["error"] = str(e)
        finding("ERROR", "artifact", rec["path"], str(e))
    return rec


def read_test_results() -> dict[str, Any]:
    xml_path = DIAGNOSTICS_DIR / "test_results.xml"
    tests_dir = REPO_ROOT / "tests"
    discovered = []
    if tests_dir.exists():
        discovered = sorted(str(p.relative_to(REPO_ROOT)) for p in tests_dir.rglob("test_*.py"))
    base = {
        "path": "diagnostics/test_results.xml",
        "present": xml_path.exists(),
        "source": "diagnostics/test_results.xml" if xml_path.exists() else "unavailable",
        "executed": False,
        "discovered_files": discovered,
        "discovered_n": len(discovered),
        "total": None, "passed": None, "failures": None, "errors": None,
        "failed": None, "skipped": None, "rate": None, "duration": None,
        "suites": [], "cases": [], "error": None,
    }
    if not xml_path.exists():
        finding("INFO", "tests", base["path"], "artefacto ausente")
        return base
    try:
        root = ET.parse(xml_path).getroot()
    except Exception as e:
        base["error"] = str(e)
        finding("ERROR", "tests", base["path"], str(e))
        return base
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    total = failures = errors = skipped = 0
    duration = 0.0
    suite_rows = []
    cases = []
    for s in suites:
        t = int(s.get("tests", 0) or 0)
        f = int(s.get("failures", 0) or 0)
        e = int(s.get("errors", 0) or 0)
        k = int(s.get("skipped", 0) or 0)
        try:
            dur = float(s.get("time") or 0)
        except Exception:
            dur = 0.0
        total += t
        failures += f
        errors += e
        skipped += k
        duration += dur
        suite_rows.append({
            "name": s.get("name"), "tests": t, "failures": f, "errors": e,
            "skipped": k, "passed": t - f - e - k, "time": dur,
        })
        for tc in s.iter("testcase"):
            status = "passed"
            detail = None
            if tc.find("failure") is not None:
                status = "failure"
                node = tc.find("failure")
                detail = ((node.get("message") or "") + "\n" + (node.text or "")).strip()
            elif tc.find("error") is not None:
                status = "error"
                node = tc.find("error")
                detail = ((node.get("message") or "") + "\n" + (node.text or "")).strip()
            elif tc.find("skipped") is not None:
                status = "skipped"
                node = tc.find("skipped")
                detail = node.get("message") or node.text
            try:
                ttime = float(tc.get("time") or 0)
            except Exception:
                ttime = None
            cases.append({
                "classname": tc.get("classname"), "name": tc.get("name"),
                "time": ttime, "status": status, "detail": detail,
            })
    failed = failures + errors
    passed = total - failed - skipped
    base.update({
        "executed": True, "total": total, "passed": passed, "failures": failures,
        "errors": errors, "failed": failed, "skipped": skipped,
        "rate": (passed / total * 100.0) if total else None,
        "duration": duration, "suites": suite_rows, "cases": cases,
    })
    return base


def read_history() -> dict[str, Any]:
    path = DIAGNOSTICS_DIR / "coherence_history.json"
    rec = {"path": "diagnostics/coherence_history.json", "present": path.exists(), "read_ok": False, "data": [], "error": None}
    if not path.exists():
        finding("INFO", "history", rec["path"], "ausente")
        return rec
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        rec["data"] = data if isinstance(data, list) else [data]
        rec["read_ok"] = True
    except Exception as e:
        rec["error"] = str(e)
        finding("ERROR", "history", rec["path"], str(e))
    return rec


def build_ci_evidence() -> dict[str, Any]:
    ev: dict[str, Any] = {}
    for key, filename in CI_JSON_ARTIFACTS:
        ev[key] = _read_json_artifact(filename)
    ev["tests"] = read_test_results()
    ev["coherence_history"] = read_history()
    return ev


def derive_system_status(ci: dict[str, Any], engine: dict[str, Any]) -> dict[str, Any]:
    contratos = (ci.get("contratos") or {}).get("data")
    if isinstance(contratos, dict) and "incoherente" in contratos:
        return {
            "coherente": (not bool(contratos.get("incoherente"))),
            "estado": "COHERENTE" if not contratos.get("incoherente") else "INCOHERENTE",
            "source": "diagnostics/contratos_report.json:incoherente",
            "source_type": "DERIVED_ADAPTER",
            "note": "coherente = not contratos_report['incoherente']",
        }
    axioms = (ci.get("axioms") or {}).get("data")
    if isinstance(axioms, dict) and "coherente" in axioms:
        return {
            "coherente": bool(axioms.get("coherente")),
            "estado": "COHERENTE" if axioms.get("coherente") else "INCOHERENTE",
            "source": "diagnostics/axioms_report.json:coherente",
            "source_type": "CI_ARTIFACT",
            "note": None,
        }
    if engine.get("estado"):
        return {
            "coherente": None,
            "estado": engine.get("estado"),
            "source": "Engine.estado",
            "source_type": "ENGINE",
            "note": "estado de arranque; no equivale a coherencia global",
        }
    return {
        "coherente": None,
        "estado": "N/D",
        "source": None,
        "source_type": "UNAVAILABLE",
        "note": "ninguna autoridad de coherencia global disponible",
    }


def _classify_import(name: str, internal_roots: set[str]) -> str:
    if not name:
        return "unknown"
    root = name.split(".")[0]
    if root in internal_roots:
        return "internal"
    stdlib = set(getattr(sys, "stdlib_module_names", set()))
    if root in stdlib:
        return "stdlib"
    return "third-party"


def _spec_exists(name: str) -> bool | None:
    if not name:
        return None
    try:
        spec = importlib.util.find_spec(name)
        return spec is not None
    except (ImportError, ValueError, ModuleNotFoundError):
        return False
    except Exception:
        return None


def build_dependency_graph(python_rows: list[dict[str, Any]]) -> dict[str, Any]:
    nodes = []
    for row in python_rows:
        rel = row.get("path") or ""
        if rel.endswith(".py"):
            parts = Path(rel).with_suffix("").parts
            if parts and parts[-1] == "__init__":
                parts = parts[:-1]
            if parts:
                nodes.append(".".join(parts))
    internal = set(nodes)
    roots = {n.split(".")[0] for n in internal}
    edges = []
    unresolved = []
    for row in python_rows:
        rel = row.get("path") or ""
        parts = Path(rel).with_suffix("").parts
        if parts and parts[-1] == "__init__":
            parts = parts[:-1]
        src = ".".join(parts) if parts else rel
        for imp in row.get("imports") or []:
            if imp.get("kind") == "import":
                target = imp.get("name")
            else:
                target = imp.get("module")
                if imp.get("relative"):
                    parent = src.split(".")[:-imp["relative"]]
                    tail = (target.split(".") if target else [])
                    target = ".".join([p for p in parent + tail if p])
            if not target:
                continue
            kind = _classify_import(target, roots)
            if kind == "internal":
                resolved = target in internal or target.split(".")[0] in roots
            elif kind == "stdlib":
                resolved = True
            else:
                resolved = _spec_exists(target.split(".")[0])
            edge = {"from": src, "to": target, "kind": kind, "resolved": resolved}
            edges.append(edge)
            if resolved is False:
                unresolved.append(edge)

    adj: dict[str, list[str]] = {}
    for e in edges:
        if e["kind"] == "internal":
            adj.setdefault(e["from"], []).append(e["to"])
    index = 0
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    onstack: set[str] = set()
    cycles: list[list[str]] = []

    def strongconnect(v: str) -> None:
        nonlocal index
        indices[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        onstack.add(v)
        for w in adj.get(v, []):
            if w not in indices:
                adj.setdefault(w, [])
                strongconnect(w)
                if w in low:
                    low[v] = min(low[v], low[w])
            elif w in onstack:
                low[v] = min(low[v], indices[w])
        if low.get(v) == indices.get(v):
            comp = []
            while True:
                w = stack.pop()
                onstack.discard(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1:
                cycles.append(comp)

    for v in list(adj.keys()):
        if v not in indices:
            strongconnect(v)

    return {
        "nodes": sorted(internal),
        "edges": edges,
        "unresolved": unresolved,
        "cycles": cycles,
        "cycles_status": "EVALUATED",
    }


def collect_constants(python_rows: list[dict[str, Any]]) -> dict[str, Any]:
    declared = []
    for row in python_rows:
        for a in row.get("assigns") or []:
            name = a.get("name") or ""
            if name.isupper():
                declared.append({
                    "name": name, "path": row.get("path"), "line": a.get("line"),
                    "literal": a.get("literal"), "annotation": a.get("annotation"),
                    "source_type": "REPOSITORY_STATIC", "class": "DECLARED",
                })
    runtime = []
    try:
        from modules.constante import ALPHA, BETA
        runtime.append({
            "name": "ALPHA", "value": _json_ready(ALPHA, "ALPHA"),
            "type": type(ALPHA).__name__, "source": "modules.constante.ALPHA",
            "source_type": "RUNTIME_INTROSPECTION", "class": "DECLARED",
            "measured": True, "fallback": False,
        })
        runtime.append({
            "name": "BETA", "value": _json_ready(BETA, "BETA"),
            "type": type(BETA).__name__, "source": "modules.constante.BETA",
            "source_type": "RUNTIME_INTROSPECTION", "class": "DECLARED",
            "measured": True, "fallback": False,
        })
    except Exception as e:
        finding("ERROR", "constants", "modules.constante", "{0}: {1}".format(type(e).__name__, e))
        for n in ("ALPHA", "BETA"):
            runtime.append({
                "name": n, "value": None,
                "source": "modules.constante.{0}".format(n),
                "source_type": "UNAVAILABLE", "class": "UNAVAILABLE",
                "measured": False, "fallback": False, "error": str(e),
            })
    return {"invariants_ci": runtime, "static_uppercase": declared}


def build_paquete() -> dict[str, Any]:
    FINDINGS.clear()
    inventory = build_repository_inventory()
    engine = collect_engine()
    ci = build_ci_evidence()
    system_status = derive_system_status(ci, engine)
    deps = build_dependency_graph(inventory.get("python") or [])
    constants = collect_constants(inventory.get("python") or [])
    py = inventory.get("python") or []
    coverage = {
        "files_discovered": (inventory.get("summary") or {}).get("files"),
        "files_unreadable": (inventory.get("summary") or {}).get("unreadable"),
        "directories_discovered": (inventory.get("summary") or {}).get("directories"),
        "python_discovered": (inventory.get("summary") or {}).get("python"),
        "python_parsed": sum(1 for p in py if p.get("parse_ok")),
        "python_parse_error": sum(1 for p in py if not p.get("parse_ok")),
        "functions_static": sum(len(p.get("functions") or []) for p in py),
        "classes_static": sum(len(p.get("classes") or []) for p in py),
        "assigns_static": sum(len(p.get("assigns") or []) for p in py),
        "engine_available": engine.get("available"),
        "engine_containers": len(engine.get("containers") or []),
        "engine_paquete": engine.get("paquete_from_engine"),
        "artifacts_expected": len(CI_JSON_ARTIFACTS) + 2,
        "artifacts_present": sum(
            1 for k, _ in CI_JSON_ARTIFACTS if (ci.get(k) or {}).get("present")
        ) + int(bool((ci.get("tests") or {}).get("present"))) + int(bool((ci.get("coherence_history") or {}).get("present"))),
        "tests_discovered": (ci.get("tests") or {}).get("discovered_n"),
        "tests_executed": (ci.get("tests") or {}).get("executed"),
        "findings_n": None,
    }
    generated = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "omega_version": OMEGA_VERSION,
        "schema_version": SCHEMA_VERSION,
        "sha": (os.environ.get("GITHUB_SHA") or "local")[:12],
        "ref": os.environ.get("GITHUB_REF") or "",
        "run_id": os.environ.get("GITHUB_RUN_ID") or "",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "repository": REPO_ROOT.name,
    }
    pkg = {
        "schema_version": SCHEMA_VERSION,
        "generated": generated,
        "authority": {
            "engine_constructor": engine.get("constructor"),
            "paquete_from_engine": engine.get("paquete_from_engine"),
            "system_status_source": system_status.get("source"),
        },
        "system_status": system_status,
        "engine": {
            "state": {k: engine[k] for k in engine if k not in {"package", "containers", "census", "public"}},
            "public": engine.get("public"),
            "census": engine.get("census"),
            "containers": engine.get("containers"),
            "package": engine.get("package"),
        },
        "repository": inventory,
        "ci_evidence": ci,
        "omega_observation": {"constants": constants, "dependencies": deps},
        "coverage": coverage,
        "findings": list(FINDINGS),
    }
    pkg["coverage"]["findings_n"] = len(pkg["findings"])
    return pkg


def md_cell(value: Any) -> str:
    text = "N/D" if value is None else str(value)
    return text.replace("\n", " ").replace("|", "\\|").replace("`", "'")


def md_table(headers: list[str], rows: list[list[Any]], align: list[str] | None = None) -> str:
    line1 = "| " + " | ".join(headers) + " |"
    marks = []
    for i, _h in enumerate(headers):
        a = (align[i] if align and i < len(align) else "left")
        marks.append(":---:" if a == "center" else ("---:" if a == "right" else "---"))
    line2 = "| " + " | ".join(marks) + " |"
    body = ["| " + " | ".join(md_cell(c) for c in row) + " |" for row in rows]
    return "\n".join([line1, line2] + body)


def mark_path(path: str) -> None:
    RENDERED_PATHS.add(path)


def _fmt(value: Any) -> str:
    if value is None:
        return "N/D"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, float):
        if abs(value) >= 1e6 or (abs(value) < 1e-4 and value != 0.0):
            return "{0:.4e}".format(value)
        return "{0:.6f}".format(value)
    return str(value)


def render_node(key: str, value: Any, lines: list[str], path: str) -> None:
    if _is_secret_name(key):
        mark_path(path)
        lines.append("- {0} `{1}` presente=`True` valor=`[REDACTED]`".format(ICON_LOCK, key))
        return
    if value is None or isinstance(value, (bool, int, float, str)):
        mark_path(path)
        lines.append("- {0} **{1}**: `{2}`".format(ICON_ITEM, key, md_cell(_fmt(value))))
        return
    if isinstance(value, list):
        if not value:
            mark_path(path)
            lines.append("- {0} **{1}**: `[]`".format(ICON_ITEM, key))
            return
        if all(isinstance(x, dict) for x in value):
            cols: list[str] = []
            for x in value:
                for k in x.keys():
                    if str(k) not in cols:
                        cols.append(str(k))
            rows = []
            for i, x in enumerate(value):
                row = []
                for c in cols:
                    cell = x.get(c)
                    mark_path("{0}[{1}].{2}".format(path, i, c))
                    if isinstance(cell, (dict, list)):
                        row.append("[{0}]".format(type(cell).__name__))
                    else:
                        row.append(_fmt(cell))
                rows.append(row)
            lines.append("- {0} **{1}** ({2})".format(ICON_ITEM, key, len(value)))
            lines.append("")
            lines.append(md_table(cols, rows))
            lines.append("")
            complex_items = []
            for i, x in enumerate(value):
                extra = {k: v for k, v in x.items() if isinstance(v, (dict, list)) and v}
                if extra:
                    complex_items.append((i, extra))
            if complex_items:
                lines.append("<details><summary>{0} detalle anidado de {1}</summary>".format(ICON_FILE, key))
                lines.append("")
                for i, extra in complex_items:
                    for k, v in extra.items():
                        render_node(k, v, lines, "{0}[{1}].{2}".format(path, i, k))
                lines.append("")
                lines.append("</details>")
                lines.append("")
            return
        if all(not isinstance(x, (dict, list)) for x in value):
            lines.append("- {0} **{1}** ({2})".format(ICON_NUM, key, len(value)))
            for i, x in enumerate(value, 1):
                mark_path("{0}[{1}]".format(path, i - 1))
                lines.append("  {0:>3}. {1}".format(i, md_cell(_fmt(x))))
            lines.append("")
            return
        lines.append("- {0} **{1}** ({2})".format(ICON_ITEM, key, len(value)))
        for i, x in enumerate(value):
            render_node("#{0}".format(i), x, lines, "{0}[{1}]".format(path, i))
        return
    if isinstance(value, dict):
        if not value:
            mark_path(path)
            lines.append("- {0} **{1}**: `{{}}`".format(ICON_ITEM, key))
            return
        scalars = {k: v for k, v in value.items() if not isinstance(v, (dict, list))}
        nested = {k: v for k, v in value.items() if isinstance(v, (dict, list))}
        lines.append("- {0} **{1}**".format(ICON_PKG, key))
        if scalars:
            rows = []
            for k, v in scalars.items():
                mark_path("{0}.{1}".format(path, k) if path else str(k))
                if _is_secret_name(str(k)):
                    rows.append([ICON_LOCK, k, "[REDACTED]"])
                else:
                    rows.append([ICON_ITEM, k, _fmt(v)])
            lines.append("")
            lines.append(md_table(["", "Campo", "Valor"], rows, ["center", "left", "left"]))
            lines.append("")
        for k, v in nested.items():
            child = "{0}.{1}".format(path, k) if path else str(k)
            lines.append("<details><summary>{0} {1}</summary>".format(ICON_FILE, k))
            lines.append("")
            render_node(str(k), v, lines, child)
            lines.append("")
            lines.append("</details>")
            lines.append("")
        return
    mark_path(path)
    lines.append("- {0} **{1}**: `{2}`".format(ICON_ITEM, key, md_cell(_fmt(_json_ready(value, key)))))


def render_markdown(pkg: dict[str, Any]) -> str:
    RENDERED_PATHS.clear()
    lines: list[str] = []
    gen = pkg.get("generated") or {}
    status = pkg.get("system_status") or {}
    engine = pkg.get("engine") or {}
    estate = engine.get("state") or {}
    repo = pkg.get("repository") or {}
    summary = repo.get("summary") or {}
    ci = pkg.get("ci_evidence") or {}
    obs = pkg.get("omega_observation") or {}
    cov = pkg.get("coverage") or {}
    findings = pkg.get("findings") or []

    lines.append("# {0} OMEGA DIAGNOSTIC REPORT".format(ICON_OMEGA))
    lines.append("")
    lines.append("## Identification")
    lines.append("")
    render_node("generated", gen, lines, "generated")
    lines.append("")

    lines.append("## Executive System Status")
    lines.append("")
    coh = status.get("coherente")
    if coh is True:
        badge = "{0} COHERENTE".format(ICON_OK)
    elif coh is False:
        badge = "{0} INCOHERENTE".format(ICON_FAIL)
    else:
        badge = "{0} N/D".format(ICON_INFO)
    lines.append(md_table(
        ["Campo", "Valor"],
        [
            ["{0} Estado global".format(ICON_COH), badge],
            ["coherente", status.get("coherente")],
            ["estado", status.get("estado")],
            ["{0} source".format(ICON_SRC), status.get("source")],
            ["source_type", status.get("source_type")],
            ["note", status.get("note")],
            ["{0} Engine startup".format(ICON_ENGINE), estate.get("startup")],
            ["Engine estado", estate.get("estado")],
        ],
    ))
    for k in status:
        mark_path("system_status.{0}".format(k))
    lines.append("")

    lines.append("## {0} Audit Coverage".format(ICON_MET))
    lines.append("")
    render_node("coverage", cov, lines, "coverage")
    lines.append("")

    lines.append("## {0} Repository Inventory".format(ICON_REPO))
    lines.append("")
    render_node("summary", summary, lines, "repository.summary")
    lines.append("")
    lines.append("<details><summary>{0} Directorios ({1})</summary>".format(ICON_DIR, len(repo.get("directories") or [])))
    lines.append("")
    render_node("directories", repo.get("directories") or [], lines, "repository.directories")
    lines.append("")
    lines.append("</details>")
    lines.append("")
    lines.append("<details><summary>{0} Archivos ({1})</summary>".format(ICON_FILE, len(repo.get("files") or [])))
    lines.append("")
    render_node("files", repo.get("files") or [], lines, "repository.files")
    lines.append("")
    lines.append("</details>")
    lines.append("")
    lines.append("<details><summary>{0} Python AST ({1})</summary>".format(ICON_PY, len(repo.get("python") or [])))
    lines.append("")
    render_node("python", repo.get("python") or [], lines, "repository.python")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    lines.append("## {0} Engine State".format(ICON_ENGINE))
    lines.append("")
    render_node("state", estate, lines, "engine.state")
    lines.append("")
    lines.append("<details><summary>{0} Atributos públicos</summary>".format(ICON_PKG))
    lines.append("")
    render_node("public", engine.get("public") or {}, lines, "engine.public")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    lines.append("## {0} Engine Census / Registry".format(ICON_AUDIT))
    lines.append("")
    render_node("census", engine.get("census"), lines, "engine.census")
    lines.append("")
    lines.append("<details><summary>{0} Contenedores ({1})</summary>".format(ICON_PKG, len(engine.get("containers") or [])))
    lines.append("")
    render_node("containers", engine.get("containers") or [], lines, "engine.containers")
    lines.append("")
    lines.append("</details>")
    lines.append("")
    if engine.get("package") is not None:
        lines.append("<details><summary>{0} Engine.package</summary>".format(ICON_PKG))
        lines.append("")
        render_node("package", engine.get("package"), lines, "engine.package")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    axioms = ci.get("axioms") or {}
    lines.append("## {0} Axiomatic Audit".format(ICON_AX))
    lines.append("")
    render_node("axioms_meta", {k: axioms.get(k) for k in ("path", "present", "bytes", "read_ok", "error")}, lines, "ci_evidence.axioms")
    data = axioms.get("data")
    if isinstance(data, dict):
        cuerpos = data.get("cuerpos") or []
        lines.append("```")
        lines.append(W)
        lines.append("{0} AXIOMATIC AUDIT".format(ICON_AX))
        lines.append(S)
        lines.append("{0} Coherente             {1} {2}".format(ICON_COH, ICON_OK if data.get("coherente") else ICON_FAIL, data.get("coherente")))
        lines.append("{0} Declaraciones         {1}".format(ICON_NUM, data.get("declaraciones")))
        n_cuerpos = len(cuerpos) if isinstance(cuerpos, list) else data.get("cuerpos")
        lines.append("{0} Cuerpos               {1}".format(ICON_NUM, n_cuerpos))
        n_err = len(data.get("errores") or []) if isinstance(data.get("errores"), list) else data.get("errores")
        n_cho = len(data.get("choques") or []) if isinstance(data.get("choques"), list) else data.get("choques")
        lines.append("{0} Errores               {1}".format(ICON_ERR, n_err))
        lines.append("{0} Choques               {1}".format(ICON_WARN, n_cho))
        if isinstance(cuerpos, list) and cuerpos:
            lines.append("{0} CUERPOS AXIOMÁTICOS".format(ICON_FILE))
            lines.append(S)
            for i, c in enumerate(cuerpos, 1):
                lines.append("  {0:>2}. {1}".format(i, c))
        lines.append("```")
        lines.append("")
        lines.append("<details><summary>{0} axioms_report.json completo</summary>".format(ICON_DISK))
        lines.append("")
        render_node("data", data, lines, "ci_evidence.axioms.data")
        lines.append("")
        lines.append("</details>")
    lines.append("")

    genr = ci.get("generatividad") or {}
    lines.append("## {0} Generativity Audit".format(ICON_GEN))
    lines.append("")
    render_node("generatividad_meta", {k: genr.get(k) for k in ("path", "present", "bytes", "read_ok", "error")}, lines, "ci_evidence.generatividad")
    gdata = genr.get("data")
    if isinstance(gdata, dict):
        operativa = {k: v for k, v in gdata.items() if k != "canonica"}
        lines.append("### OPERATIVA")
        lines.append("")
        render_node("operativa", operativa, lines, "ci_evidence.generatividad.data")
        lines.append("")
        lines.append("### CANÓNICA TR1")
        lines.append("")
        render_node("canonica", gdata.get("canonica") or {}, lines, "ci_evidence.generatividad.data.canonica")
    lines.append("")

    contra = ci.get("contratos") or {}
    lines.append("## {0} Contract Forensic Audit".format(ICON_CONTRACT))
    lines.append("")
    render_node("contratos_meta", {k: contra.get(k) for k in ("path", "present", "bytes", "read_ok", "error")}, lines, "ci_evidence.contratos")
    cdata = contra.get("data")
    if isinstance(cdata, dict):
        lines.append("<details><summary>{0} contratos_report.json completo</summary>".format(ICON_DISK))
        lines.append("")
        render_node("data", cdata, lines, "ci_evidence.contratos.data")
        lines.append("")
        lines.append("</details>")
    lines.append("")

    ev = ci.get("evaluaciones") or {}
    lines.append("## {0} Evaluation Evidence".format(ICON_EV))
    lines.append("")
    render_node("evaluaciones_meta", {k: ev.get(k) for k in ("path", "present", "bytes", "read_ok", "error")}, lines, "ci_evidence.evaluaciones")
    if ev.get("data") is not None:
        lines.append("<details><summary>{0} evaluaciones.json completo</summary>".format(ICON_DISK))
        lines.append("")
        render_node("data", ev.get("data"), lines, "ci_evidence.evaluaciones.data")
        lines.append("")
        lines.append("</details>")
    lines.append("")

    lines.append("## {0} Python Module Census".format(ICON_PY))
    lines.append("")
    lines.append("{0} censo estático AST; runtime sólo vía Engine.".format(ICON_INFO))
    lines.append("")
    lines.append("<details><summary>{0} Ver censo Python</summary>".format(ICON_PY))
    lines.append("")
    render_node("python", repo.get("python") or [], lines, "repository.python")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    lines.append("## {0} Framework Constants".format(ICON_FORM))
    lines.append("")
    render_node("constants", obs.get("constants") or {}, lines, "omega_observation.constants")
    lines.append("")

    lines.append("## {0} Tests".format(ICON_TEST))
    lines.append("")
    tests = ci.get("tests") or {}
    render_node("tests_summary", {k: tests.get(k) for k in (
        "path", "present", "source", "executed", "discovered_n", "total", "passed",
        "failures", "errors", "failed", "skipped", "rate", "duration", "error",
    )}, lines, "ci_evidence.tests")
    lines.append("")
    lines.append("<details><summary>{0} Suites</summary>".format(ICON_TEST))
    lines.append("")
    render_node("suites", tests.get("suites") or [], lines, "ci_evidence.tests.suites")
    lines.append("")
    lines.append("</details>")
    lines.append("")
    lines.append("<details><summary>{0} Test cases ({1})</summary>".format(ICON_TEST, len(tests.get("cases") or [])))
    lines.append("")
    render_node("cases", tests.get("cases") or [], lines, "ci_evidence.tests.cases")
    lines.append("")
    lines.append("</details>")
    lines.append("")
    lines.append("<details><summary>{0} Tests descubiertos (estático)</summary>".format(ICON_FILE))
    lines.append("")
    render_node("discovered_files", tests.get("discovered_files") or [], lines, "ci_evidence.tests.discovered_files")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    hist = ci.get("coherence_history") or {}
    lines.append("## {0} Coherence History".format(ICON_HIST))
    lines.append("")
    render_node("history_meta", {k: hist.get(k) for k in ("path", "present", "read_ok", "error")}, lines, "ci_evidence.coherence_history")
    lines.append("")
    lines.append("<details><summary>{0} Historial completo ({1})</summary>".format(ICON_HIST, len(hist.get("data") or [])))
    lines.append("")
    render_node("data", hist.get("data") or [], lines, "ci_evidence.coherence_history.data")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    lines.append("## {0} Dependency Graph".format(ICON_GRAPH))
    lines.append("")
    render_node("dependencies", obs.get("dependencies") or {}, lines, "omega_observation.dependencies")
    lines.append("")

    lines.append("## {0} Diagnostic Artifacts".format(ICON_DISK))
    lines.append("")
    art_rows = []
    for key, _filename in CI_JSON_ARTIFACTS:
        rec = ci.get(key) or {}
        art_rows.append([ICON_OK if rec.get("present") else ICON_FAIL, rec.get("path"), rec.get("bytes"), rec.get("read_ok")])
    art_rows.append([ICON_OK if tests.get("present") else ICON_FAIL, tests.get("path"), None, tests.get("executed")])
    art_rows.append([ICON_OK if hist.get("present") else ICON_FAIL, hist.get("path"), None, hist.get("read_ok")])
    lines.append(md_table(["", "Path", "Bytes", "Leído"], art_rows, ["center", "left", "center", "center"]))
    lines.append("")

    lines.append("## {0} Findings".format(ICON_ERR))
    lines.append("")
    if findings:
        render_node("findings", findings, lines, "findings")
    else:
        mark_path("findings")
        lines.append("{0} sin hallazgos de introspección".format(ICON_OK))
    lines.append("")

    lines.append("## Additional / Unknown Fields")
    lines.append("")
    known = {
        "schema_version", "generated", "authority", "system_status", "engine",
        "repository", "ci_evidence", "omega_observation", "coverage", "findings",
        "zero_loss",
    }
    extra = {k: pkg[k] for k in pkg.keys() if k not in known}
    if extra:
        for k, v in extra.items():
            render_node(k, v, lines, k)
    else:
        lines.append("{0} sin campos extra".format(ICON_INFO))
    lines.append("")

    leafs = iter_leaf_paths(pkg)
    unrepr = [p for p in leafs if p not in RENDERED_PATHS and not str(p).startswith("zero_loss")]
    zero = {
        "package_leaf_count": len(leafs),
        "rendered_path_count": len(RENDERED_PATHS),
        "unrepresented_n": len(unrepr),
        "zero_loss": len(unrepr) == 0,
        "unrepresented_paths": unrepr,
    }
    pkg["zero_loss"] = zero
    lines.append("## {0} Zero-loss self audit".format(ICON_AUDIT))
    lines.append("")
    render_node("zero_loss_meta", {k: zero[k] for k in zero if k != "unrepresented_paths"}, lines, "zero_loss")
    lines.append("")
    lines.append("<details><summary>{0} unrepresented_paths ({1})</summary>".format(ICON_FILE, len(unrepr)))
    lines.append("")
    render_node("unrepresented_paths", unrepr, lines, "zero_loss.unrepresented_paths")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    lines.append("## Final Closure")
    lines.append("")
    if coh is True:
        lines.append("{0} **SYSTEM COHERENT** — autoridad: `{1}`".format(ICON_OK, status.get("source")))
    elif coh is False:
        lines.append("{0} **SYSTEM INCOHERENT** — autoridad: `{1}`".format(ICON_FAIL, status.get("source")))
    else:
        lines.append("{0} **SYSTEM STATUS N/D** — no hay autoridad de coherencia global.".format(ICON_INFO))
    lines.append("")
    lines.append("**Omega**")
    lines.append("")
    return "\n".join(lines)


def render_ci(pkg: dict[str, Any]) -> str:
    gen = pkg.get("generated") or {}
    status = pkg.get("system_status") or {}
    estate = (pkg.get("engine") or {}).get("state") or {}
    cov = pkg.get("coverage") or {}
    tests = (pkg.get("ci_evidence") or {}).get("tests") or {}
    findings = pkg.get("findings") or []
    zero = pkg.get("zero_loss") or {}
    coh = status.get("coherente")
    if coh is True:
        coh_s = "{0} COHERENTE".format(ICON_OK)
    elif coh is False:
        coh_s = "{0} INCOHERENTE".format(ICON_FAIL)
    else:
        coh_s = "{0} N/D".format(ICON_INFO)
    return "\n".join([
        W,
        "{0} OMEGA {1}".format(ICON_OMEGA, OMEGA_VERSION),
        W,
        "{0} SHA            {1}".format(ICON_SRC, gen.get("sha")),
        "{0} Authority      {1}".format(ICON_ENGINE, "Engine.paquete" if estate.get("paquete_from_engine") else "CI+static"),
        "{0} Engine         {1}".format(ICON_ENGINE, estate.get("startup")),
        "{0} Sistema        {1}".format(ICON_COH, coh_s),
        S,
        "{0} Py files       {1}".format(ICON_PY, cov.get("python_discovered")),
        "{0} Parsed         {1}".format(ICON_OK, cov.get("python_parsed")),
        "{0} Engine cont.   {1}".format(ICON_PKG, cov.get("engine_containers")),
        "{0} Tests exec     {1}".format(ICON_TEST, tests.get("executed")),
        "{0} Passed         {1}".format(ICON_OK, tests.get("passed")),
        "{0} Failed         {1}".format(ICON_FAIL, tests.get("failed")),
        "{0} Findings       {1}".format(ICON_ERR, len(findings)),
        "{0} Zero-loss      {1}".format(ICON_AUDIT, zero.get("zero_loss")),
        S,
        "{0} JSON           diagnostics/omega_report_data.json".format(ICON_DISK),
        "{0} Markdown       diagnostics/OMEGA_REPORT.md".format(ICON_FILE),
        W,
    ])


def main() -> int:
    print("Running Omega Report...")
    try:
        paquete = build_paquete()
        markdown = render_markdown(paquete)
        compact = render_ci(paquete)
        DIAGNOSTICS_DIR.mkdir(parents=True, exist_ok=True)
        md_path = DIAGNOSTICS_DIR / "OMEGA_REPORT.md"
        js_path = DIAGNOSTICS_DIR / "omega_report_data.json"
        md_path.write_text(markdown, encoding="utf-8")
        js_path.write_text(
            json.dumps(_json_ready(paquete), indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        print(compact)
        print("\nReport saved to: {0}".format(md_path))
        print("JSON data saved to: {0}".format(js_path))
        return 0
    except Exception as e:
        print("{0} OMEGA EXECUTION ERROR: {1}: {2}".format(ICON_FAIL, type(e).__name__, e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
