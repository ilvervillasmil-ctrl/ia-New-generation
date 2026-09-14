# tests/test_oscillator_regimes.py

import math


def compute_omega_d(phi: float) -> float:
    """
    Frecuencia amortiguada del oscilador UCF v3.1.

    ω_d = sqrt(π² - φ²/4), truncada a 0 cuando el término se vuelve negativo.
    """
    term = math.pi**2 - (phi**2) / 4.0
    if term <= 0:
        return 0.0
    return math.sqrt(term)


def classify_regime(phi: float, tol: float = 1e-9) -> str:
    """
    Clasifica el régimen dinámico según φ_total:

    - "alive"    si φ < 2π  (subamortiguado, oscila)
    - "critical" si φ ≈ 2π  (crítico)
    - "dead"     si φ > 2π  (sobreamortiguado, no oscila)
    """
    two_pi = 2.0 * math.pi
    if phi < two_pi - tol:
        return "alive"
    if abs(phi - two_pi) <= tol:
        return "critical"
    return "dead"


def test_omega_d_and_regimes():
    """
    Verifica que la dinámica de UCF v3.1 cumple:

    - φ_total = 0.22 → régimen "alive" con ω_d > 0.
    - φ_total = 2π   → régimen "critical" con ω_d ≈ 0.
    - φ_total > 2π   → régimen "dead" con ω_d = 0 (sin oscilación).
    """

    # Régimen vivo (subamortiguado)
    phi_alive = 0.22
    omega_alive = compute_omega_d(phi_alive)
    regime_alive = classify_regime(phi_alive)
    assert omega_alive > 0.0
    assert regime_alive == "alive"

    # Régimen crítico
    phi_crit = 2.0 * math.pi
    omega_crit = compute_omega_d(phi_crit)
    regime_crit = classify_regime(phi_crit)
    assert abs(omega_crit) < 1e-9
    assert regime_crit == "critical"

    # Régimen muerto (sobreamortiguado)
    phi_dead = 2.0 * math.pi + 0.5
    omega_dead = compute_omega_d(phi_dead)
    regime_dead = classify_regime(phi_dead)
    assert omega_dead == 0.0
    assert regime_dead == "dead"
