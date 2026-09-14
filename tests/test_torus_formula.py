"""
tests/test_torus_formula.py
===========================
Tests de la formula del toroide - Villasmil-Omega v3.2

Basados en:
  [TORUS] "Structural Cycles and Operational Infinity" - Ilver Villasmil, 2026
  [RH]    "Resolution of the Riemann Hypothesis" - Ilver Villasmil, 2026
  [UCF]   "Villasmil-Omega Framework: Integration of Everything" - 2026

============================================================
PREDICCIONES FIJADAS ANTES DE CORRER (protocolo no-circularidad)
============================================================

  P1 - Ley 1:
     T2-T7 son pairwise coprimos -> coverage = 1.0 exactamente.
     Biyeccion completa del estado.
     PREDICTED: PASS para todos los sistemas del paper.

  P2 - Ley 2:
     (4,6): coverage = 0.5 exactamente (12/24)
     (4,6,9): coverage = 36/216 = 1/6 exactamente
     PREDICTED: valores exactos del paper.

  P3 - Ley 3:
     0 violaciones para primos q > B, todo B probado.
     Es un teorema - no puede fallar.
     PREDICTED: violations = [] siempre.

  P4 - Ley 4:
     E(M) < 1e-3 con corpus de primos hasta 5000 (cota conservadora).
     E(M) ~ O(10^-7) requiere corpus hasta ~10^6.
     PREDICTED: law_holds = True con cota conservadora.

  P5 - Infinito operacional:
     T3 tiene exactamente 30 estados unicos antes de cerrar.
     T4 tiene exactamente 210 estados unicos.
     PREDICTED: is_bijection = True, P = M para todos.

  P6 - Beta como residuo:
     beta^4 es el mas cercano a E(M7) con ratio ~= 2.29.
     NO son iguales - la conexion formal es OPEN.
     PREDICTED: closest_n = 4, ratio_T7 ~= 2.29.

  P7 - C_max desde el toroide:
     C_max = alpha = 26/27 - invariante en todos los sistemas.
     PREDICTED: C_max = ALPHA para T2-T7.

  P8 - Campo plano (Teorema Espectral):
     sum_epsilon ~= 0 (por construccion).
     PREDICTED: |sum_epsilon| < 1e-9.
"""

import math
import pytest
from formulas.torus_formula import (
    # Estructura
    torus_dimension, primorial_M, phi_M, state_map,
    period, torus_coverage, phase_vector, is_covering_space,
    # Las 4 leyes
    law1_cycle_independence, law2_cycle_resonance,
    law3_prime_filtering, law4_field_energy,
    # Espectral
    spectral_modes,
    # UCF
    beta_torus_residue_analysis, c_max_from_torus,
    # Infinito operacional
    operational_infinity,
    # Reporte
    torus_formula_report,
    # Constantes
    TORUS_PRIMES, E_M6_PAPER, E_M7_PAPER,
)
from formulas.constants import ALPHA, BETA, PHI


# ============================================================
# I. ESTRUCTURA BASICA DEL TOROIDE
# ============================================================

