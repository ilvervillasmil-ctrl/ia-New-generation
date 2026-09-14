# tests/test_dream_coherence.py

from dataclasses import dataclass
from typing import List


@dataclass
class DreamNode:
    """
    Nodo de un sueño: representa una escena o elemento estructural.
    - density (δ_i): cuánta información relevante contiene el nodo.
    - weight (α_i): importancia relativa del nodo en la secuencia.
    - dispersion (σ_i): dispersión / ambigüedad en torno al nodo.
    - noise (R_i): ruido asociado al nodo o a su transición.
    """
    name: str
    density: float      # δ_i
    weight: float       # α_i
    dispersion: float   # σ_i
    noise: float = 0.0  # R_i


def node_coherence(node: DreamNode) -> float:
    """
    Coherencia local de un nodo de sueño.

    C_i = (δ_i * α_i) / σ_i

    Se protege la división con un mínimo para evitar división por cero.
    """
    denom = max(node.dispersion, 1e-9)
    return (node.density * node.weight) / denom


def dream_coherence(nodes: List[DreamNode], alpha_noise: float = 1.0) -> float:
    """
    Coherencia total de un sueño como suma de la contribución de cada nodo,
    penalizada por el ruido asociado.

    C_total = Σ C_i / (1 + α * R_i)
    """
    total = 0.0
    for node in nodes:
        c_i = node_coherence(node)
        total += c_i / (1.0 + alpha_noise * node.noise)
    return total


def test_dream_coherence_interpretation():
    """
    Este test implementa el protocolo básico de decodificación estructural de un sueño.

    Idea:
    - Se construye una interpretación "alineada" del sueño, donde los nodos
      y sus pesos reflejan una lectura coherente de la secuencia
      (por ejemplo: presión → refugio → ilusión → tránsito → ruptura → revelación).
    - Se construye una interpretación "forzada", donde los mismos nodos se tratan
      como símbolos aislados, con más ruido y menor peso estructural.
    - La métrica debe dar C_total(alineada) > C_total(forzada).

    No buscamos aquí valores absolutos, sino verificar que la métrica es sensible
    a la diferencia entre una lectura estructural coherente y una lectura ruidosa.
    """

    # Interpretación alineada (estructura global coherente)
    aligned_nodes = [
        DreamNode(
            name="desert_run",
            density=0.9,   # escena rica en información (presión/huida)
            weight=1.0,    # muy relevante para el inicio de la narrativa
            dispersion=0.3,
            noise=0.1,
        ),
        DreamNode(
            name="pyramid_refuge",
            density=0.8,   # refugio arcaico coherente con la huida
            weight=1.0,
            dispersion=0.4,
            noise=0.1,
        ),
        DreamNode(
            name="white_house_island",
            density=0.7,   # normalidad/seguridad ilusoria
            weight=0.9,
            dispersion=0.5,
            noise=0.2,
        ),
        DreamNode(
            name="canoe_transition",
            density=0.6,   # tránsito entre estados (isla ↔ tierra)
            weight=0.8,
            dispersion=0.5,
            noise=0.2,
        ),
        DreamNode(
            name="hostility_rocks",
            density=0.7,   # amenaza externa explícita
            weight=0.9,
            dispersion=0.6,
            noise=0.3,
        ),
        DreamNode(
            name="lava_and_dead_family",
            density=0.95,  # revelación final muy cargada
            weight=1.1,    # peso ligeramente mayor por ser clímax
            dispersion=0.3,
            noise=0.1,
        ),
    ]
    aligned_C = dream_coherence(aligned_nodes, alpha_noise=1.0)

    # Interpretación forzada (símbolos aislados, más ruido, menos peso estructural)
    forced_nodes = [
        DreamNode(
            name="desert_run",
            density=0.5,
            weight=0.6,
            dispersion=0.8,
            noise=0.6,
        ),
        DreamNode(
            name="pyramid_refuge",
            density=0.4,
            weight=0.5,
            dispersion=0.9,
            noise=0.7,
        ),
        DreamNode(
            name="white_house_island",
            density=0.4,
            weight=0.4,
            dispersion=1.0,
            noise=0.7,
        ),
        DreamNode(
            name="canoe_transition",
            density=0.3,
            weight=0.4,
            dispersion=1.0,
            noise=0.8,
        ),
        DreamNode(
            name="hostility_rocks",
            density=0.3,
            weight=0.4,
            dispersion=1.1,
            noise=0.8,
        ),
        DreamNode(
            name="lava_and_dead_family",
            density=0.5,
            weight=0.5,
            dispersion=0.9,
            noise=0.7,
        ),
    ]
    forced_C = dream_coherence(forced_nodes, alpha_noise=1.0)

    # Afirmación clave: la lectura estructural coherente
    # debe producir mayor coherencia total que la lectura forzada.
    assert aligned_C > forced_C
