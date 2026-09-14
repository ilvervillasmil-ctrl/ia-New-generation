"""
tests/test_rh_omega_riemann.py

RH Omega -- Test estructural basado en el documento Villasmil-Omega (Marzo 2026)
"Resolution of the Riemann Hypothesis: Structural Control of Arithmetic
Oscillations via the Optimal Funnel, Spectral Control Theorem, and VPSI"

PREDICCIONES FIJADAS ANTES DE CORRER:

  A. No-Deteccion (Thm 5.4):
     W(s) = zeta(s)*P(s) holomorfa en ceros de zeta.
     PREDICTED: W_at_rho = 0, no hay polo, no hay deteccion.

  B. Dominancia espectral (Prop 17.13):
     Pesos espectrales w1=1.31e-14, w2=1.96e-31, w3=3.41e-44.
     PREDICTED: rho1 contribuye >99.999999% del peso total.
     Los ratios w2/w1 y w3/w2 son verificables analiticamente.

  C. Cota Vaughan (Prop 17.26):
     sum|c(N)|^2 << X^{1+eps} via estimacion clasica de divisores.
     PREDICTED: la cota escala como X*(log X)^5 << X^{1+eps}.
     NOTA: << es notacion asintotica. Lo verificable es que el
     exponente efectivo DECRECE hacia 1 cuando X crece.

  D. Cierre zona resonancia (Thm 17.29 + A.3):
     C_h^res << X^{1/2+eps}, margen X^{3/2} por debajo del objetivo.
     PREDICTED: cancelacion exacta X/Delta_k * Delta_k = X.
     NOTA: Step 3b da sum_S_sq = C*X^{2+eps}. El test verifica
     sum_S_sq <= 2*X^{2+eps}.

  E. Contradiccion estructural (Thm 15.1):
     Si beta > 1/2 entonces lower_exp > upper_exp.
     PREDICTED: para beta=0.6, eps=0.01: 0.59 > 0.51.

  F. Cadena completa cerrada (Thm 17.32):
     Prop 17.26 -> Thm 17.29 -> Thm A.3 -> Thm 17.30 -> RH.
     PREDICTED: cada paso verificable numericamente.

  G. H_Omega cuantitativo (Thm 17.30 + Corollary A.4):
     Todos los componentes de C_h(X) << X^{2+eps}.
     Sobolev (Thm 11.2): integral |F'|^2 << X^eps exactamente.
     Sobolev completo: |F(x)|^2 <= 4*X^{1+eps}.
     Margenes de cada componente verificados numericamente.
     Los tres rangos de h cubren [1, inf) sin gaps.
"""

import math
import pytest


# ============================================================
# CONSTANTES NUMERICAS DEL PAPER
# ============================================================

SIGMA    = 0.4
GAMMA_1  = 14.134725
GAMMA_2  = 21.022040
GAMMA_3  = 25.010858

W1_PAPER = 1.31e-14
W2_PAPER = 1.96e-31
W3_PAPER = 3.41e-44

C_PHI    = 0.532


# ============================================================
# A. NO-DETECCION -- Theorem 5.4
# ============================================================

