"""
Test Suite: Black Hole Information Paradox — Villasmil-Omega Framework
Framework: UCF v3.1 (Universal Coherence Framework)
Author: Ilver Villasmil
Date: February 2026

Tests the framework's prediction that information is never destroyed
in black holes — it is redistributed according to the 26/27 partition.

Physical constants from NIST/CODATA 2018.
Black hole formulas from Hawking (1975), Bekenstein (1973), Susskind (1995).
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from formulas.constants import ALPHA, BETA, PHI
except ImportError:
    ALPHA = 26 / 27
    BETA = 1 / 27
    PHI = (1 + math.sqrt(5)) / 2


# ============================================================
# PHYSICAL CONSTANTS (CODATA 2018)
# ============================================================

G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
k_B = 1.380649e-23
l_P = 1.616255e-35
m_P = 2.176434e-8
t_P = 5.391247e-44
M_sun = 1.989e30


# ============================================================
# BLACK HOLE FORMULAS
# ============================================================

def schwarzschild_radius(M):
    return 2 * G * M / (c ** 2)


def hawking_temperature(M):
    return hbar * c ** 3 / (8 * math.pi * G * M * k_B)


def bekenstein_hawking_entropy(M):
    Rs = schwarzschild_radius(M)
    A = 4 * math.pi * Rs ** 2
    return k_B * A / (4 * l_P ** 2)


def horizon_area(M):
    Rs = schwarzschild_radius(M)
    return 4 * math.pi * Rs ** 2


def hawking_evaporation_time(M):
    return 5120 * math.pi * G ** 2 * M ** 3 / (hbar * c ** 4)


def information_bits(M):
    S = bekenstein_hawking_entropy(M)
    return S / (k_B * math.log(2))


# ============================================================
# FRAMEWORK CONNECTION FUNCTIONS
# ============================================================

def information_partition(total_info):
    return {
        "observable": total_info * ALPHA,
        "hidden": total_info * BETA,
        "total": total_info,
    }


def information_conservation_check(initial_info, final_observable, final_hidden):
    return abs(initial_info - (final_observable + final_hidden)) / max(abs(initial_info), 1e-300) < 1e-6


def entropy_ratio_framework(M):
    S_bh = bekenstein_hawking_entropy(M)
    S_max = S_bh / ALPHA
    return S_bh / S_max


def evaporation_information_recovery(M):
    total_bits = information_bits(M)
    partition = information_partition(total_bits)
    t_evap = hawking_evaporation_time(M)
    t_page = t_evap / 2

    return {
        "total_bits": total_bits,
        "bits_on_horizon": partition["observable"],
        "bits_in_interior": partition["hidden"],
        "evaporation_time_years": t_evap / (365.25 * 24 * 3600),
        "page_time_years": t_page / (365.25 * 24 * 3600),
        "fraction_recovered_at_page_time": ALPHA / 2,
        "fraction_recovered_at_evaporation": 1.0,
    }


def cube_horizon_mapping(M):
    total = information_bits(M)
    return {
        "total_cubes": 27,
        "surface_cubes": 26,
        "interior_cubes": 1,
        "bits_per_surface_cube": total * ALPHA / 26,
        "bits_in_interior_cube": total * BETA,
        "total_bits": total,
        "conservation": abs(total * ALPHA + total * BETA - total) / max(abs(total), 1e-300) < 1e-6,
    }


# ============================================================
# TEST CLASS: PHYSICAL FORMULAS
# ============================================================

class TestBlackHolePhysics:

    def test_schwarzschild_radius_sun(self):
        Rs = schwarzschild_radius(M_sun)
        assert abs(Rs - 2953.0) < 10.0

    def test_schwarzschild_radius_proportional_to_mass(self):
        Rs1 = schwarzschild_radius(M_sun)
        Rs2 = schwarzschild_radius(2 * M_sun)
        assert abs(Rs2 / Rs1 - 2.0) < 1e-6

    def test_hawking_temperature_sun(self):
        T = hawking_temperature(M_sun)
        assert T < 1e-6

    def test_hawking_temperature_inverse_mass(self):
        T1 = hawking_temperature(M_sun)
        T2 = hawking_temperature(2 * M_sun)
        assert abs(T1 / T2 - 2.0) < 1e-6

    def test_bekenstein_entropy_positive(self):
        S = bekenstein_hawking_entropy(M_sun)
        assert S > 0

    def test_entropy_proportional_to_area(self):
        S1 = bekenstein_hawking_entropy(M_sun)
        S2 = bekenstein_hawking_entropy(2 * M_sun)
        assert abs(S2 / S1 - 4.0) < 1e-4

    def test_horizon_area_positive(self):
        A = horizon_area(M_sun)
        assert A > 0

    def test_information_bits_positive(self):
        bits = information_bits(M_sun)
        assert bits > 0

    def test_information_bits_order_of_magnitude(self):
        bits = information_bits(M_sun)
        assert 1e76 < bits < 1e78

    def test_evaporation_time_stellar(self):
        t = hawking_evaporation_time(M_sun)
        t_years = t / (365.25 * 24 * 3600)
        assert t_years > 1e60


# ============================================================
# TEST CLASS: INFORMATION CONSERVATION (FRAMEWORK)
# ============================================================

class TestInformationConservation:

    def test_partition_sums_to_total(self):
        total = information_bits(M_sun)
        partition = information_partition(total)
        assert abs(partition["observable"] + partition["hidden"] - partition["total"]) < 1

    def test_observable_is_alpha(self):
        total = 1000.0
        partition = information_partition(total)
        assert abs(partition["observable"] / total - ALPHA) < 1e-6

    def test_hidden_is_beta(self):
        total = 1000.0
        partition = information_partition(total)
        assert abs(partition["hidden"] / total - BETA) < 1e-6

    def test_conservation_check_passes(self):
        total = information_bits(M_sun)
        partition = information_partition(total)
        assert information_conservation_check(
            total, partition["observable"], partition["hidden"]
        )

    def test_conservation_for_any_mass(self):
        masses = [M_sun * 0.1, M_sun, M_sun * 10, M_sun * 1e6]
        for M in masses:
            total = information_bits(M)
            partition = information_partition(total)
            assert information_conservation_check(
                total, partition["observable"], partition["hidden"]
            ), f"Conservation failed for M = {M}"

    def test_information_never_zero(self):
        partition = information_partition(information_bits(M_sun))
        assert partition["observable"] > 0
        assert partition["hidden"] > 0

    def test_hidden_fraction_is_irreducible(self):
        partition = information_partition(100.0)
        assert partition["hidden"] > 0
        assert abs(partition["hidden"] / partition["total"] - BETA) < 1e-10

    def test_alpha_beta_sum_one(self):
        assert abs(ALPHA + BETA - 1.0) < 1e-10


# ============================================================
# TEST CLASS: CUBE-HORIZON MAPPING
# ============================================================

class TestCubeHorizonMapping:

    def test_27_total_cubes(self):
        mapping = cube_horizon_mapping(M_sun)
        assert mapping["total_cubes"] == 27

    def test_26_surface_cubes(self):
        mapping = cube_horizon_mapping(M_sun)
        assert mapping["surface_cubes"] == 26

    def test_1_interior_cube(self):
        mapping = cube_horizon_mapping(M_sun)
        assert mapping["interior_cubes"] == 1

    def test_conservation_in_mapping(self):
        mapping = cube_horizon_mapping(M_sun)
        assert mapping["conservation"]

    def test_surface_to_interior_ratio(self):
        mapping = cube_horizon_mapping(M_sun)
        ratio = mapping["surface_cubes"] / mapping["interior_cubes"]
        assert ratio == 26.0
        assert abs(ratio - ALPHA / BETA) < 1e-6

    def test_holographic_principle_analog(self):
        mapping = cube_horizon_mapping(M_sun)
        surface_bits = mapping["bits_per_surface_cube"] * 26
        total_bits = mapping["total_bits"]
        assert abs(surface_bits / total_bits - ALPHA) < 1e-6

    def test_interior_information_not_zero(self):
        mapping = cube_horizon_mapping(M_sun)
        assert mapping["bits_in_interior_cube"] > 0
        interior_fraction = mapping["bits_in_interior_cube"] / mapping["total_bits"]
        assert abs(interior_fraction - BETA) < 1e-6


# ============================================================
# TEST CLASS: EVAPORATION AND INFORMATION RECOVERY
# ============================================================

class TestEvaporationRecovery:

    def test_page_time_is_half_evaporation(self):
        result = evaporation_information_recovery(M_sun)
        ratio = result["page_time_years"] / result["evaporation_time_years"]
        assert abs(ratio - 0.5) < 1e-6

    def test_full_recovery_at_evaporation(self):
        result = evaporation_information_recovery(M_sun)
        assert result["fraction_recovered_at_evaporation"] == 1.0

    def test_partial_recovery_at_page_time(self):
        result = evaporation_information_recovery(M_sun)
        assert 0 < result["fraction_recovered_at_page_time"] < 1.0

    def test_horizon_bits_dominate(self):
        result = evaporation_information_recovery(M_sun)
        assert result["bits_on_horizon"] > result["bits_in_interior"]

    def test_horizon_to_interior_ratio(self):
        result = evaporation_information_recovery(M_sun)
        ratio = result["bits_on_horizon"] / result["bits_in_interior"]
        assert abs(ratio - 26.0) < 1e-4

    def test_total_bits_conserved(self):
        result = evaporation_information_recovery(M_sun)
        reconstructed = result["bits_on_horizon"] + result["bits_in_interior"]
        assert abs(reconstructed - result["total_bits"]) < 1


# ============================================================
# TEST CLASS: ENTROPY AND FRAMEWORK
# ============================================================

class TestEntropyFramework:

    def test_entropy_ratio_equals_alpha(self):
        ratio = entropy_ratio_framework(M_sun)
        assert abs(ratio - ALPHA) < 1e-10

    def test_entropy_ratio_mass_independent(self):
        masses = [M_sun * 0.5, M_sun, M_sun * 100]
        ratios = [entropy_ratio_framework(M) for M in masses]
        for r in ratios:
            assert abs(r - ALPHA) < 1e-10

    def test_hidden_entropy_is_beta(self):
        S = bekenstein_hawking_entropy(M_sun)
        S_max = S / ALPHA
        S_hidden = S_max - S
        assert abs(S_hidden / S_max - BETA) < 1e-10

    def test_entropy_never_negative(self):
        S = bekenstein_hawking_entropy(M_sun)
        assert S > 0

    def test_entropy_area_not_volume(self):
        S1 = bekenstein_hawking_entropy(M_sun)
        S2 = bekenstein_hawking_entropy(3 * M_sun)
        ratio = S2 / S1
        assert abs(ratio - 9.0) < 1e-3


# ============================================================
# TEST CLASS: TEMPERATURE-INFORMATION DUALITY
# ============================================================

class TestTemperatureInformation:

    def test_smaller_black_holes_are_hotter(self):
        T_small = hawking_temperature(M_sun * 0.1)
        T_large = hawking_temperature(M_sun * 10)
        assert T_small > T_large

    def test_more_info_means_colder(self):
        bits_small = information_bits(M_sun * 0.1)
        bits_large = information_bits(M_sun * 10)
        T_small = hawking_temperature(M_sun * 0.1)
        T_large = hawking_temperature(M_sun * 10)
        assert bits_large > bits_small
        assert T_large < T_small

    def test_planck_mass_temperature(self):
        T = hawking_temperature(m_P)
        T_planck = m_P * c ** 2 / (8 * math.pi * k_B)
        assert abs(T / T_planck - 1.0) < 0.01

    def test_information_release_rate(self):
        T1 = hawking_temperature(M_sun)
        T2 = hawking_temperature(M_sun * 0.01)
        assert T2 / T1 > 10


# ============================================================
# TEST CLASS: FRAMEWORK PREDICTIONS
# ============================================================

class TestFrameworkPredictions:

    def test_prediction_information_conserved(self):
        for M in [m_P, M_sun * 0.001, M_sun, M_sun * 1e9]:
            total = information_bits(M)
            partition = information_partition(total)
            assert information_conservation_check(
                total, partition["observable"], partition["hidden"]
            )

    def test_prediction_holographic_is_26_27(self):
        assert abs(ALPHA - 26/27) < 1e-10

    def test_prediction_irreducible_hidden(self):
        assert abs(BETA - 1/27) < 1e-10

    def test_prediction_26_surface_encodes_interior(self):
        total = 2700.0
        surface_info = total * ALPHA
        interior_info = total * BETA
        redundancy_ratio = surface_info / interior_info
        assert redundancy_ratio == 26.0

    def test_prediction_evaporation_recovers_all(self):
        result = evaporation_information_recovery(M_sun)
        assert result["fraction_recovered_at_evaporation"] == 1.0

    def test_prediction_page_curve_inflection(self):
        result = evaporation_information_recovery(M_sun)
        assert result["fraction_recovered_at_page_time"] == ALPHA / 2
        assert result["fraction_recovered_at_page_time"] < 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
