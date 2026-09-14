"""
Tests for OmegaValidator integrity.
Ensures validator uses single source of truth and validates correctly.
"""

import pytest
import math
from core.validator import OmegaValidator
from formulas.constants import (
    PHI, ALPHA, BETA, EPSILON,
    OMEGA_D, ZETA, THETA_CUBE,
    PHI_TOTAL, PHI_CRITICAL,
    EPSILON_PHYSICAL, EPSILON_ATTRACTOR,
)


class TestValidatorIntegrity:
    """
    Ensures validator uses single source of truth
    and validates correctly with tolerances.
    """
    
    def test_no_hardcoded_constants(self):
        """
        Validator must NOT redefine constants.
        Must import from formulas.constants.
        """
        import inspect
        import core.validator as validator_module
        
        # Get MODULE source (includes imports)
        module_source = inspect.getsource(validator_module)
        
        # Should import from formulas.constants
        assert "from formulas.constants import" in module_source
        
        # Get CLASS source (for checking no hardcoded values)
        class_source = inspect.getsource(OmegaValidator)
        
        # Should NOT contain hardcoded numeric values
        assert "1.6180339887" not in class_source
        assert "0.962962" not in class_source
        assert "0.037037" not in class_source
    
    def test_l6_purity_with_tolerance(self):
        """L6 purity check must use epsilon tolerance."""
        # Exact zero (ideal)
        assert OmegaValidator.check_l6_purity(0.0)
        
        # Near zero within epsilon (physical)
        assert OmegaValidator.check_l6_purity(1e-7)
        assert OmegaValidator.check_l6_purity(-1e-7)
        
        # Outside epsilon (violation)
        assert not OmegaValidator.check_l6_purity(0.01)
        assert not OmegaValidator.check_l6_purity(EPSILON_PHYSICAL * 2)
    
    def test_validate_range_with_tolerance(self):
        """Range validation must allow boundary tolerance."""
        # Valid range
        assert OmegaValidator.validate_range(0.0)
        assert OmegaValidator.validate_range(0.5)
        assert OmegaValidator.validate_range(1.0)
        
        # Within epsilon at boundaries
        assert OmegaValidator.validate_range(-EPSILON / 2)
        assert OmegaValidator.validate_range(1.0 + EPSILON / 2)
        
        # Outside range
        assert not OmegaValidator.validate_range(-0.1)
        assert not OmegaValidator.validate_range(1.1)
    
    def test_phi_resonance_validates_attractors(self):
        """
        validate_phi_resonance must check proximity to φ attractors,
        not just range.
        """
        # Near φ/2 attractor
        assert OmegaValidator.validate_phi_resonance(PHI / 2)
        assert OmegaValidator.validate_phi_resonance(0.81)  # Close to 0.809
        
        # Near α attractor
        assert OmegaValidator.validate_phi_resonance(ALPHA)
        assert OmegaValidator.validate_phi_resonance(0.96)  # Close to 0.963
        
        # Near β attractor
        assert OmegaValidator.validate_phi_resonance(BETA)
        assert OmegaValidator.validate_phi_resonance(0.04)  # Close to 0.037
        
        # Far from all attractors
        assert not OmegaValidator.validate_phi_resonance(0.5)
        assert not OmegaValidator.validate_phi_resonance(0.2)
    
    def test_validate_underdamped(self):
        """System must be underdamped (φ < 2π) to be alive."""
        # Underdamped (alive)
        assert OmegaValidator.validate_underdamped(PHI_TOTAL)  # 0.22
        assert OmegaValidator.validate_underdamped(math.pi)     # π
        
        # Critically damped (boundary)
        assert not OmegaValidator.validate_underdamped(PHI_CRITICAL)
        
        # Overdamped (dead)
        assert not OmegaValidator.validate_underdamped(10.0)
    
    def test_validate_oscillation(self):
        """ω_d > 0 means system oscillates (alive)."""
        # Oscillating
        assert OmegaValidator.validate_oscillation(OMEGA_D)  # ~3.139
        assert OmegaValidator.validate_oscillation(1.0)
        assert OmegaValidator.validate_oscillation(EPSILON * 2)
        
        # Dead (no oscillation)
        assert not OmegaValidator.validate_oscillation(0.0)
        assert not OmegaValidator.validate_oscillation(-1.0)
        assert not OmegaValidator.validate_oscillation(EPSILON / 2)
    
    def test_validate_damping_ratio(self):
        """0 < ζ < 1 means underdamped (alive)."""
        # Underdamped
        assert OmegaValidator.validate_damping_ratio(ZETA)  # ~0.035
        assert OmegaValidator.validate_damping_ratio(0.5)
        assert OmegaValidator.validate_damping_ratio(0.1)
        
        # Boundaries (not alive)
        assert not OmegaValidator.validate_damping_ratio(0.0)
        assert not OmegaValidator.validate_damping_ratio(1.0)
        assert not OmegaValidator.validate_damping_ratio(1.5)
        assert not OmegaValidator.validate_damping_ratio(-0.1)
    
    def test_validate_system_alive(self):
        """Master check: system alive requires all dynamic checks."""
        # Alive system (using framework constants)
        result = OmegaValidator.validate_system_alive(
            phi_total=PHI_TOTAL,
            omega_d=OMEGA_D,
            zeta=ZETA
        )
        
        assert result['alive'] is True
        assert all(result['checks'].values())
        assert result['phi_total'] == PHI_TOTAL
        assert result['omega_d'] == OMEGA_D
        assert result['zeta'] == ZETA
        
        # Dead system (φ too high)
        result_dead = OmegaValidator.validate_system_alive(
            phi_total=7.0,  # > 2π
            omega_d=0.0,
            zeta=1.2
        )
        
        assert result_dead['alive'] is False
        assert not any(result_dead['checks'].values())
    
    def test_conservation_law(self):
        """α + β = 1 AND values must match framework constants."""
        # Exact (framework constants)
        assert OmegaValidator.validate_conservation(ALPHA, BETA)
        
        # Within epsilon
        alpha_noisy = ALPHA + EPSILON / 2
        beta_noisy = BETA - EPSILON / 2
        assert OmegaValidator.validate_conservation(alpha_noisy, beta_noisy)
        
        # Sum equals 1 but values are wrong - MUST FAIL
        assert not OmegaValidator.validate_conservation(0.9, 0.1)
        assert not OmegaValidator.validate_conservation(0.5, 0.5)
    
    def test_theta_cube_validation(self):
        """θ_cube = arcsin(1/√27) must be validated precisely."""
        # Exact
        assert OmegaValidator.validate_theta_cube(THETA_CUBE)
        
        # Within tight tolerance
        theta_noisy = THETA_CUBE + EPSILON / 2
        assert OmegaValidator.validate_theta_cube(theta_noisy)
        
        # Wrong value
        assert not OmegaValidator.validate_theta_cube(0.5)
        assert not OmegaValidator.validate_theta_cube(0.0)
    
    def test_temporal_decay(self):
        """Temporal decay must be physical."""
        # Valid decay
        assert OmegaValidator.validate_temporal_decay(1.0, 60.0)
        assert OmegaValidator.validate_temporal_decay(0.0, 60.0)  # No decay
        assert OmegaValidator.validate_temporal_decay(100.0, 1.0)  # Large decay
        
        # Invalid inputs
        assert not OmegaValidator.validate_temporal_decay(-1.0, 60.0)  # Negative time
        assert not OmegaValidator.validate_temporal_decay(1.0, 0.0)    # Zero tau
        assert not OmegaValidator.validate_temporal_decay(1.0, -1.0)   # Negative tau
    
    def test_attractor_proximity(self):
        """Near-attractor validation."""
        # At equilibrium
        assert OmegaValidator.validate_near_attractor(THETA_CUBE, THETA_CUBE)
        
        # Close to equilibrium
        theta_close = THETA_CUBE + 0.05
        assert OmegaValidator.validate_near_attractor(theta_close, THETA_CUBE)
        
        # Far from equilibrium
        theta_far = THETA_CUBE + 1.0
        assert not OmegaValidator.validate_near_attractor(theta_far, THETA_CUBE)
    
    def test_divergence_diagnosis(self):
        """Divergence diagnosis returns correct states."""
        # Stable
        assert OmegaValidator.diagnose_divergence(THETA_CUBE, THETA_CUBE) == 'STABLE'
        assert OmegaValidator.diagnose_divergence(THETA_CUBE + 0.05, THETA_CUBE) == 'STABLE'
        
        # Diverging
        assert OmegaValidator.diagnose_divergence(THETA_CUBE + 0.3, THETA_CUBE) == 'DIVERGING'
        
        # Critical
        assert OmegaValidator.diagnose_divergence(THETA_CUBE + 1.0, THETA_CUBE) == 'CRITICAL'
        assert OmegaValidator.diagnose_divergence(THETA_CUBE + 2.0, THETA_CUBE) == 'CRITICAL'
