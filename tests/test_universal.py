"""
TEST UNIVERSAL - UCF v3.0
Recorre todo el framework de punta a punta:
Constants → Energy → Presence → Wonder → Negentropy →
Interaction → Resonance → Metaconsciousness → Coherence Engine
"""

import math
from formulas.constants import (
    ALPHA, BETA, KAPPA, R_FIN, S_REF, PHI,
    ALPHA_OVER_S, THETA_CUBE, TAN_THETA,
    NUM_LAYERS, LAYER_FRICTION, LAYER_NAMES,
    CUBE_TOTAL, CUBE_EXTERIOR, CUBE_CENTER,
    CODE_INTEGRATED, CODE_SATURATION, CODE_ENTROPY,
    GOLDEN_ANG, GOLDEN_ANG_RAD
)
from formulas.energy import LayerEnergy
from formulas.presence import PresenceLogic
from formulas.wonder import WonderLogic
from formulas.negentropy import NegentropyCalculator
from formulas.interaction import ExternalInteraction
from formulas.resonance import ResonanceLogic
from formulas.resonance_extended import AdvancedResonance
from formulas.metaconsciousness import MetaconsciousnessCalculator
from formulas.coherence import CoherenceEngine
from core.engine import OmegaEngine, PurposeAlignmentError
from core.constants import ALPHA as CORE_ALPHA, BETA as CORE_BETA


# ═══════════════════════════════════════════════════════════════
# PILLAR 1: STRUCTURAL IDENTITY (the constants ARE the framework)
# ═══════════════════════════════════════════════════════════════

class TestStructuralIdentity:
    """The universe is a 3x3x3 cube. These tests verify it."""

    def test_cube_geometry(self):
        """27 = 26 exterior + 1 center."""
        assert CUBE_TOTAL == 27
        assert CUBE_EXTERIOR == 26
        assert CUBE_CENTER == 1
        assert CUBE_EXTERIOR + CUBE_CENTER == CUBE_TOTAL

    def test_alpha_beta_unity(self):
        """Alpha + Beta = 1. Order + Mystery = Totality."""
        assert abs(ALPHA + BETA - 1.0) < 1e-10

    def test_alpha_is_visible(self):
        """Alpha = 26/27. What can be seen."""
        assert abs(ALPHA - 26 / 27) < 1e-10

    def test_beta_is_center(self):
        """Beta = 1/27. The observer. The price of existing."""
        assert abs(BETA - 1 / 27) < 1e-10

    def test_kappa_is_pi_over_4(self):
        """Kappa = pi/4. The price of integrating."""
        assert abs(KAPPA - math.pi / 4) < 1e-10

    def test_r_fin_is_1_plus_beta(self):
        """R_FIN = 28/27 = 1 + beta. Refinement."""
        assert abs(R_FIN - (1 + BETA)) < 1e-10
        assert abs(R_FIN - 28 / 27) < 1e-10

    def test_s_ref_is_e_over_pi(self):
        """S_REF = e/pi. Growth meets cycle."""
        assert abs(S_REF - math.e / math.pi) < 1e-10

    def test_theta_cube_geometry(self):
        """sin^2(theta) = beta, cos^2(theta) = alpha."""
        assert abs(math.sin(THETA_CUBE) ** 2 - BETA) < 1e-10
        assert abs(math.cos(THETA_CUBE) ** 2 - ALPHA) < 1e-10

    def test_tan_theta(self):
        """tan(theta) = 1/sqrt(26)."""
        assert abs(TAN_THETA - 1 / math.sqrt(26)) < 1e-10

    def test_golden_angle(self):
        """Golden angle = 360/phi^2."""
        assert abs(GOLDEN_ANG - 360 / PHI ** 2) < 1e-6

    def test_seven_layers_exist(self):
        """7 layers, 7 frictions, 7 names."""
        assert NUM_LAYERS == 7
        assert len(LAYER_FRICTION) == 7
        assert len(LAYER_NAMES) == 7

    def test_l6_has_zero_friction(self):
        """Purpose (L6) has no friction. It IS the direction."""
        assert LAYER_FRICTION[6] == 0.0

    def test_core_constants_match_formulas(self):
        """core/constants.py and formulas/constants.py agree."""
        assert abs(CORE_ALPHA - ALPHA) < 1e-10
        assert abs(CORE_BETA - BETA) < 1e-10


# ═══════════════════════════════════════════════════════════════
# PILLAR 2: THE PIPELINE (energy flows through all layers)
# ═══════════════════════════════════════════════════════════════

