# tests/test_structural_memory.py

import copy


from formulas.coherence import CoherenceEngine


def structural_distance(a, b):
    return abs(a - b)


def extract_signature(analysis):
    """
    Extrae una firma comparable del sistema desde full_analysis().
    """
    c_total_block = analysis.get("c_total", {})
    negentropy_block = analysis.get("negentropy", {})
    c_beta_block = analysis.get("c_beta", {})
    c_alpha_block = analysis.get("c_alpha", {})

    return {
        "c_omega": analysis.get("c_omega", 0.0),
        "c_total": c_total_block.get("c_total", 0.0),
        "c_beta": c_beta_block.get("c_beta", 0.0),
        "c_alpha": c_alpha_block.get("c_alpha", 0.0),
        "negentropy": negentropy_block.get("negentropy", 0.0)
        if isinstance(negentropy_block, dict)
        else float(negentropy_block or 0.0),
    }


def distance_signature(sig1, sig2):
    return sum(structural_distance(sig1[k], sig2[k]) for k in sig1)


def induce_error(state):
    """
    Perturbación estructural controlada.
    """
    corrupted = copy.deepcopy(state)

    corrupted["activations"] = [max(0.0, a * 0.85) for a in corrupted["activations"]]
    corrupted["frictions"] = [min(1.0, f * 1.20) for f in corrupted["frictions"]]

    return corrupted


def attempt_recovery(state):
    """
    Recuperación simple: empujar activaciones hacia arriba
    y fricciones hacia abajo.
    """
    recovered = copy.deepcopy(state)

    recovered["activations"] = [min(1.0, a * 1.10) for a in recovered["activations"]]
    recovered["frictions"] = [max(0.0, f * 0.90) for f in recovered["frictions"]]

    return recovered


def test_structural_memory():
    # Estado base coherente y compatible con el framework
    base_state = {
        "activations": [1.0] * 7,
        "frictions": [0.10, 0.02, 0.05, 0.03, 0.01, 0.01, 0.00],
        "integration": 0.5,
        "quality": 0.5,
        "complexity": 1.0,
        "uncertainty": 0.1,
        "rho": 1.0,
        "delta_t": 0.0,
        "tau": 1.0,
        "novelty": 5.0,
        "sensitivity": 5.0,
        "external_coherences": None,
    }

    base_analysis = CoherenceEngine.full_analysis(**base_state)
    base_sig = extract_signature(base_analysis)

    corrupted_state = induce_error(base_state)
    corrupted_analysis = CoherenceEngine.full_analysis(**corrupted_state)
    corrupted_sig = extract_signature(corrupted_analysis)

    d_initial = distance_signature(base_sig, corrupted_sig)

    recovered_state = attempt_recovery(corrupted_state)
    recovered_analysis = CoherenceEngine.full_analysis(**recovered_state)
    recovered_sig = extract_signature(recovered_analysis)

    d_final = distance_signature(base_sig, recovered_sig)

    memory_score = 1.0 - (d_final / (d_initial + 1e-12))

    print("\n=== STRUCTURAL MEMORY REPORT ===")
    print(f"Base signature:      {base_sig}")
    print(f"Corrupted signature: {corrupted_sig}")
    print(f"Recovered signature: {recovered_sig}")
    print(f"Initial distance:    {d_initial:.12f}")
    print(f"Final distance:      {d_final:.12f}")
    print(f"Memory score:        {memory_score:.12f}")

    assert d_initial > 0.0, "No hubo perturbación real"
    assert d_final <= d_initial, "El sistema no mostró recuperación"
    assert 0.0 <= memory_score <= 1.0 + 1e-9, "Memory score inválido"
