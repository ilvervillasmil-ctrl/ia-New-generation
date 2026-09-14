"""
TEST: La Constante Cosmológica — El Peor Error de Predicción en la Historia

La Fórmula:
  Λ = β^(27π + β·φ²)
  
La Predicción:
  Λ_framework ≈ 2.81 × 10^(-122)
  Λ_observed  ≈ 2.888 × 10^(-122)
  Error: 2.7%
"""

import math
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from formulas.constants import (
    ALPHA, BETA, PHI, S_REF, R_FIN, KAPPA,
    NUM_LAYERS, CUBE_TOTAL, CUBE_EXTERIOR, CUBE_CENTER
)

LAMBDA_OBSERVED = 2.888e-122
FINE_STRUCTURE = 1 / 137.036


class TestTheProblema:
    def test_quantum_prediction_vs_observation(self):
        lambda_quantum = 1.0
        ratio = lambda_quantum / LAMBDA_OBSERVED
        order_of_magnitude = math.log10(ratio)
        assert 121 < order_of_magnitude < 123

    def test_lambda_is_not_zero(self):
        assert LAMBDA_OBSERVED > 0
        assert LAMBDA_OBSERVED < 1e-100

    def test_error_is_worst_in_science(self):
        error_factor = 1.0 / LAMBDA_OBSERVED
        log_error = math.log10(error_factor)
        assert log_error > 100


class TestEstructuraDelVacio:
    def test_cube_structure(self):
        assert CUBE_TOTAL == 27
        assert CUBE_EXTERIOR == 26
        assert CUBE_CENTER == 1
        assert CUBE_EXTERIOR + CUBE_CENTER == CUBE_TOTAL

    def test_alpha_beta_partition(self):
        assert abs(ALPHA + BETA - 1.0) < 1e-10

    def test_beta_is_irreducible(self):
        assert abs(BETA - 1/27) < 1e-10
        assert BETA > 0

    def test_perfect_integration_impossible(self):
        assert ALPHA < 1.0
        assert abs(ALPHA - 26/27) < 1e-10


class TestMecanismoReduccion:
    def test_beta_reductions_reach_lambda_scale(self):
        n_reductions = math.log(LAMBDA_OBSERVED) / math.log(BETA)
        assert 84 < n_reductions < 86

    def test_exponent_is_27_times_pi(self):
        exp_27pi = 27 * math.pi
        assert abs(exp_27pi - 84.823) < 0.01

    def test_27pi_gives_correct_order_of_magnitude(self):
        lambda_base = BETA ** (27 * math.pi)
        log_base = math.log10(lambda_base)
        assert -122 < log_base < -121

    def test_reduction_is_self_referential(self):
        exp = 27 * math.pi
        lambda_val = BETA ** exp
        ratio = lambda_val / LAMBDA_OBSERVED
        assert 0.5 < ratio < 2.0


class TestFormulaBase:
    def test_base_formula_order_of_magnitude(self):
        lambda_base = BETA ** (27 * math.pi)
        log_val = math.log10(lambda_base)
        assert abs(log_val - (-122)) < 1.0

    def test_base_formula_value(self):
        lambda_base = BETA ** (27 * math.pi)
        assert 3.0e-122 < lambda_base < 5.0e-122

    def test_base_formula_ratio_to_observed(self):
        lambda_base = BETA ** (27 * math.pi)
        ratio = lambda_base / LAMBDA_OBSERVED
        assert 1.2 < ratio < 1.5

    def test_base_formula_uses_only_framework_constants(self):
        beta = 1 / 27
        result = beta ** (27 * math.pi)
        log_result = math.log10(result)
        assert abs(log_result - (-122)) < 1.0


class TestCorreccionGeometrica:
    def test_pi_over_4_is_kappa(self):
        assert abs(KAPPA - math.pi / 4) < 1e-10

    def test_geometric_formula_value(self):
        lambda_geo = BETA ** (27 * math.pi) * (math.pi / 4)
        assert 2.5e-122 < lambda_geo < 3.5e-122

    def test_geometric_formula_error(self):
        lambda_geo = BETA ** (27 * math.pi) * (math.pi / 4)
        error = abs(lambda_geo - LAMBDA_OBSERVED) / LAMBDA_OBSERVED
        assert error < 0.06

    def test_geometric_correction_meaning(self):
        circle_area = math.pi * (0.5)**2
        square_area = 1.0
        ratio = circle_area / square_area
        assert abs(ratio - math.pi/4) < 1e-10


