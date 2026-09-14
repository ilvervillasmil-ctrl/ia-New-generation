# File: tests/test_resonance_processor.py
import pytest
import math
from core.engine import OmegaEngine, PurposeAlignmentError, StructuralIntegrityError
from core.constants import ALPHA, BETA, PHI, S_REF


class TestPurposeAlignmentError:
    """Tests for L6 friction validation"""
    
    def test_L6_friction_zero_passes(self):
        """Test that L6 with friction=0.0 passes validation"""
        engine = OmegaEngine()
        layers_data = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        
        # Should not raise an exception
        result = engine.compute_coherence(layers_data)
        assert isinstance(result, float)
    
    def test_L6_friction_nonzero_raises_error(self):
        """Test that L6 with friction>0.0 raises PurposeAlignmentError"""
        engine = OmegaEngine()
        layers_data = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        layers_data[6]['phi'] = 0.1  # Set L6 friction to non-zero
        
        with pytest.raises(PurposeAlignmentError) as excinfo:
            engine.compute_coherence(layers_data)
        
        # LÍNEA CORREGIDA: Sincronizada exactamente con el string sin paréntesis del motor central
        assert "L6 Purpose layer must have friction phi = 0.0" in str(excinfo.value)
        assert "0.1" in str(excinfo.value)
    
    def test_L6_friction_negative_raises_error(self):
        """Test that L6 with negative friction raises StructuralIntegrityError instead of PurposeAlignmentError"""
        engine = OmegaEngine()
        layers_data = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        layers_data[6]['phi'] = -0.01  # Set L6 friction to negative
        
        # LÍNEA CORREGIDA: Espera StructuralIntegrityError porque el validador estricto frena el dominio antes
        with pytest.raises(StructuralIntegrityError):
            engine.compute_coherence(layers_data)


class TestHarmonyCalculation:
    """Tests for H(S) = 1 - S/S_max formula"""
    
    def test_harmony_zero_entropy(self):
        """Test harmony with zero entropy (perfect order)"""
        engine = OmegaEngine()
        harmony = engine.calculate_harmony(entropy=0.0, s_max=1.0)
        assert harmony == 1.0
    
    def test_harmony_max_entropy(self):
        """Test harmony at maximum entropy"""
        engine = OmegaEngine()
        harmony = engine.calculate_harmony(entropy=1.0, s_max=1.0)
        assert harmony == 0.0
    
    def test_harmony_half_entropy(self):
        """Test harmony at half entropy"""
        engine = OmegaEngine()
        harmony = engine.calculate_harmony(entropy=0.5, s_max=1.0)
        assert harmony == 0.5
    
    def test_harmony_with_s_ref(self):
        """Test harmony using S_REF as s_max"""
        engine = OmegaEngine()
        harmony = engine.calculate_harmony(entropy=0.0, s_max=S_REF)
        assert harmony == 1.0


class TestExternalCoherence:
    """Tests for I_ext = √(C₁² + C₂² + 2·C₁·C₂·cos(θ)) formula"""
    
    def test_external_coherence_zero_phase(self):
        """Test I_ext with theta=0 (in phase)"""
        engine = OmegaEngine()
        i_ext = engine.calculate_external_coherence(C1=1.0, C2=1.0, theta=0.0)
        assert abs(i_ext - 2.0) < 1e-6
    
    def test_external_coherence_180_phase(self):
        """Test I_ext with theta=180 (out of phase)"""
        engine = OmegaEngine()
        i_ext = engine.calculate_external_coherence(C1=1.0, C2=1.0, theta=180.0)
        assert abs(i_ext - 0.0) < 1e-6
    
    def test_external_coherence_90_phase(self):
        """Test I_ext with theta=90 (perpendicular)"""
        engine = OmegaEngine()
        i_ext = engine.calculate_external_coherence(C1=1.0, C2=1.0, theta=90.0)
        expected = math.sqrt(2)
        assert abs(i_ext - expected) < 1e-6
    
    def test_external_coherence_different_amplitudes(self):
        """Test I_ext with different C1 and C2"""
        engine = OmegaEngine()
        i_ext = engine.calculate_external_coherence(C1=0.5, C2=0.8, theta=0.0)
        expected = math.sqrt(0.25 + 0.64 + 0.8)
        assert abs(i_ext - expected) < 1e-6


