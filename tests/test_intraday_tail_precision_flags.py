"""Z-G03/Z-G04 precision flags contract — DAILY_OHLCV_PROXY, not M1"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_zg03_has_data_precision_flag():
    """Z-G03 output includes data_precision=DAILY_OHLCV_PROXY"""
    spec = importlib.util.spec_from_file_location("zg03", "pipelines/Z-G03_盘中确认/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    mod.market_truth = lambda t: {"status":"PASS","name":"测试","price":10.5,"open":10.0,"high":10.8,"low":10.0}
    mod.get_kline = lambda t,d: {"prices":[10]*20,"volume":[1000]*20,"count":20}
    mod.get_sectors = lambda: {"status":"PASS"}
    
    r = mod.run(tickers=["002463"])
    item = r["sections"]["L3确认结果"][0]
    assert item.get("data_precision") == "DAILY_OHLCV_PROXY", f"got {item.get('data_precision')}"
    assert item.get("m1_connected") is False, f"got {item.get('m1_connected')}"
    assert "DAILY_OHLCV_PROXY" in r["sections"].get("data_precision_note", "")
    print(f"✅ Z-G03 precision={item['data_precision']} m1={item['m1_connected']}")


def test_zg04_has_data_precision_flag():
    """Z-G04 output includes data_precision=DAILY_OHLCV_PROXY and m1_connected=False"""
    spec = importlib.util.spec_from_file_location("zg04", "pipelines/Z-G04_尾盘过滤/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    mod.market_truth = lambda t: {"status":"PASS","price":10.5,"open":10.0,"name":"测试"}
    mod.l4_health = lambda t: {"status":"PASS"}
    mod.get_kline = lambda t,d: {"prices":[10]*60,"volume":[1000]*60,"count":60,"data_contract":"OHLCV_DAILY_V1"}
    mod.get_sectors = lambda: {"status":"PASS"}
    
    r = mod.run(tickers=["002463"])
    assert r.get("data_precision") == "DAILY_OHLCV_PROXY", f"got {r.get('data_precision')}, keys={list(r.keys())[:10]}"
    assert r.get("m1_connected") is False
    print(f"✅ Z-G04 precision={r['data_precision']} m1={r['m1_connected']}")


def test_zg03_zg04_no_m1_claim_in_docs():
    """Z-G03/Z-G04 source must not claim 'real M1' or '真实M1已接入'"""
    for name, path in [("Z-G03","pipelines/Z-G03_盘中确认/gate_pipeline.py"),
                        ("Z-G04","pipelines/Z-G04_尾盘过滤/gate_pipeline.py")]:
        source = open(path).read()
        # Must not claim it IS M1 (positive claim). "非M1" (negation) is OK.
        misleading = ["M1已接入", "M1盘中确认系统", "真实M1", "M1 realtime", "M1尾盘检测系统"]
        for term in misleading:
            assert term not in source, f"{name} has misleading claim: '{term}'"
        # Should have negation or proxy note
        assert "DAILY_OHLCV_PROXY" in source or "非M1" in source or "代理" in source, \
            f"{name} missing precision disclaimer"


if __name__ == "__main__":
    test_zg03_has_data_precision_flag()
    test_zg04_has_data_precision_flag()
    test_zg03_zg04_no_m1_claim_in_docs()
    print("\n🏁 precision flags contract tests PASS")
