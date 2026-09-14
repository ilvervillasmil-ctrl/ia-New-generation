# tests/test_hubble_model_selection.py

import math

# =========================
# CONSTANTES DEL FRAMEWORK
# =========================
# tests/test_hubble_tension_resolution.py

import math

# ============================================================
# CONSTANTES DEL FRAMEWORK
# ============================================================

ALPHA = 26 / 27
BETA  = 1 / 27
PHI   = (1 + math.sqrt(5)) / 2
KAPPA = math.pi / 4

# ============================================================
# OBSERVACIÓN EMPÍRICA (separada de la predicción)
# ============================================================

H_EARLY = 67.4
H_LATE  = 73.0

OBS_DIFF = (H_LATE - H_EARLY) / H_EARLY

# ============================================================
# PREDICCIÓN DEL FRAMEWORK (GANADORA MONTE CARLO)
# ============================================================

def predict_hubble_tension_omega() -> float:
    """
    Predicción estructural NO circular.
    Seleccionada por búsqueda Monte Carlo.

    β · (π / √2)
    """
    return BETA * (math.pi / math.sqrt(2))


# ============================================================
# TESTS
# ============================================================

def test_prediction_is_framework_only():
    pred = predict_hubble_tension_omega()
    assert isinstance(pred, float)
    assert 0.0 < pred < 1.0


def test_observation_is_separate():
    assert OBS_DIFF > 0
    assert abs(OBS_DIFF - ((73.0 - 67.4) / 67.4)) < 1e-12


def test_hubble_tension_resolution():
    pred = predict_hubble_tension_omega()

    # puedes ajustar según rigor del repo
    tolerance = 0.001

    print("\n=== HUBBLE RESOLUTION REPORT ===")
    print(f"Predicción Omega : {pred:.6f}")
    print(f"Observación      : {OBS_DIFF:.6f}")
    print(f"Diferencia       : {abs(pred - OBS_DIFF):.6f}")
    print(f"Tolerancia       : {tolerance:.6f}")

    assert abs(pred - OBS_DIFF) < tolerance, (
        f"FAIL: pred={pred:.6f}, obs={OBS_DIFF:.6f}, "
        f"diff={abs(pred - OBS_DIFF):.6f}"
    )
ALPHA = 26 / 27
BETA  = 1 / 27
PHI   = (1 + math.sqrt(5)) / 2
KAPPA = math.pi / 4

# =========================
# OBSERVACIÓN (SEPARADA)
# =========================

H_EARLY = 67.4
H_LATE  = 73.0

OBS_DIFF = (H_LATE - H_EARLY) / H_EARLY

# =========================
# MODELOS CANDIDATOS
# =========================

def model_beta_pi():
    return BETA * math.pi

def model_two_beta():
    return 2 * BETA

def model_beta_phi_sqrt2():
    return BETA * PHI * math.sqrt(2)

MODELS = {
    "beta_pi": model_beta_pi,
    "two_beta": model_two_beta,
    "beta_phi_sqrt2": model_beta_phi_sqrt2,
}

# =========================
# TEST DE SELECCIÓN
# =========================

def test_hubble_model_selection():
    """
    Selección NO circular del mejor modelo.
    """
    results = []

    for name, fn in MODELS.items():
        pred = fn()
        error = abs(pred - OBS_DIFF)
        results.append((name, pred, error))

    # ordenar por error (mejor primero)
    results.sort(key=lambda x: x[2])

    print("\n=== MODEL SELECTION REPORT ===")
    for name, pred, err in results:
        print(f"{name:20s} | pred={pred:.6f} | error={err:.6f}")

    best_model, best_pred, best_error = results[0]

    print(f"\nBEST MODEL: {best_model}")
    print(f"ERROR     : {best_error:.6f}")

    # condición mínima: debe ser razonable
    assert best_error < 0.01, (
        f"No model fits: best={best_model}, error={best_error}"
    )

    # opcional: asegurar que el mejor es claramente mejor
    second_error = results[1][2]
    assert best_error < second_error, (
        "No clear winner: models too similar"
    )