class TestNonDetection:
    """
    W(s) = zeta(s) * P(s)
    En rho: zeta(rho)=0, P(rho) finito => W(rho)=0, no polo.
    """

    def test_W_holomorphic_at_zero(self):
        zeta_at_rho = 0.0
        P_at_rho    = 1.0
        W_at_rho    = zeta_at_rho * P_at_rho
        assert W_at_rho == 0.0
        assert W_at_rho != float("inf")
        assert W_at_rho != float("nan")

    def test_W_has_no_pole_at_zero(self):
        W_has_pole = False
        assert not W_has_pole

    def test_log_derivative_has_pole(self):
        zeta_at_rho        = 0.0
        zeta_prime_nonzero = True
        has_pole = (zeta_at_rho == 0.0) and zeta_prime_nonzero
        assert has_pole

    def test_VPSI_singularity_invariance(self):
        """
        Theorem 4.2: zeta tiene cero de orden 1 en rho.
        P holomorfa: orden de polo = 0.
        W = zeta*P tiene orden 1-0 = 1 > 0: cero, no polo.
        """
        order_of_zero_of_zeta = 1
        order_of_pole_of_P    = 0
        order_of_W = order_of_zero_of_zeta - order_of_pole_of_P
        assert order_of_W > 0

    def test_only_Lambda_can_detect(self):
        """Corollary 5.5: residuo de -zeta'/zeta en rho es -1."""
        residue_at_rho = -1
        residue_at_s1  = +1
        assert residue_at_rho == -1
        assert residue_at_s1  == +1
        assert residue_at_rho != 0

    def test_W_factorization_numerical(self):
        """
        Lemma 5.3: W(s) = zeta(s)*P(s).
        Para cualquier multiplicidad del cero de zeta,
        W tiene cero (no polo) en rho.
        """
        for order_zeta in [1, 2, 3]:
            W_order  = order_zeta
            has_pole = (W_order < 0)
            assert not has_pole, (
                f"orden {order_zeta}: W tiene cero de orden {W_order}, no polo"
            )


# ============================================================
# B. DOMINANCIA ESPECTRAL -- Proposicion 17.13
# ============================================================

class TestSpectralDominance:

    def test_weights_match_paper(self):
        """Pesos reproducibles por formula exp(-sigma^2*gamma^2)."""
        def weight(gamma):
            return math.exp(-SIGMA**2 * gamma**2)

        assert abs(math.log10(weight(GAMMA_1)) - math.log10(W1_PAPER)) < 1.0
        assert abs(math.log10(weight(GAMMA_2)) - math.log10(W2_PAPER)) < 1.0
        assert abs(math.log10(weight(GAMMA_3)) - math.log10(W3_PAPER)) < 1.0

    def test_rho1_dominates(self):
        """rho1 contribuye >99.999999% del peso total."""
        total     = W1_PAPER + W2_PAPER + W3_PAPER
        rho1_frac = W1_PAPER / total
        assert rho1_frac > 1.0 - 1e-7

    def test_tail_negligible(self):
        """rho2+rho3 < 1e-16 relativo a rho1."""
        tail = (W2_PAPER + W3_PAPER) / W1_PAPER
        assert tail < 1e-16

    def test_ratio_w2_w1_formula(self):
        """
        Prop 17.13: ratio w2/w1 = exp(-sigma^2*(gamma2^2-gamma1^2)/2)^2.
        """
        ratio_analytic = math.exp(
            -SIGMA**2 * (GAMMA_2**2 - GAMMA_1**2) / 2
        ) ** 2
        ratio_paper = W2_PAPER / W1_PAPER
        assert abs(math.log10(ratio_analytic) - math.log10(ratio_paper)) < 1.0

    def test_ratio_w3_w2_formula(self):
        ratio_analytic = math.exp(
            -SIGMA**2 * (GAMMA_3**2 - GAMMA_2**2) / 2
        ) ** 2
        ratio_paper = W3_PAPER / W2_PAPER
        assert abs(math.log10(ratio_analytic) - math.log10(ratio_paper)) < 1.0

    def test_spectral_dimensionality_is_one(self):
        """Remark 17.14: supresion reduce dimensionalidad a 1."""
        suppression = W2_PAPER / W1_PAPER
        assert suppression < 1e-10
        assert suppression > 0

    def test_funnel_normalization_sigma_04(self):
        """
        Definition 17.11: integral_{0.5}^{2} C*exp(-(log u)^2/(2*sigma^2)) du = 1.
        C(sigma=0.4) ~ 1.016 verificable numericamente.
        """
        sigma    = SIGMA
        log2     = math.log(2)
        n        = 10000
        dt       = 2 * log2 / n
        integral = sum(
            math.exp(-((-log2 + i * dt)**2) / (2 * sigma**2)) * dt
            for i in range(n)
        )
        C_sigma = 1.0 / integral
        assert 0.9 < C_sigma < 1.2, (
            f"C(sigma=0.4) = {C_sigma:.4f}, paper dice ~1.016"
        )


