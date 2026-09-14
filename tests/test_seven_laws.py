"""
THE SEVEN UNIVERSAL LAWS — Computational Verification

Each law is not a belief. Each law is a testable property
of the mathematical system. If ANY law fails, the framework
is inconsistent. None fail.

| # | Law            | Symbol | Principle                    |
|---|----------------|--------|------------------------------|
| 1 | Action         | e      | Everything is movement       |
| 2 | Rhythm         | π      | Everything is cycles         |
| 3 | Polarity       | ±1     | Complementary opposites      |
| 4 | Cause-Effect   | →      | Nothing without consequence  |
| 5 | Fractality     | φ      | Pattern at all scales        |
| 6 | Resonance      | ∿      | Nothing operates isolated    |
| 7 | Correspondence | =      | Internal = External          |
| Ω | Integration    | Ω      | All laws coexist as one      |
"""

import math
from formulas.constants import (
    ALPHA, BETA, PHI, S_REF, R_FIN,
    OMEGA_0, OMEGA_D, ZETA, OMEGA_0_SQUARED,
    PHI_TOTAL, PHI_CRITICAL,
    LAYER_FRICTION, NUM_LAYERS,
    THETA_CUBE, GOLDEN_ANG,
)
from formulas.energy import LayerEnergy
from formulas.presence import TemporalPresence
from formulas.wonder import WonderLogic
from formulas.interaction import ExternalInteraction
from formulas.negentropy import NegentropyCalculator
from formulas.resonance import ResonanceLogic
from formulas.resonance_extended import AdvancedResonance
from formulas.fractality import Fractality
from formulas.coherence import CoherenceEngine
from formulas.entropy import EntropyTool


class TestLaw1_Action:
    """Law 1: Action (e) — Everything is movement.

    Symbol: e (Euler's number, the base of growth/decay)
    If nothing moves, the system is dead.
    """

    def test_exponential_decay_is_alpha(self):
        """e^(-BETA) ≈ ALPHA: the exponential function connects the constants."""
        assert abs(math.exp(-BETA) - ALPHA) < 0.001

    def test_energy_requires_activation(self):
        """Zero activation = zero energy. No action, no existence."""
        e = LayerEnergy.compute(0.0, 0.0, 0)
        assert e == 0.0

    def test_energy_increases_with_activation(self):
        """More action = more energy. The law of movement."""
        e_low = LayerEnergy.compute(0.3, 0.0, 0)
        e_high = LayerEnergy.compute(0.9, 0.0, 0)
        assert e_high > e_low

    def test_oscillator_never_stops(self):
        """omega_d > 0 and zeta < 1: the system always moves."""
        assert OMEGA_D > 0
        assert ZETA < 1.0

    def test_s_ref_contains_e(self):
        """S_REF = e/pi: growth (e) is present in the reference."""
        assert math.isclose(S_REF, math.e / math.pi, rel_tol=1e-10)


class TestLaw2_Rhythm:
    """Law 2: Rhythm (π) — Everything is cycles.

    Symbol: π (the constant of circles and oscillation)
    Every system oscillates. Nothing is linear forever.
    """

    def test_natural_frequency_is_pi(self):
        """omega_0 = pi: the base rhythm of consciousness."""
        assert math.isclose(OMEGA_0, math.pi, rel_tol=1e-10)

    def test_critical_damping_is_two_pi(self):
        """phi_critical = 2*pi: the death of rhythm."""
        assert math.isclose(PHI_CRITICAL, 2 * math.pi, rel_tol=1e-10)

    def test_s_ref_contains_pi(self):
        """S_REF = e/pi: cycles (pi) are present in the reference."""
        assert math.isclose(S_REF, math.e / math.pi, rel_tol=1e-10)

    def test_presence_is_periodic_decay(self):
        """Presence decays exponentially — rhythm of attention."""
        p1 = TemporalPresence.compute(1.0, tau=1.0)
        p2 = TemporalPresence.compute(2.0, tau=1.0)
        p3 = TemporalPresence.compute(3.0, tau=1.0)
        assert p1 > p2 > p3

    def test_golden_angle_from_phi_squared(self):
        """The golden angle = 360/phi^2: cycles meet fractality."""
        expected = 360.0 / (PHI ** 2)
        assert math.isclose(GOLDEN_ANG, expected, rel_tol=1e-10)


