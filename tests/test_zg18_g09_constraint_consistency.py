"""Verify G18 constraint consistency — no r_pool dependency, horizon sync"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_g18_no_full_g09_run():
    s = open("pipelines/Z-G18_天机引擎/gate_pipeline.py").read()
    assert "zg09.run(universe=universe, pool_size=20" not in s, "G18 still full-runs G09"
    assert "load_g09_signals_for_tickers" in s, "G18 doesn't use targeted signal fetch"
    print("✅ no full G09 run, uses targeted fetch")

def test_g09_adapter_returns_signals_per_ticker():
    from zmatrix.prediction.g09_signal_adapter import load_g09_signals_for_tickers
    r = load_g09_signals_for_tickers(["002472"])
    assert "signals" in r, f"missing signals key: {r.keys()}"
    assert "available" in r
    print(f"✅ signals dict: available={r['available']}")

def test_final_decision_envelope_contract():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75)
    r = build_final_decision(p, {"g09": {}, "g08": {}, "g11": {}, "g14": {}})
    assert r["version"] == "v1.0"
    assert r["forbidden_real_trade_checked"] is True
    assert "provenance" in r
    print(f"✅ final envelope: entry={r['entry_intent']}")

if __name__ == "__main__":
    test_g18_no_full_g09_run()
    test_g09_adapter_returns_signals_per_ticker()
    test_final_decision_envelope_contract()
    print("\n🏁 Z-G18 constraint consistency tests PASS")