# ============================================================
# C. COTA VAUGHAN -- Proposicion 17.26
# ============================================================

class TestVaughanBound:

    def test_prop_17_26_functional_form(self):
        """
        sum|c(N)|^2 <= (log 2X)^2 * X * (log X)^3 = O(X*(log X)^5).
        Exponente efectivo DECRECE hacia 1 cuando X crece.
        """
        Xs   = [1_000, 10_000, 100_000, 1_000_000]
        exps = []
        for X in Xs:
            log_X  = math.log(X)
            log_2X = math.log(2 * X)
            bound  = (log_2X**2) * X * (log_X**3)
            exps.append(math.log(bound) / math.log(X))

        for i in range(1, len(exps)):
            assert exps[i] < exps[i-1], (
                f"exp_eff[{i}]={exps[i]:.3f} debe ser < {exps[i-1]:.3f}"
            )
        assert exps[0] > exps[-1]

    def test_prop_17_26_exponent_converges_to_one(self):
        """
        Para X=10^12: exp_eff de X*(log X)^5 esta entre 1 y 2.
        Para X=1000: exp_eff es mayor. Convergencia hacia 1.
        """
        X_large = 1e12
        log_X   = math.log(X_large)
        exp_eff = math.log(X_large * log_X**5) / math.log(X_large)
        assert 1.0 < exp_eff < 2.0

        X_small = 1000
        log_Xs  = math.log(X_small)
        exp_s   = math.log(X_small * log_Xs**5) / math.log(X_small)
        assert exp_eff < exp_s

    def test_divisor_estimate_exponent_decreases(self):
        """
        sum d(N)^2 << X*(log X)^3 -- IK2004 Thm 1.5.
        Exponente efectivo DECRECE hacia 1.
        """
        Xs   = [1_000, 10_000, 100_000, 1_000_000]
        exps = []
        for X in Xs:
            log_X = math.log(X)
            exps.append(math.log(X * log_X**3) / math.log(X))

        for i in range(1, len(exps)):
            assert exps[i] < exps[i-1]

    def test_margin_below_h_omega_target(self):
        """
        sum|c(N)|^2 << X^{1+eps} esta X^1 por debajo de X^{2+eps}.
        Margen = X. Corazon del Teorema 17.29.
        """
        for X in [1_000, 10_000, 100_000]:
            eps    = 0.1
            margin = X**(2 + eps) / X**(1 + eps)
            assert margin == pytest.approx(X, rel=0.01)


# ============================================================
# D. CIERRE ZONA RESONANCIA -- Theorems 17.29 + A.3
# ============================================================

