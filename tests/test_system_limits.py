import pytest
import math
from formulas.constants import (
    ALPHA, BETA, PHI, S_REF, R_FIN,
    OMEGA_0, OMEGA_0_SQUARED,
    PHI_TOTAL, PHI_CRITICAL,
    OMEGA_D, ZETA,
    LAYER_FRICTION, NUM_LAYERS,
    GOLDEN_ANG, THETA_CUBE,
)
from formulas.entropy import EntropyTool
from formulas.fractality import Fractality
from formulas.coherence import CoherenceEngine
from formulas.interaction import ExternalInteraction
from formulas.presence import TemporalPresence
from formulas.wonder import WonderLogic


class TestInvariantsNeverBreak:
    """The absolute invariants: these must hold under ALL conditions."""

    def test_alpha_plus_beta_equals_one(self):
        assert abs(ALPHA + BETA - 1.0) < 1e-10

    def test_sin_squared_theta_equals_beta(self):
        assert abs(math.sin(THETA_CUBE)**2 - BETA) < 1e-10

    def test_cos_squared_theta_equals_alpha(self):
        assert abs(math.cos(THETA_CUBE)**2 - ALPHA) < 1e-10

    def test_rfin_equals_one_plus_beta(self):
        assert abs(R_FIN - (1 + BETA)) < 1e-10

    def test_alpha_approximates_e_minus_beta(self):
        assert abs(ALPHA - math.exp(-BETA)) < 0.001

    def test_cube_constants(self):
        """The 3x3x3 cube: 27 total, 26 exterior, 1 center."""
        from formulas.constants import CUBE_TOTAL, CUBE_EXTERIOR, CUBE_CENTER
        assert CUBE_TOTAL == 27
        assert CUBE_EXTERIOR == 26
        assert CUBE_CENTER == 1
        assert CUBE_EXTERIOR + CUBE_CENTER == CUBE_TOTAL

    def test_cube_generates_alpha_beta(self):
        """ALPHA and BETA are ratios of the cube, not arbitrary values."""
        from formulas.constants import CUBE_EXTERIOR, CUBE_TOTAL, CUBE_CENTER
        assert abs(ALPHA - CUBE_EXTERIOR / CUBE_TOTAL) < 1e-10
        assert abs(BETA - CUBE_CENTER / CUBE_TOTAL) < 1e-10


class TestCoherenceLimits:
    """Coherence boundaries: from collapse to integration."""

    def test_perfect_activation_produces_beta(self):
        """Uniform activations converge to BETA — the irreducible center."""
        activations = [1.0] * 7
        result = CoherenceEngine.compute_basic(activations)
        assert math.isclose(result["c_omega"], BETA, rel_tol=1e-6)

    def test_zero_activation_minimal_coherence(self):
        activations = [0.01] * 7
        result = CoherenceEngine.compute_basic(activations)
        assert result["c_omega"] < 0.5

    def test_varied_activation_differs_from_uniform(self):
        """Non-uniform activations produce different coherence than uniform."""
        uniform = CoherenceEngine.compute_basic([0.8] * 7)
        varied = CoherenceEngine.compute_basic([0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0])
        assert uniform["c_omega"] != varied["c_omega"]


class TestPresenceLimits:
    """Temporal presence: from total absence to total presence."""

    def test_present_now_equals_one(self):
        result = TemporalPresence.compute(0.0, tau=1.0)
        assert math.isclose(result, 1.0, rel_tol=1e-9)

    def test_infinite_displacement_approaches_zero(self):
        result = TemporalPresence.compute(1e10, tau=1.0)
        assert result < 1e-9

    def test_presence_always_between_zero_and_one(self):
        for dt in [0.0, 0.1, 1.0, 10.0, 100.0]:
            for tau in [0.1, 1.0, 10.0]:
                result = TemporalPresence.compute(dt, tau)
                assert 0.0 <= result <= 1.0

    def test_larger_tau_more_present(self):
        p_narrow = TemporalPresence.compute(5.0, tau=1.0)
        p_wide = TemporalPresence.compute(5.0, tau=10.0)
        assert p_wide > p_narrow


