"""
Universal Coherence Framework v3.2 - Cosmology Module
Formalizes Lambda UCF and alpha_em candidates as importable functions.

Author: Ilver Villasmil
Framework: Villasmil-Ω
"""

import math
from .constants import (
    BETA, PHI, ALPHA,
    LAMBDA_UCF, LAMBDA_OBS, LAMBDA_ERROR,
    SQRT_LAMBDA, OMEGA_REDUCED,
    PHI_CUBED, ALPHA_PHI3,
    ALPHA_EM_INV_OBS,
    ALPHA_EM_CANDIDATE_A,
    ALPHA_EM_CANDIDATE_B,
    ALPHA_EM_CANDIDATE_C,
    ALPHA_EM_CANDIDATE_D,
)


def lambda_ucf() -> float:
    """
    Cosmological constant derived from the framework.

    Formula: Λ = β^(π/β + β·φ²)
    Reduced form shows everything comes from β alone:
    the 27 disappears — the dominant exponent is π/β = 27π.

    Value:  2.8096e-122
    Error:  2.72% vs observed
    Free parameters: 0
    Improvement over standard QM: 10^120

    Returns:
        float: Lambda UCF value
    """
    return LAMBDA_UCF


def lambda_error() -> float:
    """
    Relative error between UCF prediction and observation.

    Returns:
        float: Error as fraction (0.0272 = 2.72%)
    """
    return LAMBDA_ERROR


def lambda_exponent() -> float:
    """
    The exponent in Λ = β^exponent.
    Dominant term: π/β = 27π ≈ 84.823
    Fractal correction: β·φ² ≈ 0.097

    Returns:
        float: Full exponent value ≈ 84.920
    """
    return math.pi / BETA + BETA * PHI ** 2


def sqrt_lambda() -> float:
    """
    √Λ — cosmological root scale.
    Bridge between macro and micro scales.

    Returns:
        float: ≈ 1.676e-61
    """
    return SQRT_LAMBDA


def omega_reduced() -> float:
    """
    Reduced Omega operator: (π/e)·(1 - β²)
    Shows Omega depends only on β: 1-β² = 728/729.

    Returns:
        float: ≈ 1.15414
    """
    return OMEGA_REDUCED


def alpha_em_candidates() -> dict:
    """
    Dictionary of candidates for α_em^-1 ≈ 137.036.
    Each candidate uses only framework constants.

    Status: active hypothesis, not closed.
    Open question for candidate A: why 42?

    Returns:
        dict: {name: {"value": float, "error_pct": float, "formula": str}}
    """
    def err(v):
        return abs(v - ALPHA_EM_INV_OBS) / ALPHA_EM_INV_OBS * 100

    return {
        "A": {
            "value":     ALPHA_EM_CANDIDATE_A,
            "error_pct": err(ALPHA_EM_CANDIDATE_A),
            "formula":   "42 * pi / alpha",
        },
        "B": {
            "value":     ALPHA_EM_CANDIDATE_B,
            "error_pct": err(ALPHA_EM_CANDIDATE_B),
            "formula":   "28 * phi^3 * (pi/e)",
        },
        "C": {
            "value":     ALPHA_EM_CANDIDATE_C,
            "error_pct": err(ALPHA_EM_CANDIDATE_C),
            "formula":   "20 * phi^4",
        },
        "D": {
            "value":     ALPHA_EM_CANDIDATE_D,
            "error_pct": err(ALPHA_EM_CANDIDATE_D),
            "formula":   "52 * (alpha/beta) / pi^2",
        },
    }


def best_alpha_em_candidate() -> tuple:
    """
    Returns the candidate closest to the experimental value.

    Returns:
        tuple: (name, value, error_pct)
    """
    candidates = alpha_em_candidates()
    best = min(candidates, key=lambda k: candidates[k]["error_pct"])
    return best, candidates[best]["value"], candidates[best]["error_pct"]


def factor4_candidates() -> dict:
    """
    Candidates for the relation r_p ≈ 4·λ̄_C,p.
    Empirical: r_p / λ̄_C,p ≈ 3.9977 (error 0.058%)

    Returns:
        dict: {name: {"value": float, "description": str}}
    """
    return {
        "phi_cubed": {
            "value":       PHI_CUBED,
            "description": "φ³ ≈ 4.236 — geometric approximation",
        },
        "alpha_phi_cubed": {
            "value":       ALPHA_PHI3,
            "description": "α·φ³ ≈ 4.079 — structural correction, closer to 4",
        },
        "empirical": {
            "value":       3.9977,
            "description": "r_p / λ̄_C,p measured (error 0.058%)",
        },
    }


def cosmology_report() -> dict:
    """
    Full cosmology report as dictionary.

    Returns:
        dict: All cosmological metrics
    """
    candidates = alpha_em_candidates()
    best_name, best_val, best_err = best_alpha_em_candidate()

    return {
        "lambda_ucf":         LAMBDA_UCF,
        "lambda_obs":         LAMBDA_OBS,
        "lambda_error_pct":   LAMBDA_ERROR * 100,
        "lambda_exponent":    lambda_exponent(),
        "sqrt_lambda":        SQRT_LAMBDA,
        "omega_reduced":      OMEGA_REDUCED,
        "alpha_em_obs":       ALPHA_EM_INV_OBS,
        "alpha_em_best":      best_name,
        "alpha_em_best_val":  best_val,
        "alpha_em_best_err":  best_err,
        "alpha_em_all":       candidates,
        "factor4":            factor4_candidates(),
    }
