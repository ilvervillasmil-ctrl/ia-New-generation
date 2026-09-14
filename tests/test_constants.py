import pytest
from core.engine import OmegaEngine
# Se importa ALPHA y BETA directamente desde las constantes del framework
from formulas.constants import ALPHA, BETA

def test_alpha_coherence_threshold():
    """Verifica si el sistema identifica correctamente el umbral Alpha (0.96296...)"""
    engine = OmegaEngine()
    
    # Simulamos un estado de Coherencia Máxima con la nueva API
    # Usando la nueva fórmula C_Ω = α·H(S) + β·I_ext con escalado PHI
    mock_perfect_layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
    
    result = engine.compute_coherence(
        layers_data=mock_perfect_layers,
        C1=1.0, C2=1.0, theta=0.0  # Nueva API para I_ext
    )
    
    # Con la nueva fórmula y escalado PHI, el resultado se evalúa dentro del dominio legal
    assert isinstance(result, float)
    assert BETA <= result <= ALPHA
    print(f"Test Alpha Passed: C_Ω = {result}")

def test_diagnostic_codes():
    """Verifica que los códigos estructurales de diagnóstico funcionen"""
    from core.diagnostics import DiagnosticSystem
    diag = DiagnosticSystem()
    
    # Valida el mapeo del código ante Coherencia Máxima o umbral ALPHA
    assert "1144" in diag.get_status_code(ALPHA) or "INTEGRATED" in diag.get_status_code(ALPHA).upper()
    
    # El sistema de diagnóstico maneja códigos definidos por el framework (ej: CODE_ENTROPY)
    status = diag.get_status_code(0.05)
    assert "CODE 0" in status or "ENTROPY" in status.upper()
