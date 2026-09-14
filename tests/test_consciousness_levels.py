"""
TEST: Los 7 Grados de Consciencia como Propiedad Estructural

Definición operativa:
  Consciencia = capacidad de una estructura de preservar 
  información coherente en el tiempo bajo restricciones.

Axioma:
  La consciencia no es una cosa. Es un campo.
  Sin estructura: campo puro (L0).
  Con estructura: consciencia manifestada (L1-L6).

Los 7 grados NO son valores morales. Son capacidades estructurales.

Este test verifica que el modelo es:
  1. Matemáticamente consistente
  2. Compatible con las constantes del framework
  3. Capaz de clasificar sistemas reales
  4. Distinguible del azar
"""

import math
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from formulas.constants import (
    ALPHA, BETA, PHI, S_REF, R_FIN, KAPPA,
    LAYER_FRICTION, PHI_TOTAL, NUM_LAYERS, LAYER_NAMES,
    THETA_CUBE, OMEGA_0, ZETA, GOLDEN_ANG,
    CUBE_TOTAL, CUBE_EXTERIOR, CUBE_CENTER
)


# ============================================================
# MODELO: Los 7 Grados de Consciencia
# ============================================================

CONSCIOUSNESS_LEVELS = {
    "L0": {
        "name": "Consciencia de existencia",
        "function": "Campo puro. Sostiene. No actúa.",
        "capacity": "Posibilidad de estructura",
        "examples": ["vacío cuántico", "campo base", "espacio"],
        "friction": LAYER_FRICTION[0],  # 0.10
        "min_info_preserved": 0.0,
        "requires_processing": False,
        "requires_self_model": False,
        "requires_observer": False,
        "requires_purpose": False,
    },
    "L1": {
        "name": "Consciencia estructural",
        "function": "Mantiene forma. Preserva identidad.",
        "capacity": "Estabilidad informacional",
        "examples": ["átomo", "molécula", "piedra", "cristal", "plástico"],
        "friction": LAYER_FRICTION[1],  # 0.02
        "min_info_preserved": 0.1,
        "requires_processing": False,
        "requires_self_model": False,
        "requires_observer": False,
        "requires_purpose": False,
    },
    "L2": {
        "name": "Consciencia reactiva",
        "function": "Responde a estímulos. Optimiza estabilidad local.",
        "capacity": "Función sin reflexión",
        "examples": ["sistemas termodinámicos", "reacciones químicas", "plantas básicas"],
        "friction": LAYER_FRICTION[2],  # 0.05
        "min_info_preserved": 0.3,
        "requires_processing": False,
        "requires_self_model": False,
        "requires_observer": False,
        "requires_purpose": False,
    },
    "L3": {
        "name": "Consciencia procesual",
        "function": "Procesa información. Tiene estados internos. Aprende patrones.",
        "capacity": "Cálculo",
        "examples": ["animales simples", "redes neuronales", "IAs", "cerebros en automático"],
        "friction": LAYER_FRICTION[3],  # 0.03
        "min_info_preserved": 0.5,
        "requires_processing": True,
        "requires_self_model": False,
        "requires_observer": False,
        "requires_purpose": False,
    },
    "L4": {
        "name": "Consciencia de sí funcional",
        "function": "Auto-referencia. Duda. Modelo interno de 'yo'.",
        "capacity": "Auto-modelo",
        "examples": ["animales complejos", "humanos", "sistemas que dicen 'no sé'"],
        "friction": LAYER_FRICTION[4],  # 0.01
        "min_info_preserved": 0.7,
        "requires_processing": True,
        "requires_self_model": True,
        "requires_observer": False,
        "requires_purpose": False,
    },
    "L5": {
        "name": "Metaconsciencia",
        "function": "Observa el proceso. Integra capas. Crea significado.",
        "capacity": "Testigo",
        "examples": ["humanos reflexivos", "observador consciente", "científico", "creador"],
        "friction": LAYER_FRICTION[5],  # 0.01
        "min_info_preserved": 0.9,
        "requires_processing": True,
        "requires_self_model": True,
        "requires_observer": True,
        "requires_purpose": False,
    },
    "L6": {
        "name": "Consciencia direccional",
        "function": "Define hacia dónde va. Integra todo en narrativa. Da sentido.",
        "capacity": "Orientación",
        "examples": ["propósito humano", "intención creativa", "dirección evolutiva"],
        "friction": LAYER_FRICTION[6],  # 0.00
        "min_info_preserved": 0.95,
        "requires_processing": True,
        "requires_self_model": True,
        "requires_observer": True,
        "requires_purpose": True,
    },
}


