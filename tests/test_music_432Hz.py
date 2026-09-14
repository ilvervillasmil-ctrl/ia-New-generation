import math

from core.engine import OmegaEngine
from formulas.coherence import CoherenceEngine
from formulas.constants import LAYER_FRICTION, NUM_LAYERS


# ============================================================
# TEST DE FALSACIÓN DEL ESTUDIO MUSICAL
# ============================================================
#
# Qué hace:
#   - usa el core real del repo
#   - adapta una frecuencia musical a layers_data
#   - compara coherencia estructural por la fórmula
#   - no usa datasets, audio ni conclusiones hardcodeadas
#
# Qué NO hace:
#   - no mete "432 gana" como expected arbitrario
#   - no usa valores externos como verdad
#   - no usa mocks
#
# Hipótesis del estudio:
#   menor distorsión estructural => menor fricción => mayor coherencia
#
# Nota técnica:
#   Para comparar frecuencias usamos c_beta crudo del CoherenceEngine.
#   El wrapper OmegaEngine se prueba aparte como contrato público.
# ============================================================


BODY_BASE_HZ = 12.0
REFERENCE_HZ = 432.0
STANDARD_HZ = 440.0


def structural_ratio(freq: float, base_hz: float = BODY_BASE_HZ) -> float:
    return freq / base_hz


def nearest_integer_multiple(freq: float, base_hz: float = BODY_BASE_HZ) -> int:
    return round(structural_ratio(freq, base_hz))


def structural_distortion(freq: float, base_hz: float = BODY_BASE_HZ) -> float:
    """
    Distorsión = distancia al múltiplo entero más cercano de la base estructural.
    0.0 = alineación perfecta
    """
    ratio = structural_ratio(freq, base_hz)
    return abs(ratio - round(ratio))


def structural_alignment(freq: float, base_hz: float = BODY_BASE_HZ) -> float:
    """
    Alineación en (0,1], derivada solo de la distorsión.
    """
    d = structural_distortion(freq, base_hz)
    return 1.0 / (1.0 + d)


def build_music_layers(freq: float, base_hz: float = BODY_BASE_HZ) -> list[dict]:
    """
    Adapter musical -> layers_data del core.

    Regla:
      - activación uniforme (la música existe)
      - la fricción estructural crece con la distorsión
      - L6 mantiene phi = 0.0 por contrato del engine
    """
    d = structural_distortion(freq, base_hz)

    layers = []
    for i in range(NUM_LAYERS):
        base_phi = LAYER_FRICTION[i]

        if i == NUM_LAYERS - 1:
            phi = 0.0
        else:
            phi = min(0.99, base_phi + d * 0.10)

        layers.append(
            {
                "L": 1.0,
                "phi": phi,
            }
        )

    return layers


def music_c_beta(freq: float, base_hz: float = BODY_BASE_HZ) -> float:
    """
    Coherencia estructural cruda, sin clamp del wrapper legacy.
    """
    layers = build_music_layers(freq, base_hz=base_hz)
    activations = [layer["L"] for layer in layers]
    frictions = [layer["phi"] for layer in layers]

    result = CoherenceEngine.compute_c_beta(
        activations=activations,
        frictions=frictions,
        delta_t=0.0,
        tau=1.0,
        novelty=5.0,
        sensitivity=5.0,
        external_coherences=None,
    )
    return result["c_beta"]


def music_coherence_wrapped(freq: float, base_hz: float = BODY_BASE_HZ) -> float:
    """
    Wrapper público del sistema.
    """
    engine = OmegaEngine()
    layers = build_music_layers(freq, base_hz=base_hz)
    return engine.compute_coherence(layers)


# ============================================================
# A. Propiedades matemáticas de la estructura musical (1–8)
# ============================================================

def test_01_reference_frequency_is_positive():
    assert REFERENCE_HZ > 0.0


def test_02_standard_frequency_is_positive():
    assert STANDARD_HZ > 0.0


def test_03_reference_is_exact_integer_multiple_of_body_base():
    ratio = structural_ratio(REFERENCE_HZ)
    assert math.isclose(ratio, round(ratio), rel_tol=0.0, abs_tol=1e-12)


def test_04_standard_is_not_exact_integer_multiple_of_body_base():
    ratio = structural_ratio(STANDARD_HZ)
    assert not math.isclose(ratio, round(ratio), rel_tol=0.0, abs_tol=1e-12)


def test_05_reference_distortion_is_zero():
    assert math.isclose(structural_distortion(REFERENCE_HZ), 0.0, rel_tol=0.0, abs_tol=1e-12)


def test_06_standard_distortion_is_positive():
    assert structural_distortion(STANDARD_HZ) > 0.0


def test_07_alignment_is_bounded():
    for f in [432.0, 433.0, 440.0, 441.0]:
        a = structural_alignment(f)
        assert 0.0 < a <= 1.0


def test_08_reference_alignment_exceeds_standard_alignment():
    assert structural_alignment(REFERENCE_HZ) > structural_alignment(STANDARD_HZ)


# ============================================================
# B. Adapter musical -> core del repo (9–14)
# ============================================================