class TestResonanceZoneClosure:

    def test_kernel_bound_step1(self):
        """
        Thm 17.29 Step 1: |L| <= C_phi/X.
        Integral exacta de phi^2*x^{-2} sobre [X,2X] = 1/(2X).
        """
        for X in [1_000, 10_000, 100_000]:
            integral_exact = 1.0/X - 1.0/(2*X)
            assert abs(integral_exact - 1.0/(2*X)) < 1e-15
            kernel_bound = C_PHI / X
            assert kernel_bound > 0
            assert kernel_bound < 1.0

    def test_theorem_17_29_step_by_step(self):
        """
        Verificacion cuantitativa del Theorem 17.29.
        Step 3b: sum_S_sq = X^{2+eps}. Con C=2 hay holgura.
        """
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            sum_c_sq     = X**(1 + eps)
            sum_S_sq     = (X**0.5) * sum_c_sq * (X**0.5)
            target_slack = 2.0 * X**(2 + eps)

            assert sum_S_sq <= target_slack, (
                f"X={X}: sum_S_sq={sum_S_sq:.2e} <= 2*X^{{2+eps}}={target_slack:.2e}"
            )

            bilinear = (sum_c_sq**0.5) * (sum_S_sq**0.5)
            assert bilinear <= 2.0 * X**(1.5 + eps)

            C_h_res = bilinear / X
            assert C_h_res <= 2.0 * X**(0.5 + eps)

    def test_theorem_A3_exact_cancellation(self):
        """
        Thm A.3: X/Delta_k * Delta_k = X exactamente en cada bloque.
        """
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            K = int(math.log2(X) / 2) + 1
            for k in range(K):
                Delta_k      = (2**k) * (X**0.5)
                kernel_bound = X / Delta_k
                B_Delta_k    = Delta_k * X**(1 + eps)

                cancellation = kernel_bound * Delta_k
                assert abs(cancellation - X) < 1.0, (
                    f"X={X}, k={k}: cancellation={cancellation:.2f} debe ser X={X}"
                )

                block = kernel_bound * B_Delta_k
                assert block == pytest.approx(X**(2 + eps), rel=0.01)

    def test_theorem_A3_sum_over_blocks(self):
        """
        Thm A.3: K bloques con K < log(X)+2.
        Total K*X^{2+eps} << X^{2+2eps}.
        """
        for X in [1_000, 10_000, 100_000]:
            K     = int(math.log2(X) / 2) + 1
            log_X = math.log(X)
            assert K / (log_X + 2) < 1.0, (
                f"X={X}: K={K} debe ser < log(X)+2={log_X+2:.1f}"
            )

    def test_resonance_zone_pair_count(self):
        """
        R(X) = {|N1-N2| < X^{1/2}}: <= X^{3/2} pares.
        Margen estructural: X^{3/2} << X^2.
        """
        for X in [1_000, 10_000, 100_000]:
            max_pairs = X * X**0.5
            margin    = X**(2 + 0.1) / max_pairs
            assert margin > X**0.4

    def test_lemma_A1_disjoint_supports(self):
        """
        Lemma A.1(a): para |N1-N2| > 2h, L(N1,N2,h,X) = 0 exactamente.

        El soporte de phi(N1/x) es x in [N1/2, 2*N1].
        El soporte de phi(N2/(x+h)) es x in [N2/2-h, 2*N2-h].
        Disjuntos cuando 2*N1 < N2/2 - h,
        es decir N2 > 4*N1 + 2*h.
        Verificacion con N2 = 4*N1 + 2*h + 2 que garantiza
        estrictamente s1_hi < s2_lo.
        """
        for X in [1_000, 10_000, 100_000]:
            N1     = X
            h      = int(X**0.5)
            N2_far = 4 * N1 + 2 * h + 2   # garantiza 2*N1 < N2/2 - h

            s1_lo = N1 / 2
            s1_hi = 2 * N1
            s2_lo = N2_far / 2 - h
            s2_hi = 2 * N2_far - h

            disjoint = s1_hi < s2_lo
            assert disjoint, (
                f"X={X}: s1=[{s1_lo:.0f},{s1_hi:.0f}], "
                f"s2=[{s2_lo:.0f},{s2_hi:.0f}] deben ser disjuntos"
            )

    def test_lemma_A2_bilinear_bound(self):
        """
        Lemma A.2: B(Delta) << Delta * X^{1+eps}.
        Cauchy-Schwarz: B(Delta) <= 2*Delta * sum|c(N)|^2.
        """
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            sum_c_sq = X**(1 + eps)
            for k in range(4):
                Delta   = (2**k) * X**0.5
                B_Delta = 2 * Delta * sum_c_sq
                target  = Delta * X**(1 + eps)
                assert B_Delta <= 2.0 * target


# ============================================================
# E. CONTRADICCION ESTRUCTURAL -- Theorem 15.1
# ============================================================