class TestTorusStructure:

    def test_torus_dimension(self):
        assert torus_dimension([2, 3]) == 2
        assert torus_dimension([2, 3, 5, 7]) == 4
        assert torus_dimension(TORUS_PRIMES[7]) == 7

    def test_primorial_M(self):
        assert primorial_M([2, 3]) == 6
        assert primorial_M([2, 3, 5]) == 30
        assert primorial_M([2, 3, 5, 7]) == 210
        assert primorial_M([2, 3, 5, 7, 11, 13, 17]) == 510510

    def test_phi_M(self):
        assert phi_M([2, 3]) == 2
        assert phi_M([2, 3, 5]) == 8
        assert phi_M([2, 3, 5, 7]) == 48
        assert phi_M(TORUS_PRIMES[7]) == 92160

    def test_state_map_origin(self):
        """phi(0) = (0, 0, ..., 0) - el origen del toroide."""
        assert state_map(0, [2, 3, 5]) == (0, 0, 0)
        assert state_map(0, TORUS_PRIMES[7]) == (0,) * 7

    def test_state_map_closure(self):
        """phi(P) = phi(0) - la trayectoria cierra en n=P."""
        for k in [2, 3, 4, 5]:
            ps = TORUS_PRIMES[k]
            P  = period(ps)
            assert state_map(P, ps) == state_map(0, ps), (
                f"T{k}: phi(P={P}) != phi(0)"
            )

    def test_period_equals_primorial(self):
        """Para primos: P = lcm = producto (Ley 1)."""
        for k in [2, 3, 4, 5, 6, 7]:
            ps = TORUS_PRIMES[k]
            M  = primorial_M(ps)
            P  = period(ps)
            assert P == M, f"T{k}: P={P} != M={M}"

    def test_coverage_is_one_for_primes(self):
        """Primos son pairwise coprimos -> coverage = 1.0 exactamente."""
        for k in [2, 3, 4, 5, 6, 7]:
            cov = torus_coverage(TORUS_PRIMES[k])
            assert cov == pytest.approx(1.0), f"T{k}: coverage={cov}"

    def test_is_covering_space(self):
        """N es el espacio de cobertura de T_k (Thm 5.4)."""
        for k in [2, 3, 4]:
            assert is_covering_space(TORUS_PRIMES[k]), (
                f"T{k} no es espacio de cobertura"
            )

    def test_phase_advances_uniformly(self):
        """theta_i(n) avanza 2*pi/p_i por paso (Thm 5.2 Phase Dynamics)."""
        primes = [3, 5]
        for n in range(15):
            ph      = phase_vector(n, primes)
            ph_next = phase_vector(n + 1, primes)
            step0   = (ph_next[0] - ph[0]) % (2 * math.pi)
            step1   = (ph_next[1] - ph[1]) % (2 * math.pi)
            assert abs(step0 - 2 * math.pi / 3) < 1e-9
            assert abs(step1 - 2 * math.pi / 5) < 1e-9

    def test_all_states_unique_T3(self):
        """T3 visita exactamente 30 estados unicos antes de cerrar."""
        primes = TORUS_PRIMES[3]
        P      = period(primes)
        states = [state_map(n, primes) for n in range(P)]
        assert len(set(states)) == P == 30


# ============================================================
# II. LEY 1 - INDEPENDENCIA DE CICLOS
# ============================================================

class TestLaw1Independence:
    """
    Ley 1: gcd(p_i, p_j) = 1 para todo i!=j -> P = prod(p_i) = |S(M)| (biyeccion)

    PREDICTED: PASS para T2-T7. Coverage = 1.0 exactamente.
    """

    @pytest.mark.parametrize("k", [2, 3, 4, 5, 6, 7])
    def test_Tk_is_independent(self, k):
        ps = TORUS_PRIMES[k]
        r  = law1_cycle_independence(ps)
        assert r["all_coprime"] is True
        assert r["bijection"]   is True
        assert r["law_holds"]   is True
        assert r["coverage"]    == pytest.approx(1.0)

    def test_T7_exact_values(self):
        """T7 del paper: M=510510, phi=92160, P=510510."""
        r = law1_cycle_independence(TORUS_PRIMES[7])
        assert r["M"]      == 510510
        assert r["period"] == 510510
        assert r["regime"] == "INDEPENDENT"

    def test_bijection_visits_all_states(self):
        """En regimen independiente, cada estado es visitado exactamente una vez."""
        primes = [3, 5]
        P      = period(primes)
        states = [state_map(n, primes) for n in range(P)]
        assert len(set(states)) == P == 15


# ============================================================
# III. LEY 2 - RESONANCIA DE CICLOS
# ============================================================

