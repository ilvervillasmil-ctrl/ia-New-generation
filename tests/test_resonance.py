# File: tests/test_resonance.py
from formulas.resonance import ResonanceLogic
from formulas.constants import PHI

def test_calculate_layer_frequency():
    value = ResonanceLogic.calculate_layer_frequency(2)
    assert round(value, 5) == round(PHI ** (2 / 2), 5), "Layer frequency is incorrect!"

def test_calculate_phase_alignment():
    value = ResonanceLogic.calculate_phase_alignment(10, 5)
    assert round(value, 5) == 0.5, f"Unexpected alignment: {value}"

    # Edge case
    value = ResonanceLogic.calculate_phase_alignment(0, 5)
    assert value == 0.0, "Alignment should be 0 when one energy level is 0."
