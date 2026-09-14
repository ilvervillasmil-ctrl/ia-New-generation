# tests/test_coherence_identity.py
"""
Tests que formalizan la distinción entre:
  C_structural  — coherencia real, limitada por alpha = 26/27
  C_global_norm — normalizada relativa al máximo operativo
  C_CI          — proxy del CI (pass_rate), no es coherencia estructural

La colisión semántica entre estas tres magnitudes
es el error más peligroso del framework:
parece pequeño pero cambia toda la lectura del sistema.
"""
import pytest
from formulas.constants import ALPHA, BETA
from formulas.coherence import CoherenceEngine


def test_structural_coherence_never_reaches_one():
    """C_struct <= alpha siempre. Beta es irreducible."""
    result = CoherenceEngine.full_analysis(
        activations=[1.0] * 7,
        integration=1.0, quality=1.0,
        complexity=0.1, uncertainty=0.0,
    )
    c_omega = result["c_omega"]
    assert c_omega < 1.0,    f"C_Ω = {c_omega:.6f} viola beta > 0"
    assert c_omega <= ALPHA, f"C_Ω = {c_omega:.6f} viola C_max = alpha = {ALPHA:.6f}"


def test_global_coherence_can_reach_one_only_by_normalization():
    """
    C_global = C_struct / alpha puede llegar a 1.0
    pero SOLO porque es relativa al máximo operativo.
    No es coherencia ontológica absoluta.
    """
    c_struct = ALPHA           # máximo estructural posible
    c_global = c_struct / ALPHA

    assert c_struct < 1.0     # estructural nunca llega a 1
    assert c_struct == ALPHA
    assert c_global == pytest.approx(1.0)  # normalizada sí puede ser 1


def test_structural_and_global_are_not_the_same():
    """Dos magnitudes distintas no deben usar el mismo símbolo."""
    c_struct = 0.9292
    c_global = c_struct / ALPHA

    assert c_struct != c_global
    assert c_struct < 1.0
    assert c_global <= 1.0
    assert abs(c_global - c_struct / ALPHA) < 1e-9


def test_pass_rate_is_not_structural_coherence():
    """
    pass_rate/100 = 1.0 cuando todos los tests pasan.
    Eso no significa coherencia estructural perfecta.
    Son magnitudes distintas que no deben llamarse igual.
    """
    pass_rate = 100.0
    c_ci = pass_rate / 100.0       # proxy del CI

    assert c_ci == 1.0             # el CI puede dar 1.0
    assert ALPHA < 1.0             # pero la estructura nunca llega a 1
    assert c_ci != ALPHA           # son magnitudes distintas
    assert BETA > 0                # beta siempre presente


def test_beta_irreducible_prevents_perfect_structural_coherence():
    """
    El residuo β = 1/27 impide el cierre total.
    Ningún sistema real alcanza C_struct = 1.
    C_max = alpha = 26/27 es el límite estructural absoluto.
    """
    result = CoherenceEngine.full_analysis(
        activations=[1.0] * 7,
        integration=1.0, quality=1.0,
        complexity=0.1, uncertainty=0.0,
    )
    c_omega = result["c_omega"]

    assert BETA > 0
    assert ALPHA == pytest.approx(26/27)
    assert c_omega <= ALPHA
    assert c_omega != 1.0
    assert 1.0 - c_omega >= BETA * 0.1  # el residuo siempre deja huella


def test_three_coherences_are_distinct_quantities():
    """
    Las tres magnitudes tienen rangos y semánticas distintas.
    Ninguna debe confundirse con las otras.

    C_structural  ∈ [0, alpha]   — coherencia real del framework
    C_global_norm ∈ [0, 1]       — relativa al máximo operativo
    C_CI          ∈ [0, 1]       — proxy de calidad del CI
    """
    result = CoherenceEngine.full_analysis(
        activations=[1.0] * 7,
        integration=1.0, quality=1.0,
        complexity=0.1, uncertainty=0.0,
    )

    c_structural  = result["c_omega"]
    c_global_norm = c_structural / ALPHA
    c_ci          = 1.0  # todos los tests pasan

    # rangos distintos
    assert c_structural  <= ALPHA
    assert c_global_norm <= 1.0
    assert c_ci          <= 1.0

    # semánticas distintas
    assert c_structural != c_ci
    assert c_structural < 1.0   # structural nunca es 1
    assert c_ci == 1.0           # CI puede ser 1
