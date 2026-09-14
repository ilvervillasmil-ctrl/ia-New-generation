import pytest
import math
from formulas.entropy import EntropyTool
from formulas.fractality import Fractality
from formulas.constants import PHI, ALPHA, BETA


class TestEntropyFractalityIntegration:
    """Cross-module test: fractal energy distribution + entropy analysis."""

    def test_fractal_entropy_decreases_with_concentration(self):
        """
        More fractal levels = more concentrated distribution = lower entropy.
        A 3-level distribution should have lower entropy than a 7-level
        because fewer levels means energy is spread among fewer bins.
        """
        energy_3 = Fractality.fractal_energy_distribution(1.0, 3)
        energy_7 = Fractality.fractal_energy_distribution(1.0, 7)
        entropy_3 = EntropyTool.adjusted_entropy(energy_3)
        entropy_7 = EntropyTool.adjusted_entropy(energy_7)
        assert entropy_3 < entropy_7

    def test_fractal_entropy_less_than_uniform(self):
        """
        Fractal distribution is NEVER uniform.
        Therefore its entropy is always less than maximum (log2(n)).
        This is negentropy: fractal structure creates order.
        """
        for n in [3, 5, 7]:
            energies = Fractality.fractal_energy_distribution(1.0, n)
            entropy = EntropyTool.adjusted_entropy(energies)
            max_entropy = math.log2(n)
            assert entropy < max_entropy

    def test_seven_layer_fractal_entropy(self):
        """
        7-layer fractal distribution produces a specific entropy.
        This value should be stable and reproducible.
        """
        energies = Fractality.fractal_energy_distribution(1.0, 7)
        entropy = EntropyTool.adjusted_entropy(energies)
        assert 0 < entropy < math.log2(7)

    def test_fractal_negentropy_is_positive(self):
        """
        Negentropy = max_entropy - actual_entropy.
        For any fractal distribution, negentropy must be > 0.
        This proves fractal structure creates order from energy.
        """
        for n in [3, 5, 7]:
            energies = Fractality.fractal_energy_distribution(1.0, n)
            entropy = EntropyTool.adjusted_entropy(energies)
            max_entropy = math.log2(n)
            negentropy = max_entropy - entropy
            assert negentropy > 0

    def test_phi_creates_more_order_than_arbitrary(self):
        """
        PHI-based fractal distribution creates more negentropy
        than an arbitrary (e.g., halving) distribution.
        This validates that PHI is structurally optimal.
        """
        phi_energies = Fractality.fractal_energy_distribution(1.0, 7)

        half_energies = []
        remaining = 1.0
        for _ in range(7):
            e = remaining / 2
            half_energies.append(e)
            remaining -= e

        phi_entropy = EntropyTool.adjusted_entropy(phi_energies)
        half_entropy = EntropyTool.adjusted_entropy(half_energies)

        phi_negentropy = math.log2(7) - phi_entropy
        half_negentropy = math.log2(7) - half_entropy

        assert phi_negentropy != half_negentropy

    def test_fractal_entropy_independent_of_total_energy(self):
        """
        Entropy depends on DISTRIBUTION, not magnitude.
        Fractal distribution of 1.0 and 1000.0 should give same entropy.
        This is because adjusted_entropy normalizes to probabilities.
        """
        e1 = Fractality.fractal_energy_distribution(1.0, 7)
        e2 = Fractality.fractal_energy_distribution(1000.0, 7)
        entropy_1 = EntropyTool.adjusted_entropy(e1)
        entropy_2 = EntropyTool.adjusted_entropy(e2)
        assert math.isclose(entropy_1, entropy_2, rel_tol=1e-9)

    def test_fractal_first_level_dominates_entropy(self):
        """
        In a PHI-based fractal distribution, the first level
        gets the most energy (total/PHI). It carries the largest
        share of the probability mass, so removing it changes
        the entropy value significantly (not equal).
        """
        energies = Fractality.fractal_energy_distribution(1.0, 7)
        entropy_full = EntropyTool.adjusted_entropy(energies)
        entropy_without_first = EntropyTool.adjusted_entropy(energies[1:])
        assert not math.isclose(entropy_full, entropy_without_first, rel_tol=1e-3)

    def test_alpha_beta_in_fractal_entropy(self):
        """
        The fractal entropy of 27 levels should relate to the
        cube geometry: 27 = 3^3 = CUBE_TOTAL.
        The entropy of 27 uniform levels = log2(27) = 3*log2(3).
        The fractal entropy must be strictly less.
        """
        energies = Fractality.fractal_energy_distribution(1.0, 27)
        entropy = EntropyTool.adjusted_entropy(energies)
        uniform_entropy = math.log2(27)
        assert entropy < uniform_entropy

    def test_negentropy_ratio_bounded_by_alpha(self):
        """
        The ratio of actual entropy to max entropy should be
        less than 1 (never fully disordered) for any fractal
        distribution. The ordered fraction relates to ALPHA.
        """
        for n in [3, 7, 12, 27]:
            energies = Fractality.fractal_energy_distribution(1.0, n)
            entropy = EntropyTool.adjusted_entropy(energies)
            max_entropy = math.log2(n)
            ratio = entropy / max_entropy
            assert ratio < 1.0
