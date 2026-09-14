import math
import sys
from pathlib import Path

# Asegura que la raíz del repo esté en el path antes de importar
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from formulas.constants import ALPHA, BETA
from formulas.action import omega_action
from formulas.neuroscience_logic import NeuroscienceLogic


class TestOmegaActionBrainCollapse:
    """
    TEST Ω-CEREBRO: colapso extremo de la acción en el cerebro.
    Usa funciones ya existentes: resonancia neural + decaimiento neural.
    """

    def test_brain_living_high_resonance(self):
        """
        Escenario cerebro vivo: high gamma, capas sincronizadas.
        """
        a = 1.0
        b = 1.0
        S = NeuroscienceLogic.compute_neural_resonance(a, b)
        S_MAX = 1.0

        nu0 = 40.0
        decay_rate = 0.01
        t = 0.0
        dt = 0.1

        nu = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t)
        nu_plus = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t + dt)
        dnu = (nu_plus - nu) / dt

        A_omega = omega_action(S, S_MAX, nu, dnu)

        assert A_omega > 0.0, f"Brain should be alive, but Ω = {A_omega}"

    def test_brain_dying_resonance_lost(self):
        """
        Escenario de cerebro moribundo: menor latido y menor resonancia.
        """
        a = 1.0
        b = 0.0
        S = NeuroscienceLogic.compute_neural_resonance(a, b)
        S_MAX = 1.0

        nu0 = 1.0
        decay_rate = 0.05
        t = 0.0
        dt = 0.1

        nu = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t)
        nu_plus = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t + dt)
        dnu = (nu_plus - nu) / dt

        A_omega = omega_action(S, S_MAX, nu, dnu)

        assert 0.0 < A_omega < 1.0, f"Brain low energy, but Ω = {A_omega}"

    def test_brain_collapse(self):
        """
        Escenario de colapso total: resonancia 0, latido 0, variación 0.
        """
        a = 0.0
        b = 0.0
        S = NeuroscienceLogic.compute_neural_resonance(a, b)
        S_MAX = 1.0

        nu0 = 0.0
        decay_rate = 1.0
        t = 100.0
        dt = 0.1

        nu = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t)
        nu_plus = NeuroscienceLogic.simulate_neural_decay(nu0, decay_rate, t + dt)
        dnu = (nu_plus - nu) / dt

        A_omega = omega_action(S, S_MAX, nu, dnu)

        assert math.isclose(A_omega, 0.0, abs_tol=1e-10), \
            f"Ω should be 0 in collapse, but got {A_omega}"

    def test_omega_grows_with_resonance_and_latido(self):
        """
        A mayor resonancia y latido, Ω crece.
        """
        dt = 0.1

        # Caso 1: cerebro vivo, alta resonancia y alto latido
        S1 = NeuroscienceLogic.compute_neural_resonance(1.0, 1.0)
        nu1 = NeuroscienceLogic.simulate_neural_decay(40.0, 0.01, 0.0)
        nu1_plus = NeuroscienceLogic.simulate_neural_decay(40.0, 0.01, dt)
        dnu1 = (nu1_plus - nu1) / dt
        A_omega1 = omega_action(S1, 1.0, nu1, dnu1)

        # Caso 2: menor resonancia y menor latido
        S2 = NeuroscienceLogic.compute_neural_resonance(1.0, 0.0)
        nu2 = NeuroscienceLogic.simulate_neural_decay(1.0, 0.1, 0.0)
        nu2_plus = NeuroscienceLogic.simulate_neural_decay(1.0, 0.1, dt)
        dnu2 = (nu2_plus - nu2) / dt
        A_omega2 = omega_action(S2, 1.0, nu2, dnu2)

        assert A_omega1 > A_omega2, \
            f"Living brain resonance should be higher, but A1={A_omega1}, A2={A_omega2}"

    def test_neural_resonance_bounds(self):
        """
        La resonancia neural queda acotada entre 0 y ALPHA.
        """
        samples = [
            (0.0, 0.0),
            (1.0, 1.0),
            (1.0, 0.0),
            (0.7, 0.5),
            (0.3, 0.9),
        ]

        for a, b in samples:
            S = NeuroscienceLogic.compute_neural_resonance(a, b)
            assert 0.0 <= S <= ALPHA, f"Out of bounds: a={a}, b={b}, S={S}"

    def test_neural_decay_monotonic(self):
        """
        Si decay_factor > 0, la frecuencia decrece con el tiempo.
        """
        nu0 = 40.0
        decay_factor = 0.05

        early = NeuroscienceLogic.simulate_neural_decay(nu0, decay_factor, 0.0)
        late = NeuroscienceLogic.simulate_neural_decay(nu0, decay_factor, 1.0)

        assert late < early
