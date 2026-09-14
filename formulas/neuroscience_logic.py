from formulas.constants import ALPHA, BETA
import math

class NeuroscienceLogic:
    @staticmethod
    def compute_neural_resonance(layer_a: float, layer_b: float) -> float:
        """
        Calculates resonance between two neural layers based on ALPHA and BETA.

        layer_a: Activity in layer A.
        layer_b: Activity in layer B.
        """
        max_energy = max(layer_a, layer_b)
        if max_energy == 0:
            return 0.0
        return ALPHA - (BETA * abs(layer_a - layer_b) / max_energy)

    @staticmethod
    def simulate_neural_decay(frequency: float, decay_factor: float, time: float) -> float:
        """
        Simulates the decay of neural resonance frequency over time.

        frequency: Initial frequency.
        decay_factor: Decay constant.
        time: Time elapsed.
        """
        return frequency * math.exp(-decay_factor * time)
