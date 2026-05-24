"""G18 Final Decision Envelope v1.1 contract tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_g09_sell_decision_blocks_entry():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="PAPER_TRACK")
    g09 = {"available": True, "position_action": "REDUCE_CORE", "hard_blocks": []}
    r = build_final_decision(p, {"g09": g09, "g08": {}, "g11": {}, "g14": {}})
    assert r["entry_intent"] == "WAIT", f"entry should be WAIT, got {r['entry_intent']}"
    assert r["exit_intent"] == "REDUCE_CORE"
    assert "G09_SELL_DECISION_ACTIVE" in r["blocking_reasons"]
    print(f"✅ G09 sell blocks: entry={r['entry_intent']} exit={r['exit_intent']}")

def test_g09_hard_blocks_prevent_paper_entry():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17")
    g09 = {"available": True, "position_action": "", "hard_blocks": ["ROTATION_TREND_DOWN"]}
    r = build_final_decision(p, {"g09": g09, "g08": {}, "g11": {}, "g14": {}})
    assert r["entry_intent"] == "WAIT"
    assert r["paper_action"] is None
    assert "G09_HARD_BLOCKS" in r["blocking_reasons"]
    print(f"✅ G09 hard_blocks: paper=None blocks={r['blocking_reasons']}")

def test_g11_warning_only_no_hard_veto():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="WATCH")
    g11 = {"risk_authority": "STRONG_WARNING_ONLY", "warnings": ["concentration_high"]}
    r = build_final_decision(p, {"g09": {}, "g08": {}, "g11": g11, "g14": {}})
    assert r["entry_intent"] != "WAIT"  # G11 should NOT change to WAIT
    assert "concentration_high" in r["risk_warnings"]
    print(f"✅ G11 warn only: entry={r['entry_intent']} warnings={r['risk_warnings']}")

def test_paper_action_requires_z16_g17():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="PAPER_TRACK")
    r = build_final_decision(p, {"g09": {}, "g08": {}, "g11": {}, "g14": {}})
    assert "Z16_PRICE_GATE" in r["required_confirmations"]
    assert "G17_ACCOUNT_CONFIRMATION" in r["required_confirmations"]
    print(f"✅ Z16/G17 required: {r['required_confirmations']}")

def test_forbidden_real_trade_rejected():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    for bad in ["BUY", "SELL", "AUTO_TRADE"]:
        try:
            p = PredictionResult(ticker="002472", probability=0.75, action_proposal=bad)
            r = build_final_decision(p, {"g09": {}, "g08": {}, "g11": {}, "g14": {}})
            assert False, f"Should have rejected {bad}"
        except (ValueError, AssertionError):
            pass
    print("✅ forbidden real trade actions rejected")

if __name__ == "__main__":
    test_g09_sell_decision_blocks_entry()
    test_g09_hard_blocks_prevent_paper_entry()
    test_g11_warning_only_no_hard_veto()
    test_paper_action_requires_z16_g17()
    test_forbidden_real_trade_rejected()
    print("\n🏁 G18 Final Decision Envelope v1.1 tests PASS")
