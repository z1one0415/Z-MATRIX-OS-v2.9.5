"""G11 Risk adapter — STRONG_WARNING_ONLY, never hard veto."""
def load_g11_signal(ticker=None):
    return {"source": "Z-G11", "available": False, "risk_authority": "STRONG_WARNING_ONLY",
            "hard_veto_allowed": False, "warnings": []}
