"""Z-G03 intraday confirmation contract tests — VWAP/volume/vwap_abbreviation"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_zg03_vwap_confirmed_branch():
    """ABOVE_VWAP + high volume_ratio → CONFIRMED"""
    spec = importlib.util.spec_from_file_location("zg03", "pipelines/Z-G03_盘中确认/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    mod.market_truth = lambda t: {
        "status": "PASS", "name": "测试股",
        "price": 10.5, "open": 10.0, "high": 10.8, "low": 10.0,
        "baostock_close": 9.8, "source": "mock", "time": "10:30",
    }
    mod.get_kline = lambda t, d: {
        "prices": [10]*20,
        "volume": [1000,1000,1000,1000,1000,2000],  # 2000/1000=2x ratio
        "count": 20,
        "data_contract": "OHLCV_DAILY_V1",
    }
    mod.get_sectors = lambda: {"status": "PASS"}
    
    r = mod.run(tickers=["002463"])
    items = r["sections"]["L3确认结果"]
    assert len(items) == 1
    item = items[0]
    assert item["vwap_status"] == "ABOVE_VWAP", f"got {item['vwap_status']}"
    assert item["verdict"] == "CONFIRMED", f"got {item['verdict']} vol_ratio={item['volume_ratio']}"
    print(f"✅ VWAP ABOVE→CONFIRMED (vol_ratio={item['volume_ratio']})")


def test_zg03_vwap_strings_match():
    """_vwap_check returns must match run() comparison strings"""
    source = open("pipelines/Z-G03_盘中确认/gate_pipeline.py").read()
    # _vwap_check returns these
    assert "ABOVE_VWAP" in source
    assert "BELOW_VWAP" in source
    # run() checks must use the same
    assert 'vwap == "ABOVE_VWAP"' in source, "run() should check ABOVE_VWAP not ABOVE_OPEN"
    assert 'vwap == "BELOW_VWAP"' in source, "run() should check BELOW_VWAP not BELOW_OPEN"
    # Must NOT use old wrong strings
    assert 'ABOVE_OPEN' not in source.split("def run")[1], "legacy ABOVE_OPEN still in run()"
    assert 'BELOW_OPEN' not in source.split("def run")[1], "legacy BELOW_OPEN still in run()"
    print("✅ VWAP strings: _vwap_check and run() consistent")


def test_zg03_volume_ratio_uses_ohlcv():
    """_volume_ratio must use kl['volume'] not price diffs"""
    source = open("pipelines/Z-G03_盘中确认/gate_pipeline.py").read()
    vr_func = source.split("def _volume_ratio")[1].split("def run")[0]
    assert "kl.get(\"volume\"" in vr_func or 'kl["volume"]' in vr_func, \
        "_volume_ratio doesn't use OHLCV volume field"
    assert "prices" not in vr_func or "volume" in vr_func, \
        "_volume_ratio still uses prices for pseudo-volume"
    print("✅ _volume_ratio uses OHLCV volume")


def test_zg03_below_vwap_rejected()
    test_zg03_final_status_not_running():
    """BELOW_VWAP + low volume → REJECTED"""
    spec = importlib.util.spec_from_file_location("zg03", "pipelines/Z-G03_盘中确认/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    mod.market_truth = lambda t: {
        "status": "PASS", "name": "测试", "price": 9.1, "open": 10.0, "high": 10.0, "low": 9.0,
        "baostock_close": 9.2, "source": "mock", "time": "10:30",
    }
    mod.get_kline = lambda t, d: {
        "prices": [10]*20,
        "volume": [2000,2000,2000,2000,2000,500],  # 500/2000=0.25x
        "count": 20,
    }
    mod.get_sectors = lambda: {"status": "PASS"}
    
    r = mod.run(tickers=["002463"])
    item = r["sections"]["L3确认结果"][0]
    assert item["vwap_status"] == "BELOW_VWAP", f"got {item['vwap_status']}"
    assert item["verdict"] == "REJECTED", f"got {item['verdict']}"
    print(f"✅ BELOW_VWAP + low vol→REJECTED (vol_ratio={item['volume_ratio']})")




def test_zg03_final_status_not_running():
    spec = importlib.util.spec_from_file_location('zg03','pipelines/Z-G03_盘中确认/gate_pipeline.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    mod.market_truth = lambda t: {'status':'PASS','name':'测试股','price':10.5,'open':10.0,'high':10.8,'low':10.0,'baostock_close':9.8,'source':'mock','time':'10:30'}
    mod.get_kline = lambda t,d: {'prices':[10]*20,'volume':[1000,1000,1000,1000,1000,2000],'count':20,'data_contract':'OHLCV_DAILY_V1'}
    mod.get_sectors = lambda: {'status':'PASS'}
    r = mod.run(tickers=['002463'])
    assert r['status'] == 'PASS_PROXY'
    assert r['status'] != 'running'
    sc = r['sections']['status_contract']
    assert sc['data_precision'] == 'DAILY_OHLCV_PROXY'
    assert sc['m1_connected'] is False
    assert sc['allows_buy_signal'] is False
    print(f'✅ Z-G03 status={r["status"]} proxy={sc["data_precision"]}')

if __name__ == "__main__":
    test_zg03_vwap_confirmed_branch()
    test_zg03_vwap_strings_match()
    test_zg03_volume_ratio_uses_ohlcv()
    test_zg03_below_vwap_rejected()
    test_zg03_final_status_not_running()
    print("\n🏁 Z-G03 intraday contract tests PASS")
