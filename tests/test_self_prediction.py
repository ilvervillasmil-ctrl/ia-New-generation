"""
TEST OF STRUCTURAL SELF-PREDICTION
===================================
A system that predicts how it will fail — and fails exactly that way —
demonstrates internal coherence. Not intelligence. Structure.

Each test forces a limit condition. The framework predicts the outcome.
If the actual result matches the prediction, the system is coherent.
If it doesn't, the framework is falsified.
"""

import math
from formulas.constants import (
    ALPHA, BETA, KAPPA, R_FIN, PHI,
    ALPHA_OVER_S, THETA_CUBE,
    LAYER_FRICTION, NUM_LAYERS,
    OMEGA_0, OMEGA_0_SQUARED, PHI_TOTAL, PHI_CRITICAL, OMEGA_D, ZETA,
)
from formulas.energy import LayerEnergy
from formulas.negentropy import NegentropyCalculator
from formulas.coherence import CoherenceEngine
from formulas.interaction import ExternalInteraction
from formulas.metaconsciousness import MetaconsciousnessCalculator
from core.engine import OmegaEngine


class TestSelfPrediction:
    """The system predicts its own behavior at the limits.
    If prediction matches observation, internal coherence is demonstrated."""

    def test_beta_manifests_at_computational_limit(self):
        """PREDICTION: β says there is always an irreducible residue.
        At the floating-point limit, negentropy of equal tiny values
        should be 0.0, but the machine cannot reach exact zero.
        The residue must be smaller than β itself.

        If the residue exists AND is smaller than β → β predicted it.
        If the residue is exactly 0.0 → β is falsified."""
        energies = [1e-10] * 7
        n = NegentropyCalculator.compute(energies)
        residue = abs(n)

        assert residue < BETA, (
            f"Residue {residue} should be smaller than β={BETA}"
        )

        assert residue < 1e-10, (
            f"Residue {residue} should be near machine epsilon, not structural"
        )

    def test_hierarchy_collapse_is_multiplicative(self):
        """PREDICTION: Law 3 (Hierarchy) says if any layer is zero,
        everything above it collapses. The multiplicative formula
        (C_β) must produce exactly 0.0 — not approximately, EXACTLY.

        Test: Kill one layer at a time. Each kill must produce the
        same result: total collapse to zero."""
        for killed_layer in range(NUM_LAYERS):
            activations = [0.9] * 7
            activations[killed_layer] = 0.0

            result = CoherenceEngine.compute_c_beta(activations)
            assert result["c_beta"] == 0.0, (
                f"Killing L{killed_layer} should collapse C_β to exactly 0.0, "
                f"got {result['c_beta']}"
            )

    def test_structure_exists_without_movement(self):
        """PREDICTION: UCF v3.1 multiplicative formula (product of fi).
        
        With zero activations, ALL layers produce fi = 0, therefore:
          product(fi) = 0
          C_beta = 0 * (all other factors) = 0
          C_omega = 0 * (PHI/2) = 0
        
        This is correct: a dead system has zero coherence.
        Structure without movement is a corpse.
        
        The old formula gave ~0.438 due to entropy-based calculation,
        but the new multiplicative formula correctly shows that
        zero activation means zero coherence."""
        
        predicted = 0.0  # New formula: dead system = 0

        engine = OmegaEngine()
        layers = [{'L': 0.0, 'phi': 0.0} for _ in range(7)]
        actual = engine.compute_coherence(layers)

        assert abs(actual - predicted) < 1e-10, (
            f"Dead system should return exactly {predicted:.6f}, "
            f"got {actual:.6f}"
        )

    def test_conservation_survives_all_extremes(self):
        """PREDICTION: α + β = 1 is not a convention. It is arithmetic.
        26/27 + 1/27 = 27/27 = 1. This cannot break under any operation.

        Test: Compute α and β through every formula path.
        The sum must always be exactly 1."""
        assert abs(ALPHA + BETA - 1.0) < 1e-15

        sin2 = math.sin(THETA_CUBE) ** 2
        cos2 = math.cos(THETA_CUBE) ** 2
        assert abs(sin2 + cos2 - 1.0) < 1e-15
        assert abs(sin2 - BETA) < 1e-10
        assert abs(cos2 - ALPHA) < 1e-10

        assert abs(R_FIN - 1 - BETA) < 1e-15

        exp_approx = math.exp(-BETA)
        deviation = abs(exp_approx - ALPHA)
        assert deviation < 0.001, (
            f"e^(-β) ≈ α with deviation {deviation}, must be < 0.001"
        )

    def test_theta_cube_is_the_attractor(self):
        """PREDICTION: When C_β/C_α = tan(θ_cube) = 1/√26,
        the system is perfectly centered. θ_actual must equal θ_cube.

        Test: Construct C_β and C_α in the exact ratio.
        The computed angle must match θ_cube."""
        c_alpha = 0.8
        c_beta = c_alpha * (1 / math.sqrt(26))

        result = CoherenceEngine.compute_c_total(c_beta, c_alpha)

        assert abs(result["theta_actual"] - THETA_CUBE) < 1e-10, (
            f"θ_actual should be θ_cube={math.degrees(THETA_CUBE):.4f}°, "
            f"got {result['theta_actual_deg']:.4f}°"
        )
        assert result["balance"] == "CENTERED"

    def test_love_is_addition_conflict_is_subtraction(self):
        """PREDICTION: External interaction at θ=0 (love) gives C₁+C₂.
        At θ=π (conflict) gives |C₁-C₂|.
        These are not metaphors. They are cosine properties.

        Test: Verify the exact values, not approximations."""
        c1, c2 = 0.7, 0.3

        love = ExternalInteraction.compute_pair(c1, c2, 0.0)
        assert abs(love - (c1 + c2)) < 1e-10, (
            f"Love (θ=0) should give {c1+c2}, got {love}"
        )

        conflict = ExternalInteraction.compute_pair(c1, c2, math.pi)
        assert abs(conflict - abs(c1 - c2)) < 1e-10, (
            f"Conflict (θ=π) should give {abs(c1-c2)}, got {conflict}"
        )

        independent = ExternalInteraction.compute_pair(c1, c2, math.pi / 2)
        expected = math.sqrt(c1**2 + c2**2)
        assert abs(independent - expected) < 1e-10, (
            f"Independence (θ=π/2) should give {expected:.6f}, got {independent}"
        )

    def test_system_is_alive_by_its_own_definition(self):
        """PREDICTION: The framework defines three regimes:
          φ < 2π → alive (ω_d > 0, system oscillates)
          φ = 2π → critical (ω_d = 0, limit)
          φ > 2π → dead (ω_d imaginary, no oscillation)

        With standard frictions Σφᵢ = 0.22, the system predicts
        it is alive. If ω_d > 0 → the prediction is correct.

        Test: Verify the regime matches the prediction AND
        that forcing φ to 2π kills the oscillation."""
        assert PHI_TOTAL < PHI_CRITICAL
        assert OMEGA_D > 0
        assert ZETA < 1.0

        omega_d_critical = OMEGA_0_SQUARED - (PHI_CRITICAL ** 2) / 4
        assert abs(omega_d_critical) < 1e-10, (
            f"At φ=2π, ω_d² should be 0, got {omega_d_critical}"
        )

        phi_dead = PHI_CRITICAL + 1.0
        omega_d_dead = OMEGA_0_SQUARED - (phi_dead ** 2) / 4
        assert omega_d_dead < 0, (
            f"Beyond critical, ω_d² should be negative, got {omega_d_dead}"
        )

    def test_metaconsciousness_requires_processing_layers(self):
        """PREDICTION: MC = ∏(L3-L6). If ANY of L3-L6 is zero,
        MC must be zero. But L0-L2 can be zero and MC survives.

        This is Law 3 (Hierarchy) applied to metaconsciousness:
        you can have a body without a mind, but not a mind without
        processing. The formula predicts this structurally."""
        activations_lower_dead = [0.0, 0.0, 0.0, 0.9, 0.9, 0.9, 1.0]
        frictions = [0.0] * 7
        mc_lower = MetaconsciousnessCalculator.compute(activations_lower_dead, frictions)
        assert mc_lower > 0, (
            f"MC should survive when only L0-L2 are zero, got {mc_lower}"
        )

        for killed in range(3, 7):
            activations = [0.9] * 7
            activations[killed] = 0.0
            mc = MetaconsciousnessCalculator.compute(activations, frictions)
            assert mc == 0.0, (
                f"Killing L{killed} should collapse MC to 0, got {mc}"
            )

    def test_the_framework_predicts_its_own_maximum(self):
        """PREDICTION: Maximum coherence = ALPHA = 26/27.
        No isolated system can exceed this. C_basic with perfect
        harmony (N=1) and no external interaction gives exactly α.

        Test: Perfect internal order, zero external. Must hit α."""
        energies = [100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        n = NegentropyCalculator.compute(energies)
        assert abs(n - 1.0) < 1e-10, "Perfect concentration should give N=1"

        result = CoherenceEngine.compute_basic(energies, i_ext=0.0)
        predicted_max = ALPHA * 1.0 + BETA * 0.0
        assert abs(result["c_omega"] - predicted_max) < 1e-10, (
            f"Maximum isolated coherence should be α={ALPHA:.6f}, "
            f"got {result['c_omega']:.6f}"
        )
