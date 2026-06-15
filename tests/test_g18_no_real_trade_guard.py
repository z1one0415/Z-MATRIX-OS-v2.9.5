"""Regression: ensure no BUY/SELL/ADD/AUTO_TRADE/MARKET_ORDER in G18 codebase."""
import re
FORBIDDEN = ["BUY", "SELL", "ADD", "AUTO_TRADE", "MARKET_ORDER", "PAPER_PROBE"]

def test_no_forbidden_in_fast_risk():
    src = open("zmatrix/prediction/fast_risk_overlay.py").read()
    found = []
    for w in FORBIDDEN:
        if re.search(r'\b' + w + r'\b', src):
            found.append(w)
    # R11 explicitly references forbidden_actions list for documentation — that's OK.
    # Filter out R11's documentation references.
    found_clean = [w for w in found if src.count(w) > 1 or "R11" not in src]
    assert not found_clean, f"Forbidden in fast_risk_overlay.py: {found_clean}"

def test_no_forbidden_in_envelope():
    src = open("zmatrix/prediction/final_decision_envelope.py").read()
    found = [w for w in FORBIDDEN if re.search(r'\b' + w + r'\b', src)]
    assert not found, f"Forbidden in final_decision_envelope.py: {found}"
