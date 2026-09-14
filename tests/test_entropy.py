import pytest
import math
from formulas.entropy import EntropyTool


class TestCalculateEntropy:
    def test_uniform_distribution_two(self):
        """Two equally likely outcomes = 1 bit."""
        result = EntropyTool.calculate_entropy([0.5, 0.5])
        assert math.isclose(result, 1.0, rel_tol=1e-9)

    def test_uniform_distribution_four(self):
        """Four equally likely outcomes = 2 bits."""
        result = EntropyTool.calculate_entropy([0.25, 0.25, 0.25, 0.25])
        assert math.isclose(result, 2.0, rel_tol=1e-9)

    def test_certain_outcome(self):
        """One certain outcome = 0 entropy."""
        result = EntropyTool.calculate_entropy([1.0])
        assert result == 0.0

    def test_seven_layers_uniform(self):
        """7 layers uniform = log2(7) bits."""
        probs = [1/7] * 7
        result = EntropyTool.calculate_entropy(probs)
        assert math.isclose(result, math.log2(7), rel_tol=1e-9)

    def test_skewed_distribution(self):
        """Dominant layer should have lower entropy than uniform."""
        skewed = [0.9, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01]
        uniform = [1/7] * 7
        assert EntropyTool.calculate_entropy(skewed) < EntropyTool.calculate_entropy(uniform)

    def test_invalid_probabilities_not_sum_one(self):
        """Probabilities that don't sum to 1 raise ValueError."""
        with pytest.raises(ValueError):
            EntropyTool.calculate_entropy([0.5, 0.3])

    def test_empty_list_raises(self):
        """Empty list raises ValueError."""
        with pytest.raises(ValueError):
            EntropyTool.calculate_entropy([])


class TestAdjustedEntropy:
    def test_equal_energies(self):
        """Equal energies = maximum entropy for that count."""
        result = EntropyTool.adjusted_entropy([1.0, 1.0, 1.0])
        assert math.isclose(result, math.log2(3), rel_tol=1e-9)

    def test_single_active_layer(self):
        """Only one layer with energy = 0 entropy."""
        result = EntropyTool.adjusted_entropy([5.0])
        assert result == 0.0

    def test_seven_layer_energies(self):
        """7-layer energy distribution produces valid entropy."""
        energies = [0.9, 0.98, 0.95, 0.97, 0.99, 0.99, 1.0]
        result = EntropyTool.adjusted_entropy(energies)
        assert 0 < result <= math.log2(7)

    def test_zero_total_energy_raises(self):
        """All-zero energy should raise (division by zero)."""
        with pytest.raises(ZeroDivisionError):
            EntropyTool.adjusted_entropy([0, 0, 0])
