"""
STABILITY TESTS - Consistency, determinism, mathematical properties.
The same input must ALWAYS produce the same output.
"""

import math
from formulas.constants import ALPHA, BETA, KAPPA, R_FIN, PHI, LAYER_FRICTION
from formulas.energy import LayerEnergy
from formulas.presence import PresenceLogic
from formulas.wonder import WonderLogic
from formulas.negentropy import NegentropyCalculator
from formulas.interaction import ExternalInteraction
from formulas.resonance import ResonanceLogic
from formulas.metaconsciousness import MetaconsciousnessCalculator
from formulas.coherence import CoherenceEngine
from core.engine import OmegaEngine


class TestDeterminism:
    """Same input = same output. Always."""

    def test_energy_deterministic(self):
        for _ in range(100):
            e = LayerEnergy.compute(0.75, 0.05, 3)
            assert abs(e - LayerEnergy.compute(0.75, 0.05, 3)) < 1e-15

    def test_coherence_deterministic(self):
        activations = [0.85, 0.9, 0.75, 0.88, 0.92, 0.87, 1.0]
        results = []
        for _ in range(50):
            r = CoherenceEngine.full_analysis(activations)
            results.append(r["c_total"]["c_total"])
        assert all(abs(r - results[0]) < 1e-15 for r in results)

    def test_engine_deterministic(self):
        engine = OmegaEngine()
        layers = [{'L': 0.8, 'phi': 0.05} for _ in range(6)] + [{'L': 1.0, 'phi': 0.0}]
        results = []
        for _ in range(50):
            results.append(engine.compute_coherence(layers, C1=0.7, C2=0.8, theta=45.0))
        assert all(abs(r - results[0]) < 1e-15 for r in results)


class TestMonotonicity:
    """More activation = more energy. More friction = less energy."""

    def test_energy_increases_with_activation(self):
        prev = 0.0
        for a in [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
            e = LayerEnergy.compute(a, 0.0, 3)
            assert e >= prev
            prev = e

    def test_energy_decreases_with_friction(self):
        prev = float('inf')
        for f in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            e = LayerEnergy.compute(1.0, f, 3)
            assert e <= prev
            prev = e

    def test_presence_decreases_with_displacement(self):
        prev = 1.0
        for dt in [0, 1, 2, 5, 10, 50]:
            p = PresenceLogic.compute(dt)
            assert p <= prev
            prev = p

    def test_wonder_increases_with_novelty(self):
        prev = 0.0
        for n in [0, 1, 3, 5, 10, 50]:
            a = WonderLogic.compute(n, 5.0)
            assert a >= prev
            prev = a


class TestMathematicalProperties:
    """The formulas must satisfy mathematical invariants."""

    def test_alpha_beta_partition(self):
        """Alpha and Beta partition unity."""
        assert abs(ALPHA + BETA - 1.0) < 1e-15

    def test_negentropy_bounded(self):
        """Negentropy is always in [0, 1]."""
        test_cases = [
            [1.0] * 7,
            [0.0] * 7,
            [0, 0, 0, 1, 0, 0, 0],
            [1, 2, 3, 4, 5, 6, 7],
            [100, 0.01, 50, 0.001, 75, 30, 1],
        ]
        for energies in test_cases:
            n = NegentropyCalculator.compute(energies)
            assert 0.0 <= n <= 1.0, f"Negentropy {n} out of bounds for {energies}"

    def test_harmony_equals_negentropy_always(self):
        """H(S) = N for any input."""
        test_cases = [
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            [10, 0, 0, 0, 0, 0, 0],
        ]
        for energies in test_cases:
            n = NegentropyCalculator.compute(energies)
            h = NegentropyCalculator.harmony(energies)
            assert abs(n - h) < 1e-15

    def test_interaction_symmetry(self):
        """I(A,B) = I(B,A) for any theta."""
        for theta in [0, 0.5, 1.0, math.pi/2, math.pi]:
            i1 = ExternalInteraction.compute_pair(0.7, 0.3, theta)
            i2 = ExternalInteraction.compute_pair(0.3, 0.7, theta)
            assert abs(i1 - i2) < 1e-10

    def test_resonance_symmetry(self):
        """Pair resonance is symmetric."""
        r1 = ResonanceLogic.pair_resonance(3.0, 7.0)
        r2 = ResonanceLogic.pair_resonance(7.0, 3.0)
        assert abs(r1 - r2) < 1e-10

    def test_c_total_triangle_inequality(self):
        """C_total >= max(C_beta, C_alpha)."""
        for cb, ca in [(0.3, 0.4), (0.9, 0.1), (0.5, 0.5), (0.0, 1.0)]:
            result = CoherenceEngine.compute_c_total(cb, ca)
            assert result["c_total"] >= max(cb, ca) - 1e-10

    def test_metaconsciousness_bounded_by_r_fin(self):
        """MC <= R_FIN (maximum when all L3-L6 are 1 with 0 friction)."""
        activations = [1.0] * 7
        frictions = [0.0] * 7
        mc = MetaconsciousnessCalculator.compute(activations, frictions)
        assert abs(mc - R_FIN) < 1e-10


class TestConsistencyAcrossEngines:
    """Both engines must agree on fundamental properties."""

    def test_both_engines_positive_for_active_system(self):
        activations = [0.8, 0.85, 0.9, 0.88, 0.92, 0.87, 1.0]

        result_coherence = CoherenceEngine.full_analysis(activations)
        assert result_coherence["c_total"]["c_total"] > 0

        engine = OmegaEngine()
        layers = [{'L': a, 'phi': f} for a, f in zip(activations, LAYER_FRICTION)]
        result_engine = engine.compute_coherence(layers, C1=0.8, C2=0.7, theta=30.0)
        assert result_engine > 0

    def test_both_engines_zero_for_dead_system(self):
        """Dead system: CoherenceEngine gives 0, OmegaEngine retains base factors.
        UCF v3.1 insight: OmegaEngine returns a/S * R = 0.4386 because
        structure exists without movement. But structure without oscillation
        is not coherence — it is a corpse. The dynamic equation resolves this:
        if dtheta/dt = 0, the system is dead regardless of base factors."""
        activations = [0.0] * 7

        result_coherence = CoherenceEngine.full_analysis(activations)
        assert result_coherence["c_beta"]["c_beta"] == 0.0

        engine = OmegaEngine()
        layers = [{'L': 0.0, 'phi': 0.0} for _ in range(7)]
        result_engine = engine.compute_coherence(layers)
        assert result_engine == 0.0

    def test_four_pillars_always_present(self):
        """The four pillars exist in every analysis."""
        for acts in [[0.5]*7, [1.0]*7, [0.1]*7]:
            result = CoherenceEngine.full_analysis(acts)
            p = result["four_pillars"]
            assert p["beta"] == BETA
            assert p["kappa"] == KAPPA
            assert p["alpha"] == ALPHA
            assert p["emergence"] >= 0