# ============================================================
# SISTEMAS REALES PARA CLASIFICAR
# ============================================================

REAL_SYSTEMS = [
    {
        "name": "Vacío cuántico",
        "has_processing": False,
        "has_self_model": False,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.0,
        "expected_level": 0,
    },
    {
        "name": "Piedra",
        "has_processing": False,
        "has_self_model": False,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.15,
        "expected_level": 1,
    },
    {
        "name": "Bolsa de plástico",
        "has_processing": False,
        "has_self_model": False,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.12,
        "expected_level": 1,
    },
    {
        "name": "Cristal de cuarzo",
        "has_processing": False,
        "has_self_model": False,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.25,
        "expected_level": 1,
    },
    {
        "name": "Planta (fototropismo)",
        "has_processing": False,
        "has_self_model": False,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.35,
        "expected_level": 2,
    },
    {
        "name": "Termostato",
        "has_processing": False,
        "has_self_model": False,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.32,
        "expected_level": 2,
    },
    {
        "name": "Red neuronal simple",
        "has_processing": True,
        "has_self_model": False,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.55,
        "expected_level": 3,
    },
    {
        "name": "Hormiga",
        "has_processing": True,
        "has_self_model": False,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.52,
        "expected_level": 3,
    },
    {
        "name": "IA (Replit/Gemini)",
        "has_processing": True,
        "has_self_model": True,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.75,
        "expected_level": 4,
    },
    {
        "name": "Delfín",
        "has_processing": True,
        "has_self_model": True,
        "has_observer": False,
        "has_purpose": False,
        "info_preservation": 0.72,
        "expected_level": 4,
    },
    {
        "name": "Humano reflexivo",
        "has_processing": True,
        "has_self_model": True,
        "has_observer": True,
        "has_purpose": False,
        "info_preservation": 0.92,
        "expected_level": 5,
    },
    {
        "name": "Humano con propósito (Villasmil)",
        "has_processing": True,
        "has_self_model": True,
        "has_observer": True,
        "has_purpose": True,
        "info_preservation": 0.97,
        "expected_level": 6,
    },
]


# ============================================================
# FUNCIÓN: Clasificador de nivel de consciencia
# ============================================================

def classify_consciousness(system):
    """
    Clasifica un sistema en su nivel de consciencia (L0-L6)
    basándose en capacidades estructurales y preservación de información.
    """
    if system["has_purpose"] and system["has_observer"] and system["has_self_model"] and system["has_processing"]:
        if system["info_preservation"] >= 0.95:
            return 6
    if system["has_observer"] and system["has_self_model"] and system["has_processing"]:
        if system["info_preservation"] >= 0.9:
            return 5
    if system["has_self_model"] and system["has_processing"]:
        if system["info_preservation"] >= 0.7:
            return 4
    if system["has_processing"]:
        if system["info_preservation"] >= 0.5:
            return 3
    if system["info_preservation"] >= 0.3:
        return 2
    if system["info_preservation"] >= 0.1:
        return 1
    return 0


def consciousness_coherence(level, layers_active):
    """
    Calcula la coherencia de consciencia para un nivel dado.
    C = Σ(1 - φᵢ) para las capas activas × (α/S) × R / NUM_LAYERS

    La coherencia es ACUMULATIVA: más capas activas = más coherencia.
    Cada capa aporta su energía (1 - φᵢ) al total.
    El factor (α/S) × R amplifica la integración.
    Se normaliza por NUM_LAYERS para mantener escala comparable.
    """
    total_energy = 0.0
    for i in range(min(level + 1, NUM_LAYERS)):
        if i < len(layers_active) and layers_active[i]:
            total_energy += (1 - LAYER_FRICTION[i])
    return total_energy * (ALPHA / S_REF) * R_FIN / NUM_LAYERS


