"""G17 Account Confirmation placeholder — required but NOT_CONNECTED."""
def load_g17_signal(ticker=None):
    return {"source": "G17_ACCOUNT_CONFIRMATION", "available": False, "required": True,
            "status": "PLACEHOLDER_NOT_CONNECTED", "warnings": ["G17_NOT_CONNECTED"]}
