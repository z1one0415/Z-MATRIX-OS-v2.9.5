"""G18 behavior tests — constraint logic + final_decision in output"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_apply_g09_constraints_hard_blocks_cap_prob():
    from zmatrix.prediction.g09_signal_adapter import apply_g09_constraints
    g09 = {"available": True, "hard_blocks": ["ROTATION_TREND_DOWN"], "position_action": "MAJOR_REDUCE_OR_EXIT",
           "exit_alert": "NONE"}
    r = apply_g09_constraints(g09, "WAIT", 0.75, 0.75)
    assert r["probability_override"] <= 0.55, f"prob not capped: {r['probability_override']}"
    print(f"✅ hard_blocks cap: {r['probability_override']}")

def test_final_decision_sell_overrides():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="PAPER_TRACK")
    g09 = {"available": True, "position_action": "REDUCE_CORE"}
    r = build_final_decision(p, {"g09": g09, "g08": {}, "g11": {}, "g14": {}})
    assert r["entry_intent"] == "WAIT"
    assert r["exit_intent"] == "REDUCE_CORE"
    print(f"✅ sell overrides: entry={r['entry_intent']} exit={r['exit_intent']}")

def test_g18_predictions_contain_final_decision()
    test_g09_adapter_returns_signal_for_every_ticker():
    spec = importlib.util.spec_from_file_location("zg18", "pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    for p in r["predictions"]:
        assert "final_decision" in p, f"missing final_decision in prediction: {list(p.keys())}"
    print(f"✅ predictions contain final_decision: {len(r['predictions'])} entries")


def test_g09_adapter_returns_signal_for_every_ticker():
    from zmatrix.prediction.g09_signal_adapter import load_g09_signals_for_tickers
    r = load_g09_signals_for_tickers(["000001", "002472"])
    assert "000001" in r["signals"], "missing signal for 000001"
    assert "002472" in r["signals"], "missing signal for 002472"
    assert "available" in r["signals"]["000001"], "missing available field"
    print(f"✅ every ticker has signal: {list(r['signals'].keys())}")

if __name__ == "__main__":
    test_apply_g09_constraints_hard_blocks_cap_prob()
    test_final_decision_sell_overrides()
    test_g18_predictions_contain_final_decision()
    test_g09_adapter_returns_signal_for_every_ticker()
    print("\n🏁 Z-G18 constraint consistency tests PASS")