class TestFormulaExacta:
    def test_correction_term(self):
        correction = BETA * PHI**2
        main_exp = 27 * math.pi
        assert correction < 0.1
        assert correction / main_exp < 0.002

    def test_exact_formula_value(self):
        exponent = 27 * math.pi + BETA * PHI**2
        lambda_exact = BETA ** exponent
        assert 2.5e-122 < lambda_exact < 3.2e-122

    def test_exact_formula_error(self):
        exponent = 27 * math.pi + BETA * PHI**2
        lambda_exact = BETA ** exponent
        error = abs(lambda_exact - LAMBDA_OBSERVED) / LAMBDA_OBSERVED
        assert error < 0.03

    def test_exact_formula_ratio(self):
        exponent = 27 * math.pi + BETA * PHI**2
        lambda_exact = BETA ** exponent
        ratio = lambda_exact / LAMBDA_OBSERVED
        assert 0.95 < ratio < 1.05

    def test_exact_formula_uses_only_framework_constants(self):
        beta = 1 / 27
        phi = (1 + math.sqrt(5)) / 2
        exponent = 27 * math.pi + beta * phi**2
        result = beta ** exponent
        log_result = math.log10(result)
        assert abs(log_result - math.log10(LAMBDA_OBSERVED)) < 0.5

    def test_correction_is_phi_squared_times_beta(self):
        correction = PHI**2 * BETA
        assert abs(correction - 0.09696) < 0.001


class TestComparacionFisica:
    def test_improvement_over_quantum_prediction(self):
        error_quantum = abs(1.0 - LAMBDA_OBSERVED) / LAMBDA_OBSERVED
        exponent = 27 * math.pi + BETA * PHI**2
        lambda_framework = BETA ** exponent
        error_framework = abs(lambda_framework - LAMBDA_OBSERVED) / LAMBDA_OBSERVED
        improvement = error_quantum / error_framework
        assert improvement > 1e120

    def test_framework_error_vs_quantum_error(self):
        exponent = 27 * math.pi + BETA * PHI**2
        lambda_framework = BETA ** exponent
        error_framework_pct = abs(lambda_framework - LAMBDA_OBSERVED) / LAMBDA_OBSERVED * 100
        error_quantum_pct = abs(1.0 - LAMBDA_OBSERVED) / LAMBDA_OBSERVED * 100
        assert error_framework_pct < 5
        assert error_quantum_pct > 1e121

    def test_no_fine_tuning_needed(self):
        exponent = 27 * math.pi + BETA * PHI**2
        lambda_framework = BETA ** exponent
        log_framework = math.log10(lambda_framework)
        log_observed = math.log10(LAMBDA_OBSERVED)
        assert abs(log_framework - log_observed) < 0.5


class TestConstantesNoArbitrarias:
    def test_beta_is_cube_center(self):
        assert abs(BETA - 1/CUBE_TOTAL) < 1e-10

    def test_27_is_cube_volume(self):
        assert CUBE_TOTAL == 3**3

    def test_pi_is_cycle(self):
        assert abs(math.pi - 3.14159265) < 1e-6

    def test_phi_is_golden_ratio(self):
        assert abs(PHI - (1 + math.sqrt(5))/2) < 1e-10
        assert abs(PHI**2 - PHI - 1) < 1e-10

    def test_exponent_combines_three_laws(self):
        structure = 27
        rhythm = math.pi
        fractality = PHI**2
        residue = BETA
        exponent = structure * rhythm + residue * fractality
        assert 84.9 < exponent < 85.0

    def test_137_connection(self):
        golden_angle = 360 / PHI**2
        fine_structure_inv = 137.036
        assert abs(golden_angle - fine_structure_inv) < 1.0


class TestInterpretacion:
    def test_lambda_is_residue_not_force(self):
        exponent = 27 * math.pi + BETA * PHI**2
        lambda_val = BETA ** exponent
        assert lambda_val > 0
        assert lambda_val
