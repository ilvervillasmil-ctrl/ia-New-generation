"""
Universal Coherence Framework v3.2 - Tension Module
Detects latent incompatibilities between premises before
they become visible errors.

Author: Ilver Villasmil
Framework: Villasmil-Ω
"""

from .constants import (
    BETA, ALPHA,
    TENSION_WEIGHTS,
    TENSION_DIRECT,
    TENSION_PARTIAL,
    TENSION_AMBIGUOUS,
    TENSION_COMPATIBLE,
)


def theta_tension(premises: list) -> float:
    """
    Θ(C) — global tension between system premises.

    Detects latent incompatibilities BEFORE they become errors.
    This is the difference between measuring if a bridge holds
    today vs detecting microfractures that will fail tomorrow.

    Tension levels:
        1.0 — direct contradiction  (p1 and p2 are mutually exclusive)
        0.5 — partial incompatibility
        0.2 — structural ambiguity
        0.0 — compatible premises

    Args:
        premises: list of (value1, value2, relation_type) tuples
                  relation_type: 'equal', 'opposite', 'partial', 'ambiguous'

    Returns:
        float: tension in [0.0, 1.0]
    """
    if not premises:
        return TENSION_COMPATIBLE

    max_tension = 0.0

    for item in premises:
        if len(item) < 3:
            continue

        v1, v2, relation = item[0], item[1], item[2]

        if relation == "equal":
            if abs(v1 - v2) < BETA:
                t = TENSION_COMPATIBLE
            elif abs(v1 - v2) < ALPHA:
                t = TENSION_AMBIGUOUS
            else:
                t = TENSION_PARTIAL
        elif relation == "opposite":
            t = TENSION_DIRECT
        elif relation == "partial":
            t = TENSION_PARTIAL
        elif relation == "ambiguous":
            t = TENSION_AMBIGUOUS
        else:
            t = TENSION_COMPATIBLE

        if t > max_tension:
            max_tension = t

    return min(max_tension, 1.0)


def relevance_R(
    MC: float,
    CI: float,
    phi_noise: float,
    delta: float,
    theta_c: float,
    P: float,
    N: float,
) -> float:
    """
    R(C) — relevance function with tension penalty.

    R(C) = w1·MC + w2·CI + w3·(1-φ) + w4·Δ - w5·Θ(C) + w6·P·N

    The -w5·Θ(C) term is the first NEGATIVE structural term
    in the framework: an explicit penalty for internal incoherence,
    not just a modulator that reduces.

    Weights (calibrated UCF v2.6):
        MC    (conceptual coherence)  = 0.30
        CI    (internal coherence)    = 0.25
        noise (structural noise)      = 0.20
        delta (semantic precision)    = 0.10
        theta (tension — NEGATIVE)    = 0.05
        P·N   (purpose × neutrality)  = 0.10

    Args:
        MC:        conceptual coherence [0,1]
        CI:        internal coherence [0,1]
        phi_noise: structural noise level [0,1]
        delta:     semantic precision [0,1]
        theta_c:   tension Θ(C) from theta_tension() [0,1]
        P:         purpose alignment [0,1]
        N:         neutrality [0,1]

    Returns:
        float: relevance R(C) clamped to [0.0, 1.0]
    """
    w = TENSION_WEIGHTS

    R = (
        w["MC"]      * MC
        + w["CI"]      * CI
        + w["noise"]   * (1.0 - phi_noise)
        + w["delta"]   * delta
        - w["tension"] * theta_c        # NEGATIVE — penalty
        + w["purpose"] * (P * N)
    )

    return min(1.0, max(0.0, R))


def tension_level(theta_c: float) -> str:
    """
    Returns a human-readable tension level label.

    Args:
        theta_c: tension value from theta_tension()

    Returns:
        str: 'COMPATIBLE' | 'AMBIGUOUS' | 'PARTIAL' | 'DIRECT'
    """
    if theta_c <= TENSION_COMPATIBLE:
        return "COMPATIBLE"
    elif theta_c <= TENSION_AMBIGUOUS:
        return "AMBIGUOUS"
    elif theta_c < TENSION_DIRECT:
        return "PARTIAL"
    else:
        return "DIRECT"


def is_coherent(MC: float, CI: float, theta_c: float) -> bool:
    """
    Quick coherence check: high MC and CI with low tension.

    A system can be internally coherent but have high tension
    between premises — this detects that case.

    Args:
        MC:      conceptual coherence
        CI:      internal coherence
        theta_c: tension Θ(C)

    Returns:
        bool: True if system passes coherence + tension check
    """
    return MC >= ALPHA and CI >= ALPHA and theta_c < TENSION_PARTIAL