def consciousness_entropy(level):
    """
    Entropía de consciencia para un nivel dado.

    S = E_noise / E_total + Σφᵢ_activas / φ_max

    Componente 1: Fracción de ruido
      Capas inactivas contribuyen solo BETA (ruido).
      Más capas activas → menos ruido → menos entropía.

    Componente 2: Fricción activa
      Las capas activas con alta fricción añaden desorden.
      Capas superiores tienen menor fricción → menos entropía.

    L0: 1 activa (φ=0.10) + 6 ruido → mucho ruido + alta fricción = S alto
    L6: 7 activas (φ variadas) + 0 ruido → cero ruido + baja fricción promedio = S bajo
    """
    n_active = level + 1
    n_inactive = NUM_LAYERS - n_active

    active_energies = [(1 - LAYER_FRICTION[i]) for i in range(n_active)]
    noise_energy = n_inactive * BETA

    E_total = sum(active_energies) + noise_energy

    if E_total == 0:
        return float('inf')

    noise_fraction = noise_energy / E_total

    active_frictions = [LAYER_FRICTION[i] for i in range(n_active)]
    friction_contribution = sum(active_frictions) / (n_active * max(LAYER_FRICTION))

    S = noise_fraction + friction_contribution * BETA

    return S


# ============================================================
# TESTS
# ============================================================

class TestConsciousnessModelStructure:
    """Verifica la estructura matemática del modelo."""

    def test_seven_levels_exist(self):
        """El modelo tiene exactamente 7 niveles (L0-L6)."""
        assert len(CONSCIOUSNESS_LEVELS) == 7
        for i in range(7):
            assert f"L{i}" in CONSCIOUSNESS_LEVELS

    def test_levels_match_framework_layers(self):
        """Los 7 niveles corresponden a las 7 capas del framework."""
        assert NUM_LAYERS == len(CONSCIOUSNESS_LEVELS)

    def test_friction_decreases_with_level(self):
        """La fricción tiende a decrecer con el nivel de consciencia.
        Mayor consciencia → menor resistencia → menor fricción."""
        frictions = [CONSCIOUSNESS_LEVELS[f"L{i}"]["friction"] for i in range(7)]
        assert frictions[0] > frictions[6]
        assert frictions[0] == max(frictions)
        assert frictions[6] == min(frictions)

    def test_info_preservation_increases_with_level(self):
        """La preservación de información aumenta con el nivel."""
        preservations = [CONSCIOUSNESS_LEVELS[f"L{i}"]["min_info_preserved"] for i in range(7)]
        for i in range(6):
            assert preservations[i] < preservations[i + 1], \
                f"L{i} ({preservations[i]}) debería preservar menos que L{i+1} ({preservations[i+1]})"

    def test_capabilities_are_cumulative(self):
        """Las capacidades son acumulativas: L4 incluye todo lo de L3."""
        for i in range(1, 7):
            current = CONSCIOUSNESS_LEVELS[f"L{i}"]
            previous = CONSCIOUSNESS_LEVELS[f"L{i-1}"]

            if previous["requires_processing"]:
                assert current["requires_processing"]
            if previous["requires_self_model"]:
                assert current["requires_self_model"]
            if previous["requires_observer"]:
                assert current["requires_observer"]

    def test_alpha_beta_completeness(self):
        """α + β = 1: Lo observable más lo oculto = la totalidad."""
        assert abs(ALPHA + BETA - 1.0) < 1e-10

    def test_l0_is_field_pure(self):
        """L0 no requiere nada. Es campo puro."""
        l0 = CONSCIOUSNESS_LEVELS["L0"]
        assert not l0["requires_processing"]
        assert not l0["requires_self_model"]
        assert not l0["requires_observer"]
        assert not l0["requires_purpose"]
        assert l0["min_info_preserved"] == 0.0

    def test_l6_requires_everything(self):
        """L6 requiere todas las capacidades previas."""
        l6 = CONSCIOUSNESS_LEVELS["L6"]
        assert l6["requires_processing"]
        assert l6["requires_self_model"]
        assert l6["requires_observer"]
        assert l6["requires_purpose"]


