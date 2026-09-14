# File: tests/test_presence.py
from formulas.presence import PresenceLogic

def test_compute_pt():
    value = PresenceLogic.compute_pt(5)
    assert round(value, 5) == 0.16667, f"Unexpected value: {value}"

    # Edge cases
    value = PresenceLogic.compute_pt(0)
    assert value == 1.0, "Presence should be 1 when dispersion is 0."
