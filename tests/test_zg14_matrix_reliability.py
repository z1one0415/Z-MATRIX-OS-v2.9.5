"""Z-G14 matrix reliability — scorer errors not zero, score_scale, payload builder"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_zg14_dmatrix_error_not_zero_score_silently():
    """D-Matrix exception → status=ERROR, score=None, error visible"""
    spec = importlib.util.spec_from_file_location("zg14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Force D-Matrix to raise
    orig = mod._get_d_matrix
    mod._D_MATRIX = lambda p: (_ for _ in ()).throw(RuntimeError("mock d error"))
    try:
        d = mod._real_d_score("002463", "test", [1, 2, 3]*100,
                              {"prices": [1, 2, 3]*100, "volume": [], "amount": []})
        assert d["status"] == "ERROR", f"expected ERROR got {d['status']}"
        assert d["score"] is None, f"score should be None, got {d['score']}"
        assert "mock d error" in d.get("error", ""), f"error not propagated: {d.get('error')}"
        print(f"✅ D-Matrix error→status={d['status']} score={d['score']} error={d['error'][:60]}")
    finally:
        mod._D_MATRIX = orig


def test_zg14_r_matrix_error_visible():
    """R-Matrix exception → structured return, not silent 0"""
    spec = importlib.util.spec_from_file_location("zg14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    orig = mod._get_r_matrix
    mod._R_MATRIX = (None, None)  # force DATA_GAP
    try:
        r = mod._real_r_score("002463", "test", [1]*300)
        assert r["status"] == "DATA_GAP"
        assert r["score"] is None
        print(f"✅ R-Matrix DATA_GAP→status={r['status']}")
    finally:
        mod._R_MATRIX = orig


def test_zg14_candidate_has_score_scale_and_status():
    """candidate output includes score_scale, score_status, weighted_total"""
    spec = importlib.util.spec_from_file_location("zg14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    
    # Inject load_universe + mock everything
    import pipelines.universe_provider as up
    orig_load = up.load_universe
    up.load_universe = lambda **kw: {
        "status": "PASS", "source": "A_SHARE_ALL", "tickers": ["002463"], "count": 4000,
        "is_global": True, "universe_level": "FULL_MARKET",
        "fallback_used": False, "warnings": [],
    }
    try:
        spec.loader.exec_module(mod)
        mod.market_truth = lambda t: {"status": "PASS", "name": "测试", "price": 10}
        mod.l4_health = lambda t: {"status": "PASS"}
        mod.get_kline = lambda t, d: {"prices": [10]*300, "volume": [1000]*300, "count": 300,
                                       "data_contract": "OHLCV_DAILY_V1",
                                       "close": [10]*300, "dates": ["2026-05-20"]*300,
                                       "open": [10]*300, "high": [11]*300, "low": [9]*300,
                                       "amount": [10000]*300}
        
        r = mod.run()
        candidates = r.get("candidates", [])
        assert candidates, f"expected at least one candidate, got status={r.get('status')} sections={r.get('sections',{}).keys()}"
        c = candidates[0]
        assert "score_scale" in c, f"missing score_scale: {list(c.keys())}"
        assert c["score_scale"]["b"] == "0-100"
        assert c["score_scale"]["r"] == "0-100"
        assert c["score_scale"]["d"] == "0-100"
        assert "score_status" in c
        assert "weighted_total" in c
        assert "confidence" in c
        print(f"✅ candidate: scale={c['score_scale']} status={c['score_status']} weighted={c['weighted_total']}")
    finally:
        up.load_universe = orig_load


def test_dmatrix_payload_builder_used_by_all_three():
    """G07/G10/G14 all use build_dmatrix_payload"""
    for code, path in [("G07", "pipelines/Z-G07_轮动黑马选股/gate_pipeline.py"),
                        ("G10", "pipelines/Z-G10_全局黑马筛选/gate_pipeline.py"),
                        ("G14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")]:
        source = open(path, encoding="utf-8").read()
        assert "build_dmatrix_payload" in source, f"{code} does not use build_dmatrix_payload"
    print("✅ G07/G10/G14 all use build_dmatrix_payload")



def test_zg14_sorts_by_weighted_total_not_raw_total():
    """G14 run() sorts by weighted_total, not raw total"""
    source = open("pipelines/Z-G14_月度全量选股/gate_pipeline.py", encoding="utf-8").read()
    # Check the sort line
    assert 'key=lambda x: x.get("weighted_total"' in source,         "G14 does not sort by weighted_total"
    assert 'key=lambda x: x["total"]' not in source,         "G14 still sorts by raw total"
    print("✅ G14 sorts by weighted_total")


def test_zg14_data_gap_confidence_not_pass():
    """DATA_GAP scorer → confidence=DEGRADED_MATRIX_DATA_GAP, not PASS"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.market_truth = lambda t: {"status":"PASS","name":"测试","price":10}
    mod.l4_health = lambda t: {"status":"PASS"}
    mod.get_kline = lambda t,d: {"prices":[10]*300,"volume":[1000]*300,"amount":[10000]*300,
                                  "close":[10]*300,"open":[10]*300,"high":[11]*300,"low":[9]*300,
                                  "dates":["2026-05-20"]*300,"data_contract":"OHLCV_DAILY_V1"}
    mod._real_b_score = lambda t,n: {"score":None,"status":"DATA_GAP","base_type":None,"rating":None,"traps":[],"error":"b gap"}
    mod._real_r_score = lambda t,n,p: {"score":50,"status":"PASS","subtype":"A","error":None}
    mod._real_d_score = lambda t,n,p,kl: {"score":50,"status":"PASS","lifecycle":"D1","error":None}
    candidates = mod._full_scan(["002463"])
    assert candidates, "no candidates"
    assert candidates[0]["score_status"]["b"] == "DATA_GAP"
    assert candidates[0]["confidence"] == "DEGRADED_MATRIX_DATA_GAP", f"got {candidates[0]['confidence']}"
    print(f"✅ DATA_GAP→confidence={candidates[0]['confidence']}")


