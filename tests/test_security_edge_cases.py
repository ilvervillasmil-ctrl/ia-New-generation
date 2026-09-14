"""
SECURITY TESTS - Edge cases, invalid inputs, boundary conditions.
The framework must never crash. It must degrade gracefully.
"""

import math
import pytest
from formulas.constants import ALPHA, BETA, S_REF
from formulas.energy import LayerEnergy
from formulas.presence import PresenceLogic
from formulas.wonder import WonderLogic
from formulas.negentropy import NegentropyCalculator
from formulas.interaction import ExternalInteraction
from formulas.resonance import ResonanceLogic
from formulas.resonance_extended import AdvancedResonance
from formulas.metaconsciousness import MetaconsciousnessCalculator
from formulas.coherence import CoherenceEngine
# Se importa StructuralIntegrityError para alinearse al escudo protector del motor
from core.engine import OmegaEngine, PurposeAlignmentError, StructuralIntegrityError


class TestEnergyEdgeCases:

    def test_zero_activation_all_layers(self):
        energies = LayerEnergy.compute_all([0.0] * 7)
        assert all(e == 0.0 for e in energies)

    def test_maximum_activation(self):
        energies = LayerEnergy.compute_all([1.0] * 7)
        assert all(e > 0 for e in energies)

    def test_very_small_activation(self):
        energies = LayerEnergy.compute_all([0.0001] * 7)
        assert all(e > 0 for e in energies)

    def test_very_large_activation(self):
        energies = LayerEnergy.compute_all([100.0] * 7)
        assert all(e > 0 for e in energies)

    def test_full_friction_kills_energy(self):
        energies = LayerEnergy.compute_all([1.0] * 7, [1.0] * 7)
        assert all(e == 0.0 for e in energies)


class TestPresenceEdgeCases:

    def test_zero_displacement(self):
        assert PresenceLogic.compute(0.0) == 1.0

    def test_huge_displacement(self):
        p = PresenceLogic.compute(1000.0)
        assert p >= 0.0
        assert p < 0.01

    def test_negative_displacement(self):
        p = PresenceLogic.compute(-5.0)
        assert 0.0 < p < 1.0

    def test_compute_pt_zero(self):
        assert PresenceLogic.compute_pt(0) == 1.0

    def test_compute_pt_negative(self):
        p = PresenceLogic.compute_pt(-3)
        assert abs(p - 0.25) < 1e-10


class TestWonderEdgeCases:

    def test_zero_novelty(self):
        assert WonderLogic.compute(0.0) == 0.0

    def test_huge_novelty(self):
        a = WonderLogic.compute(10000.0, 5.0)
        assert abs(a - 1.0) < 1e-6

    def test_negative_novelty(self):
        assert WonderLogic.compute(-5.0) == 0.0

    def test_zero_sensitivity_uses_s_ref(self):
        a = WonderLogic.compute(5.0, 0.0)
        expected = 1.0 - math.exp(-5.0 / S_REF)
        assert abs(a - expected) < 1e-10

    def test_negative_sensitivity_uses_s_ref(self):
        a = WonderLogic.compute(5.0, -10.0)
        expected = 1.0 - math.exp(-5.0 / S_REF)
        assert abs(a - expected) < 1e-10


class TestNegentropyEdgeCases:

    def test_all_zeros(self):
        n = NegentropyCalculator.compute([0.0] * 7)
        assert abs(n) < 1e-10

    def test_single_nonzero(self):
        energies = [0, 0, 0, 5.0, 0, 0, 0]
        n = NegentropyCalculator.compute(energies)
        assert abs(n - 1.0) < 1e-10

    def test_very_small_values(self):
        energies = [1e-10] * 7
        n = NegentropyCalculator.compute(energies)
        assert -1e-10 <= n <= 1.0

    def test_very_large_values(self):
        energies = [1e10] * 7
        n = NegentropyCalculator.compute(energies)
        assert abs(n) < 1e-10


