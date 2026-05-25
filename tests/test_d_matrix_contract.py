"""D-Matrix v1.0 contract tests — v2.9.8-dev investment role control"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.investment.d_matrix import evaluate_d_matrix, _FORBIDDEN
import json


def _sample_narrative():
    return {"narrative_heat": 8, "catalyst_score": 7, "event_validity": 8,
            "fund_flow_heat": 7, "narrative_decay": 5}


def _sample_event():
    return {"invalidation_condition": "跌破30日线", "stop_loss_pct": 8}


def test_d_matrix_required_fields():
    r = evaluate_d_matrix("002472", _sample_narrative(), _sample_event())
    for k in ["matrix_id", "matrix_version", "ticker", "status", "short_event_eligible",
              "stop_loss_required", "cannot_convert_to_base", "d_action_cap",
              "score_final", "reasons", "real_trade_allowed", "forbidden_real_trade_checked"]:
        assert k in r, f"missing: {k}"
    assert r["matrix_id"] == "D-MATRIX"
    assert r["stop_loss_required"] is True
    assert r["cannot_convert_to_base"] is True
    assert r["real_trade_allowed"] is False
    print("✅ D-Matrix: required fields present")


def test_d_matrix_pass():
    r = evaluate_d_matrix("002472", _sample_narrative(), _sample_event())
    assert r["status"] == "PASS"
    assert r["short_event_eligible"] is True
    assert r["d_action_cap"] == "PAPER_PROBE"
    print(f"✅ D-Matrix: PASS, score={r['score_final']}")


def test_d_matrix_degraded_on_missing_data():
    r = evaluate_d_matrix("002472", {}, {})
    assert r["status"] == "DEGRADED"
    assert "INSUFFICIENT_NARRATIVE_DATA" in str(r.get("degraded_reason", ""))
    assert r["short_event_eligible"] is False
    print("✅ D-Matrix: DEGRADED on insufficient data")


def test_d_matrix_no_forbidden_trade():
    r = evaluate_d_matrix("002472", _sample_narrative(), _sample_event())
    raw = json.dumps(r)
    for token in _FORBIDDEN:
        assert token not in raw, f"forbidden token found: {token}"
    print("✅ D-Matrix: no forbidden real trade tokens")


def test_d_matrix_cannot_convert_to_base():
    """硬规则: 短线票不得转长期底仓"""
    r = evaluate_d_matrix("002472", _sample_narrative(), _sample_event())
    assert r["cannot_convert_to_base"] is True
    print("✅ D-Matrix: cannot_convert_to_base=True (hard rule)")


if __name__ == "__main__":
    test_d_matrix_required_fields()
    test_d_matrix_pass()
    test_d_matrix_degraded_on_missing_data()
    test_d_matrix_no_forbidden_trade()
    test_d_matrix_cannot_convert_to_base()
    print("\n🏁 D-Matrix v1.0 — contract tests PASS")