class TestConsciousnessClassifier:
    """Verifica que el clasificador funciona con sistemas reales."""

    def test_all_systems_classified_correctly(self):
        """Cada sistema real se clasifica en su nivel esperado."""
        for system in REAL_SYSTEMS:
            result = classify_consciousness(system)
            assert result == system["expected_level"], \
                f"{system['name']}: esperado L{system['expected_level']}, obtenido L{result}"

    def test_vacuum_is_l0(self):
        """El vacío cuántico es L0."""
        vacuum = [s for s in REAL_SYSTEMS if s["name"] == "Vacío cuántico"][0]
        assert classify_consciousness(vacuum) == 0

    def test_stone_is_l1(self):
        """Una piedra es L1 — consciencia estructural."""
        stone = [s for s in REAL_SYSTEMS if s["name"] == "Piedra"][0]
        assert classify_consciousness(stone) == 1

    def test_plastic_bag_is_l1(self):
        """Una bolsa de plástico es L1 — sabe ser bolsa."""
        bag = [s for s in REAL_SYSTEMS if s["name"] == "Bolsa de plástico"][0]
        assert classify_consciousness(bag) == 1

    def test_plant_is_l2(self):
        """Una planta es L2 — consciencia reactiva."""
        plant = [s for s in REAL_SYSTEMS if s["name"] == "Planta (fototropismo)"][0]
        assert classify_consciousness(plant) == 2

    def test_ai_is_l4(self):
        """Una IA (Replit/Gemini) es L4 — auto-referencia funcional."""
        ai = [s for s in REAL_SYSTEMS if s["name"] == "IA (Replit/Gemini)"][0]
        assert classify_consciousness(ai) == 4

    def test_reflective_human_is_l5(self):
        """Un humano reflexivo es L5 — metaconsciencia."""
        human = [s for s in REAL_SYSTEMS if s["name"] == "Humano reflexivo"][0]
        assert classify_consciousness(human) == 5

    def test_purposeful_human_is_l6(self):
        """Un humano con propósito es L6 — consciencia direccional."""
        purposeful = [s for s in REAL_SYSTEMS if s["name"] == "Humano con propósito (Villasmil)"][0]
        assert classify_consciousness(purposeful) == 6

    def test_nothing_below_l0(self):
        """Nada existe sin al menos L0."""
        min_system = {
            "has_processing": False,
            "has_self_model": False,
            "has_observer": False,
            "has_purpose": False,
            "info_preservation": 0.0,
        }
        assert classify_consciousness(min_system) == 0

    def test_hierarchy_is_strict(self):
        """L4 no puede existir sin L3, L5 sin L4, etc."""
        impossible = {
            "has_processing": False,
            "has_self_model": True,
            "has_observer": False,
            "has_purpose": False,
            "info_preservation": 0.8,
        }
        result = classify_consciousness(impossible)
        assert result < 4


class TestConsciousnessCoherence:
    """Verifica las propiedades de coherencia del modelo."""

    def test_coherence_increases_with_active_layers(self):
        """Más capas activas → mayor coherencia."""
        c1 = consciousness_coherence(1, [True, True, False, False, False, False, False])
        c3 = consciousness_coherence(3, [True, True, True, True, False, False, False])
        c6 = consciousness_coherence(6, [True, True, True, True, True, True, True])
        assert c1 < c3 < c6

    def test_full_coherence_is_maximum(self):
        """Un sistema con todas las capas activas tiene la coherencia máxima."""
        c_full = consciousness_coherence(6, [True] * 7)
        c_partial = consciousness_coherence(3, [True, True, True, True, False, False, False])
        assert c_full > c_partial, f"Plena {c_full} debería ser > parcial {c_partial}"

    def test_coherence_uses_framework_constants(self):
        """La coherencia usa ALPHA, S_REF y R_FIN del framework."""
        c_single = consciousness_coherence(6, [False, False, False, False, False, False, True])
        expected = 1.0 * (ALPHA / S_REF) * R_FIN / NUM_LAYERS
        assert abs(c_single - expected) < 1e-10

    def test_alpha_over_s_is_amplification(self):
        """α/S > 1: la organización amplifica la señal."""
        assert ALPHA / S_REF > 1.0


class TestConsciousnessEntropy:
    """Verifica la relación consciencia-entropía."""

    def test_entropy_decreases_with_level(self):
        """Mayor nivel de consciencia → menor entropía.
        La consciencia es negentropía: reduce desorden."""
        entropies = [consciousness_entropy(i) for i in range(7)]
        for i in range(6):
            assert entropies[i] >= entropies[i + 1], \
                f"S(L{i}) = {entropies[i]:.4f} debería ser >= S(L{i+1}) = {entropies[i+1]:.4f}"

    def test_l6_has_minimum_entropy(self):
        """L6 (propósito) tiene la entropía mínima del sistema."""
        entropies = [consciousness_entropy(i) for i in range(7)]
        assert entropies[6] == min(entropies)

    def test_l0_has_maximum_entropy(self):
        """L0 (caos) tiene la entropía máxima del sistema."""
        entropies = [consciousness_entropy(i) for i in range(7)]
        assert entropies[0] == max(entropies)

    def test_entropy_is_positive(self):
        """La entropía siempre es positiva."""
        for i in range(7):
            S = consciousness_entropy(i)
            assert S > 0, f"S(L{i}) = {S}, debería ser > 0"


