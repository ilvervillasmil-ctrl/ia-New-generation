# formulas/metabolic_scaling.py
# UCF v3.3 — Corollary 8: Metabolic Scaling
# Author: Ilver Villasmil | ORCID: 0009-0009-3413-4270
# Investigador Independiente
#
# TEORÍA:
#   El metabolismo basal (BMR) de un mamífero es la coherencia
#   emergente de 7 subsistemas acoplados (L0-L6).
#   Seis escalan con la masa M. L6 (Propósito) no escala —
#   es el atractor estructural α = 26/27, constante para
#   todo organismo vivo independiente de su tamaño.
#
#   BMR(M) = B₀ · α · M^κ
#
#   donde κ = Σ bᵢ·cᵢ / Σcᵢ  emerge de datos reales de órganos
#
# FUENTES:
#   Wang et al. 2001 — J. Nutrition 131:2967
#   Gallagher et al. 1998 — MRI in vivo humans
#   Karbowski 2007 — brain metabolic scaling
#   Lindstedt & Calder 1981 — organ mass scaling

from formulas.constants import ALPHA, BETA


# ── CAPAS L0-L5: datos reales de literatura ──────────────────
# Cada capa: (b_masa, b_tasa_especifica, ci_fraccion_BMR)
#   b_total = b_masa + b_tasa_especifica
#   ci      = fracción del BMR total aportada por ese órgano

LAYER_DATA = {
    "L0_caos_adiposo":   (1.000,  0.000, 0.100),  # Gallagher 1998
    "L1_cuerpo_musculo": (1.000, -0.170, 0.220),  # Wang 2001
    "L2_ego_higado":     (0.870, -0.270, 0.216),  # Wang 2001
    "L3_mente_cerebro":  (0.760, -0.140, 0.202),  # Karbowski 2007
    "L4_ser_cardio":     (0.917, -0.101, 0.169),  # Wang 2001
    "L5_meta_residual":  (1.000, -0.170, 0.093),  # Wang 2001
    # L6 Propósito: b=0, factor α constante — no entra en κ
}

# ── CONSTANTE DE L6 ───────────────────────────────────────────
L6_PURPOSE = ALPHA   # 26/27 — coherencia máxima, invariante


def kappa_bio() -> float:
    """
    Exponente metabólico de Kleiber derivado desde UCF.

    κ = Σᵢ (bᵢ_masa + bᵢ_tasa) · cᵢ / Σcᵢ

    Donde la suma corre sobre L0-L5 únicamente.
    L6 entra como factor multiplicativo constante α en B₀.

    Returns:
        κ ≈ 0.7526  (Kleiber empírico: 0.75, error < 0.3%)
    """
    weighted_sum = 0.0
    total_ci     = 0.0
    for b_masa, b_tasa, ci in LAYER_DATA.values():
        b_total       = b_masa + b_tasa
        weighted_sum += b_total * ci
        total_ci     += ci
    return weighted_sum / total_ci


def bmr(mass_kg: float, b0: float = 4.6196) -> float:
    """
    Metabolismo basal predicho por UCF.

    BMR(M) = B₀ · α · M^κ

    Args:
        mass_kg: masa corporal en kg
        b0:      constante de escala calibrada (W·kg^-κ)
                 default: 4.6196 calibrado sobre 9 mamíferos
                 (Kleiber 1932, McNab 2008)

    Returns:
        BMR en Watts
    """
    if mass_kg <= 0:
        raise ValueError("mass_kg debe ser positivo")
    return b0 * L6_PURPOSE * (mass_kg ** kappa_bio())


def layer_contribution(layer_name: str) -> float:
    """
    Contribución de una capa al exponente global κ.

    Returns:
        bᵢ_total · cᵢ  (contribución ponderada al exponente)
    """
    if layer_name not in LAYER_DATA:
        raise KeyError(f"Capa desconocida: {layer_name}")
    b_masa, b_tasa, ci = LAYER_DATA[layer_name]
    return (b_masa + b_tasa) * ci
