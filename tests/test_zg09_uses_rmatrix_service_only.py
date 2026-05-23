"""Z-G09 uses r_matrix_service only — no old scan calls in run()"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_zg09_run_uses_rmatrix_service_only():
    s = open("pipelines/Z-G09_全局轮动筛选/gate_pipeline.py").read()
    run_body = s.split("def run", 1)[1]
    assert "evaluate_r_matrix_cycle" in run_body, "G09 run() doesn't use r_matrix_service"
    for token in ["scan_impulse_king","scan_oscillation_king","scan_rhythm_king","scan_rotation_king","evaluate_cycle_four_king","evaluate_position_sell_decision"]:
        assert token not in run_body, f"forbidden legacy call in G09 run(): {token}"
    print("✅ G09 run(): only evaluate_r_matrix_cycle, no old scan calls")

def test_zg09_run_calls_service_with_monkeypatch():
    spec = importlib.util.spec_from_file_location("zg09","pipelines/Z-G09_全局轮动筛选/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    import pipelines.universe_provider as up
    orig_uni = up.load_universe
    up.load_universe = lambda *a,**kw: {"status":"PASS","source":"TEST","count":1,"tickers":["002472"],"is_global":False}
    mod.get_kline = lambda t,d: {"prices":[100+i*0.1 for i in range(300)]}
    mod.market_truth = lambda t: {"status":"PASS","name":"双环传动","price":45.0}
    mod._read_positions = lambda: {}
    
    import zmatrix.scoring.r_matrix.r_matrix_service as rms
    orig_svc = rms.evaluate_r_matrix_cycle
    called = {"count":0}
    def fake_svc(ticker,prices=None,position=None,**kw):
        called["count"]+=1
        return {"ticker":ticker,"version":"v2.0-cycle-four-king","status":"PASS","legacy_fallback":False,"r_score":88.0,"r_resonance_status":"CYCLE_RESONANCE_ENTRY","r_action_cap":"WATCH_ENTRY","entry_action_cap":"WATCH_ENTRY","exit_alert":"NONE","hard_blocks":[],"conflicts":[],"kings":{},"sell_decision":{"position_action":"NO_POSITION"},"data_lineage":{"source":"TEST"},"errors":[],"warnings":[]}
    rms.evaluate_r_matrix_cycle = fake_svc
    try:
        result = mod.run(pool_size=5, universe="TEST", allow_fallback=True)
        assert called["count"]==1
        p = result["r_pool"][0]
        assert p["r_score"]==88.0
        assert p["r_resonance_status"]=="CYCLE_RESONANCE_ENTRY"
        assert p["r_action_cap"]=="WATCH_ENTRY"
        print(f"✅ G09→service: score={p['r_score']} resonance={p['r_resonance_status']}")
    finally:
        up.load_universe = orig_uni
        rms.evaluate_r_matrix_cycle = orig_svc

if __name__ == "__main__":
    test_zg09_run_uses_rmatrix_service_only()
    test_zg09_run_calls_service_with_monkeypatch()
    print("\n🏁 Z-G09 r_matrix_service-only tests PASS")
