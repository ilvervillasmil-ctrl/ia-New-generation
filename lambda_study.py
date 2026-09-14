"""
Lambda Study - Villasmil-Ω
Estudio numérico de las fórmulas de Λ del framework
y comparación con valores observados en unidades de Planck.

Incluye:
- Λ_base  = β^(27π)
- Λ_geo   = β^(27π) · κ
- Λ_Ω     = β^(27π + β φ²)
- Escaneo de una familia Λ(a, X) = β^(aπ + βX)
  con a ∈ [1, 100] y X ∈ {φ², π, κ², S_ref²}
"""

from math import pi
from core.constants import BETA, PHI, KAPPA, S_REF  # ajusta el import al módulo real


# ─────────────────────────────────────────────
# 1. Valores observados (en unidades de Planck)
# ─────────────────────────────────────────────
# En tus textos usas estos dos valores de referencia
# derivados de Λ en SI + longitud de Planck.
LAMBDA_OBS_1 = 2.888e-122
LAMBDA_OBS_2 = 2.845e-122


# ─────────────────────────────────────────────
# 2. Fórmulas centrales del marco
# ─────────────────────────────────────────────

def lambda_base() -> float:
    """
    Λ_base = β^(27π)
    """
    return BETA ** (27 * pi)


def lambda_geo() -> float:
    """
    Λ_geo = β^(27π) · κ
    """
    return lambda_base() * KAPPA


def lambda_omega() -> float:
    """
    Λ_Ω = β^(27π + β φ²)
    """
    return BETA ** (27 * pi + BETA * (PHI ** 2))


# ─────────────────────────────────────────────
# 3. Utilidades numéricas
# ─────────────────────────────────────────────

def rel_error(pred: float, target: float) -> float:
    """
    Error relativo |pred - target| / target.
    """
    return abs(pred - target) / target


# ─────────────────────────────────────────────
# 4. Resumen de las tres fórmulas núcleo
# ─────────────────────────────────────────────

def compute_core_results():
    """
    Devuelve un resumen con:
    - valores de Λ_base, Λ_geo, Λ_Ω
    - errores relativos contra LAMBDA_OBS_1 y LAMBDA_OBS_2
    """
    lb = lambda_base()
    lg = lambda_geo()
    lo = lambda_omega()

    return {
        "lambda_values": {
            "base": lb,
            "geo": lg,
            "omega": lo,
        },
        "errors_obs1": {
            "base": rel_error(lb, LAMBDA_OBS_1),
            "geo":  rel_error(lg, LAMBDA_OBS_1),
            "omega": rel_error(lo, LAMBDA_OBS_1),
        },
        "errors_obs2": {
            "base": rel_error(lb, LAMBDA_OBS_2),
            "geo":  rel_error(lg, LAMBDA_OBS_2),
            "omega": rel_error(lo, LAMBDA_OBS_2),
        },
    }


# ─────────────────────────────────────────────
# 5. Familia Λ(a, X) = β^(aπ + βX)
# ─────────────────────────────────────────────

# Candidatos X tomados de constantes ya presentes en el framework
X_CANDIDATES = {
    "phi_sq":   PHI ** 2,
    "pi":       pi,
    "kappa_sq": KAPPA ** 2,
    "sref_sq":  S_REF ** 2,
}


def lambda_family(a: int, X_value: float) -> float:
    """
    Λ(a, X) = β^(aπ + βX)
    """
    return BETA ** (a * pi + BETA * X_value)


def scan_family(
    target: float = LAMBDA_OBS_2,
    a_min: int = 1,
    a_max: int = 100,
):
    """
    Escanea la familia Λ(a, X) = β^(aπ + βX)
    para a ∈ [a_min, a_max] y X en X_CANDIDATES,
    y devuelve una lista ordenada por error relativo ascendente.
    """
    results = []
    for a in range(a_min, a_max + 1):
        for name, X in X_CANDIDATES.items():
            val = lambda_family(a, X)
            err = rel_error(val, target)
            results.append({
                "a": a,
                "X_name": name,
                "lambda": val,
                "error": err,
            })
    results.sort(key=lambda r: r["error"])
    return results


def find_omega_in_family(
    target: float = LAMBDA_OBS_2,
    a_min: int = 1,
    a_max: int = 100,
):
    """
    Localiza la posición de tu fórmula Λ_Ω
    dentro del ranking de la familia (mismo target).
    """
    all_results = scan_family(target=target, a_min=a_min, a_max=a_max)

    # Definición explícita de tu par (a=27, X="phi_sq")
    omega_a = 27
    omega_X_name = "phi_sq"

    rank = None
    for idx, r in enumerate(all_results):
        if r["a"] == omega_a and r["X_name"] == omega_X_name:
            rank = idx + 1  # rank humano (1-based)
            break

    return {
        "rank": rank,
        "total": len(all_results),
        "omega_record": next(
            (r for r in all_results
             if r["a"] == omega_a and r["X_name"] == omega_X_name),
            None,
        ),
        "top10": all_results[:10],
    }


# ─────────────────────────────────────────────
# 6. Ejecución directa (quick report en consola)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    from pprint import pprint

    print("=== CORE FORMULAS VS OBSERVED VALUES ===")
    summary = compute_core_results()
    print("\nΛ values:")
    pprint(summary["lambda_values"])

    print("\nRelative errors vs LAMBDA_OBS_1 (2.888e-122):")
    pprint(summary["errors_obs1"])

    print("\nRelative errors vs LAMBDA_OBS_2 (2.845e-122):")
    pprint(summary["errors_obs2"])

    print("\n=== FAMILY SCAN (Λ(a, X) = β^(aπ + βX)) vs LAMBDA_OBS_2 ===")
    family_report = find_omega_in_family(target=LAMBDA_OBS_2)
    print(f"\nTotal candidates: {family_report['total']}")
    print(f"Λ_Ω (a=27, X='phi_sq') rank: {family_report['rank']}")

    print("\nΛ_Ω record in family:")
    pprint(family_report["omega_record"])

    print("\nTop 10 candidates in family:")
    for r in family_report["top10"]:
        print(r)