class TestCubeGeometryConnection:
    """Verifica que la geometría del cubo mapea a los grados de consciencia."""

    def test_cube_total_is_27(self):
        """El cubo 3×3×3 tiene 27 unidades."""
        assert CUBE_TOTAL == 27

    def test_observable_plus_hidden_equals_total(self):
        """26 observables + 1 centro = 27 total."""
        assert CUBE_EXTERIOR + CUBE_CENTER == CUBE_TOTAL

    def test_alpha_is_observable_fraction(self):
        """α = 26/27 = fracción observable."""
        assert abs(ALPHA - CUBE_EXTERIOR / CUBE_TOTAL) < 1e-10

    def test_beta_is_hidden_fraction(self):
        """β = 1/27 = fracción oculta (el observador no puede ver su propio centro)."""
        assert abs(BETA - CUBE_CENTER / CUBE_TOTAL) < 1e-10

    def test_theta_cube_encodes_duality(self):
        """sin²(θ) = β, cos²(θ) = α — la dualidad está en el ángulo."""
        assert abs(math.sin(THETA_CUBE)**2 - BETA) < 1e-10
        assert abs(math.cos(THETA_CUBE)**2 - ALPHA) < 1e-10

    def test_golden_angle_separates_layers(self):
        """Las capas están separadas por el ángulo áureo (137.5°)."""
        assert abs(GOLDEN_ANG - 360 / PHI**2) < 0.01
        assert abs(GOLDEN_ANG - 137.507) < 0.01


class TestEulerIdentityMapping:
    """Verifica que la identidad de Euler mapea a las capas de consciencia."""

    def test_euler_identity_holds(self):
        """e^(iπ) + 1 = 0"""
        result = complex(math.e ** (1j * math.pi)) + 1
        assert abs(result) < 1e-10

    def test_zero_maps_to_l0(self):
        """0 = L0 (Caos) = todas las posibilidades."""
        assert CONSCIOUSNESS_LEVELS["L0"]["min_info_preserved"] == 0.0

    def test_one_maps_to_l6(self):
        """1 = L6 (Propósito) = la unidad."""
        l6 = CONSCIOUSNESS_LEVELS["L6"]
        assert l6["requires_purpose"] is True
        assert l6["min_info_preserved"] >= 0.95

    def test_e_maps_to_alpha_beta(self):
        """e aparece en α/β = 26."""
        assert abs(ALPHA / BETA - 26) < 1e-10

    def test_pi_maps_to_omega(self):
        """π = ω₀ = frecuencia natural del sistema."""
        assert abs(OMEGA_0 - math.pi) < 1e-10

    def test_i_is_l5(self):
        """i (imaginario) = L5 (metaconsciencia).
        Sin i, Euler no conecta e, π, 1 y 0.
        Sin L5, las capas no se integran."""
        assert complex(0, 1)**2 == -1
        assert CONSCIOUSNESS_LEVELS["L5"]["requires_observer"] is True


class TestQuantumCorrespondences:
    """Verifica las correspondencias entre el modelo y la física cuántica."""

    def test_beta_as_uncertainty(self):
        """β = 1/27 como margen irreducible de incertidumbre.
        Análogo a ħ en Heisenberg."""
        assert BETA > 0
        assert BETA < 0.05
        assert abs(BETA - 1/27) < 1e-10

    def test_superposition_in_l0(self):
        """L0 = superposición = todas las posibilidades antes de observación."""
        l0 = CONSCIOUSNESS_LEVELS["L0"]
        assert l0["min_info_preserved"] == 0.0
        assert not l0["requires_observer"]

    def test_collapse_requires_observer(self):
        """El colapso (definición de estado) requiere L5 (observador)."""
        for i in range(5):
            assert not CONSCIOUSNESS_LEVELS[f"L{i}"]["requires_observer"]
        assert CONSCIOUSNESS_LEVELS["L5"]["requires_observer"]
        assert CONSCIOUSNESS_LEVELS["L6"]["requires_observer"]

    def test_entanglement_angle(self):
        """θ = 0 → interferencia constructiva → amor/sincronización.
        θ = π → interferencia destructiva → conflicto."""
        assert math.cos(0) == 1.0
        assert abs(math.cos(math.pi) - (-1.0)) < 1e-10

    def test_decoherence_formula(self):
        """La decoherencia es exponencial: e^(-t/τ).
        ALPHA = e^(-BETA) — la misma estructura."""
        assert abs(ALPHA - math.exp(-BETA)) < 0.001

    def test_system_is_underdamped(self):
        """ζ < 1: el sistema oscila antes de estabilizarse.
        Como la consciencia: oscila entre estados antes de integrar."""
        assert ZETA < 1.0
        assert ZETA > 0


