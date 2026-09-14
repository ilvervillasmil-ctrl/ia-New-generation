"""
Tests for formulas/tension.py — UCF v3.2
"""
import pytest
from formulas.tension import (
    theta_tension,
    relevance_R,
    tension_level,
    is_coherent,
)
from formulas.constants import (
    ALPHA, BETA,
    TENSION_WEIGHTS,
    TENSION_DIRECT,
    TENSION_PARTIAL,
    TENSION_AMBIGUOUS,
    TENSION_COMPATIBLE,
)


def test_tension_empty_premises():
    assert theta_tension([]) == TENSION_COMPATIBLE


def test_tension_compatible_premises():
    premises = [(0.963, 0.963, "equal")]
    assert theta_tension(premises) == TENSION_COMPATIBLE


def test_tension_opposite_is_direct():
    premises = [(1.0, 0.0, "opposite")]
    assert theta_tension(premises) == TENSION_DIRECT


def test_tension_partial_relation():
    premises = [(0.5, 0.5, "partial")]
    assert theta_tension(premises) == TENSION_PARTIAL


def test_tension_ambiguous_relation():
    premises = [(0.5, 0.5, "ambiguous")]
    assert theta_tension(premises) == TENSION_AMBIGUOUS


def test_tension_max_of_multiple():
    premises = [
        (0.963, 0.963, "equal"),
        (1.0, 0.0, "opposite"),
    ]
    assert theta_tension(premises) == TENSION_DIRECT


def test_tension_returns_float():
    assert isinstance(theta_tension([]), float)


def test_tension_clamped_to_one():
    premises = [(0.0, 1.0, "opposite"), (0.0, 1.0, "opposite")]
    assert theta_tension(premises) <= 1.0


def test_relevance_R_perfect_system():
    R = relevance_R(
        MC=1.0, CI=1.0, phi_noise=0.0,
        delta=1.0, theta_c=0.0, P=1.0, N=1.0
    )
    assert R > 0.9


def test_relevance_R_high_tension_reduces():
    R_low  = relevance_R(1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0)
    R_high = relevance_R(1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0)
    assert R_low > R_high


def test_relevance_R_clamped_to_one():
    R = relevance_R(1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0)
    assert R <= 1.0


def test_relevance_R_never_negative():
    R = relevance_R(0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0)
    assert R >= 0.0


def test_relevance_R_weights_sum_to_one():
    total = sum(TENSION_WEIGHTS.values())
    assert abs(total - 1.0) < 1e-9


def test_relevance_R_tension_weight_is_negative_term():
    assert TENSION_WEIGHTS["tension"] > 0
    R_no_tension   = relevance_R(0.8, 0.8, 0.2, 0.8, 0.0, 0.8, 0.8)
    R_with_tension = relevance_R(0.8, 0.8, 0.2, 0.8, 1.0, 0.8, 0.8)
    assert R_no_tension > R_with_tension


def test_tension_level_compatible():
    assert tension_level(0.0) == "COMPATIBLE"


def test_tension_level_ambiguous():
    assert tension_level(0.2) == "AMBIGUOUS"


def test_tension_level_partial():
    assert tension_level(0.5) == "PARTIAL"


def test_tension_level_direct():
    assert tension_level(1.0) == "DIRECT"


def test_is_coherent_healthy_system():
    assert is_coherent(MC=0.97, CI=0.97, theta_c=0.0)


def test_is_coherent_fails_with_high_tension():
    assert not is_coherent(MC=0.97, CI=0.97, theta_c=0.5)


def test_is_coherent_fails_with_low_MC():
    assert not is_coherent(MC=0.5, CI=0.97, theta_c=0.0)


def test_beta_structural_minimum():
    assert BETA > 0
    assert TENSION_COMPATIBLE == 0.0
    assert TENSION_DIRECT == 1.0
