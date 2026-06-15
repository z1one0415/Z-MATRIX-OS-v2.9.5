"""Board Classifier v1.0 — classifies A-share tickers by board type.

Boards: MAINBOARD, STAR, CHINEXT, SME, BSE, UNKNOWN.
"""
def classify_board(ticker: str) -> dict:
    """Classify ticker by board type from prefix."""
    t = str(ticker)
    # STAR: 688xxx / 689xxx
    if t.startswith("688") or t.startswith("689"):
        return {"ticker": t, "board_type": "STAR", "confidence": "RULE_BASED", "source": "ticker_prefix"}
    # CHINEXT: 300xxx / 301xxx
    if t.startswith("300") or t.startswith("301"):
        return {"ticker": t, "board_type": "CHINEXT", "confidence": "RULE_BASED", "source": "ticker_prefix"}
    # SME: 002xxx / 003xxx
    if t.startswith("002") or t.startswith("003"):
        return {"ticker": t, "board_type": "SME", "confidence": "RULE_BASED", "source": "ticker_prefix"}
    # MAINBOARD: 600/601/603/605/000/001
    if t.startswith(("600", "601", "603", "605", "000", "001")):
        return {"ticker": t, "board_type": "MAINBOARD", "confidence": "RULE_BASED", "source": "ticker_prefix"}
    # BSE: 8/4/9 prefix
    if t[0] in ("8", "4", "9"):
        return {"ticker": t, "board_type": "BSE", "confidence": "RULE_BASED", "source": "ticker_prefix"}
    return {"ticker": t, "board_type": "UNKNOWN", "confidence": "LOW", "source": "no_rule_match"}
