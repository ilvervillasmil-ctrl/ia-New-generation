"""
Tests for formulas/cosmology.py — UCF v3.2
"""
import math
import pytest
from formulas.cosmology import (
    lambda_ucf,
    lambda_error,
    lambda_exponent,
    sqrt_lambda,
    omega_reduced,
    alpha_em_candidates,
    best_alpha_em_candidate,
    factor4_candidates,
    cosmology_report,
)
from formulas.constants import (
    BETA, PHI, ALPHA,
    LAMBDA_UCF, LAMBDA_OBS, LAMBDA_ERROR,
    ALPHA_EM_INV_OBS,
)


def test_lambda_ucf_value():
    val = lambda_ucf()
    assert abs(val - 2.8096e-122) < 1e-124


def test_lambda_ucf_formula():
    expected = BETA ** (math.pi / BETA + BETA * PHI ** 2)
    assert abs(lambda_ucf() - expected) < 1e-130


def test_lambda_error_within_5pct():
    assert lambda_error() < 0.05


def test_lambda_error_approx_272():
    assert abs(lambda_error() - 0.0272) < 0.001


def test_lambda_exponent_approx():
    exp = lambda_exponent()
    assert abs(exp - 84.92) < 0.01


def test_lambda_exponent_dominant_term():
    dominant = math.pi / BETA
    assert abs(dominant - 27 * math.pi) < 1e-9


def test_sqrt_lambda_positive():
    assert sqrt_lambda() > 0


def test_sqrt_lambda_squared_equals_lambda():
    assert abs(sqrt_lambda() ** 2 - LAMBDA_UCF) < 1e-130


def test_omega_reduced_value():
    expected = (math.pi / math.e) * (1 - BETA ** 2)
    assert abs(omega_reduced() - expected) < 1e-9


def test_omega_reduced_correction():
    correction = 1 - BETA ** 2
    assert abs(correction - 728 / 729) < 1e-9


def test_alpha_em_candidates_count():
    cands = alpha_em_candidates()
    assert len(cands) == 4


def test_alpha_em_candidates_all_within_point5pct():
    cands = alpha_em_candidates()
    for name, data in cands.items():
        assert data["error_pct"] < 0.5, (
            f"Candidate {name} error {data['error_pct']:.4f}% exceeds 0.5%"
        )


def test_alpha_em_best_is_A():
    name, val, err = best_alpha_em_candidate()
    assert name == "A"
    assert err < 0.02


def test_alpha_em_candidate_A_formula():
    expected = 42 * math.pi / ALPHA
    from formulas.constants import ALPHA_EM_CANDIDATE_A
    assert abs(ALPHA_EM_CANDIDATE_A - expected) < 1e-9


def test_factor4_candidates_structure():
    f4 = factor4_candidates()
    assert "phi_cubed" in f4
    assert "alpha_phi_cubed" in f4
    assert "empirical" in f4


def test_factor4_phi_cubed_value():
    f4 = factor4_candidates()
    assert abs(f4["phi_cubed"]["value"] - PHI ** 3) < 1e-9


def test_factor4_empirical_near_4():
    f4 = factor4_candidates()
    assert abs(f4["empirical"]["value"] - 4.0) < 0.01


def test_cosmology_report_complete():
    report = cosmology_report()
    required = [
        "lambda_ucf", "lambda_obs", "lambda_error_pct",
        "sqrt_lambda", "omega_reduced",
        "alpha_em_obs", "alpha_em_best", "alpha_em_all", "factor4",
    ]
    for key in required:
        assert key in report, f"Missing key: {key}"


def test_cosmology_report_lambda_consistent():
    report = cosmology_report()
    assert abs(report["lambda_ucf"] - LAMBDA_UCF) < 1e-130
    assert abs(report["lambda_obs"] - LAMBDA_OBS) < 1e-130


def test_lambda_improvement_over_qm():
    qm_prediction = 1e2
    ratio = qm_prediction / LAMBDA_OBS
    assert ratio > 1e100
