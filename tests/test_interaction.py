import math
from formulas.interaction import ExternalInteraction


def test_love_adds_coherence():
    """theta=0: C1 + C2"""
    result = ExternalInteraction.love(0.8, 0.6)
    assert abs(result - 1.4) < 1e-10


def test_conflict_subtracts():
    """theta=pi: |C1 - C2|"""
    result = ExternalInteraction.conflict(0.8, 0.6)
    assert abs(result - 0.2) < 1e-10


def test_independence_pythagorean():
    """theta=pi/2: sqrt(C1^2 + C2^2)"""
    result = ExternalInteraction.independence(3.0, 4.0)
    assert abs(result - 5.0) < 1e-10


def test_compute_pair_zero_angle():
    """compute_pair at theta=0 equals C1+C2."""
    result = ExternalInteraction.compute_pair(0.5, 0.5, 0.0)
    assert abs(result - 1.0) < 1e-10


def test_compute_pair_pi_angle():
    """compute_pair at theta=pi equals |C1-C2|."""
    result = ExternalInteraction.compute_pair(0.8, 0.3, math.pi)
    assert abs(result - 0.5) < 1e-10


def test_compute_multi_single():
    """Single system returns its own coherence."""
    result = ExternalInteraction.compute_multi([0.75])
    assert abs(result - 0.75) < 1e-10


def test_compute_multi_empty():
    """Empty list returns 0."""
    result = ExternalInteraction.compute_multi([])
    assert result == 0.0


def test_compute_multi_love():
    """Multiple systems at theta=0 (love) = sum."""
    result = ExternalInteraction.compute_multi([0.3, 0.4, 0.3])
    assert abs(result - 1.0) < 1e-10
