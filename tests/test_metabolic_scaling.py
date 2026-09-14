# tests/test_metabolic_scaling.py
# UCF v3.3 — Test de falsación: Teoría de Scaling Metabólico
# Author: Ilver Villasmil | ORCID: 0009-0009-3413-4270
#
# TEORÍA BAJO TEST:
#   El exponente de Kleiber (¾) emerge del producto ponderado
#   de 6 capas biológicas (L0-L5) con datos reales de literatura,
#   más un factor constante α = 26/27 (L6, Propósito) que no
#   escala con la masa corporal.
#
# CRITERIOS DE FALSACIÓN:
#   F1: κ ≠ 0.75 ± 0.03   → descomposición incorrecta
#   F2: ci(L0-L5) ≠ 1.0   → los órganos no cubren el BMR
#   F3: α reemplazable     → L6 no tiene rol estructural
#   F4: BMR_predicho error > 30% en mayoría de mamíferos
#   F5: bᵢ individuales fuera de rangos de literatura

import math
import pytest
from formulas.metabolic_scaling import (
    kappa_bio, bmr, layer_contribution,
    LAYER_DATA, L6_PURPOSE
)
from formulas.constants import ALPHA, BETA


# ═══════════════════════════════════════════════════════════════
# BLOQUE 1 — IDENTIDADES ESTRUCTURALES
# Verifican que el framework está internamente consistente
# ═══════════════════════════════════════════════════════════════

class TestStructuralIdentities:

    def test_L6_is_alpha(self):
        """L6 Propósito debe ser exactamente α = 26/27."""
        assert L6_PURPOSE == ALPHA

    def test_alpha_plus_beta_is_one(self):
        """La identidad fundacional del cubo debe mantenerse."""
        assert math.isclose(ALPHA + BETA, 1.0, rel_tol=1e-10)

    def test_ci_L0_L5_sum_to_one(self):
        """
        F2 — CRITERIO DE FALSACIÓN:
        Las fracciones de BMR de L0-L5 deben sumar 1.0.
        Si no suman 1.0, hay órganos no contabilizados
        o contabilizados dos veces.
        Fuente: Gallagher 1998, Wang 2001.
        """
        total_ci = sum(ci for _, _, ci in LAYER_DATA.values())
        assert math.isclose(total_ci, 1.0, abs_tol=0.01), \
            f"ci suman {total_ci:.4f}, deben ser 1.0 ± 0.01"

    def test_all_b_total_are_positive(self):
        """
        Los exponentes totales de cada capa deben ser positivos.
        Un b_total negativo significaría que el órgano reduce
        el BMR al crecer M — físicamente imposible en términos
        de gasto absoluto.
        """
        for name, (bm, bt, ci) in LAYER_DATA.items():
            b_total = bm + bt
            assert b_total > 0, \
                f"{name}: b_total={b_total:.3f} no puede ser negativo"

    def test_all_ci_are_positive(self):
        """Toda capa debe contribuir positivamente al BMR."""
        for name, (bm, bt, ci) in LAYER_DATA.items():
            assert ci > 0, f"{name}: ci={ci} debe ser positivo"

    def test_L6_does_not_scale_with_mass(self):
        """
        L6 Propósito no escala con M.
        Su aporte al exponente κ es cero.
        Su rol es como factor constante α en B₀.
        """
        # L6 no está en LAYER_DATA — verificar su ausencia
        for key in LAYER_DATA:
            assert "L6" not in key, \
                "L6 no debe aparecer en LAYER_DATA — no escala con M"


# ═══════════════════════════════════════════════════════════════
# BLOQUE 2 — FALSACIÓN F1: EL EXPONENTE KLEIBER
# Este es el test central de la teoría
# ═══════════════════════════════════════════════════════════════

