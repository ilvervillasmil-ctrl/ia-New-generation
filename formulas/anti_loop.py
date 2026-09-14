# ======================================================================
# ANTI-LOOP CEMYCA
# CONTROL DE BUCLE CIEGO Y RUPTURA DE ESTADOS ESTÁTICOS
#
# Framework: Villasmil-Omega / UIS
#
# Fórmula:
#
#                   -|E_L3(now) - E_L3(past)|
#                   --------------------------
#                              β
# Ω_loop = e
#
#          × [ 1 - ΔL1 / (ΔL1 + β) ]
#
#          × [ 1 - tanh(E_L5(now) / (E_L3(now) + β)) ]
#
#
# donde:
#
# ΔL3 = |E_L3(now) - E_L3(past)|
# ΔL1 = |E_L1(now) - E_L1(past)|
#
# β = 1/27
#
# Interpretación:
#
# Φ_estático:
#     Detecta permanencia o inmovilidad del estado L3.
#
# Ψ_input:
#     Detecta perturbación exógena procedente de L1.
#
# Ψ_supervisor:
#     Detecta intervención/reflexión endógena procedente de L5.
#
# Ω_loop → 1:
#     Estado estático sin interrupción externa y sin supervisión.
#
# Ω_loop → 0:
#     Estado dinámico, interrumpido o supervisado.
#
# IMPORTANTE:
# El nombre técnico de Python se conserva como AntiLoopCemycaFormula
# para mantener compatibilidad con tests/test_anti_loop.py.
# ======================================================================

import math

from .constants import BETA


class AntiLoopCemycaFormula:
    """
    Fórmula Anti-Luck CEMYCA.

    Evalúa el grado de secuestro operacional de un estado L3
    considerando tres componentes:

        1. Persistencia estructural de L3.
        2. Interrupción exógena procedente de L1.
        3. Supervisión endógena procedente de L5.

    La salida Ω_loop queda restringida al intervalo [0.0, 1.0].
    """

    @staticmethod
    def calculate_omega_loop(
        e_l1_now: float,
        e_l1_past: float,
        e_l3_now: float,
        e_l3_past: float,
        e_l5_now: float,
    ) -> float:
        """
        Calcula Ω_loop.

        Parámetros
        ----------
        e_l1_now:
            Estado actual de la entrada externa L1.

        e_l1_past:
            Estado anterior de la entrada externa L1.

        e_l3_now:
            Estado estructural actual L3.

        e_l3_past:
            Estado estructural anterior L3.

        e_l5_now:
            Nivel actual de supervisión L5.

        Retorna
        -------
        float
            Índice Ω_loop restringido a [0.0, 1.0].

            Ω_loop ≈ 1.0:
                Estado estático ciego.

            Ω_loop ≈ 0.0:
                Estado dinámico, interrumpido o supervisado.
        """

        # ==============================================================
        # 1. VARIACIÓN TEMPORAL DEL ESTADO ESTRUCTURAL L3
        # ==============================================================

        delta_l3 = abs(
            e_l3_now - e_l3_past
        )

        # ==============================================================
        # 2. VARIACIÓN DE LA ENTRADA EXÓGENA L1
        # ==============================================================

        delta_l1 = abs(
            e_l1_now - e_l1_past
        )

        # ==============================================================
        # 3. COMPONENTE DE ESTATICIDAD
        #
        # Φ_estático = exp(-ΔL3 / β)
        #
        # Si L3 no cambia:
        #     ΔL3 = 0
        #     Φ = 1
        #
        # Si L3 cambia:
        #     Φ disminuye exponencialmente.
        # ==============================================================

        phi_estatico = math.exp(
            -delta_l3 / BETA
        )

        # ==============================================================
        # 4. INTERRUPCIÓN EXÓGENA
        #
        #                ΔL1
        # Ψ_input = -------------
        #             ΔL1 + β
        #
        # Si L1 permanece constante:
        #     Ψ_input = 0
        #
        # Si aparece una perturbación:
        #     Ψ_input → 1
        # ==============================================================

        psi_input = (
            delta_l1
            / (delta_l1 + BETA)
        )

        # ==============================================================
        # 5. SUPERVISIÓN ENDÓGENA
        #
        #                         E_L5(now)
        # Ψ_supervisor = tanh( ---------------- )
        #                       E_L3(now) + β
        #
        # β actúa como término regularizador dentro del dominio
        # operacional esperado por el Framework.
        # ==============================================================

        psi_supervisor = math.tanh(
            e_l5_now
            / (e_l3_now + BETA)
        )

        # ==============================================================
        # 6. ECUACIÓN ANTI-LUCK / OMEGA LOOP
        #
        # Ω_loop =
        #
        #     Φ_estático
        #     × (1 - Ψ_input)
        #     × (1 - Ψ_supervisor)
        #
        # Un bucle ciego fuerte requiere simultáneamente:
        #
        #   - alta estaticidad,
        #   - ausencia de perturbación externa,
        #   - ausencia de supervisión.
        # ==============================================================

        omega_loop = (
            phi_estatico
            * (1.0 - psi_input)
            * (1.0 - psi_supervisor)
        )

        # ==============================================================
        # 7. BLINDAJE DEL DOMINIO
        #
        # Garantiza:
        #
        #     0.0 <= Ω_loop <= 1.0
        # ==============================================================

        return max(
            0.0,
            min(1.0, omega_loop),
        )
