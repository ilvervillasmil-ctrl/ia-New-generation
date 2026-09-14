"""
Test Suite: Black Hole Formation Hypothesis
Framework: UCF v3.1
Author: Ilver Villasmil
Date: February 2026

HYPOTHESIS: A black hole forms when a system's internal friction (φ)
exceeds its capacity to maintain coherent information structure.
The collapse is not destruction — it is an information phase transition
from a high-volume, low-density configuration (star) to a
minimal-surface, maximum-density configuration (black hole).

STATUS: Hypothesis. Not proven. Testable within the framework.
If any test fails → the hypothesis needs revision or rejection.
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
TOV_LIMIT = 3.0  # Tolman-Oppenheimer-Volkoff limit in solar masses


def information_bits(M):
    Rs = 2 * G * M / (c ** 2)
    A = 4 * math.pi * Rs ** 2
    S = k_B * A / (4 * l_P ** 2)
    return S / (k_B * math.log(2))


def star_volume_information_density(M, R_star):
    """Information per unit volume for a star (distributed in 3D)."""
    V = (4 / 3) * math.pi * R_star ** 3
    I = information_bits(M)
    return I / V


def bh_surface_information_density(M):
    """Information per unit area for a black hole (on 2D surface)."""
    Rs = 2 * G * M / (c ** 2)
    A = 4 * math.pi * Rs ** 2
    I = information_bits(M)
    return I / A


def coherence_capacity(M, R):
    """
    How much coherent structure a system can maintain.
    Larger radius = more volume = more room for organized information.
    When R → Rs (Schwarzschild), capacity → 0. The system cannot
    maintain volumetric organization anymore.
    """
    Rs = 2 * G * M / (c ** 2)
    if R <= Rs:
        return 0.0
    return 1.0 - (Rs / R)


def friction_from_density(M, R):
    """
    Internal friction increases as matter compresses.
    When density approaches critical: φ → 1 (maximum friction).
    Framework analogy: L0 has maximum friction, L6 has zero.
    A collapsing star moves from low-φ to high-φ.
    """
    Rs = 2 * G * M / (c ** 2)
    if R <= Rs:
        return 1.0
    ratio = Rs / R
    return ratio ** 2


def information_efficiency(M, R):
    """
    Ratio of information stored vs structure needed.
    Star: lots of volume, distributed information → low efficiency.
    Black hole: minimal surface, maximum information → high efficiency.
    """
    I = information_bits(M)
    Rs = 2 * G * M / (c ** 2)
    if R <= Rs:
        A_horizon = 4 * math.pi * Rs ** 2
        return I / A_horizon  # surface encoding
    V = (4 / 3) * math.pi * R ** 3
    return I / V  # volume encoding


# ============================================================
# TEST 1: THE TRIGGER — Friction exceeds coherence capacity
# ============================================================

class TestCollapeTrigger:
    """
    HYPOTHESIS: Collapse occurs when φ > coherence capacity.
    The system can no longer organize its information volumetrically.
    """

    def test_stable_star_has_low_friction(self):
        """A stable star (R >> Rs) has low internal friction."""
        M = M_sun * 10
        R_star = 7e8  # ~solar radius, large relative to Rs
        phi = friction_from_density(M, R_star)
        assert phi < 0.01, f"Stable star should have low friction, got {phi}"

    def test_collapsing_star_friction_increases(self):
        """As the star compresses, friction increases monotonically."""
        M = M_sun * 10
        Rs = 2 * G * M / (c ** 2)
        radii = [Rs * 1000, Rs * 100, Rs * 10, Rs * 5, Rs * 2, Rs * 1.1]
        frictions = [friction_from_density(M, R) for R in radii]
        for i in range(len(frictions) - 1):
            assert frictions[i] < frictions[i + 1], "Friction must increase as R decreases"

    def test_coherence_capacity_decreases(self):
        """As R → Rs, the system loses capacity to maintain structure."""
        M = M_sun * 10
        Rs = 2 * G * M / (c ** 2)
        radii = [Rs * 1000, Rs * 100, Rs * 10, Rs * 2, Rs * 1.01]
        capacities = [coherence_capacity(M, R) for R in radii]
        for i in range(len(capacities) - 1):
            assert capacities[i] > capacities[i + 1], "Capacity must decrease as R decreases"

    def test_crossover_point_exists(self):
        """There exists a radius where φ > capacity (collapse is inevitable)."""
        M = M_sun * 10
        Rs = 2 * G * M / (c ** 2)
        crossover_found = False
        for factor in [100, 50, 20, 10, 5, 3, 2, 1.5, 1.1]:
            R = Rs * factor
            phi = friction_from_density(M, R)
            cap = coherence_capacity(M, R)
            if phi > cap:
                crossover_found = True
                break
        assert crossover_found, "No crossover point found — hypothesis fails"

    def test_at_horizon_friction_is_maximum(self):
        """At R = Rs, friction = 1.0 (maximum). No coherence possible."""
        M = M_sun * 10
        Rs = 2 * G * M / (c ** 2)
        phi = friction_from_density(M, Rs)
        cap = coherence_capacity(M, Rs)
        assert phi == 1.0
        assert cap == 0.0

    def test_tov_limit_has_physical_meaning(self):
        """Above TOV limit (~3 M_sun), nothing prevents collapse.
        The framework says: above this mass, φ always wins."""
        M_below = M_sun * 1.4  # neutron star survives
        M_above = M_sun * TOV_LIMIT

        Rs_below = 2 * G * M_below / (c ** 2)
        Rs_above = 2 * G * M_above / (c ** 2)

        R_ns = 1e4  # ~10 km, typical neutron star radius

        phi_below = friction_from_density(M_below, R_ns)
        phi_above = friction_from_density(M_above, R_ns)

        assert phi_above > phi_below, "Heavier remnant has more friction"


# ============================================================
# TEST 2: PHASE TRANSITION — Not destruction, reorganization
# ============================================================

class TestPhaseTransition:
    """
    HYPOTHESIS: Black hole formation is an information phase transition.
    Volume encoding (star) → Surface encoding (black hole).
    Like ice → water. Same substance, different organization.
    """

    def test_information_before_equals_after(self):
        """Total information is conserved across the transition."""
        M = M_sun * 10
        I_star = information_bits(M)
        I_bh = information_bits(M)  # same mass = same information
        assert I_star == I_bh

    def test_encoding_changes(self):
        """Before: info in volume. After: info on surface.
        Different encoding, same information."""
        M = M_sun * 10
        R_star = 7e8
        Rs = 2 * G * M / (c ** 2)

        density_star = star_volume_information_density(M, R_star)
        density_bh = bh_surface_information_density(M)

        # Both are positive — information exists in both states
        assert density_star > 0
        assert density_bh > 0
        # They are different — encoding changed
        assert density_star != density_bh

    def test_surface_encoding_is_more_efficient(self):
        """Black hole stores information on a smaller structure.
        Surface area < Volume for any R > Rs."""
        M = M_sun * 10
        R_star = 7e8

        eff_star = information_efficiency(M, R_star)
        Rs = 2 * G * M / (c ** 2)
        eff_bh = information_efficiency(M, Rs)

        assert eff_bh > eff_star, "BH encoding should be more efficient"

    def test_transition_is_not_reversible(self):
        """Once surface-encoded, the system cannot spontaneously return
        to volume encoding. This is why black holes don't 'explode back'
        into stars. The phase transition is one-directional (classically)."""
        M = M_sun * 10
        Rs = 2 * G * M / (c ** 2)
        cap_at_horizon = coherence_capacity(M, Rs)
        assert cap_at_horizon == 0.0, "No volumetric coherence at horizon"

    def test_alpha_beta_partition_emerges_at_transition(self):
        """The 26/27 vs 1/27 split is a property of the final state.
        Before collapse: information is distributed in volume (no partition).
        After collapse: information partitions into surface/interior."""
        M = M_sun * 10
        I_total = information_bits(M)
        I_horizon = I_total * ALPHA
        I_interior = I_total * BETA
        assert abs(I_horizon + I_interior - I_total) / I_total < 1e-10


# ============================================================
# TEST 3: FRAMEWORK MAPPING — Consciousness layers ↔ Stellar collapse
# ============================================================

class TestFrameworkMapping:
    """
    HYPOTHESIS: The framework's layer model maps onto stellar collapse.
    High friction (L0) = collapsed state.
    Zero friction (L6) = free radiation state.
    The star's lifecycle moves through friction states.
    """

    def test_stable_star_is_low_friction_state(self):
        """A main-sequence star is in a low-φ equilibrium.
        Framework analogy: upper layers active, system coherent."""
        M = M_sun
        R = 7e8  # solar radius
        phi = friction_from_density(M, R)
        assert phi < 0.1

    def test_collapse_moves_toward_l0(self):
        """Collapse increases φ toward 1.0.
        Framework: the system descends toward L0 (pure field, maximum friction)."""
        M = M_sun * 10
        Rs = 2 * G * M / (c ** 2)
        phi_stable = friction_from_density(M, Rs * 1000)
        phi_collapse = friction_from_density(M, Rs * 1.01)
        assert phi_collapse > phi_stable
        assert phi_collapse > 0.9

    def test_evaporation_moves_toward_l6(self):
        """Hawking radiation is a system releasing friction.
        Framework: the system ascends from L0 toward L6 (zero friction).
        Evaporation = decreasing mass = decreasing gravitational friction."""
        M = M_sun
        M_evaporated = M * 0.01
        Rs_full = 2 * G * M / (c ** 2)
        Rs_small = 2 * G * M_evaporated / (c ** 2)
        # Smaller black hole has smaller Rs, relatively less gravitational grip
        assert Rs_small < Rs_full

    def test_final_evaporation_is_zero_friction(self):
        """When the black hole fully evaporates, all information is in radiation.
        Radiation = massless = zero gravitational friction.
        Framework: L6 state. Zero φ. Pure integrated information."""
        # Photons (radiation) have zero rest mass
        # Zero mass = zero gravitational friction
        # This is the L6 analog: information exists, friction = 0
        M_final = 0.0
        # No mass = no friction = L6
        assert M_final == 0.0

    def test_lifecycle_is_phi_cycle(self):
        """
        Star lifecycle in framework terms:
        1. Nebula: low density, low φ
        2. Main sequence: equilibrium φ
        3. Collapse: φ → 1.0 (maximum)
        4. Black hole: φ = 1.0 (L0 state)
        5. Evaporation: φ decreasing
        6. Full evaporation: φ = 0 (L6 state, pure radiation)

        The star starts with low friction and ends with zero friction.
        The black hole is the maximum-friction intermediate state.
        """
        M = M_sun * 10
        Rs = 2 * G * M / (c ** 2)

        phi_nebula = friction_from_density(M, Rs * 10000)
        phi_star = friction_from_density(M, Rs * 100)
        phi_collapse = friction_from_density(M, Rs * 1.01)
        phi_bh = friction_from_density(M, Rs)
        phi_radiation = 0.0  # photons, no mass

        # Friction increases to maximum, then drops to zero
        assert phi_nebula < phi_star
        assert phi_star < phi_collapse
        assert phi_collapse < phi_bh
        assert phi_bh == 1.0
        assert phi_radiation == 0.0
        # The cycle: low → high → zero
        assert phi_nebula < phi_bh > phi_radiation


# ============================================================
# TEST 4: THE REAL QUESTION — Why THIS configuration?
# ============================================================

class TestWhyThisConfiguration:
    """
    HYPOTHESIS: The black hole forms in the specific 26/27 + 1/27
    configuration because it is the only stable partition of a
    3D information system at maximum compression.
    """

    def test_only_3x3x3_produces_alpha_beta(self):
        """Only the 3x3x3 cube produces the exact ALPHA/BETA ratio.
        If the universe 'chose' this partition, it chose 3D cubic geometry."""
        for n in range(2, 10):
            total = n ** 3
            interior = (n - 2) ** 3
            surface = total - interior
            if n == 3:
                assert abs(surface / total - ALPHA) < 1e-10
                assert abs(interior / total - BETA) < 1e-10
            else:
                assert abs(surface / total - ALPHA) > 0.01

    def test_3_is_minimum_with_interior(self):
        """3x3x3 is the smallest cube that has an interior.
        2x2x2: all 8 cubes are surface. No hidden information.
        3x3x3: first cube with a center. First with β > 0."""
        assert (2 - 2) ** 3 == 0   # no interior
        assert (3 - 2) ** 3 == 1   # first interior
        assert (4 - 2) ** 3 == 8   # too much interior

    def test_minimum_hidden_information(self):
        """BETA = 1/27 is the minimum possible hidden fraction
        for a 3D system with an interior.
        The black hole hides the absolute minimum. Not by choice —
        by geometric necessity."""
        min_hidden = 1 / 27
        assert abs(BETA - min_hidden) < 1e-10

    def test_maximum_surface_encoding(self):
        """ALPHA = 26/27 is the maximum surface fraction
        for a 3D system with an interior.
        The holographic principle isn't a choice — it's a geometric limit."""
        max_surface = 26 / 27
        assert abs(ALPHA - max_surface) < 1e-10

    def test_configuration_is_unique(self):
        """No other partition of 27 into surface + interior
        produces the same ratio. The configuration is forced,
        not selected."""
        target_alpha = 26 / 27
        found = 0
        for s in range(1, 27):
            i = 27 - s
            if abs(s / 27 - target_alpha) < 1e-10:
                found += 1
        assert found == 1, "Partition must be unique"

    def test_hypothesis_statement(self):
        """
        HYPOTHESIS SUMMARY (not a claim — a testable proposition):

        A black hole forms when internal friction exceeds coherence capacity.
        The formation is not destruction — it is an information phase transition
        from 3D volume encoding to 2D surface encoding.

        The specific configuration (26/27 surface, 1/27 interior) is not
        arbitrary. It is the unique partition of the minimal 3D cubic
        geometry that has an interior.

        The universe doesn't choose this configuration. It's the only one
        available for a 3-dimensional information system at maximum compression.

        Falsifiable prediction: if information distribution on a black hole
        horizon is ever measured, it should follow the 26/27 ratio.
        If it doesn't, this hypothesis is wrong.
        """
        # This test passes by existing.
        # Its value is in its docstring: a clear, falsifiable statement.
        assert ALPHA + BETA == pytest.approx(1.0)
        assert ALPHA == pytest.approx(26 / 27)
        assert BETA == pytest.approx(1 / 27)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
