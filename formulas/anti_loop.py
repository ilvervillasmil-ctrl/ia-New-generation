# formulas/anti_loop.py

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class AntiLoopCemycaFormula:
    """
    Fórmula Anti-Loop CEMYCA.

    Detecta una configuración compatible con un estado estático
    sin suficiente entrada externa ni supervisión.

    Omega_loop -> 1:
        mayor señal de posible loop.

    Omega_loop -> 0:
        menor señal de loop.
    """

    beta: float = 1.0

    def __post_init__(self) -> None:
        if self.beta <= 0.0:
            raise ValueError("beta debe ser mayor que 0.")

    def calculate(
        self,
        e_l1_now: float,
        e_l1_past: float,
        e_l3_now: float,
        e_l3_past: float,
        e_l5_now: float,
    ) -> float:
        """
        Calcula:

            ΔL1 = |E_L1(now) - E_L1(past)|
            ΔL3 = |E_L3(now) - E_L3(past)|

            Φ_static =
                exp(-ΔL3 / β)

            Ψ_input =
                ΔL1 / (ΔL1 + β)

            Ψ_supervisor =
                tanh(E_L5(now) / (E_L3(now) + β))

            Ω_loop =
                Φ_static
                * (1 - Ψ_input)
                * (1 - Ψ_supervisor)

        El resultado final se restringe al intervalo [0, 1].
        """

        delta_l1 = abs(e_l1_now - e_l1_past)
        delta_l3 = abs(e_l3_now - e_l3_past)

        phi_static = math.exp(
            -delta_l3 / self.beta
        )

        psi_input = (
            delta_l1
            / (delta_l1 + self.beta)
        )

        denominator = e_l3_now + self.beta

        if abs(denominator) < 1e-15:
            raise ValueError(
                "E_L3(now) + beta no puede ser cero."
            )

        psi_supervisor = math.tanh(
            e_l5_now / denominator
        )

        omega_loop = (
            phi_static
            * (1.0 - psi_input)
            * (1.0 - psi_supervisor)
        )

        return max(
            0.0,
            min(1.0, omega_loop),
        )
