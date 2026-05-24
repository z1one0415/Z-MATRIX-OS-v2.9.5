"""G18 Paper Execution Record v1.0 tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_record_contains_required_fields():
    from zmatrix.prediction.paper_execution_record import build_paper_execution_record
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", name="测试", probability=0.75, action_proposal="PAPER_TRACK", confidence="MEDIUM")
    r = build_paper_execution_record(p)
    for k in ["record_version","record_type","run_id","ticker","timestamp","prediction",
              "final_decision","upstream_evidence_available","conflict_summary",
              "paper_execution","z9_calibration_hooks","forbidden_real_trade_checked"]:
        assert k in r, f"missing {k}"
    assert r["record_version"] == "v1.0"
    print("✅ record: all fields present")

def test_record_blocks_real_trade_actions():
    from zmatrix.prediction.paper_execution_record import build_paper_execution_record
    from zmatrix.prediction.contracts import PredictionResult
    from zmatrix.action.action_contracts import FORBIDDEN_REAL_ACTIONS
    s = open("zmatrix/prediction/paper_execution_record.py").read()
    for bad in ["BUY","SELL","AUTO_TRADE","MARKET_ORDER"]:
        assert bad not in s.split('forbidden_real_trade_checked')[0], f"leaked {bad}"
    print("✅ record: no real trade actions leaked")

def test_record_allowed_false_when_no_paper_action():
    from zmatrix.prediction.paper_execution_record import build_paper_execution_record
    from zmatrix.prediction.contracts import PredictionResult
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="WAIT")
    up = {"g09": {"hard_blocks": ["BLOCK"]}, "g08": {}, "g11": {}, "g14": {}}
    fd = build_final_decision(p, up)
    p.final_decision = fd
    r = build_paper_execution_record(p)
    assert r["paper_execution"]["allowed"] is False
    assert r["paper_execution"]["paper_action"] is None
    print("✅ record: not allowed when no paper_action")

def test_record_preserves_conflict_codes():
    from zmatrix.prediction.paper_execution_record import build_paper_execution_record
    from zmatrix.prediction.contracts import PredictionResult
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="PAPER_TRACK")
    up = {"g09": {"position_action": "REDUCE_CORE", "hard_blocks": []}, "g08": {}, "g11": {}, "g14": {}}
    fd = build_final_decision(p, up)
    p.final_decision = fd
    r = build_paper_execution_record(p)
    assert len(r["conflict_summary"]["conflict_codes"]) > 0
    assert "G09_SELL_VS_G18_ENTRY" in r["conflict_summary"]["conflict_codes"]
    print("✅ record: conflict codes preserved")

def test_z9_hooks_present_but_no_real_write():
    from zmatrix.prediction.paper_execution_record import build_paper_execution_record
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75)
    r = build_paper_execution_record(p)
    zh = r["z9_calibration_hooks"]
    assert zh["needs_future_review"] is True
    assert "T1" in zh.get("review_horizons", [])
    assert "actual_return_T1" in zh.get("expected_fields", [])
    # No real write
    assert "written" not in str(zh).lower() or "deferred" in str(zh).lower()
    print("✅ z9 hooks: present, no real write")

if __name__ == "__main__":
    test_record_contains_required_fields()
    test_record_blocks_real_trade_actions()
    test_record_allowed_false_when_no_paper_action()
    test_record_preserves_conflict_codes()
    test_z9_hooks_present_but_no_real_write()
    print("\n🏁 G18 Paper Execution Record v1.0 tests PASS")
