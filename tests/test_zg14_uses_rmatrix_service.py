"""G14 behavior tests — actual function calls with monkeypatched service"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_g14_real_r_score_calls_service():
    spec = importlib.util.spec_from_file_location("zg14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    # Monkeypatch r_matrix_service
    called = {"count": 0}
    def fake_service(ticker, prices, position=None, **kw):
        called["count"] += 1
        return {"ticker": ticker, "version": "v2.0-cycle-four-king", "status": "PASS",
                "r_score": 7.5, "r_resonance_status": "CYCLE_RESONANCE_ENTRY", "r_action_cap": "WATCH_ENTRY",
                "kings": {}, "sell_decision": None, "errors": [], "warnings": [], "legacy_fallback": False}
    
    import zmatrix.scoring.r_matrix.r_matrix_service as rms
    orig = rms.evaluate_r_matrix_cycle
    rms.evaluate_r_matrix_cycle = fake_service
    try:
        r = mod._real_r_score("002472", "双环传动", [10]*300)
        assert called["count"] == 1, f"service not called: {called}"
        assert r["r_version"] == "v2.0-cycle-four-king"
        assert r["status"] == "PASS"
    assert "r_resonance_status" in r
    assert "r_action_cap" in r
    finally:
        rms.evaluate_r_matrix_cycle = orig
    print(f"✅ G14: r_version={r['r_version']} status={r['status']}")

if __name__ == "__main__":
    test_g14_real_r_score_calls_service()
    print("\n🏁 Z-G14 R-Matrix service tests PASS")
