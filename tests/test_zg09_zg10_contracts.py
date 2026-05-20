"""v2.9.5-RC Z-G09/Z-G10 scorer contract tests"""
import importlib.util, sys, os
from pathlib import Path

def _load(mod_path):
    spec = importlib.util.spec_from_file_location(Path(mod_path).stem, mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_zg10_accepts_dearly_v22_dataclass():
    """Z-G10: handles DEarlyV22Result dataclass via to_dict()"""
    mod = _load("pipelines/Z-G10_全局黑马筛选/gate_pipeline.py")
    
    # Mock evaluate_d_early_v22 to return a fake dataclass
    class FakeDEarly:
        def to_dict(self):
            return {"final_score":7.5,"raw_score":8.0,"coverage_ratio":0.82,
                    "stage_hint":"D3_CANDIDATE","allowed_action_max":"WATCH",
                    "score_breakdown":{"gene":8},"warnings":[]}
    
    # Direct test: call _d_matrix_score with mocked data layer
    mod.market_truth = lambda t: {"status":"PASS","name":"测试"}
    mod.l4_health = lambda t: {"status":"PASS"}
    mod.get_kline = lambda t, d: {"prices":[100+i*0.1 for i in range(120)],"count":120}
    
    # Monkeypatch the import of evaluate_d_early_v22
    import zmatrix.scoring.d_band.d_early_v22_scorer as de
    orig_fn = de.evaluate_d_early_v22
    de.evaluate_d_early_v22 = lambda p: FakeDEarly()
    
    try:
        r = mod._d_matrix_score("002463")
        assert r["status"] == "PASS", f"Expected PASS, got {r['status']}"
        assert r["score"] == 7.5
        assert r["lifecycle"] == "D3_CANDIDATE"
        assert r["coverage_ratio"] == 0.82
        print("✅ test_zg10_accepts_dearly_v22_dataclass")
    finally:
        de.evaluate_d_early_v22 = orig_fn

def test_zg09_ranker_result_contract():
    """Z-G09: ranker returns valid structure"""
    mod = _load("pipelines/Z-G09_全局轮动筛选/gate_pipeline.py")
    
    # Mock data layer
    mod.market_truth = lambda t: {"status":"PASS","name":"测试"}
    mod.l4_health = lambda t: {"status":"PASS"}
    prices = [100 + i*0.2 + ((-1)**i)*2 for i in range(250)]
    mod.get_kline = lambda t, d: {"prices":prices,"count":len(prices)}
    
    r = mod._r_matrix_score("002463")
    assert r["status"] in {"PASS","ERROR","DATA_INSUFFICIENT","BLOCKED"}, f"Invalid status: {r['status']}"
    if r["status"] == "PASS":
        assert "score" in r
        assert "oscillation_type" in r
        assert r["allowed_action"] in {"WATCH","WAIT","PAPER_PROBE","HARVEST"}
    print(f"✅ test_zg09_ranker_result_contract (status={r['status']})")

if __name__ == "__main__":
    test_zg10_accepts_dearly_v22_dataclass()
    test_zg09_ranker_result_contract()
    print("\n🏁 Z-G09/Z-G10 contract tests PASS")
