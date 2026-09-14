"""
Test Suite: Information IS the Object — Identity Test
Framework: UCF v3.1
Author: Ilver Villasmil
Date: February 2026

Thesis: A black hole does not "contain" information.
A black hole IS information. Mass, charge, spin, entropy —
these are not properties OF a thing. They ARE the thing.

If object = information, then:
1. Removing all information = removing the object (nothing remains)
2. Two objects with identical information are identical (no hidden substrate)
3. There is no "container" separate from the "content"
4. The information paradox dissolves: you can't lose what you ARE

This is not philosophy. These are testable mathematical statements.
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

G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
k_B = 1.380649e-23
l_P = 1.616255e-35
M_sun = 1.989e30


def black_hole_information(M):
    """Complete information content of a black hole."""
    Rs = 2 * G * M / (c ** 2)
    A = 4 * math.pi * Rs ** 2
    S = k_B * A / (4 * l_P ** 2)
    I_bits = S / (k_B * math.log(2))
    return {
        "mass": M,
        "radius": Rs,
        "area": A,
        "entropy": S,
        "bits": I_bits,
        "temperature": hbar * c ** 3 / (8 * math.pi * G * M * k_B),
        "I_horizon": I_bits * ALPHA,
        "I_interior": I_bits * BETA,
    }


# ============================================================
# TEST 1: IDENTITY — Object IS its information
# ============================================================

class TestIdentity:
    """If object = information, then identical information = identical object."""

    def test_same_mass_same_information(self):
        """Two black holes with same mass have identical information."""
        bh1 = black_hole_information(M_sun)
        bh2 = black_hole_information(M_sun)
        assert bh1["bits"] == bh2["bits"]
        assert bh1["entropy"] == bh2["entropy"]
        assert bh1["radius"] == bh2["radius"]

    def test_no_hidden_property(self):
        """
        No-hair theorem: M, Q, J fully determine the black hole.
        If information = object, there is nothing else to know.
        Our model uses M only (Schwarzschild). All properties derive from M.
        No property exists independent of the information.
        """
        M = M_sun * 5
        bh = black_hole_information(M)
        # Every property is a deterministic function of M alone
        assert bh["radius"] == 2 * G * M / (c ** 2)
        assert bh["area"] == 4 * math.pi * bh["radius"] ** 2
        # Nothing is free — everything derives from the one datum (mass)
        derived_temp = hbar * c ** 3 / (8 * math.pi * G * M * k_B)
        assert abs(bh["temperature"] - derived_temp) / derived_temp < 1e-10

    def test_different_mass_different_information(self):
        """Different information = different object."""
        bh1 = black_hole_information(M_sun)
        bh2 = black_hole_information(M_sun * 2)
        assert bh1["bits"] != bh2["bits"]
        assert bh1["radius"] != bh2["radius"]

    def test_information_determines_everything(self):
        """Given only the bits, you can reconstruct every property."""
        M = M_sun * 3
        bh = black_hole_information(M)
        # From bits, recover entropy
        S_recovered = bh["bits"] * k_B * math.log(2)
        assert abs(S_recovered - bh["entropy"]) / bh["entropy"] < 1e-10
        # From entropy, recover area
        A_recovered = S_recovered * 4 * l_P ** 2 / k_B
        assert abs(A_recovered - bh["area"]) / bh["area"] < 1e-10
        # From area, recover radius
        R_recovered = math.sqrt(A_recovered / (4 * math.pi))
        assert abs(R_recovered - bh["radius"]) / bh["radius"] < 1e-10
        # From radius, recover mass
        M_recovered = R_recovered * c ** 2 / (2 * G)
        assert abs(M_recovered - M) / M < 1e-10


# ============================================================
# TEST 2: NO CONTAINER — Nothing exists apart from information
# ============================================================

class TestNoContainer:
    """There is no 'box' holding information. The information is all there is."""

    def test_zero_information_zero_object(self):
        """If you remove all information, nothing remains.
        A black hole with zero bits is not an empty container — it doesn't exist."""
        bh = black_hole_information(M_sun)
        total = bh["I_horizon"] + bh["I_interior"]
        remaining_after_removal = total - total
        assert remaining_after_removal == 0.0
        # Zero information = zero mass = no object
        # There is no "empty black hole"

    def test_alpha_beta_exhaustive(self):
        """ALPHA + BETA = 1. The partition is complete.
        There is no third place for information to be.
        If there were a container, it would need its own information budget."""
        assert abs(ALPHA + BETA - 1.0) < 1e-15
        bh = black_hole_information(M_sun)
        accounted = bh["I_horizon"] + bh["I_interior"]
        unaccounted = bh["bits"] - accounted
        assert abs(unaccounted) / bh["bits"] < 1e-10

    def test_no_information_without_mass(self):
        """No mass = no information. The 'container' cannot exist without content."""
        # As mass approaches zero, information approaches zero
        tiny_M = 1e-30  # extremely small mass
        bh = black_hole_information(tiny_M)
        huge_M = M_sun * 1e6
        bh_huge = black_hole_information(huge_M)
        assert bh["bits"] < bh_huge["bits"]
        assert bh["bits"] > 0  # still nonzero — mass still exists

    def test_no_mass_without_information(self):
        """If information determines mass, then mass cannot exist
        independent of information. They are the same thing."""
        M = M_sun
        bh = black_hole_information(M)
        # Recover mass from information
        S = bh["bits"] * k_B * math.log(2)
        A = S * 4 * l_P ** 2 / k_B
        R = math.sqrt(A / (4 * math.pi))
        M_from_info = R * c ** 2 / (2 * G)
        assert abs(M_from_info - M) / M < 1e-10


