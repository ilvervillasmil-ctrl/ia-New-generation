import math

class ExponentialDecay:
    @staticmethod
    def calculate_decay(initial_value: float, decay_rate: float, time: float) -> float:
        """
        Models exponential decay over time.
        Formula: V(t) = V0 * e^(-k * t)

        initial_value: Initial quantity.
        decay_rate: Rate of decay (k).
        time: Time (t).
        """
        if initial_value <= 0:
            raise ValueError("Initial value must be greater than zero.")
        return initial_value * math.exp(-decay_rate * time)

    @staticmethod
    def half_life(decay_rate: float) -> float:
        """
        Calculates the half-life based on the decay rate.
        Formula: T_half = ln(2) / decay_rate
        """
        if decay_rate <= 0:
            raise ValueError("Decay rate must be greater than zero.")
        return math.log(2) / decay_rate
