from core.constants import ALPHA, BETA, S_REF

class IntegrationLaws:
    @staticmethod
    def calculate_omega_law(alpha: float, beta: float, s_ref: float) -> float:
        """
        Calculates the integration law (Law Ω) using the constants:
        Formula: Ω = (α / S_REF) * (1 + β)

        alpha: ALPHA constant.
        beta: BETA constant.
        s_ref: S_REF constant.
        """
        return (alpha / s_ref) * (1 + beta)

    @staticmethod
    def system_collapse_integration(integration: float, threshold: float = ALPHA) -> bool:
        """
        Checks if the system is collapsing based on its integration level.
        Collapse occurs when integration < threshold.
        """
        return integration < threshold