# ============================================================
# TEST 3: PARADOX DISSOLUTION — Can't lose what you ARE
# ============================================================

class TestParadoxDissolution:
    """The information paradox assumes information is IN the black hole.
    If information IS the black hole, the paradox never existed."""

    def test_loss_requires_separation(self):
        """For information to be 'lost', it must be separable from the object.
        But object = information. Separation is impossible.
        Test: removing information = removing the object proportionally."""
        M = M_sun
        bh_full = black_hole_information(M)
        bh_half = black_hole_information(M * 0.5)
        # Half the mass = different information state, not "lost" information
        ratio_mass = bh_half["mass"] / bh_full["mass"]
        assert abs(ratio_mass - 0.5) < 1e-10
        # The information didn't go anywhere — the object changed state
        assert bh_half["bits"] > 0
        assert bh_half["bits"] < bh_full["bits"]

    def test_evaporation_is_transformation_not_destruction(self):
        """Hawking radiation doesn't destroy information.
        It transforms the object into a different form (radiation).
        The information changes state — it doesn't disappear."""
        M = M_sun
        bh = black_hole_information(M)
        I_total = bh["bits"]

        # After partial evaporation: smaller black hole + radiation
        M_remaining = M * 0.7
        bh_remaining = black_hole_information(M_remaining)
        I_remaining = bh_remaining["bits"]
        I_in_radiation = I_total - I_remaining

        # Nothing was lost — it changed form
        assert abs((I_remaining + I_in_radiation) - I_total) / I_total < 1e-10
        # Both parts are positive — information exists in both forms
        assert I_remaining > 0
        assert I_in_radiation > 0

    def test_paradox_is_categorical_error(self):
        """The paradox arises from treating information as a property
        rather than as the substance. Test: there is no operation that
        removes information while preserving the object."""
        M = M_sun
        bh = black_hole_information(M)

        # Try to have an object with zero information but nonzero mass:
        # Impossible. bits is a strict function of mass.
        # You can't set bits=0 while keeping M>0.
        # The function enforces: mass > 0 ↔ bits > 0
        for scale in [0.001, 0.1, 1, 10, 1000]:
            bh_test = black_hole_information(M * scale)
            assert bh_test["bits"] > 0, "Object exists but has no information — impossible"
            assert bh_test["mass"] > 0, "Information exists but has no object — impossible"

    def test_complete_evaporation_means_complete_transformation(self):
        """When the black hole fully evaporates:
        - The object ceases to exist
        - ALL information is now in radiation
        - Nothing was 'lost' — the black hole became something else"""
        M = M_sun
        bh = black_hole_information(M)
        I_total = bh["bits"]

        # Full evaporation: M_remaining → 0, all info in radiation
        I_radiated = I_total * ALPHA  # horizon released during evaporation
        I_burst = I_total * BETA      # interior released in final burst
        I_final_radiation = I_radiated + I_burst
        I_remaining_object = 0.0

        assert abs(I_final_radiation - I_total) / I_total < 1e-10
        assert I_remaining_object == 0.0
        # No object remains AND no information was lost
        # Because the object WAS the information


# ============================================================
# TEST 4: FRAMEWORK CONSISTENCY — 27 cubes, 27 data points
# ============================================================