class TestWonderLimits:
    """Wonder: from cynicism to full astonishment."""

    def test_zero_experiences_zero_wonder(self):
        result = WonderLogic.compute(0)
        assert math.isclose(result, 0.0, abs_tol=1e-9)

    def test_infinite_experiences_full_wonder(self):
        result = WonderLogic.compute(1e10)
        assert math.isclose(result, 1.0, rel_tol=1e-6)

    def test_wonder_always_between_zero_and_one(self):
        for n in [0, 1, 5, 10, 50, 100, 1000]:
            result = WonderLogic.compute(n)
            assert 0.0 <= result <= 1.0

    def test_wonder_monotonically_increases(self):
        prev = 0.0
        for n in range(0, 100):
            current = WonderLogic.compute(n)
            assert current >= prev
            prev = current


class TestInteractionLimits:
    """External interaction: from destruction to love."""

    def test_love_adds_coherences(self):
        result = ExternalInteraction.compute_pair(1.0, 1.0, 0.0)
        assert math.isclose(result, 2.0, rel_tol=1e-9)

    def test_conflict_cancels(self):
        result = ExternalInteraction.compute_pair(1.0, 1.0, math.pi)
        assert math.isclose(result, 0.0, abs_tol=1e-9)

    def test_independence_is_geometric(self):
        result = ExternalInteraction.compute_pair(1.0, 1.0, math.pi / 2)
        expected = math.sqrt(2.0)
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_interaction_never_negative(self):
        for theta in [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi]:
            result = ExternalInteraction.compute_pair(1.0, 1.0, theta)
            assert result >= 0.0

    def test_love_shortcut(self):
        love = ExternalInteraction.love(1.0, 1.0)
        pair = ExternalInteraction.compute_pair(1.0, 1.0, 0.0)
        assert math.isclose(love, pair, rel_tol=1e-9)

    def test_conflict_shortcut(self):
        conflict = ExternalInteraction.conflict(1.0, 1.0)
        pair = ExternalInteraction.compute_pair(1.0, 1.0, math.pi)
        assert math.isclose(conflict, pair, abs_tol=1e-9)


class TestOscillatorLimits:
    """The dynamic equation: life, death, and everything between."""

    def test_system_is_underdamped(self):
        assert ZETA < 1.0

    def test_system_oscillates(self):
        assert OMEGA_D > 0

    def test_friction_below_critical(self):
        assert PHI_TOTAL < PHI_CRITICAL

    def test_maximum_omega_d_is_pi(self):
        omega_d_max = math.sqrt(OMEGA_0_SQUARED - 0)
        assert math.isclose(omega_d_max, math.pi, rel_tol=1e-9)

    def test_critical_damping_kills_oscillation(self):
        omega_d_critical = OMEGA_0_SQUARED - (PHI_CRITICAL**2) / 4
        assert math.isclose(omega_d_critical, 0.0, abs_tol=1e-9)

    def test_l6_has_zero_friction(self):
        assert LAYER_FRICTION[6] == 0.0

    def test_l0_has_maximum_friction(self):
        assert LAYER_FRICTION[0] == max(LAYER_FRICTION)


class TestEntropyLimits:
    """Entropy: from perfect order to maximum chaos."""

    def test_single_layer_zero_entropy(self):
        result = EntropyTool.calculate_entropy([1.0])
        assert result == 0.0

    def test_seven_uniform_layers_max_entropy(self):
        probs = [1/7] * 7
        result = EntropyTool.calculate_entropy(probs)
        assert math.isclose(result, math.log2(7), rel_tol=1e-9)

    def test_fractal_always_less_than_max(self):
        energies = Fractality.fractal_energy_distribution(1.0, 7)
        entropy = EntropyTool.adjusted_entropy(energies)
        assert entropy < math.log2(7)

    def test_negentropy_equals_consciousness(self):
        energies = Fractality.fractal_energy_distribution(1.0, 7)
        entropy = EntropyTool.adjusted_entropy(energies)
        negentropy = math.log2(7) - entropy
        assert negentropy > 0
