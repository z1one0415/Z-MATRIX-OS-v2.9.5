"""Z-G10 D-Matrix payload OHLCV enrichment contract"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_zg10_payload_contains_ohlcv_submodules():
    """Z-G10 _d_matrix_score passes OHLCV to market/silent/micro/volume_price_preload"""
    spec = importlib.util.spec_from_file_location("zg10", "pipelines/Z-G10_全局黑马筛选/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    
    # Patch the scorer import BEFORE loading
    captured_payload = {}
    import zmatrix.scoring.d_band.d_early_v22_scorer as scorer_mod
    orig_eval = scorer_mod.evaluate_d_early_v22
    def capture_payload(payload):
        captured_payload.update(payload)
        class FakeResult:
            def to_dict(self): return {"final_score": 75, "raw_score": 70, "stage_hint": "D2", "coverage_ratio": 0.8}
        return FakeResult()
    scorer_mod.evaluate_d_early_v22 = capture_payload
    
    try:
        spec.loader.exec_module(mod)
        mod.market_truth = lambda t: {"status": "PASS", "name": "测试", "sector": "电子"}
        mod.l4_health = lambda t: {"status": "PASS"}
        mod.get_kline = lambda t, d: {
            "prices": [10]*60, "volume": [1000]*60, "amount": [10000]*60,
            "open": [10]*60, "high": [11]*60, "low": [9]*60, "close": [10.5]*60,
            "dates": [f"2026-05-{i:02d}" for i in range(1,61)], "count": 60,
            "data_contract": "OHLCV_DAILY_V1",
        }
        
        r = mod._d_matrix_score("002463")
        assert r["status"] == "PASS"
        assert captured_payload, "scorer not called"
        
        mkt = captured_payload["market"]
        assert "volume" in mkt
        assert "dates" in mkt
        assert "open" in mkt
        assert "volume" in captured_payload["silent_accumulation"]
        assert "volume" in captured_payload["micro_absorption"]
        assert "volume" in captured_payload["volume_price_preload"]
        print(f"✅ market keys={list(mkt.keys())[:6]}... silent/micro/preload OK")
    finally:
        scorer_mod.evaluate_d_early_v22 = orig_eval


def test_zg10_payload_graceful_without_volume():
    """Z-G10 handles missing volume gracefully (empty lists, no crash, returns PASS)"""
    import zmatrix.scoring.d_band.d_early_v22_scorer as scorer_mod
    captured = {}
    orig_eval = scorer_mod.evaluate_d_early_v22
    
    class FakeResult:
        def to_dict(self):
            return {
                "final_score": 50, "raw_score": 50,
                "stage_hint": "D1_THEME_SEED", "coverage_ratio": 0.5,
                "score_breakdown": {}, "warnings": [],
            }
    
    def fake_eval(payload):
        captured.update(payload)
        return FakeResult()
    
    scorer_mod.evaluate_d_early_v22 = fake_eval
    
    try:
        spec = importlib.util.spec_from_file_location("zg10", "pipelines/Z-G10_全局黑马筛选/gate_pipeline.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.market_truth = lambda t: {"status": "PASS", "name": "测试"}
        mod.l4_health = lambda t: {"status": "PASS"}
        mod.get_kline = lambda t,d: {"prices": [10]*60, "volume": [], "count": 60}
        
        r = mod._d_matrix_score("002463")
        assert r["status"] == "PASS", f"expected PASS got {r.get('status')}"
        assert r["score"] == 50
        assert r["coverage_ratio"] == 0.5
        assert captured["market"]["volume"] == []
        assert captured["silent_accumulation"]["volume"] == []
        assert captured["micro_absorption"]["volume"] == []
        assert captured["volume_price_preload"]["volume"] == []
        print("✅ empty volume→PASS score=50 coverage=0.5, all submodules empty")
    finally:
        scorer_mod.evaluate_d_early_v22 = orig_eval


if __name__ == "__main__":
    test_zg10_payload_contains_ohlcv_submodules()
    test_zg10_payload_graceful_without_volume()
    print("\n🏁 Z-G10 OHLCV payload tests PASS")