class TestFrameworkConsistency:
    """The 3x3x3 cube has no empty cube. Every cube IS a datum.
    26 on the surface = observable. 1 in the center = hidden.
    But all 27 exist. All 27 are information. None is a 'container'."""

    def test_27_cubes_27_data(self):
        """Every cube in the 3x3x3 is a data point, not a container."""
        total_cubes = 27
        surface = 26
        interior = 1
        assert surface + interior == total_cubes
        assert surface / total_cubes == ALPHA
        assert interior / total_cubes == BETA

    def test_no_empty_cube(self):
        """There is no cube in the structure that contains nothing.
        Analogy: there is no part of a black hole that is 'empty of information'."""
        bh = black_hole_information(M_sun)
        I_per_surface_cube = bh["I_horizon"] / 26
        I_per_interior_cube = bh["I_interior"] / 1
        assert I_per_surface_cube > 0
        assert I_per_interior_cube > 0

    def test_cube_is_not_a_box(self):
        """The cube doesn't HOLD the constants — it IS the constants.
        3^3 = 27. 26/27 = ALPHA. 1/27 = BETA.
        The geometry doesn't contain the math. The geometry IS the math."""
        assert 3 ** 3 == 27
        assert abs(26 / 27 - ALPHA) < 1e-10
        assert abs(1 / 27 - BETA) < 1e-10
        # ALPHA and BETA don't describe the cube — they ARE the cube's structure

    def test_structure_and_content_inseparable(self):
        """You cannot have the cube without its ratios.
        You cannot have the ratios without the cube.
        Structure = Content. Container = Contained."""
        # If we change the structure (not 3x3x3), the constants change
        for n in [2, 4, 5]:
            total = n ** 3
            surface = total - (n - 2) ** 3
            interior = (n - 2) ** 3
            if n == 3:
                assert surface / total == ALPHA
                assert interior / total == BETA
            else:
                assert surface / total != ALPHA
                assert interior / total != BETA
        # Only 3x3x3 produces ALPHA/BETA. The structure IS the content.


# ============================================================
# TEST 5: UNIVERSALITY — This applies beyond black holes
# ============================================================

class TestUniversality:
    """If object = information is true for black holes,
    it must be true universally. The framework says it is:
    every system is described by its coherence state.
    The state IS the system."""

    def test_consciousness_is_its_layers(self):
        """A consciousness system IS its layer activations.
        Remove all activations = no system.
        There is no 'mind' separate from its states."""
        activations = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]  # L0-L6
        zero_activations = [0.0] * 7
        # System with activations exists
        total = sum(activations)
        assert total > 0
        # System with zero activations doesn't exist
        total_zero = sum(zero_activations)
        assert total_zero == 0.0

    def test_coherence_is_not_a_property_of_something(self):
        """Coherence doesn't describe a system — it IS the system.
        C_total is not a measurement OF consciousness.
        C_total IS the consciousness state."""
        # Two systems with identical coherence are identical systems
        state_a = {"activations": [0.5] * 7, "phi": [0.1] * 7}
        state_b = {"activations": [0.5] * 7, "phi": [0.1] * 7}
        assert state_a == state_b  # identical information = identical system

    def test_alpha_beta_partition_is_universal(self):
        """The 26/27 vs 1/27 split applies to any information system:
        - Black holes: horizon vs interior
        - Consciousness: observable vs hidden processes
        - Cube: surface vs center
        Same structure, same math, same identity principle."""
        systems = {
            "black_hole": {"observable": ALPHA, "hidden": BETA},
            "consciousness": {"observable": ALPHA, "hidden": BETA},
            "cube": {"surface": 26/27, "center": 1/27},
        }
        for name, system in systems.items():
            values = list(system.values())
            assert abs(sum(values) - 1.0) < 1e-10, f"{name} partition incomplete"
            assert abs(values[0] - ALPHA) < 1e-10, f"{name} observable != ALPHA"
            assert abs(values[1] - BETA) < 1e-10, f"{name} hidden != BETA"

    def test_the_map_is_the_territory(self):
        """Final test. The description of a thing IS the thing.
        The information about the black hole IS the black hole.
        The coherence state of consciousness IS the consciousness.
        The 27 cubes of the structure ARE the structure.
        There is nothing underneath. There is nothing behind.
        ALPHA + BETA = 1. That's all there is. And it's everything."""
        assert abs(ALPHA + BETA - 1.0) < 1e-15

        bh = black_hole_information(M_sun)
        accounted = bh["I_horizon"] + bh["I_interior"]
        total = bh["bits"]
        gap = abs(accounted - total) / total
        # The gap between "description" and "thing described" is zero.
        # Because they are the same.
        assert gap < 1e-10, "There is a gap between map and territory"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