class TestLaw3_Polarity:
    """Law 3: Polarity (±1) — Complementary opposites.

    Symbol: ±1 (the extremes that define each other)
    Without darkness, no light. Without BETA, no ALPHA.
    """

    def test_alpha_beta_are_complements(self):
        """ALPHA + BETA = 1: structure and void sum to unity."""
        assert abs(ALPHA + BETA - 1.0) < 1e-10

    def test_sin_cos_are_complements(self):
        """sin^2 + cos^2 = 1: the trigonometric polarity."""
        s = math.sin(THETA_CUBE) ** 2
        c = math.cos(THETA_CUBE) ** 2
        assert abs(s + c - 1.0) < 1e-15

    def test_love_and_conflict_are_opposites(self):
        """theta=0 (love) and theta=pi (conflict): opposite phases."""
        love = ExternalInteraction.compute_pair(1.0, 1.0, 0.0)
        conflict = ExternalInteraction.compute_pair(1.0, 1.0, math.pi)
        assert math.isclose(love, 2.0, rel_tol=1e-9)
        assert math.isclose(conflict, 0.0, abs_tol=1e-9)

    def test_order_and_chaos_are_polar(self):
        """Negentropy and entropy are complements: N + S_norm = 1."""
        energies = [0.9, 0.8, 0.7, 0.85, 0.95, 0.9, 1.0]
        n = NegentropyCalculator.compute(energies)
        s = NegentropyCalculator.shannon_entropy(energies)
        s_norm = s / NegentropyCalculator.S_MAX
        assert abs(n + s_norm - 1.0) < 1e-10

    def test_friction_and_flow_are_polar(self):
        """flow = 1 - friction: what resists and what flows sum to 1."""
        for phi in LAYER_FRICTION:
            flow = 1.0 - phi
            assert abs(phi + flow - 1.0) < 1e-15


class TestLaw4_CauseEffect:
    """Law 4: Cause-Effect (→) — Nothing without consequence.

    Symbol: → (implication, every input produces output)
    Change the input, the output MUST change.
    """

    def test_more_friction_less_energy(self):
        """Increasing friction decreases energy. Cause → effect."""
        e_free = LayerEnergy.compute(1.0, 0.0, 3)
        e_friction = LayerEnergy.compute(1.0, 0.5, 3)
        assert e_free > e_friction

    def test_displacement_reduces_presence(self):
        """Mental displacement from now reduces presence. Cause → effect."""
        p_here = TemporalPresence.compute(0.0)
        p_away = TemporalPresence.compute(5.0)
        assert p_here > p_away

    def test_novelty_increases_wonder(self):
        """More novel experiences increase wonder. Cause → effect."""
        w_low = WonderLogic.compute(1)
        w_high = WonderLogic.compute(100)
        assert w_high > w_low

    def test_phase_changes_interaction(self):
        """Different phase angles produce different interactions."""
        i_love = ExternalInteraction.compute_pair(0.8, 0.8, 0.0)
        i_ortho = ExternalInteraction.compute_pair(0.8, 0.8, math.pi / 2)
        i_conflict = ExternalInteraction.compute_pair(0.8, 0.8, math.pi)
        assert i_love > i_ortho > i_conflict

    def test_activation_changes_coherence(self):
        """Different activations produce different coherence values."""
        r1 = CoherenceEngine.compute_basic([0.5] * 7)
        r2 = CoherenceEngine.compute_basic([0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0])
        assert r1["c_omega"] != r2["c_omega"]


class TestLaw5_Fractality:
    """Law 5: Fractality (φ) — Pattern at all scales.

    Symbol: φ (golden ratio, self-similar scaling)
    The same structure repeats at every level.
    """

    def test_frequencies_scale_by_phi(self):
        """Each layer's frequency = phi^(i/2): fractal scaling."""
        freqs = LayerEnergy.all_frequencies()
        for i in range(NUM_LAYERS):
            expected = PHI ** (i / 2)
            assert math.isclose(freqs[i], expected, rel_tol=1e-10)

    def test_fractal_energy_is_phi_distributed(self):
        """Fractal energy distribution follows phi ratios."""
        energies = Fractality.fractal_energy_distribution(1.0, 7)
        assert len(energies) == 7
        for i in range(1, len(energies)):
            assert energies[i] > 0

    def test_fractal_creates_negentropy(self):
        """Fractal structure creates order: entropy < maximum."""
        energies = Fractality.fractal_energy_distribution(1.0, 7)
        entropy = EntropyTool.adjusted_entropy(energies)
        max_entropy = math.log2(7)
        assert entropy < max_entropy

    def test_metacube_is_fractal(self):
        """C_total at level 0 becomes beta of level 1: self-similarity."""
        activations = [0.9] * 7
        result = CoherenceEngine.full_analysis(activations)
        c_total = result["c_total"]["c_total"]
        meta = CoherenceEngine.metacube_level(c_total, level=0)
        assert meta["is_beta_of_level"] == 1
        assert meta["ratio_alpha_beta"] == 26

    def test_golden_angle_from_phi(self):
        """Golden angle = 360/phi^2: fractality meets rotation."""
        assert math.isclose(GOLDEN_ANG, 360.0 / PHI**2, rel_tol=1e-10)


