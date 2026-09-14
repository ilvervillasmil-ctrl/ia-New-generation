"""
INTEGRATION TESTS - Cross-module verification
Every formula depends on others. If one breaks, the chain breaks.
"""

import math
from formulas.constants import ALPHA, BETA, KAPPA, R_FIN, S_REF, PHI, LAYER_FRICTION
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


class TestEnergyFeedsEverything:
    """Energy is the base. Everything else consumes it."""

    def test_energy_feeds_negentropy(self):
        """Negentropy reads energy distribution."""
        activations = [0.9, 0.8, 0.7, 0.85, 0.95, 0.9, 1.0]
        energies = LayerEnergy.compute_all(activations)
        n = NegentropyCalculator.compute(energies)
        assert 0.0 <= n <= 1.0

    def test_energy_feeds_resonance(self):
        """Resonance reads energy levels."""
        activations = [0.9, 0.8, 0.7, 0.85, 0.95, 0.9, 1.0]
        energies = LayerEnergy.compute_all(activations)
        r = ResonanceLogic.compute(energies)
        assert r > 0

    def test_energy_feeds_extended_resonance(self):
        """Extended resonance reads energy levels."""
        activations = [0.9, 0.8, 0.7, 0.85, 0.95, 0.9, 1.0]
        energies = LayerEnergy.compute_all(activations)
        r = AdvancedResonance.multi_layer_resonance(energies)
        assert r > 0

    def test_energy_feeds_coherence_basic(self):
        """Basic coherence reads energy for harmony."""
        activations = [0.9, 0.8, 0.7, 0.85, 0.95, 0.9, 1.0]
        energies = LayerEnergy.compute_all(activations)
        result = CoherenceEngine.compute_basic(energies)
        assert 0.0 <= result["c_omega"] <= 1.5


class TestCoherenceIntegration:
    """C_beta and C_alpha must combine correctly."""

    def test_c_beta_uses_all_formulas(self):
        """C_beta internally calls energy, presence, wonder."""
        activations = [0.8, 0.85, 0.9, 0.75, 0.88, 0.92, 1.0]
        result = CoherenceEngine.compute_c_beta(
            activations, delta_t=1.0, tau=2.0, novelty=7.0, sensitivity=5.0
        )
        assert result["p_t"] < 1.0
        assert result["wonder"] > 0.5
        assert len(result["energies"]) == 7

    def test_c_beta_c_alpha_combine_in_c_total(self):
        """C_total is the vector sum of C_beta and C_alpha."""
        activations = [0.8] * 7
        beta_r = CoherenceEngine.compute_c_beta(activations)
        alpha_r = CoherenceEngine.compute_c_alpha(0.8, 0.9, 1.0, 0.1)
        total_r = CoherenceEngine.compute_c_total(
            beta_r["c_beta"], alpha_r["c_alpha"]
        )

        expected = math.sqrt(beta_r["c_beta"]**2 + alpha_r["c_alpha"]**2)
        assert abs(total_r["c_total"] - expected) < 1e-10

    def test_full_analysis_integrates_everything(self):
        """full_analysis touches every single module."""
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
        assert result["metaconsciousness"] > 0
        assert result["resonance"] > 0
        assert result["diagnostic_name"] in [
            "Integrated Architect", "Critical Saturation", "Terminal Entropy"
        ]


class TestEngineMatchesCoherence:
    """OmegaEngine and CoherenceEngine must be consistent."""

    def test_both_produce_valid_output(self):
        """Both engines produce results for the same input."""
        activations = [0.85, 0.9, 0.8, 0.88, 0.92, 0.87, 1.0]
        frictions = [0.10, 0.02, 0.05, 0.03, 0.01, 0.01, 0.00]

        result_formula = CoherenceEngine.full_analysis(activations, frictions)

        engine = OmegaEngine()
        layers = [{'L': a, 'phi': f} for a, f in zip(activations, frictions)]
        result_engine = engine.compute_coherence(layers, C1=0.8, C2=0.7, theta=30.0)

        assert result_formula["c_total"]["c_total"] > 0
        assert 0.0 <= result_engine <= 1.0

    def test_metacube_connects_levels(self):
        """Level 0 becomes beta of level 1."""
        activations = [0.9] * 7
        result = CoherenceEngine.full_analysis(activations)
        c_total = result["c_total"]["c_total"]

        meta = CoherenceEngine.metacube_level(c_total, level=0)
        assert meta["is_beta_of_level"] == 1
        assert meta["ratio_alpha_beta"] == 26
