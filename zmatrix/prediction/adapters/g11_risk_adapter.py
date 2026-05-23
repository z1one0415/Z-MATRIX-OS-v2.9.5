"""G11 Risk Adapter — strong warning only, never hard veto."""
def load_g11_risk() -> dict:
    return {
        "source": "Z-G11", "available": False,
        "risk_authority": "STRONG_WARNING_ONLY",
        "hard_veto_allowed": False, "requires_g17_confirmation": True,
        "warnings": [],
    }
