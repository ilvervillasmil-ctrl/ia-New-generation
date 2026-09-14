import math
import sys
from pathlib import Path

# FIX CRÍTICO: sys.path DEBE IR ANTES de los imports problemáticos
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from formulas.constants import ALPHA, BETA
from formulas.action import omega_action
from formulas.neuroscience_logic import NeuroscienceLogic


class TestOmegaActionBrainCollapse:
    """
    TEST Ω-CEREBRO: colapso extremo de la acción en el cerebro.
    Usa already-built functions: neural resonance + neural decay.
    """

    def test_brain_living_high_resonance(self):
        """
        Escenario cerebro vivo: high gamma, capas sincronizadas.
        Latido alto, resonancia ALFA.
        """
        a = 1.0
        b = 1.0
        H = NeuroscienceLogic.compute_neural_resonance(a, b)
        S_MAX = 1.0

        nu0 = 40.0
        decay_rate = 0.01

        t = 0.0
        nu = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t)

        Dt = 0.1
        nu_plus = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t + Dt)
        dnu = (nu_plus - nu) / Dt

        A_omega = omega_action(H, S_MAX, nu, dnu)

        assert A_omega > 0.0, f"Brain should be alive, but Ω = {A_omega}"

    def test_brain_dying_resonance_lost(self):
        """
        Escenario de cerebro moribundo:
        una capa muere, alta decoherencia.
        """
        a = 1.0
        b = 0.0
        H = NeuroscienceLogic.compute_neural_resonance(a, b)
        S_MAX = 1.0

        nu0 = 1.0
        decay_rate = 0.05

        t = 0.0
        nu = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t)

        Dt = 0.1
        nu_plus = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t + Dt)
        dnu = (nu_plus - nu) / Dt

        A_omega = omega_action(H, S_MAX, nu, dnu)

        assert 0.0 < A_omega < 1.0, f"Brain low energy, but Ω = {A_omega}"

    def test_brain_collapse(self):
        """
        Escenario de colapso total:
        onda 0, capa muerta, decaimiento = 1.
        """
        a = 0.0
        b = 0.0
        H = NeuroscienceLogic.compute_neural_resonance(a, b)
        S_MAX = 1.0

        nu0 = 0.0
        decay_rate = 1.0
        t = 100.0
        nu = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t)

        Dt = 0.1
        nu_plus = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t + Dt)
        dnu = (nu_plus - nu) / Dt

        A_omega = omega_action(H, S_MAX, nu, dnu)

        assert math.isclose(A_omega, 0.0, abs_tol=1e-10), \
            f"Ω should be 0 in collapse, but got {A_omega}"

    def test_omega_grows_with_resonance_and_latido(self):
        """
        A mayor resonancia y latido, A_omega crece.
        """
        a1, b1 = 1.0, 1.0
        H1 = NeuroscienceLogic.compute_neural_resonance(a1, b1)
        nu1 = NeuroscienceLogic.simulate_neural_decay(40.0, 0.01, 0.0)
        dnu1 = (
            NeuroscienceLogic.simulate_neural_decay(40.0, 0.01, 0.1) - nu1
        ) / 0.1

        A_omega1 = omega_action(H1, 1.0, nu1, dnu1)

        a2, b2 = 1.0, 0.0
        H2 = NeuroscienceLogic.compute_neural_resonance(a2, b2)
        nu2 = NeuroscienceLogic.simulate_neural_decay(1.0, 0.1, 0.0)
        dnu2 = (
            NeuroscienceLogic.simulate_neural_decay(1.0, 0.1, 0.1) - nu2
        ) / 0.1

        A_omega2 = omega_action(H2, 1.0, nu2, dnu2)

        assert A_omega1 > A_omega2, \
            f"Living brain resonance should be higher, but A1={A_omega1}, A2={A_omega2}"