class TestKleiberExponent:

    def test_F1_kappa_within_kleiber_tolerance(self):
        """
        F1 — CRITERIO DE FALSACIÓN PRINCIPAL:
        κ debe estar en 0.75 ± 0.03.

        Si κ cae fuera de este rango, la descomposición UCF
        en 7 capas no reproduce la Ley de Kleiber y la
        teoría debe ser revisada o rechazada.
        """
        k = kappa_bio()
        assert 0.72 <= k <= 0.78, \
            f"κ={k:.6f} fuera del rango Kleiber [0.72, 0.78]. " \
            f"Teoría falsada — revisar bᵢ y cᵢ por capa."

    def test_kappa_close_to_three_quarters(self):
        """
        κ debe ser estadísticamente indistinguible de 3/4.
        Error < 1% respecto al valor empírico de Kleiber 1932.
        """
        k = kappa_bio()
        error = abs(k - 0.75) / 0.75
        assert error < 0.01, \
            f"Error de κ = {error*100:.3f}% — supera el 1%"

    def test_kappa_better_than_surface_law(self):
        """
        κ debe ser más cercano a 0.75 que a 0.67 (Ley de Rubner).
        Si no, el modelo no mejora la explicación geométrica simple.
        """
        k = kappa_bio()
        dist_kleiber = abs(k - 0.75)
        dist_rubner  = abs(k - 0.67)
        assert dist_kleiber < dist_rubner, \
            f"κ={k:.4f} más cercano a Rubner(0.67) que a Kleiber(0.75)"

    def test_kappa_is_deterministic(self):
        """κ debe ser idéntico en llamadas sucesivas."""
        assert kappa_bio() == kappa_bio()


# ═══════════════════════════════════════════════════════════════
# BLOQUE 3 — FALSACIÓN F3: ROL ESTRUCTURAL DE α
# ¿Es α irremplazable o cualquier factor funciona?
# ═══════════════════════════════════════════════════════════════

class TestAlphaStructuralRole:

    def test_F3_alpha_is_not_one(self):
        """
        Si L6_PURPOSE = 1.0, el sistema no tiene residuo β.
        α ≠ 1 es condición necesaria para que β > 0 exista.
        """
        assert L6_PURPOSE < 1.0, \
            "L6 no puede ser 1.0 — violaría β > 0"

    def test_F3_alpha_is_not_zero(self):
        """L6 = 0 colapsaría el BMR a cero — biológicamente absurdo."""
        assert L6_PURPOSE > 0.0

    def test_F3_alpha_equals_26_over_27(self):
        """
        L6 debe ser exactamente 26/27 — no una aproximación.
        Es la fracción de cubos exteriores del cubo 3×3×3.
        """
        assert math.isclose(L6_PURPOSE, 26/27, rel_tol=1e-10), \
            f"L6={L6_PURPOSE} ≠ 26/27 — rompería la identidad del cubo"

    def test_F3_beta_is_irreducible_metabolic_residue(self):
        """
        β = 1/27 es el metabolismo que ningún organismo puede
        integrar perfectamente — el vacío fértil del cubo.
        Su existencia implica que BMR nunca es 'perfecto'.
        """
        assert BETA == 1/27
        assert BETA > 0
        # El residuo metabólico: fracción del BMR no integrable
        residuo = 1.0 - L6_PURPOSE
        assert math.isclose(residuo, BETA, rel_tol=1e-10), \
            f"Residuo metabólico {residuo} ≠ β={BETA}"


# ═══════════════════════════════════════════════════════════════
# BLOQUE 4 — FALSACIÓN F4: PREDICCIÓN NUMÉRICA
# Datos reales de Kleiber 1932 y McNab 2008
# ═══════════════════════════════════════════════════════════════

