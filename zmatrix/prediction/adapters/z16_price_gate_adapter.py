"""Z16 Price Gate placeholder — required but NOT_CONNECTED."""
def load_z16_signal(ticker=None):
    return {"source": "Z16_PRICE_GATE", "available": False, "required": True,
            "status": "PLACEHOLDER_NOT_CONNECTED", "warnings": ["Z16_NOT_CONNECTED"]}
