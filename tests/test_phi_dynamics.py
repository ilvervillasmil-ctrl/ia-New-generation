import pytest
import math
from formulas.phi_dynamics import PhiDynamics
from formulas.constants import PHI


class TestGoldenSpiral:
    def test_returns_100_points(self):
        """Default generates 100 points."""
        result = PhiDynamics.golden_spiral(1.0)
        assert len(result) == 100

    def test_first_point_on_x_axis(self):
        """First point at angle 0 = (radius, 0)."""
        result = PhiDynamics.golden_spiral(1.0)
        x, y = result[0]
        assert math.isclose(x, 1.0, rel_tol=1e-9)
        assert math.isclose(y, 0.0, abs_tol=1e-9)

    def test_points_are_tuples(self):
        """Each point is an (x, y) tuple."""
        result = PhiDynamics.golden_spiral(1.0)
        for point in result:
            assert isinstance(point, tuple)
            assert len(point) == 2

    def test_radius_grows(self):
        """Distance from origin increases (radius * PHI each step)."""
        result = PhiDynamics.golden_spiral(1.0)
        dist_first = math.sqrt(result[0][0]**2 + result[0][1]**2)
        dist_second = math.sqrt(result[1][0]**2 + result[1][1]**2)
        assert math.isclose(dist_second / dist_first, PHI, rel_tol=1e-9)

    def test_custom_angle(self):
        """Custom angle step works."""
        result = PhiDynamics.golden_spiral(1.0, angle_step=90.0)
        assert len(result) == 100

    def test_default_angle_is_golden(self):
        """Default angle ≈ 137.5° (golden angle)."""
        result = PhiDynamics.golden_spiral(1.0)
        x1, y1 = result[1]
        actual_angle = math.degrees(math.atan2(y1, x1)) % 360
        assert math.isclose(actual_angle, 137.507764, rel_tol=1e-4)


class TestPhiScaling:
    def test_empty_list(self):
        """Empty input returns empty."""
        result = PhiDynamics.phi_scaling([])
        assert result == []

    def test_single_value(self):
        """Single value scaled by PHI."""
        result = PhiDynamics.phi_scaling([1.0])
        assert math.isclose(result[0], PHI, rel_tol=1e-9)

    def test_seven_layers(self):
        """7 values all scaled by PHI."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        result = PhiDynamics.phi_scaling(values)
        for i, v in enumerate(values):
            assert math.isclose(result[i], v * PHI, rel_tol=1e-9)

    def test_preserves_length(self):
        """Output same length as input."""
        result = PhiDynamics.phi_scaling([1, 2, 3])
        assert len(result) == 3

    def test_zero_stays_zero(self):
        """Zero scaled is still zero."""
        result = PhiDynamics.phi_scaling([0.0])
        assert result[0] == 0.0

    def test_double_scaling(self):
        """Scaling twice = PHI^2."""
        result = PhiDynamics.phi_scaling(PhiDynamics.phi_scaling([1.0]))
        assert math.isclose(result[0], PHI ** 2, rel_tol=1e-9)
