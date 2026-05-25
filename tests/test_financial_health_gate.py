"""Financial Health Gate contract tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.financial_health_gate import check_financial_health, _FORBIDDEN
import json

GOOD = {"revenue_growth": 15, "net_profit_growth": 20, "deducted_net_profit_growth": 18,
        "gross_margin": 45, "operating_cashflow": 100, "roe": 15, "debt_ratio": 40,
        "valuation_percentile": 60, "goodwill_risk": 0, "receivable_risk": 0, "inventory_risk": 0}


def test_pass():
    r = check_financial_health({"ticker": "002472"}, {"ticker": "002472", **GOOD})
    assert r["financial_gate_passed"] is True
    assert r["degraded"] is False
    print("✅ financial_health: PASS")


def test_degraded_on_missing():
    r = check_financial_health({"ticker": "002472"}, {"ticker": "002472"})
    assert r["degraded"] is True
    assert r["financial_gate_passed"] is False
    print("✅ financial_health: DEGRADED on missing data")


def test_fails_on_bad_roe():
    fd = dict(GOOD); fd["roe"] = 2
    r = check_financial_health({"ticker": "002472"}, {"ticker": "002472", **fd})
    assert r["financial_gate_passed"] is False
    assert "roe" in str(r["failed_items"])
    print("✅ financial_health: fails on roe < 5%")


def test_no_forbidden():
    r = check_financial_health({"ticker": "002472"}, {"ticker": "002472", **GOOD})
    for t in _FORBIDDEN:
        assert t not in json.dumps(r)
    print("✅ financial_health: no forbidden tokens")


if __name__ == "__main__":
    test_pass(); test_degraded_on_missing(); test_fails_on_bad_roe(); test_no_forbidden()
    print("\n🏁 Financial Health Gate — tests PASS")