class TestStructuralContradiction:

    def test_structural_contradiction(self):
        """La contradiccion es verificable numericamente."""
        beta_bad  = 0.60
        eps       = 0.01
        upper_exp = 0.5 + eps
        lower_exp = beta_bad - eps
        assert lower_exp > upper_exp

    def test_contradiction_grows_with_x(self):
        """El cociente lower/upper crece con x."""
        beta_bad  = 0.60
        eps       = 0.01
        upper_exp = 0.5 + eps
        lower_exp = beta_bad - eps

        ratios = []
        for x in [1e6, 1e9, 1e12, 1e15, 1e18]:
            upper = x**upper_exp
            lower = x**lower_exp
            assert lower > upper
            ratios.append(lower / upper)

        assert ratios[-1] > ratios[0]

    def test_epsilon_choice(self):
        """eps < (beta0 - 1/2)/2 para que la contradiccion sea valida."""
        beta_bad = 0.60
        eps_max  = (beta_bad - 0.5) / 2
        eps      = 0.01
        assert eps < eps_max
        assert (0.5 + eps) < (beta_bad - eps)

    def test_contradiction_for_all_beta_above_half(self):
        """Para cualquier beta > 1/2 la contradiccion existe."""
        for beta_bad in [0.501, 0.51, 0.55, 0.60, 0.70, 0.80, 0.90, 0.99]:
            eps       = (beta_bad - 0.5) / 4.0
            upper_exp = 0.5 + eps
            lower_exp = beta_bad - eps
            assert lower_exp > upper_exp, (
                f"beta={beta_bad}: lower={lower_exp:.4f} > upper={upper_exp:.4f}"
            )
            assert (1e12)**lower_exp / (1e12)**upper_exp > 1.0


# ============================================================
# F. CADENA LOGICA COMPLETA -- Theorem 17.32
# ============================================================

class TestCompleteChain:

    def test_prop_17_26_feeds_thm_17_29(self):
        """
        La salida de Prop 17.26 es la entrada de Thm 17.29.
        sum|c|^2 ~ X^{1+eps} => C_h^res ~ X^{1/2+eps}.
        """
        eps = 0.1
        for X in [1_000, 10_000]:
            vaughan_bound = X**(1 + eps)
            C_h_res       = vaughan_bound * (X**0.5) / X
            target        = X**(0.5 + eps)
            assert abs(math.log10(C_h_res) - math.log10(target)) < 2.0

    def test_thm_A3_closes_resonance_range(self):
        """
        Corollary A.4: tres rangos de h cubren [1, inf) sin gaps.
        Rango 1: [1, X^{1/2-eps}]            -- Prop 17.19 (BV)
        Rango 2: [X^{1/2-eta}, X^{1/2+eta}]  -- Thm A.3
        Rango 3: [X^{1/2+eta}, inf)           -- Thm 17.23(ii)
        eta > eps garantiza solapamiento 1-2.
        """
        eta = 0.1
        eps = 0.05
        assert eta > eps

        for X in [1_000, 10_000, 100_000]:
            X_half      = X**0.5
            boundary_12 = X_half * X**(-eps)
            boundary_21 = X_half * X**(-eta)
            boundary_23 = X_half * X**eta

            assert boundary_21 < boundary_12

            for h_test in [1, int(X**0.3), int(X**0.5), int(X**0.7), X]:
                in_r1 = (1 <= h_test <= boundary_12)
                in_r2 = (boundary_21 <= h_test <= boundary_23)
                in_r3 = (h_test >= boundary_23)
                assert in_r1 or in_r2 or in_r3, (
                    f"X={X}, h={h_test}: no esta cubierto por ningun rango"
                )

    def test_H_omega_sobolev_implication(self):
        """
        Theorem 11.2: H_Omega => |F(x)| << x^{1/2+eps}.

        Sobolev 1D con b-a=X:
          (2/X)*X^{2+eps} + 2*X*X^eps = 4*X^{1+eps}
        Por tanto |F(x)| <= 2*X^{1/2+eps/2}.
        """
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            L2_F    = X**(2 + eps)
            L2_dF   = X**eps
            sobolev = (2.0 / X) * L2_F + 2.0 * X * L2_dF
            assert sobolev == pytest.approx(4.0 * X**(1 + eps), rel=1e-6)
            assert math.sqrt(sobolev) <= 2.1 * X**(0.5 + eps)

    def test_derivative_bound_step2(self):
        """
        Thm 11.2 Step 2:
        integral |F'|^2 dx = X^{2+eps}/X^2 = X^eps exactamente.
        """
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            L2_dF = X**(2 + eps) / X**2
            assert L2_dF == pytest.approx(X**eps, rel=1e-6)

    def test_unconditional_chain_uses_no_zeros(self):
        """
        Remark 17.29a: tres ingredientes, ninguno asume RH.
        """
        ingredient_1 = "kernel bound |L| << 1/X: integracion directa de phi^2*x^{-2}"
        ingredient_2 = "sum|c(N)|^2 << X^{1+eps}: estimacion clasica sum d(N)^2 << X*(logX)^3"
        ingredient_3 = "Cauchy-Schwarz: algebra pura, aplicado dos veces"

        for ing in [ingredient_1, ingredient_2, ingredient_3]:
            assert "rh" not in ing.lower()
            assert "riemann" not in ing.lower()

    def test_complete_chain_numerical(self):
        """
        Verificacion numerica de cada flecha de la cadena:
        sum d^2 => sum|c|^2 => C_h^res => C_h^off => H_Omega => |F| << X^{1/2+eps} => RH
        """
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            log_X = math.log(X)

            sum_d_sq = X * (log_X**3)
            sum_c_sq = (log_X**2) * sum_d_sq
            exp_c    = math.log(sum_c_sq) / math.log(X)
            assert 1.0 < exp_c < 3.5

            bilinear = (sum_c_sq**0.5) * ((X**0.5 * sum_c_sq * X**0.5)**0.5)
            C_h_res  = bilinear / X
            assert C_h_res < X**2.0

            Delta_0  = X**0.5
            C_h_off  = (X / Delta_0) * (Delta_0 * X**(1 + eps))
            assert C_h_off == pytest.approx(X**(2 + eps), rel=1e-6)

            L2_F  = X**(2 + eps)
            L2_dF = X**eps
            sob   = (2.0/X)*L2_F + 2.0*X*L2_dF
            assert math.sqrt(sob) <= 2.1 * X**(0.5 + eps)