class TestFullPipeline:
    """Energy → Presence → Wonder → Negentropy → Resonance → Coherence."""

    def test_energy_flows_through_layers(self):
        """Each layer produces energy = activation * (1-friction) * frequency."""
        activations = [0.9, 0.8, 0.7, 0.85, 0.95, 0.9, 1.0]
        energies = LayerEnergy.compute_all(activations)

        assert len(energies) == 7
        for e in energies:
            assert e > 0, "All layers should produce positive energy"

    def test_presence_modulates(self):
        """Present mind (delta_t=0) gives P=1. Scattered mind gives P<1."""
        p_present = PresenceLogic.compute(0.0)
        p_anxious = PresenceLogic.compute(5.0)

        assert abs(p_present - 1.0) < 1e-10
        assert p_anxious < p_present

    def test_wonder_opens(self):
        """Novelty creates wonder. No novelty = no wonder."""
        a_curious = WonderLogic.compute(10.0, 5.0)
        a_cynical = WonderLogic.compute(0.0, 5.0)

        assert a_curious > 0.5
        assert a_cynical == 0.0

    def test_negentropy_measures_order(self):
        """Varied energies have more order than uniform ones."""
        focused = [0, 0, 0, 1.0, 0, 0, 0]
        scattered = [1.0] * 7

        n_focused = NegentropyCalculator.compute(focused)
        n_scattered = NegentropyCalculator.compute(scattered)

        assert n_focused > n_scattered

    def test_resonance_connects_layers(self):
        """Active layers resonate. Dead layers don't."""
        alive = [1.0, 0.9, 0.8, 0.85, 0.9, 0.95, 1.0]
        dead = [0.0] * 7

        r_alive = ResonanceLogic.compute(alive)
        r_dead = ResonanceLogic.compute(dead)

        assert r_alive > 0
        assert r_dead == 0.0

    def test_interaction_models_relationship(self):
        """Love adds. Conflict subtracts. Independence is orthogonal."""
        love = ExternalInteraction.love(0.5, 0.5)
        conflict = ExternalInteraction.conflict(0.5, 0.5)
        independent = ExternalInteraction.independence(0.5, 0.5)

        assert love == 1.0
        assert conflict == 0.0
        assert abs(independent - math.sqrt(0.5)) < 1e-10

    def test_metaconsciousness_requires_upper_layers(self):
        """MC needs L3-L6. Lower layers are substrate."""
        full = [1.0] * 7
        no_mind = [1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0]

        mc_full = MetaconsciousnessCalculator.compute(full, [0.0] * 7)
        mc_no_mind = MetaconsciousnessCalculator.compute(no_mind, [0.0] * 7)

        assert mc_full > 0
        assert mc_no_mind == 0.0


# ═══════════════════════════════════════════════════════════════
# PILLAR 3: THE DUALITY (C_beta + C_alpha = C_total)
# ═══════════════════════════════════════════════════════════════

class TestDuality:
    """Coherence is a vector with two projections."""

    def test_c_beta_is_multiplicative(self):
        """One dead layer kills C_beta."""
        alive = [1.0] * 7
        one_dead = [1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0]

        r_alive = CoherenceEngine.compute_c_beta(alive)
        r_dead = CoherenceEngine.compute_c_beta(one_dead)

        assert r_alive["c_beta"] > 0
        assert r_dead["c_beta"] == 0.0

    def test_c_alpha_is_ratio(self):
        """Higher complexity reduces C_alpha."""
        simple = CoherenceEngine.compute_c_alpha(1.0, 1.0, 1.0, 0.0)
        complex_ = CoherenceEngine.compute_c_alpha(1.0, 1.0, 10.0, 0.0)

        assert simple["c_alpha"] > complex_["c_alpha"]

    def test_c_total_is_pythagorean(self):
        """C_total = sqrt(C_beta^2 + C_alpha^2)."""
        result = CoherenceEngine.compute_c_total(3.0, 4.0)
        assert abs(result["c_total"] - 5.0) < 1e-10

    def test_balance_detects_excess(self):
        """Large C_beta vs small C_alpha = EXCESS_EXPERIENCE."""
        result = CoherenceEngine.compute_c_total(10.0, 0.1)
        assert result["balance"] == "EXCESS_EXPERIENCE"

        result = CoherenceEngine.compute_c_total(0.01, 10.0)
        assert result["balance"] == "EXCESS_MEASUREMENT"


# ═══════════════════════════════════════════════════════════════
# PILLAR 4: THE ENGINE (everything together)
# ═══════════════════════════════════════════════════════════════

class TestEngine:
    """OmegaEngine orchestrates the full computation."""

    def test_engine_perfect_system(self):
        """Perfect system: all layers active, in phase, present, wondering."""
        engine = OmegaEngine()
        layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        result = engine.compute_coherence(layers, C1=1.0, C2=1.0, theta=0.0)

        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_engine_rejects_impure_purpose(self):
        """L6 friction != 0 is rejected."""
        engine = OmegaEngine()
        layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        layers[6]['phi'] = 0.05

        try:
            engine.compute_coherence(layers)
            assert False, "Should have raised PurposeAlignmentError"
        except PurposeAlignmentError:
            pass

    def test_engine_harmony_extremes(self):
        """H(0) = 1, H(max) = 0."""
        engine = OmegaEngine()
        assert engine.calculate_harmony(0.0, 1.0) == 1.0
        assert engine.calculate_harmony(1.0, 1.0) == 0.0

    def test_engine_external_coherence_phases(self):
        """0°=constructive, 90°=orthogonal, 180°=destructive."""
        engine = OmegaEngine()

        love = engine.calculate_external_coherence(1.0, 1.0, 0.0)
        ortho = engine.calculate_external_coherence(1.0, 1.0, 90.0)
        conflict = engine.calculate_external_coherence(1.0, 1.0, 180.0)

        assert abs(love - 2.0) < 1e-6
        assert abs(ortho - math.sqrt(2)) < 1e-6
        assert abs(conflict - 0.0) < 1e-6