class TestInteractionEdgeCases:

    def test_both_zero(self):
        assert ExternalInteraction.compute_pair(0.0, 0.0) == 0.0

    def test_one_zero(self):
        result = ExternalInteraction.compute_pair(0.0, 1.0, 0.0)
        assert abs(result - 1.0) < 1e-10

    def test_negative_coherence(self):
        result = ExternalInteraction.compute_pair(-1.0, 1.0, 0.0)
        assert isinstance(result, float)

    def test_multi_empty_list(self):
        assert ExternalInteraction.compute_multi([]) == 0.0

    def test_multi_single(self):
        assert ExternalInteraction.compute_multi([0.5]) == 0.5

    def test_conflict_equal_values(self):
        assert ExternalInteraction.conflict(0.7, 0.7) == 0.0


class TestResonanceEdgeCases:

    def test_all_zero_energies(self):
        assert ResonanceLogic.compute([0.0] * 7) == 0.0

    def test_single_energy(self):
        r = ResonanceLogic.compute([1.0])
        assert r == 0.0

    def test_two_equal_energies(self):
        r = ResonanceLogic.pair_resonance(5.0, 5.0)
        assert abs(r - 1.0) < 1e-10

    def test_phase_alignment_equal(self):
        assert ResonanceLogic.calculate_phase_alignment(7.0, 7.0) == 1.0

    def test_phase_alignment_zero(self):
        assert ResonanceLogic.calculate_phase_alignment(0.0, 5.0) == 0.0


class TestMetaconsciousnessEdgeCases:

    def test_all_zeros(self):
        mc = MetaconsciousnessCalculator.compute([0.0] * 7, [0.0] * 7)
        assert mc == 0.0

    def test_full_friction_l3(self):
        activations = [1.0] * 7
        frictions = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
        mc = MetaconsciousnessCalculator.compute(activations, frictions)
        assert mc == 0.0

    def test_negative_level(self):
        assert MetaconsciousnessCalculator.level(-1.0) == 0


class TestCoherenceEdgeCases:

    def test_c_beta_all_zeros(self):
        result = CoherenceEngine.compute_c_beta([0.0] * 7)
        assert result["c_beta"] == 0.0

    def test_c_alpha_zero_complexity(self):
        result = CoherenceEngine.compute_c_alpha(1.0, 1.0, 0.0, 0.0)
        assert result["c_alpha"] > 0

    def test_c_total_both_zero(self):
        result = CoherenceEngine.compute_c_total(0.0, 0.0)
        assert result["c_total"] == 0.0

    def test_full_analysis_all_zeros(self):
        result = CoherenceEngine.full_analysis([0.0] * 7)
        assert result["diagnostic_code"] == 0
        assert result["diagnostic_name"] == "Terminal Entropy"


class TestEngineSecurity:

    def test_l6_friction_exact_zero(self):
        engine = OmegaEngine()
        layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        result = engine.compute_coherence(layers)
        assert 0.0 <= result <= 1.0

    def test_l6_friction_tiny_nonzero(self):
        engine = OmegaEngine()
        layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        layers[6]['phi'] = 0.001
        with pytest.raises(PurposeAlignmentError):
            engine.compute_coherence(layers)

    def test_l6_friction_negative(self):
        """
        CORREGIDO: El motor valida primero las fronteras numéricas del dominio [0,1].
        Un valor de -0.1 en fricción levanta instantáneamente un StructuralIntegrityError.
        """
        engine = OmegaEngine()
        layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        layers[6]['phi'] = -0.1
        with pytest.raises(StructuralIntegrityError):
            engine.compute_coherence(layers)

    def test_result_always_clamped(self):
        """
        CORREGIDO: Las activaciones de capa deben mantenerse en el límite del dominio legal (1.0).
        Para probar el clamping ante valores masivos del sistema sin violar la integridad,
        inyectamos el estímulo masivo a través de las amplitudes externas C1 y C2.
        """
        engine = OmegaEngine()
        layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        result = engine.compute_coherence(layers, C1=100.0, C2=100.0, theta=0.0)
        assert result <= 1.0

    def test_result_never_negative(self):
        engine = OmegaEngine()
        layers = [{'L': 0.01, 'phi': 0.0} for _ in range(7)]
        result = engine.compute_coherence(layers, C1=0.01, C2=0.01, theta=180.0)
        assert result >= 0.0