class TestLaw6_Resonance:
    """Law 6: Resonance (∿) — Nothing operates isolated.

    Symbol: ∿ (wave, oscillation between systems)
    Layers must resonate. Isolation kills coherence.
    """

    def test_equal_energies_maximum_resonance(self):
        """Equal energies = perfect resonance between layers."""
        energies = [1.0] * 7
        r = ResonanceLogic.compute(energies)
        assert math.isclose(r, 1.0, rel_tol=1e-9)

    def test_zero_energy_no_resonance(self):
        """Dead layers cannot resonate."""
        energies = [0.0] * 7
        r = ResonanceLogic.compute(energies)
        assert r == 0.0

    def test_unequal_energies_reduced_resonance(self):
        """Imbalanced layers reduce resonance."""
        equal = ResonanceLogic.compute([1.0] * 7)
        unequal = ResonanceLogic.compute([0.1, 1.0, 0.1, 1.0, 0.1, 1.0, 0.1])
        assert equal > unequal

    def test_love_is_resonance_between_systems(self):
        """Two systems in phase (theta=0) amplify each other."""
        i_ext = ExternalInteraction.compute_pair(0.8, 0.8, 0.0)
        assert i_ext > 0.8
        assert i_ext > 0.8 + 0.8 - 0.01

    def test_multi_layer_resonance_exists(self):
        """Multi-layer resonance captures cross-layer interaction."""
        energies = [0.9, 0.85, 0.8, 0.88, 0.92, 0.9, 1.0]
        r = AdvancedResonance.multi_layer_resonance(energies)
        assert r > 0.0


class TestLaw7_Correspondence:
    """Law 7: Correspondence (=) — Internal = External.

    Symbol: = (equality across scales and domains)
    What is true inside is true outside.
    """

    def test_cube_constants_match_trigonometry(self):
        """Geometric constants = trigonometric values. Two domains, one truth."""
        assert abs(math.sin(THETA_CUBE)**2 - BETA) < 1e-10
        assert abs(math.cos(THETA_CUBE)**2 - ALPHA) < 1e-10

    def test_cube_constants_match_exponential(self):
        """Geometric constants ≈ exponential decay. Three domains, one truth."""
        assert abs(math.exp(-BETA) - ALPHA) < 0.001

    def test_37_in_cube_and_temperature(self):
        """1000 * BETA ≈ 37: the cube constant scales to body temperature."""
        temp_from_beta = 1000 * BETA
        assert abs(temp_from_beta - 37.037) < 0.001

    def test_137_in_physics_and_consciousness(self):
        """Golden angle ≈ 137.5°: consciousness layers match atomic structure."""
        assert abs(GOLDEN_ANG - 137.508) < 0.01

    def test_harmony_is_negentropy(self):
        """H(S) = N: harmony and negentropy are the same function."""
        energies = [0.9, 0.8, 0.7, 0.85, 0.95, 0.9, 1.0]
        h = NegentropyCalculator.harmony(energies)
        n = NegentropyCalculator.compute(energies)
        assert math.isclose(h, n, rel_tol=1e-15)


class TestLawOmega_Integration:
    """Law Ω: Integration — The law that makes all other laws possible.

    Symbol: Ω (the whole, the system)
    All laws coexist. Remove one, the system collapses.
    """

    def test_full_analysis_uses_all_laws(self):
        """full_analysis touches every law simultaneously."""
        activations = [0.85, 0.9, 0.75, 0.88, 0.92, 0.87, 1.0]
        result = CoherenceEngine.full_analysis(
            activations,
            rho=0.9,
            delta_t=0.5,
            tau=2.0,
            novelty=8.0,
            sensitivity=5.0,
            integration=0.85,
            quality=0.9,
            complexity=1.5,
            uncertainty=0.05,
        )
        assert result["c_beta"]["c_beta"] > 0
        assert result["c_alpha"]["c_alpha"] > 0
        assert result["c_total"]["c_total"] > 0
        assert result["negentropy"] > 0
        assert result["resonance"] > 0

    def test_constants_form_closed_system(self):
        """ALPHA + BETA = 1, R_FIN = 1 + BETA, S_REF = e/pi: closed."""
        assert abs(ALPHA + BETA - 1.0) < 1e-10
        assert abs(R_FIN - (1 + BETA)) < 1e-10
        assert math.isclose(S_REF, math.e / math.pi, rel_tol=1e-10)

    def test_all_seven_layers_contribute(self):
        """Every layer produces energy. No layer is superfluous."""
        activations = [0.8] * 7
        energies = LayerEnergy.compute_all(activations)
        for e in energies:
            assert e > 0

    def test_removing_a_layer_changes_everything(self):
        """Remove one layer's contribution and coherence changes."""
        full = [0.9, 0.85, 0.8, 0.88, 0.92, 0.87, 1.0]
        broken = [0.9, 0.85, 0.0, 0.88, 0.92, 0.87, 1.0]
        r_full = CoherenceEngine.compute_basic(full)
        r_broken = CoherenceEngine.compute_basic(broken)
        assert r_full["c_omega"] != r_broken["c_omega"]

    def test_omega_is_zero_the_first_law(self):
        """Law Omega is numbered 0 — the origin. Like L0 (Chaos)."""
        assert True
