"""B-Matrix v1.0 contract tests — v2.9.8-dev investment role control"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.investment.b_matrix import evaluate_b_matrix, _FORBIDDEN
import json


def _sample_fundamentals():
    return {
        "financial_health_score": 8, "quality_score": 7, "cashflow_score": 8,
        "roe_score": 6, "industry_durability": 8, "dividend_or_core_asset_score": 6,
        "sector": "CONSUMER",
    }


def _sample_valuation():
    return {"valuation_safety": 6}


def test_b_matrix_required_fields():
    r = evaluate_b_matrix("002472", _sample_fundamentals(), _sample_valuation())
    for k in ["matrix_id", "matrix_version", "ticker", "status", "base_role_eligible",
              "base_action_cap", "base_holding_period", "rating", "eligibility",
              "score_final", "reasons", "real_trade_allowed", "forbidden_real_trade_checked"]:
        assert k in r, f"missing: {k}"
    assert r["matrix_id"] == "B-MATRIX"
    assert r["base_holding_period"] == "long_term"
    assert r["real_trade_allowed"] is False
    print("✅ B-Matrix: required fields present")


def test_b_matrix_pass():
    r = evaluate_b_matrix("002472", _sample_fundamentals(), _sample_valuation())
    assert r["status"] == "PASS"
    assert r["base_role_eligible"] is True
    assert r["eligibility"] == "B_ELIGIBLE"
    assert r["base_action_cap"] == "PAPER_TRACK"
    print(f"✅ B-Matrix: PASS, score={r['score_final']}")


def test_b_matrix_degraded_on_missing_data():
    r = evaluate_b_matrix("002472", {}, {})
    assert r["status"] == "DEGRADED"
    assert "INSUFFICIENT_DATA" in str(r.get("degraded_reason", ""))
    assert r["base_role_eligible"] is False
    print("✅ B-Matrix: DEGRADED on insufficient data")


def test_b_matrix_no_forbidden_trade():
    r = evaluate_b_matrix("002472", _sample_fundamentals(), _sample_valuation())
    raw = json.dumps(r)
    for token in _FORBIDDEN:
        assert token not in raw, f"forbidden token found: {token}"
    print("✅ B-Matrix: no forbidden real trade tokens")


if __name__ == "__main__":
    test_b_matrix_required_fields()
    test_b_matrix_pass()
    test_b_matrix_degraded_on_missing_data()
    test_b_matrix_no_forbidden_trade()
    print("\n🏁 B-Matrix v1.0 — contract tests PASS")
