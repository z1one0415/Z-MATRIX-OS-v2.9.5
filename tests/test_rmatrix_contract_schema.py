"""R-Matrix v2.0 contract schema tests"""
import sys, os, json
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_rmatrix_service_contract_fields():
    from zmatrix.scoring.r_matrix.r_matrix_service import evaluate_r_matrix_cycle
    r = evaluate_r_matrix_cycle("TEST", [100 + i*0.1 for i in range(300)])
    required = ["ticker","version","status","legacy_fallback","r_score","r_resonance_status",
                "r_action_cap","entry_action_cap","exit_alert","hard_blocks","conflicts",
                "kings","sell_decision","data_lineage","errors","warnings"]
    for k in required: assert k in r, f"missing {k}"
    assert r["version"] == "v2.0-cycle-four-king"
    assert r["legacy_fallback"] is False
    print(f"✅ contract: {len(required)} fields, version={r['version']}")


def test_g09_r_pool_contract():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg09","pipelines/Z-G09_全局轮动筛选/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    import pipelines.universe_provider as up
    orig = up.load_universe
    up.load_universe = lambda *a,**kw: {"status":"PASS","source":"TEST","count":1,"tickers":["002472"],"is_global":False}
    mod.get_kline = lambda t,d: {"prices":[100+i*0.1 for i in range(300)]}
    mod.market_truth = lambda t: {"status":"PASS","name":"test","price":45.0}
    mod._read_positions = lambda: {}
    import zmatrix.scoring.r_matrix.r_matrix_service as rms
    orig_svc = rms.evaluate_r_matrix_cycle
    rms.evaluate_r_matrix_cycle = lambda t,**kw: {"ticker":t,"version":"v2.0-cycle-four-king","status":"PASS","legacy_fallback":False,"r_score":7.0,"r_resonance_status":"CYCLE_RESONANCE_ENTRY","r_action_cap":"WATCH_ENTRY","entry_action_cap":"WATCH_ENTRY","exit_alert":"NONE","hard_blocks":[],"conflicts":[],"kings":{},"sell_decision":None,"data_lineage":{"source":"test"},"errors":[],"warnings":[]}
    try:
        r = mod.run(pool_size=5, universe="TEST", allow_fallback=True)
        p = r["r_pool"][0]
        for k in ["ticker","r_score","r_resonance_status","r_action_cap","entry_action_cap","exit_alert","kings"]:
            assert k in p, f"G09 r_pool missing {k}"
        print(f"✅ G09 r_pool contract: {list(p.keys())[:8]}")
    finally:
        up.load_universe = orig; rms.evaluate_r_matrix_cycle = orig_svc


def test_g09_no_old_impulse_score():
    s = open("pipelines/Z-G09_全局轮动筛选/gate_pipeline.py").read()
    assert "def _impulse_score" not in s, "G09 still has old _impulse_score function def"
    print("✅ G09: old _impulse_score definition removed")


def test_contract_examples_exist():
    base = Path("docs/contracts/examples")
    required = ["r_matrix_v2_pass_example.json","r_matrix_v2_degraded_example.json",
                "g09_r_pool_example.json","g14_candidate_r_fields_example.json",
                "g18_g09_signal_example.json"]
    for name in required:
        assert (base/name).exists(), f"missing: {name}"
    print("✅ 5 examples present")


def test_rmatrix_examples_schema():
    base = Path("docs/contracts/examples")
    req = ["ticker","version","status","legacy_fallback","r_score","r_resonance_status",
           "r_action_cap","entry_action_cap","exit_alert","hard_blocks","conflicts",
           "kings","sell_decision","data_lineage","errors","warnings"]
    for name in ["r_matrix_v2_pass_example.json","r_matrix_v2_degraded_example.json"]:
        data = json.loads((base/name).read_text())
        for k in req: assert k in data, f"{name} missing {k}"
        assert data["version"] == "v2.0-cycle-four-king"
    print("✅ pass + degraded examples schema OK")


def test_degraded_example_consistency():
    data = json.loads(Path("docs/contracts/examples/r_matrix_v2_degraded_example.json").read_text())
    assert data["status"] == "DEGRADED"
    if "rotation_missing" in data.get("warnings",[]):
        assert "rotation" not in data["kings"], "rotation_missing but kings has rotation"
    print("✅ degraded example consistent")


if __name__ == "__main__":
    test_rmatrix_service_contract_fields()
    test_g09_r_pool_contract()
    test_g09_no_old_impulse_score()
    test_contract_examples_exist()
    test_rmatrix_examples_schema()
    test_degraded_example_consistency()
    print("\n🏁 R-Matrix contract schema tests PASS")