class TestLaw2Resonance:
    """
    Ley 2: gcd > 1 -> P < prod(n_i) (orbita colapsa)

    PREDICTED: valores exactos del paper:
      (4,6):   coverage = 0.5  (12/24)
      (4,6,9): coverage = 36/216 = 1/6
      (3,4,6): coverage = 12/72 = 1/6
    """

    def test_4x6_coverage_50pct(self):
        r = law2_cycle_resonance([4, 6])
        assert r["has_shared"] is True
        assert r["period"]   == 12
        assert r["product"]  == 24
        assert r["coverage"] == pytest.approx(0.5)
        assert r["states_missed"] == 12
        assert r["law_holds"]

    def test_4x6x9_coverage_17pct(self):
        r = law2_cycle_resonance([4, 6, 9])
        assert r["period"]  == 36
        assert r["product"] == 216
        assert r["coverage"] == pytest.approx(36 / 216)
        assert r["law_holds"]

    def test_3x4x6_coverage_17pct(self):
        r = law2_cycle_resonance([3, 4, 6])
        assert r["period"]  == 12
        assert r["product"] == 72
        assert r["law_holds"]

    def test_independent_vs_resonant(self):
        """Contraste claro entre los dos regimenes."""
        ind = law1_cycle_independence([3, 5])
        res = law2_cycle_resonance([4, 6])
        assert ind["coverage"] == pytest.approx(1.0)
        assert res["coverage"] == pytest.approx(0.5)
        assert ind["regime"] == "INDEPENDENT"
        assert res["regime"] == "RESONANT"


# ============================================================
# IV. LEY 3 - FILTRADO ESTRUCTURAL DE PRIMOS
# ============================================================