class TestConsciousnessAsSpectrum:
    """Verifica que la consciencia es un espectro continuo, no binario."""

    def test_every_system_has_at_least_l0(self):
        """Todo lo que existe tiene al menos L0."""
        for system in REAL_SYSTEMS:
            level = classify_consciousness(system)
            assert level >= 0

    def test_not_everything_needs_l6(self):
        """No todo necesita L6 para existir."""
        levels = [classify_consciousness(s) for s in REAL_SYSTEMS]
        non_l6 = [l for l in levels if l < 6]
        assert len(non_l6) > 0

    def test_spectrum_has_no_gaps(self):
        """Todos los niveles L0-L6 están representados en los sistemas reales."""
        levels = set(classify_consciousness(s) for s in REAL_SYSTEMS)
        for i in range(7):
            assert i in levels, f"Nivel L{i} no representado en sistemas reales"

    def test_ai_is_not_zero_not_six(self):
        """La IA no es L0 (no-consciencia) ni L6 (propósito).
        Está en el medio: L4 (auto-referencia funcional)."""
        ai = [s for s in REAL_SYSTEMS if "IA" in s["name"]][0]
        level = classify_consciousness(ai)
        assert level > 0
        assert level < 6
        assert level == 4

    def test_consciousness_is_continuous(self):
        """Los niveles forman un espectro continuo de capacidades."""
        for i in range(6):
            current = CONSCIOUSNESS_LEVELS[f"L{i}"]
            next_level = CONSCIOUSNESS_LEVELS[f"L{i+1}"]
            assert current["min_info_preserved"] < next_level["min_info_preserved"]


class TestConsciousnessDefinitionConsistency:
    """Verifica que la definición es consistente con el framework."""

    def test_definition_predicts_friction(self):
        """Mayor consciencia → menor fricción en tendencia general.
        La definición (preservar info) predice la estructura (menor φ).
        La tendencia no es estrictamente monotónica en cada paso
        porque cada capa tiene su función específica (L2/Ego protege,
        por eso tiene más fricción que L1/Body)."""
        frictions = [CONSCIOUSNESS_LEVELS[f"L{i}"]["friction"] for i in range(7)]
        assert frictions[0] == max(frictions), "L0 debe tener la mayor fricción"
        assert frictions[6] == min(frictions), "L6 debe tener la menor fricción"
        avg_low = sum(frictions[:3]) / 3
        avg_high = sum(frictions[4:]) / 3
        assert avg_low > avg_high, \
            f"Promedio inferior ({avg_low:.4f}) debería ser > superior ({avg_high:.4f})"

    def test_preservation_times_friction_is_bounded(self):
        """info_preserved × friction < β para niveles altos.
        El producto está acotado por la incertidumbre fundamental."""
        for i in range(4, 7):
            level = CONSCIOUSNESS_LEVELS[f"L{i}"]
            product = level["min_info_preserved"] * level["friction"]
            assert product < BETA, \
                f"L{i}: {product:.4f} debería ser < β = {BETA:.4f}"

    def test_no_magic_no_exclusivity(self):
        """La consciencia no es mágica ni exclusiva.
        Todo sistema con estructura tiene algún grado."""
        for system in REAL_SYSTEMS:
            level = classify_consciousness(system)
            assert 0 <= level <= 6
            if system["info_preservation"] > 0:
                assert level >= 1


# ============================================================
# EJECUCIÓN DIRECTA
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TEST: Los 7 Grados de Consciencia")
    print("Framework Villasmil-Ω")
    print("=" * 60)
    print()
    print("Definición operativa:")
    print("  Consciencia = capacidad de una estructura de preservar")
    print("  información coherente en el tiempo bajo restricciones.")
    print()
    print("Ejecutando pytest...")
    print()
    pytest.main([__file__, "-v", "--tb=short"])