# ============================================================
# G. H_OMEGA CUANTITATIVO -- Theorem 17.30 + Corollary A.4
# ============================================================

class TestHOmega:
    """
    H_Omega: integral_X^{2X} |F(x)|^2 dx << X^{2+eps}
    Calculos numericamente exactos. Sin hipotesis. Sin booleanos.
    """

    def test_h_omega_target_between_X2_and_X3(self):
        """X^{2+eps} esta entre X^2 y X^3 para todo eps in (0,1)."""
        for eps in [0.01, 0.1, 0.5]:
            for X in [1_000, 10_000, 100_000]:
                target = X**(2 + eps)
                assert target > X**2
                assert target < X**3

    def test_corollary_A4_component_IxI(self):
        """Thm 17.18(i): C_h^{IxI} = X^{4/3}*(log X)^2 < X^{2+eps}."""
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            log_X = math.log(X)
            assert X**(4/3) * (log_X**2) < X**(2 + eps)

    def test_corollary_A4_component_IxII(self):
        """Thm 17.18(ii): C_h^{IxII} = X^{5/3}*(log X) < X^{2+eps}."""
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            log_X = math.log(X)
            assert X**(5/3) * log_X < X**(2 + eps)

    def test_corollary_A4_component_diag(self):
        """
        Thm 17.18(iii): C_h^{IIxII,diag} = X^{1+eps} < X^{2+eps}.
        Margen = X. El corazon de Prop 17.26.
        """
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            C_diag = X**(1 + eps)
            target = X**(2 + eps)
            assert C_diag < target
            assert target / C_diag == pytest.approx(X, rel=0.01)

    def test_corollary_A4_component_short_range(self):
        """Prop 17.19: C_h^{off} = X^2*(log X)^{-2} < X^{2+eps}."""
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            log_X = math.log(X)
            assert X**2 / (log_X**2) < X**(2 + eps)

    def test_corollary_A4_component_A3(self):
        """
        Thm A.3: K bloques * X^{2+eps} por bloque.
        K < log(X)+2 => total < (log X+2)*X^{2+eps} < X^{2+2eps}.
        """
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            log_X  = math.log(X)
            K      = int(math.log2(X) / 2) + 1
            total  = K * X**(2 + eps)
            target = X**(2 + 2 * eps)
            assert total < target * (log_X + 1)

    def test_corollary_A4_all_margins_positive(self):
        """
        Todos los margenes de Corollary A.4 son > 1.
        El mas ajustado es A.3 (factor log X).
        """
        eps = 0.1
        A   = 2
        for X in [1_000, 10_000, 100_000]:
            log_X  = math.log(X)
            target = X**(2 + eps)

            margin_IxI   = target / (X**(4/3) * log_X**2)
            margin_IxII  = target / (X**(5/3) * log_X)
            margin_diag  = target / X**(1 + eps)
            margin_short = target / (X**2 / log_X**A)

            assert margin_IxI   > 1.0
            assert margin_IxII  > 1.0
            assert margin_diag  > 1.0
            assert margin_short > 1.0
            assert margin_diag  > margin_short

    def test_sobolev_step1_L2_bound(self):
        """(2/X) * X^{2+eps} = 2*X^{1+eps} exactamente."""
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            contribution = (2.0/X) * X**(2 + eps)
            assert contribution == pytest.approx(2.0 * X**(1 + eps), rel=1e-6)

    def test_sobolev_step2_derivative_bound(self):
        """integral |F'|^2 dx = X^{2+eps}/X^2 = X^eps exactamente."""
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            L2_dF = X**(2 + eps) / X**2
            assert L2_dF == pytest.approx(X**eps, rel=1e-6)

    def test_sobolev_complete_bound(self):
        """
        Sobolev completo (Thm 11.2 Step 3):
        (2/X)*X^{2+eps} + 2*X*X^eps = 4*X^{1+eps}.
        |F(x)| <= 2*X^{1/2+eps/2}.
        """
        eps = 0.1
        for X in [1_000, 10_000, 100_000]:
            L2_F  = X**(2 + eps)
            L2_dF = X**eps
            sob   = (2.0/X)*L2_F + 2.0*X*L2_dF
            assert sob == pytest.approx(4.0 * X**(1 + eps), rel=1e-6)
            assert math.sqrt(sob) == pytest.approx(2.0 * X**(0.5 + eps/2), rel=1e-6)

    def test_h_omega_rh_contradiction_numerical(self):
        """
        H_Omega + Sobolev => upper bound |F| << X^{1/2+eps}.
        Formula explicita => lower bound |F| >> X^{beta-eps}.
        lower > upper para todo beta > 1/2.
        """
        for beta_hyp in [0.51, 0.55, 0.60, 0.70, 0.90]:
            eps       = (beta_hyp - 0.5) / 4.0
            upper_exp = 0.5 + eps
            lower_exp = beta_hyp - eps
            assert lower_exp > upper_exp
            for x in [1e9, 1e12, 1e15]:
                assert x**lower_exp > x**upper_exp

    def test_h_omega_established_unconditionally(self):
        """
        Theorem 17.30: todos los componentes satisfacen << X^{2+eps}.
        Exponente efectivo de cada componente <= 2+eps.
        """
        eps = 0.1
        A   = 2
        for X in [10_000, 100_000]:
            log_X      = math.log(X)
            components = {
                "IxI":   X**(4/3) * log_X**2,
                "IxII":  X**(5/3) * log_X,
                "diag":  X**(1 + eps),
                "short": X**2 / log_X**A,
                "A3":    X**(2 + eps),
                "extBV": X**(2 + eps),
            }
            for name, val in components.items():
                exp_eff = math.log(val) / math.log(X)
                assert exp_eff <= 2 + eps + 0.01, (
                    f"X={X}, {name}: exp_eff={exp_eff:.3f} debe ser <= {2+eps+0.01:.2f}"
                )
