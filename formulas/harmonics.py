import math
from formulas.constants import PHI

class Harmonics:
    @staticmethod
    def calculate_harmonic_ratio(base_frequency: float, multiplier: int) -> float:
        """
        Calculates the harmonic ratio relative to the golden ratio (PHI).

        base_frequency: The initial frequency to calculate harmonics for.
        multiplier: The harmonic level (e.g., 1st, 2nd, etc.).
        """
        return base_frequency * (PHI ** multiplier)

    @staticmethod
    def harmonic_decay(initial_amplitude: float, decay_rate: float, time: float) -> float:
        """
        Formula: A = A0 * e^(-lambda * t)
        Models the decay of a signal over time.
        """
        return initial_amplitude * math.exp(-decay_rate * time)
