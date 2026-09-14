from src.coherence import CoherenceValidator

def test_universal_constant_convergence():
    validator = CoherenceValidator()
    empirical_beta = validator.estimate_from_csv("data/sample_ia.csv")
    is_valid, error_margin = validator.verify_vpsi(empirical_beta)
    assert is_valid, (
        f"La invarianza falló con un error de {error_margin:.6%} "
        f"(Valor Empírico: {empirical_beta:.8f})"
    )
    print(f"\n[VPSI] Coherencia Total confirmada con error de {error_margin:.6%} "
          f"(Valor Empírico: {empirical_beta:.8f})")