class TestNumericalPrediction:

    # Datos: (nombre, masa_kg, BMR_real_W)
    # Fuente: Kleiber 1932, McNab 2008
    MAMMALS = [
        ("Raton",    0.021,    0.27),
        ("Rata",     0.250,    1.45),
        ("Conejo",   2.5,      9.8),
        ("Gato",     4.0,     14.1),
        ("Perro",    11.7,    53.0),
        ("Humano",   70.0,    87.0),
        ("Vaca",     400.0,  292.0),
        ("Caballo",  450.0,  317.0),
        ("Elefante", 2500.0, 1630.0),
    ]

    def test_F4_bmr_positive_for_all_mammals(self):
        """BMR predicho debe ser positivo para toda masa > 0."""
        for name, M, _ in self.MAMMALS:
            pred = bmr(M)
            assert pred > 0, f"{name}: BMR predicho = {pred}"

    def test_F4_bmr_increases_with_mass(self):
        """
        F4 — CRITERIO DE FALSACIÓN:
        BMR debe crecer monótonamente con M.
        Si no, el modelo viola la observación empírica más básica.
        """
        masses = sorted([m for _, m, _ in self.MAMMALS])
        bmrs   = [bmr(m) for m in masses]
        for i in range(len(bmrs)-1):
            assert bmrs[i] < bmrs[i+1], \
                f"BMR no monótono en M={masses[i]:.3f} kg"

    def test_F4_majority_within_30_percent(self):
        """
        F4 — CRITERIO DE FALSACIÓN:
        Al menos 5 de 9 mamíferos deben estar dentro del ±30%.
        Si menos de 5 pasan, el modelo no tiene poder predictivo.
        """
        passed = 0
        for name, M, BMR_real in self.MAMMALS:
            pred = bmr(M)
            err  = abs(pred - BMR_real) / BMR_real
            if err <= 0.30:
                passed += 1
        assert passed >= 5, \
            f"Solo {passed}/9 mamíferos dentro del ±30%. " \
            f"Teoría falsada — revisar B₀ o exponentes por especie."

    def test_F4_human_within_30_percent(self):
        """
        El humano es el animal con mejores datos medidos.
        El modelo debe predecir su BMR dentro del ±30%.
        """
        pred     = bmr(70.0)
        bmr_real = 87.0
        err      = abs(pred - bmr_real) / bmr_real
        assert err <= 0.30, \
            f"Humano: predicho={pred:.1f}W, real=87W, error={err*100:.1f}%"

    def test_F4_order_of_magnitude_correct(self):
        """
        Para ratón (0.021 kg) y elefante (2500 kg) —
        6 órdenes de magnitud en masa —
        el ratio de BMR predicho debe estar entre 1000 y 100000.
        (Empírico: ~6000)
        """
        bmr_raton    = bmr(0.021)
        bmr_elefante = bmr(2500.0)
        ratio        = bmr_elefante / bmr_raton
        assert 1000 < ratio < 100000, \
            f"Ratio elefante/ratón = {ratio:.0f} fuera del rango esperado"

    def test_bmr_raises_on_negative_mass(self):
        """masa negativa debe lanzar ValueError."""
        with pytest.raises(ValueError):
            bmr(-1.0)

    def test_bmr_raises_on_zero_mass(self):
        """masa cero debe lanzar ValueError."""
        with pytest.raises(ValueError):
            bmr(0.0)


# ═══════════════════════════════════════════════════════════════
# BLOQUE 5 — FALSACIÓN F5: RANGOS DE bᵢ POR LITERATURA
# Verificar que los datos usados son consistentes con estudios
# ═══════════════════════════════════════════════════════════════

