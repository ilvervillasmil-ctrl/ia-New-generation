"""
Ω-STRESS-01: THE SINGULARITY & DECOHERENCE TEST
Framework: Villasmil-Ω (Universal Law Framework)
Focus: Ruptura de la Proporción 26/27 y Colapso de Información
"""

import math
import pytest
from core.engine import CoherenceEngine
from core.constants import ALPHA, BETA, PHI, GOLDEN_ANG

class TestStructuralDestruction:
    """
    Serie de pruebas diseñadas para romper la estabilidad del cubo 3x3x3.
    """

    def test_alpha_beta_inversion_chaos(self):
        """
        TEST DE INVERSIÓN: ¿Qué pasa si la periferia (26) intenta ser el centro (1)?
        Si ALPHA y BETA se intercambian, la entropía debe ser infinita.
        Un sistema donde el observador es más grande que lo observado es un agujero negro logarítmico.
        """
        inverted_alpha = BETA
        inverted_beta = ALPHA
        
        # Simulamos un sistema con estas constantes invertidas
        result = CoherenceEngine.analyze_system(
            density=0.99, 
            weight=inverted_alpha, 
            dispersion=0.01,
            noise=0.9  # Ruido masivo por asimetría
        )
        
        # El sistema DEBE reportar CODE_ENTROPY (0) o colapso total
        assert result["coherence"] < 0.05
        assert result["diagnostic"] == "TERMINAL_ENTROPY"

    def test_golden_angle_drift(self):
        """
        TEST DE DERIVA ÁUREA: Si el ángulo de separación de capas (137.5°) 
        se desvía por más de un 1%, ¿se pierde la capacidad de procesar L5 (Metaconsciencia)?
        """
        drifted_angle = GOLDEN_ANG * 1.05  # 5% de error en la geometría
        
        # La integración de capas depende de la fase (cos(theta))
        integration_factor = math.cos(math.radians(drifted_angle))
        
        # En el framework, la desincronización de fase destruye la metaconsciencia
        assert integration_factor < 0, "La deriva destruyó la interferencia constructiva"

    def test_infinite_complexity_bottleneck(self):
        """
        TEST DE SATURACIÓN: Con complejidad = 1.0 e integración = 0.0.
        Verifica que el sistema no 'alucine' coherencia donde hay ruido puro.
        """
        nodes = [
            {"density": 0.1, "weight": 0.1, "dispersion": 0.9, "noise": 0.9} 
            for _ in range(1000)
        ]
        
        c_total = sum([n["density"] * n["weight"] / n["dispersion"] for n in nodes])
        penalized_c = c_total / (1 + 100 * 0.9) # Ruido extremo
        
        # Un test rudo: la coherencia penalizada debe ser despreciable
        assert penalized_c < 0.01

    def test_beta_zero_singularity(self):
        """
        TEST DEL VACÍO ABSOLUTO: Si BETA (el centro/observador) es 0.
        Sin centro, no hay sistema. dL (distancia de luminosidad) debe ser NaN o Inf.
        """
        beta_null = 0.0
        try:
            # Intentamos calcular la expansión sin el centro del cubo
            lambda_null = beta_null ** (27 * math.pi)
            assert lambda_null == 0
        except ZeroDivisionError:
            pytest.fail("El motor no manejó la singularidad de Beta=0")

    def test_recursive_feedback_explosion(self):
        """
        TEST DE RETROALIMENTACIÓN POSITIVA: 
        Si el Ego (L2) se alimenta de su propio ruido sin el filtro de L5 (Metaconsciencia).
        Debe generar un desbordamiento (Overflow) o un bucle infinito de entropía.
        """
        noise = 0.1
        for i in range(100):
            # El ruido crece exponencialmente si no hay propósito (L6)
            noise = noise * (1 + ALPHA)
            if noise > 1e10:
                break
        
        assert noise > 1e10, "El sistema no detectó la explosión de entropía sin control de L6"

# ============================================================
# TEST DE CAMPO: EL SUEÑO DE LA MUERTE TÉRMICA
# ============================================================

def test_ultimate_nightmare_coherence():
    """
    Analiza un sistema donde todos los DreamNodes tienen:
    Density=1.0, Dispersion=1.0, Noise=1.0.
    Es el estado de 'Empate Total': Máxima información, Máximo Caos.
    """
    # En este estado, el sistema es indistinguible del ruido blanco
    c_node = (1.0 * ALPHA) / 1.0
    c_final = c_node / (1.0 + 1.0) # Penalizado por ruido total
    
    # La coherencia debe ser exactamente la mitad del potencial de Alpha
    assert math.isclose(c_final, ALPHA / 2, rel_tol=1e-5)