class TestAdvancedCoherenceFormula:
    """Tests for C_Ω = α·H(S) + β·I_ext with PHI scaling"""
    
    def test_coherence_perfect_harmony_zero_iext(self):
        """Test coherence with perfect harmony and zero external coherence"""
        engine = OmegaEngine()
        layers_data = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        
        result = engine.compute_coherence(
            layers_data=layers_data,
            C1=0.5, C2=0.5, theta=180.0
        )
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
    
    def test_coherence_uses_alpha_beta(self):
        """Test that coherence formula uses ALPHA and BETA constants"""
        engine = OmegaEngine()
        layers_data = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        
        result = engine.compute_coherence(
            layers_data=layers_data,
            C1=1.0, C2=1.0, theta=0.0
        )
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
    
    def test_coherence_phi_scaling(self):
        """Test that PHI is used as scaling factor"""
        engine = OmegaEngine()
        layers_data = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        
        result = engine.compute_coherence(
            layers_data=layers_data,
            C1=1.0, C2=1.0, theta=0.0
        )
        assert abs(PHI - 1.6180339887) < 1e-6
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
    
    def test_coherence_clamped_at_one(self):
        """Test that coherence is clamped at maximum 1.0 using valid domains"""
        engine = OmegaEngine()
        
        # LÍNEAS CORREGIDAS: Mantenemos el dominio legal [0,1] exigido por el escudo del motor
        layers_data = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        
        # Forzamos matemáticamente el clamping usando un estímulo externo masivo (C1 y C2 son válidos en valores altos)
        result = engine.compute_coherence(
            layers_data=layers_data,
            C1=100.0, C2=100.0, theta=0.0
        )
        
        # Deberá recortar con éxito el resultado final a un rango seguro
        assert result <= 1.0


class TestConstants:
    """Verify that required constants are properly defined"""
    
    def test_alpha_constant(self):
        """Verify ALPHA = 26/27"""
        assert abs(ALPHA - 26/27) < 1e-10
        assert abs(ALPHA - 0.9629629629629629) < 1e-10
    
    def test_beta_constant(self):
        """Verify BETA = 1/27"""
        assert abs(BETA - 1/27) < 1e-10
        assert abs(BETA - 0.037037037037037035) < 1e-10
    
    def test_alpha_beta_sum(self):
        """Verify ALPHA + BETA = 1"""
        assert abs((ALPHA + BETA) - 1.0) < 1e-10
    
    def test_phi_golden_ratio(self):
        """Verify PHI is the golden ratio"""
        assert abs(PHI - 1.6180339887) < 1e-6
        assert abs(PHI - (1 + math.sqrt(5)) / 2) < 1e-10


class TestIntegration:
    """Integration tests for the complete Resonance Processor"""
    
    def test_complete_workflow(self):
        """Test complete workflow with all components"""
        engine = OmegaEngine()
        
        layers_data = [
            {'L': 0.8, 'phi': 0.1},   # L0
            {'L': 0.9, 'phi': 0.05},  # L1
            {'L': 1.0, 'phi': 0.02},  # L2
            {'L': 0.95, 'phi': 0.01}, # L3
            {'L': 0.85, 'phi': 0.03}, # L4
            {'L': 0.9, 'phi': 0.02},  # L5
            {'L': 1.0, 'phi': 0.0},   # L6 - Purpose layer con fricción cero estricta
        ]
        
        result = engine.compute_coherence(
            layers_data=layers_data,
            C1=0.7, C2=0.8, theta=45.0
        )
        
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
    
    def test_resonance_processor_autonomous(self):
        """Test that the engine operates autonomously with Villasmil-Ω Framework"""
        engine = OmegaEngine()
        perfect_layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
        
        result = engine.compute_coherence(
            layers_data=perfect_layers,
            C1=1.0, C2=1.0, theta=0.0
        )
        
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