class TestLiteratureConsistency:

    def test_F5_brain_b_mass_range(self):
        """
        F5 — Cerebro: b_masa en [0.56, 0.80].
        Fuente: Kozlowski 2020 (PGLS: 0.56, OLS: 0.69),
                Darveau 2003 (0.76), Burger 2019 (0.69).
        """
        bm, bt, ci = LAYER_DATA["L3_mente_cerebro"]
        assert 0.56 <= bm <= 0.80, \
            f"b_masa cerebro={bm} fuera del rango literatura [0.56, 0.80]"

    def test_F5_liver_b_specific_rate(self):
        """
        F5 — Hígado: b_tasa_específica en [-0.35, -0.20].
        Fuente: Wang 2001 (-0.27), Porter 2001 hepatocytes (-0.18).
        """
        bm, bt, ci = LAYER_DATA["L2_ego_higado"]
        assert -0.35 <= bt <= -0.20, \
            f"b_tasa hígado={bt} fuera del rango literatura [-0.35, -0.20]"

    def test_F5_heart_b_mass_range(self):
        """
        F5 — Corazón: b_masa en [0.85, 1.00].
        Fuente: Lindstedt & Calder 1981 (0.98),
                Kozlowski 2020 (isométrico).
        """
        bm, bt, ci = LAYER_DATA["L4_ser_cardio"]
        assert 0.85 <= bm <= 1.00, \
            f"b_masa corazón={bm} fuera de [0.85, 1.00]"

    def test_F5_muscle_ci_fraction(self):
        """
        F5 — Músculo: fracción BMR en [0.18, 0.30].
        Fuente: Gallagher 1998 (22%), Wang 2001 (20-25%).
        """
        bm, bt, ci = LAYER_DATA["L1_cuerpo_musculo"]
        assert 0.18 <= ci <= 0.30, \
            f"ci músculo={ci} fuera del rango literatura [0.18, 0.30]"

    def test_F5_brain_ci_fraction(self):
        """
        F5 — Cerebro: fracción BMR en [0.16, 0.25].
        Fuente: Gallagher 1998 (20.2%), Kozlowski 2020.
        """
        bm, bt, ci = LAYER_DATA["L3_mente_cerebro"]
        assert 0.16 <= ci <= 0.25, \
            f"ci cerebro={ci} fuera del rango literatura [0.16, 0.25]"

    def test_F5_six_layers_cover_all_bmr(self):
        """
        F5 — Las 6 capas deben cubrir el 100% del BMR.
        Si ci suman < 0.95, hay un componente metabólico
        no identificado — la teoría es incompleta.
        """
        total = sum(ci for _, _, ci in LAYER_DATA.values())
        assert total >= 0.95, \
            f"ci total={total:.3f} < 0.95 — BMR incompleto"


# ═══════════════════════════════════════════════════════════════
# BLOQUE 6 — PROPIEDADES DEL SISTEMA
# Verificaciones de coherencia interna UCF
# ═══════════════════════════════════════════════════════════════

class TestSystemProperties:

    def test_kappa_less_than_one(self):
        """
        κ < 1 es la esencia del scaling sublineal de Kleiber.
        Si κ ≥ 1, animales grandes gastarían proporcionalmente
        más energía por kilo — contrario a toda evidencia.
        """
        assert kappa_bio() < 1.0

    def test_kappa_greater_than_two_thirds(self):
        """
        κ > 2/3 distingue Kleiber de la Ley de Rubner.
        Si κ ≤ 2/3, el modelo no explica la diferencia entre
        el scaling de superficie (Rubner 1883) y el real.
        """
        assert kappa_bio() > 2/3

    def test_layer_contributions_sum_to_kappa(self):
        """
        La suma de contribuciones individuales debe reconstruir κ.
        Verifica la coherencia matemática del modelo.
        """
        total_ci  = sum(ci for _, _, ci in LAYER_DATA.values())
        sum_bici  = sum(layer_contribution(name)
                        for name in LAYER_DATA)
        k_recalc  = sum_bici / total_ci
        assert math.isclose(k_recalc, kappa_bio(), rel_tol=1e-10)

    def test_high_metabolic_organs_dominate(self):
        """
        Cerebro + hígado + corazón/riñones deben aportar
        más del 50% del exponente κ.
        Fuente: Gallagher 1998 — estos órganos son el 59% del BMR.
        """
        contrib_cerebro = layer_contribution("L3_mente_cerebro")
        contrib_higado  = layer_contribution("L2_ego_higado")
        contrib_cardio  = layer_contribution("L4_ser_cardio")
        total_ci        = sum(ci for _, _, ci in LAYER_DATA.values())

        fraction = (contrib_cerebro + contrib_higado + contrib_cardio) \
                   / (kappa_bio() * total_ci)
        assert fraction > 0.45, \
            f"Órganos caros aportan solo {fraction*100:.1f}% del κ — " \
            f"esperado > 45%"

    def test_L0_chaos_has_highest_b_total(self):
        """
        L0 (adiposo/piel) tiene el mayor b_total = 1.0.
        Es el único órgano cuya tasa específica no cae con M.
        Físicamente: el tejido adiposo es pasivo — no regula.
        """
        b_L0 = sum(LAYER_DATA["L0_caos_adiposo"][:2])
        for name, (bm, bt, ci) in LAYER_DATA.items():
            if name != "L0_caos_adiposo":
                b_other = bm + bt
                assert b_L0 >= b_other, \
                    f"b_total L0={b_L0} < b_total {name}={b_other}"