class TestLaw3PrimeFiltering:
    """
    Ley 3: para todo q primo, q > B: gcd(q, M) = 1

    PREDICTED: violations = [] siempre.
    Es un teorema - no puede fallar.
    """

    @pytest.mark.parametrize("B", [7, 11, 13, 17])
    def test_no_violations(self, B):
        r = law3_prime_filtering(B=B, check_up_to=B * 30)
        assert r["violations"] == [], (
            f"B={B}: violations={r['violations']}"
        )
        assert r["law_holds"] is True

    def test_proof_is_constructive(self):
        """
        La prueba es constructiva: si gcd(q, M) > 1
        entonces p <= B divide q -> q = p <= B. Contradiccion.
        """
        from math import gcd
        B  = 11
        r  = law3_prime_filtering(B=B, check_up_to=500)
        M  = r["M"]

        for q in [13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
            g = gcd(q, M)
            assert g == 1, f"q={q}: gcd({q}, {M}) = {g} != 1"

    def test_prime_localization_in_admissible_zone(self):
        """Todo primo q > B vive en (Z/MZ)* subset T_k."""
        from math import gcd
        B      = 7
        primes = [2, 3, 5, 7]
        M      = primorial_M(primes)
        above  = [q for q in range(8, 100) if
                  all(q % i != 0 for i in range(2, q)) and q > 1]
        for q in above:
            if all(q % i != 0 for i in range(2, int(q**0.5) + 1)):
                assert gcd(q, M) == 1


# ============================================================
# V. LEY 4 - CAMPO ARITMETICO E(M)
# ============================================================

class TestLaw4FieldEnergy:
    """
    Ley 4: E(M) = sum eps(a)^2 ~ O(10^-7)

    PREDICTED:
      - E(M) < 1e-3 con corpus hasta 5000 (cota conservadora)
      - sum_epsilon ~= 0 exactamente (E_hat(0) = 0)
      - E decrece con corpus mas grande
    """

    def test_field_energy_conservative_bound(self):
        """E(M) < 1e-3 con corpus pequeno."""
        r = law4_field_energy(TORUS_PRIMES[4], prime_limit=5000)
        assert r["law_holds"] is True
        assert r["E_M"] < 1e-3, (
            f"E(M) = {r['E_M']:.2e} debe ser < 1e-3"
        )

    def test_field_mean_is_zero(self):
        """
        E_hat(0) = sum eps(a) = 0 exactamente (Theorem 6.1(i)).
        No es aproximacion - es exacto por construccion.
        """
        r = law4_field_energy(TORUS_PRIMES[3], prime_limit=2000)
        assert abs(r["sum_epsilon"]) < 1e-9, (
            f"sum_epsilon = {r['sum_epsilon']:.2e} debe ser ~0"
        )

    def test_E_decreases_with_larger_corpus(self):
        """E(M) decrece cuando el corpus crece."""
        primes = TORUS_PRIMES[4]
        r1 = law4_field_energy(primes, prime_limit=1000)
        r2 = law4_field_energy(primes, prime_limit=10000)
        assert r2["E_M"] < r1["E_M"], (
            f"E con 10000 primos={r2['E_M']:.2e} debe ser < "
            f"E con 1000 primos={r1['E_M']:.2e}"
        )

    def test_E_positive(self):
        """E(M) > 0 siempre."""
        r = law4_field_energy(TORUS_PRIMES[4], prime_limit=3000)
        assert r["E_M"] > 0

    def test_paper_values_are_O_10_minus_7(self):
        """Los valores del paper (Tabla 3) estan en O(10^-7)."""
        assert 1e-8 < E_M6_PAPER < 1e-6
        assert 1e-8 < E_M7_PAPER < 1e-6
        assert abs(math.log10(E_M6_PAPER) - (-6.26)) < 0.1
        assert abs(math.log10(E_M7_PAPER) - (-6.09)) < 0.1

    def test_field_stability_T6_vs_T7(self):
        """
        E es estable cuando phi(M) -> inf (Theorem 6.2 Field Stability).
        T7 tiene phi = 92160 vs T6 con phi = 5760 (factor 16x).
        E crece solo 1.49x - muy estable.
        """
        ratio_phi = phi_M(TORUS_PRIMES[7]) / phi_M(TORUS_PRIMES[6])
        ratio_E   = E_M7_PAPER / E_M6_PAPER

        assert ratio_phi == pytest.approx(16.0, rel=0.01)
        assert ratio_E   < 2.0


# ============================================================
# VI. CAMPO ESPECTRAL
# ============================================================

class TestSpectralField:
    """
    Theorem 6.1 (Espectral):
      (i)  e_hat(0) = 0
      (ii) E(M) = (1/phi) * sum|e_hat(k)|^2  (Parseval)
      (iii)|e_hat(k)|^2 ~= E/phi(M) para k!=0 (independencia modal)
    """

    def test_dc_component_is_zero(self):
        """e_hat(0) = 0 exactamente (componente DC = 0)."""
        r = spectral_modes(TORUS_PRIMES[3], prime_limit=2000, max_modes=10)
        assert abs(r["E_dc"]) < 1e-9, (
            f"E_dc = {r['E_dc']:.2e} debe ser ~0"
        )

    def test_modes_computed(self):
        """Los modos espectrales son calculables."""
        r = spectral_modes(TORUS_PRIMES[3], prime_limit=2000, max_modes=8)
        assert r["modes_computed"] >= 1
        assert r["E_M"] > 0

    def test_rh_connection_not_implemented(self):
        """
        La conexion formal e_hat(k) <-> gamma_k de Riemann
        no esta implementada - es trabajo en progreso [6].
        """
        r = spectral_modes(TORUS_PRIMES[3], prime_limit=1000)
        assert "rh_connection" in r
        assert "trabajo en progreso" in r["rh_connection"]


# ============================================================
# VII. BETA COMO RESIDUO DEL TOROIDE
# ============================================================

class TestBetaTorusResidue:
    """
    Pregunta abierta: beta = residuo del toroide?

    PREDICTED:
      closest_n = 4 (beta^4 es el mas cercano a E(M7))
      ratio_T7 ~= 2.29 (no es 1 - no son iguales)
      status = "OPEN" - no hay derivacion formal
    """

    def test_beta_irreducible(self):
        """beta > 0 - el residuo del cubo es irreducible."""
        assert BETA > 0
        assert abs(BETA - 1/27) < 1e-12

    def test_closest_power_is_4(self):
        """beta^4 es el exponente mas cercano a E(M7)."""
        r = beta_torus_residue_analysis()
        assert r["closest_n"] == 4, (
            f"closest_n = {r['closest_n']}, se esperaba 4"
        )

    def test_ratio_is_not_one(self):
        """
        beta^4 / E(M7) ~= 2.29 - NO son iguales.
        La conexion formal es abierta.
        """
        r = beta_torus_residue_analysis()
        ratio = r["closest_ratio"]
        assert abs(ratio - 1.0) > 0.1
        assert 0.5 < ratio < 10.0

    def test_beta4_closest_to_E_M7(self):
        """beta^4 = 1.882e-6, E(M7) = 8.20e-7: ratio ~= 2.29."""
        r     = beta_torus_residue_analysis()
        p4    = r["powers"][4]
        assert abs(p4["value"] - BETA**4) < 1e-15
        assert p4["ratio_T7"] == pytest.approx(BETA**4 / E_M7_PAPER, rel=0.01)

    def test_status_is_open(self):
        """El status de la pregunta es OPEN - documentado honestamente."""
        r = beta_torus_residue_analysis()
        assert "OPEN" in r["status"]
        assert "derivable" in r["falsifiable_if"]

    def test_both_are_irreducible_residues(self):
        """
        Analogia estructural (no prueba):
          Cubo: beta = 1 centro de 27 - no puede orbitar la superficie
          Toroide: E(M) = desviacion distribucional que no se elimina
        """
        r = beta_torus_residue_analysis()
        assert r["cube_residue"]  == BETA
        assert r["torus_residue"] == E_M7_PAPER
        assert r["cube_residue"]  > 0
        assert r["torus_residue"] > 0


# ============================================================
# VIII. C_MAX DESDE EL TOROIDE
# ============================================================

class TestCmaxFromTorus:
    """
    C_max = alpha = 1 - beta - invariante UCF.
    Derivado de la geometria del cubo 3x3x3.
    Consistente con la estructura del toroide.
    """

    @pytest.mark.parametrize("k", [2, 3, 4, 5, 6, 7])
    def test_C_max_invariant(self, k):
        """C_max = ALPHA para todos los sistemas T2-T7."""
        r = c_max_from_torus(TORUS_PRIMES[k])
        assert r["C_max"] == ALPHA
        assert r["beta_ucf"] == BETA
        assert r["coverage"] == pytest.approx(1.0)

    def test_C_max_formula(self):
        """C_max = 1 - beta = 26/27 exactamente."""
        r = c_max_from_torus(TORUS_PRIMES[4])
        assert r["C_max"] == pytest.approx(1.0 - BETA, rel=1e-9)
        assert r["C_max"] < 1.0
        assert r["C_max"] == pytest.approx(26/27, rel=1e-9)

    def test_beta_prevents_perfection(self):
        """beta > 0 garantiza que C_max < 1."""
        assert BETA > 0
        assert ALPHA < 1.0
        assert ALPHA + BETA == pytest.approx(1.0)


# ============================================================
# IX. INFINITO OPERACIONAL
# ============================================================

class TestOperationalInfinity:
    """
    Theorem 7.1: Todo proceso x_{n+1} = x_n + 1 es estructuralmente finito.
    Infinito = numero de vueltas, no tamano de la pista.
    """

    @pytest.mark.parametrize("k,expected_P", [(2, 6), (3, 30), (4, 210), (5, 2310)])
    def test_period_exact(self, k, expected_P):
        r = operational_infinity(TORUS_PRIMES[k])
        assert r["P"] == expected_P
        assert r["unique_states"] == expected_P
        assert r["is_bijection"] is True

    def test_closure_at_period(self):
        """phi(P) = phi(0) - la trayectoria cierra exactamente en n=P."""
        for k in [2, 3, 4]:
            r = operational_infinity(TORUS_PRIMES[k])
            assert r["closure_at_P"] is True

    def test_structure_is_finite(self):
        """La estructura es finita - el proceso es infinito."""
        r = operational_infinity(TORUS_PRIMES[4])
        assert r["structure_finite"] is True
        assert r["infinity_type"] == "operacional (numero de vueltas), no estructural (tamano)"

    def test_laps_are_infinite(self):
        """El proceso corre para siempre."""
        r = operational_infinity(TORUS_PRIMES[3])
        assert "infinitas" in r["laps"]


# ============================================================
# X. REPORTE COMPLETO
# ============================================================

class TestTorusFormulaReport:
    """Test de integracion: todas las piezas funcionan juntas."""

    def test_report_all_laws_pass(self):
        """Todas las 4 leyes pasan simultaneamente."""
        r = torus_formula_report(TORUS_PRIMES[4], prime_limit=3000)
        assert r["all_laws_pass"] is True

    def test_report_contains_rh_status(self):
        """El reporte documenta honestamente el estado de la conexion con RH."""
        r = torus_formula_report(TORUS_PRIMES[4])
        rh = r["rh_connection"]
        assert rh["implemented"] is False
        assert "trabajo en progreso" in rh["status"]

    def test_report_ucf_integration(self):
        """El reporte integra correctamente con UCF."""
        r = torus_formula_report(TORUS_PRIMES[4])
        ucf = r["ucf_integration"]
        assert ucf["beta"]  == BETA
        assert ucf["alpha"] == ALPHA
        assert ucf["C_max"] == ALPHA

    def test_report_papers_cited(self):
        """Los papers fuente estan citados."""
        r = torus_formula_report(TORUS_PRIMES[4])
        assert "torus" in r["papers"]
        assert "rh"    in r["papers"]
        assert "ucf"   in r["papers"]


# ============================================================
# XI. CONEXION UCF COMPLETA
# ============================================================

class TestUCFConnection:
    """
    Verifica la cadena completa:
    Toroide -> E(M) -> beta -> alpha -> C_max -> coherencia UCF
    """

    def test_alpha_beta_sum_one(self):
        """alpha + beta = 1 - conservacion estructural."""
        assert ALPHA + BETA == pytest.approx(1.0, rel=1e-12)

    def test_beta_is_1_over_27(self):
        """beta = 1/27 - del cubo 3x3x3."""
        assert BETA == pytest.approx(1/27, rel=1e-12)

    def test_alpha_is_26_over_27(self):
        """alpha = 26/27 - la superficie del cubo."""
        assert ALPHA == pytest.approx(26/27, rel=1e-12)

    def test_torus_coverage_consistent_with_alpha(self):
        """
        La cobertura del toroide T_k es siempre 1.0 para primos.
        Alpha viene de la geometria del cubo 3x3x3, no del toroide.
        """
        for k in [2, 3, 4, 5]:
            cov = torus_coverage(TORUS_PRIMES[k])
            assert cov == pytest.approx(1.0)
        # El cubo resonante (3,3,3) es diferente
        r_cube = law2_cycle_resonance([3, 3, 3])
        assert r_cube["coverage"] == pytest.approx(3/27)  # 1/9, no beta

    def test_integers_orbit_torus_forever(self):
        """phi(n+P) = phi(n) para todo n."""
        primes = TORUS_PRIMES[3]
        P      = period(primes)
        for n in range(10):
            assert state_map(n, primes) == state_map(n + P, primes)

    def test_C_max_never_reaches_one(self):
        """C_max = alpha < 1 - beta garantiza que ningun sistema alcanza perfeccion."""
        assert ALPHA < 1.0
        assert BETA  > 0.0
        assert 1.0 - ALPHA == pytest.approx(BETA, rel=1e-12)
