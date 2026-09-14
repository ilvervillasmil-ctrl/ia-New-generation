import math
from formulas.negentropy import NegentropyCalculator
from formulas.constants import NUM_LAYERS


def test_uniform_energies_zero_negentropy():
    """Equal energies = maximum entropy = zero negentropy."""
    energies = [1.0] * NUM_LAYERS
    n = NegentropyCalculator.compute(energies)
    assert abs(n) < 1e-10


def test_single_layer_active_max_negentropy():
    """Only one layer active = zero entropy = negentropy 1."""
    energies = [0.0] * NUM_LAYERS
    energies[3] = 1.0
    n = NegentropyCalculator.compute(energies)
    assert abs(n - 1.0) < 1e-10


def test_all_zeros_zero_negentropy():
    """All zeros = max entropy = zero negentropy."""
    energies = [0.0] * NUM_LAYERS
    n = NegentropyCalculator.compute(energies)
    assert abs(n) < 1e-10


def test_harmony_equals_negentropy():
    """H(S) = N. They are the same function."""
    energies = [1.0, 0.5, 0.8, 0.3, 0.9, 0.6, 1.0]
    n = NegentropyCalculator.compute(energies)
    h = NegentropyCalculator.harmony(energies)
    assert abs(n - h) < 1e-10


def test_negentropy_range():
    """Negentropy must be between 0 and 1."""
    energies = [0.3, 0.7, 0.1, 0.9, 0.5, 0.2, 0.8]
    n = NegentropyCalculator.compute(energies)
    assert 0.0 <= n <= 1.0


def test_shannon_entropy_uniform():
    """Uniform distribution = log(N)."""
    energies = [1.0] * NUM_LAYERS
    s = NegentropyCalculator.shannon_entropy(energies)
    assert abs(s - math.log(NUM_LAYERS)) < 1e-10
