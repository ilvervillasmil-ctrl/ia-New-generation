import pytest
import math
from formulas.harmonics import Harmonics
from formulas.constants import PHI


class TestHarmonicRatio:
    def test_multiplier_zero(self):
        """Multiplier 0 = base frequency (PHI^0 = 1)."""
        result = Harmonics.calculate_harmonic_ratio(440.0, 0)
        assert math.isclose(result, 440.0, rel_tol=1e-9)

    def test_multiplier_one(self):
        """Multiplier 1 = base * PHI."""
        result = Harmonics.calculate_harmonic_ratio(440.0, 1)
        assert math.isclose(result, 440.0 * PHI, rel_tol=1e-9)

    def test_multiplier_two(self):
        """Multiplier 2 = base * PHI^2."""
        result = Harmonics.calculate_harmonic_ratio(1.0, 2)
        assert math.isclose(result, PHI ** 2, rel_tol=1e-9)

    def test_seven_layers(self):
        """7th harmonic = base * PHI^7."""
        result = Harmonics.calculate_harmonic_ratio(1.0, 7)
        assert math.isclose(result, PHI ** 7, rel_tol=1e-9)

    def test_harmonics_increase(self):
        """Each harmonic level is PHI times the previous."""
        h1 = Harmonics.calculate_harmonic_ratio(100.0, 1)
        h2 = Harmonics.calculate_harmonic_ratio(100.0, 2)
        assert math.isclose(h2 / h1, PHI, rel_tol=1e-9)

    def test_negative_multiplier(self):
        """Negative multiplier = sub-harmonic (< base)."""
        result = Harmonics.calculate_harmonic_ratio(440.0, -1)
        assert result < 440.0


class TestHarmonicDecay:
    def test_zero_time(self):
        """At t=0, amplitude = initial."""
        result = Harmonics.harmonic_decay(1.0, 0.5, 0.0)
        assert math.isclose(result, 1.0, rel_tol=1e-9)

    def test_positive_decay(self):
        """Amplitude decreases over time."""
        a0 = Harmonics.harmonic_decay(1.0, 0.5, 0.0)
        a1 = Harmonics.harmonic_decay(1.0, 0.5, 1.0)
        a2 = Harmonics.harmonic_decay(1.0, 0.5, 2.0)
        assert a0 > a1 > a2

    def test_zero_decay_rate(self):
        """No decay = constant amplitude."""
        result = Harmonics.harmonic_decay(5.0, 0.0, 100.0)
        assert math.isclose(result, 5.0, rel_tol=1e-9)

    def test_large_time_approaches_zero(self):
        """Very large time → amplitude near zero."""
        result = Harmonics.harmonic_decay(1.0, 1.0, 100.0)
        assert result < 1e-40

    def test_known_value(self):
        """e^(-1) ≈ 0.3679."""
        result = Harmonics.harmonic_decay(1.0, 1.0, 1.0)
        assert math.isclose(result, math.exp(-1), rel_tol=1e-9)

    def test_scales_with_amplitude(self):
        """Double initial = double result."""
        r1 = Harmonics.harmonic_decay(1.0, 0.5, 2.0)
        r2 = Harmonics.harmonic_decay(2.0, 0.5, 2.0)
        assert math.isclose(r2, 2 * r1, rel_tol=1e-9)
