"""Stock Role Classifier v1.0 tests — v2.9.8-dev"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.investment.stock_role_classifier import classify_stock_role


def _b_pass():
    return {"status": "PASS", "base_role_eligible": True}

def _b_fail():
    return {"status": "DEGRADED", "base_role_eligible": False}

def _r_pass():
    return {"status": "PASS", "r_action_cap": "WATCH_ENTRY"}

def _r_fail():
    return {"status": "DEGRADED", "r_action_cap": "WAIT"}

def _d_pass():
    return {"status": "PASS", "short_event_eligible": True}

def _d_fail():
    return {"status": "DEGRADED", "short_event_eligible": False}


def test_b_pass_gives_long_core():
    r = classify_stock_role("002472", _b_pass(), _r_fail(), _d_fail())
    assert r["role"] == "A_LONG_CORE"
    assert r["paper_record_allowed"] is True
    print("✅ B-Matrix PASS → A_LONG_CORE")


def test_r_pass_gives_mid_rotation():
    r = classify_stock_role("002472", _b_fail(), _r_pass(), _d_fail())
    assert r["role"] == "B_MID_ROTATION"
    assert r["paper_record_allowed"] is True
    print("✅ R-Matrix PASS → B_MID_ROTATION")


def test_d_pass_gives_short_event():
    r = classify_stock_role("002472", _b_fail(), _r_fail(), _d_pass())
    assert r["role"] == "C_SHORT_EVENT"
    assert r["paper_record_allowed"] is True
    print("✅ D-Matrix PASS → C_SHORT_EVENT")


def test_all_fail_gives_reject():
    r = classify_stock_role("002472", _b_fail(), _r_fail(), _d_fail())
    assert r["role"] == "D_REJECT"
    assert r["paper_record_allowed"] is False
    print("✅ All fail → D_REJECT")


def test_d_cannot_become_long_core():
    """D-Matrix 永远不得升级为 A_LONG_CORE"""
    r = classify_stock_role("002472", _b_pass(), _r_fail(), _d_pass())
    assert r["role"] == "WATCH_ONLY", f"expected WATCH_ONLY (B+D conflict), got {r['role']}"
    assert "MULTI_MATRIX_CONFLICT" in str(r["downgrade_reasons"]), f"missing conflict reason: {r['downgrade_reasons']}"
    print("✅ B+D conflict → WATCH_ONLY (D cannot become long core via downgrade)")


def test_required_fields():
    r = classify_stock_role("002472", _b_fail(), _r_fail(), _d_fail())
    for k in ["classifier_version", "ticker", "role", "paper_record_allowed", "real_trade_allowed"]:
        assert k in r, f"missing: {k}"
    assert r["real_trade_allowed"] is False
    print("✅ Stock Role Classifier: required fields present")


if __name__ == "__main__":
    test_b_pass_gives_long_core()
    test_r_pass_gives_mid_rotation()
    test_d_pass_gives_short_event()
    test_all_fail_gives_reject()
    test_d_cannot_become_long_core()
    test_required_fields()
    print("\n🏁 Stock Role Classifier v1.0 — contract tests PASS")