def test_zg14_uses_chain_taxonomy_provider_not_hardcoded_chains():
    """G14 must use chain_taxonomy_provider, no hardcoded chains dict"""
    source = open("pipelines/Z-G14_月度全量选股/gate_pipeline.py", encoding="utf-8").read()
    assert "chain_taxonomy_provider" in source
    assert "match_chain" in source
    assert "chain_density" in source
    assert 'chains = {' not in source
    assert 'kw.split("|")' not in source
    print("✅ G14: chain_taxonomy_provider, no hardcoded chains")

def test_zg14_candidate_has_chain_field():
    """Each G14 candidate includes chain field"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    import pipelines.universe_provider as up
    up.load_universe = lambda **kw: {
        "status": "PASS", "source": "A_SHARE_ALL",
        "tickers": ["600519"], "count": 4000,
        "is_global": True, "universe_level": "FULL_MARKET",
        "fallback_used": False, "warnings": [],
    }
    mod.market_truth = lambda t: {"status":"PASS","name":"贵州茅台","industry":"食品饮料","price":1500}
    mod.l4_health = lambda t: {"status":"PASS"}
    mod.get_kline = lambda t,d: {"prices":[100]*500,"close":[100]*500,"open":[100]*500,
                                  "high":[101]*500,"low":[99]*500,"volume":[1000]*500,
                                  "amount":[10000]*500,"dates":["2026-05-20"]*500,
                                  "data_contract":"OHLCV_DAILY_V1"}
    mod._real_b_score = lambda t,n: {"score":60,"status":"PASS","base_type":"BRAND_SCARCITY_MONOPOLY","rating":"A","traps":[],"error":None}
    mod._real_r_score = lambda t,n,p: {"score":40,"status":"PASS","subtype":"A","error":None}
    mod._real_d_score = lambda t,n,p,kl: {"score":30,"status":"PASS","lifecycle":"D1","error":None}
    
    r = mod.run()
    assert r["candidates"], "no candidates"
    c = r["candidates"][0]
    assert "chain" in c, f"missing chain field: {list(c.keys())}"
    assert c["chain"] in {"消费品牌", "资源周期", "未映射"}, f"unexpected chain: {c['chain']}"
    assert "chain_density" in r["sections"]
    assert "chain_taxonomy" in r["sections"]
    print(f"✅ candidate chain={c['chain']} density={r['sections'].get('chain_density',{})}")

if __name__ == "__main__":
    test_zg14_dmatrix_error_not_zero_score_silently()
    test_zg14_r_matrix_error_visible()
    test_zg14_candidate_has_score_scale_and_status()
    test_dmatrix_payload_builder_used_by_all_three()
    test_zg14_sorts_by_weighted_total_not_raw_total()
    test_zg14_data_gap_confidence_not_pass()
    test_zg14_uses_chain_taxonomy_provider_not_hardcoded_chains()
    test_zg14_candidate_has_chain_field()
    print("\n🏁 Z-G14 matrix reliability tests PASS")
