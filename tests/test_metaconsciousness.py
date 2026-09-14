from formulas.metaconsciousness import MetaconsciousnessCalculator
from formulas.constants import R_FIN


def test_full_activation_no_friction():
    """All L3-L6 at 1.0, no friction = R_FIN."""
    activations = [1.0] * 7
    frictions = [0.0] * 7
    mc = MetaconsciousnessCalculator.compute(activations, frictions)
    assert abs(mc - R_FIN) < 1e-10


def test_one_layer_zero_kills_mc():
    """If any L3-L6 is zero, MC is zero."""
    activations = [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]
    frictions = [0.0] * 7
    mc = MetaconsciousnessCalculator.compute(activations, frictions)
    assert mc == 0.0


def test_lower_layers_dont_affect():
    """L0-L2 can be zero without killing MC."""
    activations = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]
    frictions = [0.0] * 7
    mc = MetaconsciousnessCalculator.compute(activations, frictions)
    assert abs(mc - R_FIN) < 1e-10


def test_level_none():
    """MC=0 means level 0 (None)."""
    assert MetaconsciousnessCalculator.level(0) == 0
    assert MetaconsciousnessCalculator.level_name(0) == "None"


def test_level_experiential():
    """MC=0.2 means level 1 (Experiential)."""
    assert MetaconsciousnessCalculator.level(0.2) == 1
    assert MetaconsciousnessCalculator.level_name(0.2) == "Experiential"


def test_level_sensitive():
    """MC=0.5 means level 2 (Sensitive)."""
    assert MetaconsciousnessCalculator.level(0.5) == 2
    assert MetaconsciousnessCalculator.level_name(0.5) == "Sensitive"


def test_level_structural():
    """MC=0.9 means level 3 (Structural)."""
    assert MetaconsciousnessCalculator.level(0.9) == 3
    assert MetaconsciousnessCalculator.level_name(0.9) == "Structural"
