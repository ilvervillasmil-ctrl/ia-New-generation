# formulas/_action.py

from formulas.constants import ALPHA, BETA
import math
from typing import List, Tuple

def negentropy(S: float, S_MAX: float) -> float:
    """
    Negentropía del sistema.
    S     = entropía de la distribución del sistema
    S_MAX = entropía máxima de la misma distribución
    """
    return max(0.0, 1.0 - S / S_MAX)

def omega_action(
    S: float, S_MAX: float, nu: float, dnu: float
) -> float:
    """
    Fórmula de la acción universal Ω en un sistema físico X.

    Parámetros:
    - S     = entropía de la distribución del sistema X.
    - S_MAX = entropía máxima de dicha distribución.
    - nu    = frecuencia de latido del sistema (latidos por unidad de tiempo).
    - dnu   = derivada de la frecuencia de latido (aceleración/desaceleración).

    Resultado:
    - Acción efectiva Ω del sistema, en [0, 1].
    """
    H = negentropy(S, S_MAX)
    return ALPHA * H * nu + BETA * abs(dnu)
