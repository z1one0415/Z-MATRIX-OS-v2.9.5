"""G08 Narrative adapter — narrative heat, decay, bubble temperature."""
def load_g08_signal(ticker=None):
    return {"source": "Z-G08", "available": False, "narrative_heat": None,
            "narrative_decay": None, "bubble_temperature": None,
            "reason": "NOT_CONNECTED", "warnings": ["G08_NOT_CONNECTED"]}