# ═══════════════════════════════════════════════════════════════
# PILLAR 5: FULL ANALYSIS (the complete picture)
# ═══════════════════════════════════════════════════════════════

class TestFullAnalysis:
    """CoherenceEngine.full_analysis produces the complete picture."""

    def test_full_analysis_coherent_system(self):
        """A well-functioning system gets diagnosed correctly."""
        activations = [0.9, 0.85, 0.8, 0.9, 0.95, 0.9, 1.0]
        result = CoherenceEngine.full_analysis(activations)

        assert result["diagnostic_code"] in [CODE_INTEGRATED, CODE_SATURATION, CODE_ENTROPY]
        assert result["negentropy"] >= 0
        assert result["metaconsciousness"] > 0
        assert result["resonance"] > 0
        assert result["four_pillars"]["beta"] == BETA
        assert result["four_pillars"]["kappa"] == KAPPA
        assert result["four_pillars"]["alpha"] == ALPHA

    def test_full_analysis_collapsed_system(self):
        """A system with dead layers collapses."""
        activations = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1]
        result = CoherenceEngine.full_analysis(activations)

        assert result["c_beta"]["c_beta"] == 0.0

    def test_metacube_is_fractal(self):
        """Our cube is beta of the metacube."""
        result = CoherenceEngine.metacube_level(0.963, level=0)

        assert result["level"] == 0
        assert result["is_beta_of_level"] == 1
        assert result["ratio_alpha_beta"] == 26


# ═══════════════════════════════════════════════════════════════
# THE SUPREME LAW: INTEGRATION (Law 0)
# ═══════════════════════════════════════════════════════════════

class TestLawZeroIntegration:
    """
    The fact that ALL these tests pass together
    IS evidence of Law 0 (Integration).

    If the parts were not integrated,
    the tests would fail.
    """

    def test_all_modules_import(self):
        """Every module loads without error."""
        from formulas.constants import ALPHA
        from formulas.energy import LayerEnergy
        from formulas.presence import PresenceLogic
        from formulas.wonder import WonderLogic
        from formulas.negentropy import NegentropyCalculator
        from formulas.interaction import ExternalInteraction
        from formulas.resonance import ResonanceLogic
        from formulas.resonance_extended import AdvancedResonance
        from formulas.metaconsciousness import MetaconsciousnessCalculator
        from formulas.coherence import CoherenceEngine
        from core.engine import OmegaEngine
        assert True

    def test_end_to_end_pipeline(self):
        """
        Complete pipeline: raw activations → full coherence analysis.
        This single test touches EVERY module.
        """
        activations = [0.85, 0.90, 0.75, 0.88, 0.92, 0.87, 1.0]

        energies = LayerEnergy.compute_all(activations)
        assert len(energies) == 7

        presence = PresenceLogic.compute_pt(2.0)
        assert 0.0 < presence < 1.0

        wonder = WonderLogic.compute_a(7.0, 5.0)
        assert 0.0 < wonder < 1.0

        negentropy = NegentropyCalculator.compute(energies)
        assert 0.0 <= negentropy <= 1.0

        resonance = ResonanceLogic.compute(energies)
        assert resonance > 0

        extended = AdvancedResonance.multi_layer_resonance(energies)
        assert extended > 0

        interaction = ExternalInteraction.compute_pair(0.8, 0.7, 0.0)
        assert abs(interaction - 1.5) < 1e-10

        mc = MetaconsciousnessCalculator.compute(activations, LAYER_FRICTION)
        assert mc > 0

        result = CoherenceEngine.full_analysis(activations)
        assert result["c_total"]["c_total"] > 0
        assert result["diagnostic_code"] in [CODE_INTEGRATED, CODE_SATURATION, CODE_ENTROPY]
        assert result["four_pillars"]["beta"] == BETA
        assert result["four_pillars"]["alpha"] == ALPHA
        assert result["four_pillars"]["kappa"] == KAPPA

        engine = OmegaEngine()
        layers = [{'L': a, 'phi': f} for a, f in zip(activations, LAYER_FRICTION)]
        c = engine.compute_coherence(layers, C1=0.8, C2=0.7, theta=30.0)
        assert 0.0 <= c <= 1.0