def test_09_music_layer_adapter_returns_expected_number_of_layers():
    layers = build_music_layers(REFERENCE_HZ)
    assert len(layers) == NUM_LAYERS


def test_10_music_layer_adapter_keeps_l6_friction_zero():
    layers = build_music_layers(STANDARD_HZ)
    assert layers[NUM_LAYERS - 1]["phi"] == 0.0


def test_11_music_layer_adapter_uses_unit_activation_across_layers():
    layers = build_music_layers(REFERENCE_HZ)
    assert all(math.isclose(layer["L"], 1.0, rel_tol=0.0, abs_tol=1e-12) for layer in layers)


def test_12_music_layer_adapter_increases_friction_when_distortion_increases():
    layers_432 = build_music_layers(432.0)
    layers_440 = build_music_layers(440.0)

    for i in range(NUM_LAYERS - 1):
        assert layers_440[i]["phi"] >= layers_432[i]["phi"]


def test_13_music_layer_adapter_preserves_original_floor_friction_at_zero_distortion():
    layers = build_music_layers(432.0)
    for i in range(NUM_LAYERS - 1):
        assert math.isclose(layers[i]["phi"], LAYER_FRICTION[i], rel_tol=0.0, abs_tol=1e-12)


def test_14_music_layer_adapter_never_exceeds_engine_valid_friction_range():
    layers = build_music_layers(10_000.0)
    for layer in layers[:-1]:
        assert 0.0 <= layer["phi"] <= 0.99


# ============================================================
# C. Coherencia musical calculada por la fórmula real (15–20)
# ============================================================

def test_15_raw_music_c_beta_is_positive_for_reference():
    c = music_c_beta(REFERENCE_HZ)
    assert c > 0.0


def test_16_wrapped_music_coherence_is_clamped_to_unit_interval():
    for f in [REFERENCE_HZ, STANDARD_HZ, 433.0, 444.0]:
        c = music_coherence_wrapped(f)
        assert 0.0 <= c <= 1.0


def test_17_reference_frequency_has_higher_raw_coherence_than_standard_frequency():
    c_ref = music_c_beta(REFERENCE_HZ)
    c_std = music_c_beta(STANDARD_HZ)
    assert c_ref > c_std


def test_18_exact_integer_multiple_of_base_outperforms_nearby_perturbed_frequency():
    c_exact = music_c_beta(432.0)
    c_perturbed = music_c_beta(433.0)
    assert c_exact > c_perturbed


def test_19_coherence_decreases_monotonically_under_larger_structural_distortion():
    freqs = [432.0, 433.0, 436.0, 440.0]
    distortions = {f: structural_distortion(f) for f in freqs}
    coherences = {f: music_c_beta(f) for f in freqs}

    ranked = sorted(freqs, key=lambda f: distortions[f])

    for better, worse in zip(ranked, ranked[1:]):
        assert coherences[better] >= coherences[worse], (
            f"Esperado c({better}) >= c({worse}) "
            f"porque d({better})={distortions[better]} < d({worse})={distortions[worse]}"
        )


def test_20_another_exact_multiple_of_body_base_recovers_same_raw_coherence():
    c_432 = music_c_beta(432.0)
    c_444 = music_c_beta(444.0)

    assert math.isclose(structural_distortion(444.0), 0.0, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(c_444, c_432, rel_tol=0.0, abs_tol=1e-12)


# ============================================================
# D. Falsación interna del estudio (21–24)
# ============================================================

def test_21_reference_wins_by_formula_not_by_constant_label():
    candidates = [REFERENCE_HZ, STANDARD_HZ]
    scores = {f: music_c_beta(f) for f in candidates}
    winner = max(scores, key=scores.get)

    assert winner == min(candidates, key=structural_distortion)


def test_22_if_an_exact_multiple_exists_it_can_match_reference_without_special_case():
    candidate = BODY_BASE_HZ * 38.0
    c_candidate = music_c_beta(candidate)
    c_reference = music_c_beta(REFERENCE_HZ)

    assert math.isclose(structural_distortion(candidate), 0.0, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(c_candidate, c_reference, rel_tol=0.0, abs_tol=1e-12)


def test_23_frequency_with_lower_distortion_must_have_higher_or_equal_raw_coherence():
    freqs = [432.0, 433.0, 436.0, 440.0]
    ranked = sorted(freqs, key=structural_distortion)
    coherences = {f: music_c_beta(f) for f in freqs}

    for better, worse in zip(ranked, ranked[1:]):
        assert coherences[better] >= coherences[worse]


def test_24_wrapper_preserves_formula_order_for_non_saturated_pair():
    candidates = [REFERENCE_HZ, STANDARD_HZ]

    raw_scores = {f: music_c_beta(f) for f in candidates}
    wrapped_scores = {f: music_coherence_wrapped(f) for f in candidates}

    raw_winner = max(raw_scores, key=raw_scores.get)
    wrapped_winner = max(wrapped_scores, key=wrapped_scores.get)

    assert raw_winner == wrapped_winner

    for f in candidates:
        assert 0.0 <= wrapped_scores[f] <= 1.0
