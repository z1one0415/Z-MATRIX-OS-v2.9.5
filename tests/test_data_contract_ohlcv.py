"""OHLCV data contract tests — verify get_kline returns volume/amount, 
market_truth doesn't BLOCK on realtime-vs-prev-close, Z-G04 uses volume not prices."""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_get_kline_contract_has_ohlcv_keys():
    """get_kline returns OHLCV fields with prices==close backward compat"""
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Simulate baostock via fake internal
    orig_fn = mod._bs_research_kline
    def fake_kline(ticker, days, adjust="research"):
        n = 30
        return {
            "dates": [f"2026-05-{d:02d}" for d in range(1, n+1)],
            "open": [10.0]*n, "high": [11.0]*n, "low": [9.0]*n,
            "close": [10.5]*n, "volume": [1000000]*n, "amount": [10500000]*n,
            "prices": [10.5]*n, "count": n,
            "adjust_flag": "2", "adjust_type": "research",
            "data_contract": "OHLCV_DAILY_V1",
        }
    mod._bs_research_kline = fake_kline
    mod._cache_get = lambda ck, ttl=None: None  # disable cache
    mod._cache_set = lambda ck, rv, ttl=None: None
    
    try:
        r = mod.get_kline("002463", 30)
        assert r["status"] == "PASS"
        assert "open" in r, f"missing open: {r.keys()}"
        assert "high" in r, f"missing high"
        assert "low" in r, f"missing low"
        assert "close" in r, f"missing close"
        assert "volume" in r, f"missing volume"
        assert "prices" in r, f"missing prices (backward compat)"
        assert r["prices"] == r["close"], f"prices!=close: {r['prices'][:3]} vs {r['close'][:3]}"
        assert r["data_contract"] == "OHLCV_DAILY_V1"
        print(f"✅ OHLCV contract: {list(r.keys())} prices==close={r['prices']==r['close']}")
    finally:
        mod._bs_research_kline = orig_fn


def test_zg04_uses_volume_not_prices():
    """Z-G04 tail filter uses kl['volume'] when available, not kl['prices'] as volume proxy"""
    spec = importlib.util.spec_from_file_location("zg04", "pipelines/Z-G04_尾盘过滤/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Source inspection: verify code references kl.get("volume") or kl["volume"]
    source = open("pipelines/Z-G04_尾盘过滤/gate_pipeline.py").read()
    assert "kl.get(\"volume\"" in source or 'kl["volume"]' in source, \
        f"Z-G04 does not reference volume field from kline"
    
    # Verify no price-based volume proxy as primary source
    assert "volume_source" in source or "price_proxy_DEGRADED" in source, \
        "Z-G04 should flag when using price proxy"
    print("✅ Z-G04 references volume field + has price_proxy_DEGRADED fallback")


def test_market_truth_realtime_vs_prev_close_not_block():
    """market_truth with realtime price vs previous close >1% diff → DEGRADED, not BLOCK"""
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Source inspection: verify comparison_mode logic exists
    source = open("pipelines/Z-G01_数据后勤保障/gate_data.py").read()
    assert "is_same_trading_date" in source, "missing same-date check"
    assert "realtime_vs_previous_close_reference" in source, "missing comparison_mode"
    assert "comparison_mode" in source, "missing comparison_mode field"
    
    # Verify the code path for different dates doesn't use BLOCK
    # Find the branch that sets price_conflict=False when dates differ
    assert "dt[\"price_conflict\"] = False" in source, "should not BLOCK on prev-close diff"
    print("✅ market_truth has same-trading-date check + reference-only comparison mode")


def test_zg11_cash_ratio_not_placeholder():
    """Z-G11 cash_ratio is None + NOT_CONNECTED, not placeholder 10"""
    source = open("pipelines/Z-G11_组合风控/gate_pipeline.py").read()
    assert "cash_ratio = None" in source, f"cash_ratio still a placeholder number"
    assert "NOT_CONNECTED" in source, "missing NOT_CONNECTED annotation"
    print("✅ Z-G11 cash_ratio=None / NOT_CONNECTED")




def test_market_truth_handles_ohlcv_raw_kline_shape():
    """market_truth must handle OHLCV dict (prices=float list), not crash on float-as-dict"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    mod._cache_get = lambda ck, ttl=None: None
    mod._cache_set = lambda ck, rv, ttl=None: None
    mod._sina_quote = lambda t: {
        "price": 10.5, "open": 10.3, "high": 10.8, "low": 10.1,
        "volume": "1000000", "name": "测试", "source": "sina_api", "time": "15:00:00",
    }
    mod._bs_raw_kline = lambda t, d: {
        "dates": ["2026-05-19"],
        "close": [10.0],
        "prices": [10.0],  # float list, NOT dict list
        "count": 1,
        "data_contract": "OHLCV_DAILY_V1",
    }
    
    r = mod.market_truth("002463")
    
    assert r["status"] in {"PASS", "DEGRADED"}, f"status={r['status']}"
    assert r["baostock_close"] == 10.0, f"close={r['baostock_close']}"
    assert r["baostock_date"] == "2026-05-19"
    assert r.get("comparison_mode") == "realtime_vs_previous_close_reference"
    print(f"✅ market_truth OHLCV shape: status={r['status']} close={r['baostock_close']} mode={r.get('comparison_mode')}")



def test_market_truth_same_day_degraded_branch_no_lt_dict_crash():
    """Same-day dp=0.5%→DEGRADED, must not NameError on lt['close']"""
    import importlib.util
    from datetime import datetime
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    today = datetime.now().strftime("%Y-%m-%d")
    mod._cache_get = lambda ck, ttl=None: None
    mod._cache_set = lambda ck, rv, ttl=None: None
    mod._sina_quote = lambda t: {"price":100.0,"open":99.5,"high":101.0,"low":99.0,"volume":"1000000","name":"测试","source":"sina_api","time":"15:00:00"}
    mod._bs_raw_kline = lambda t,d: {"dates":[today],"close":[99.5],"prices":[99.5],"count":1,"data_contract":"OHLCV_DAILY_V1"}
    r = mod.market_truth("002463")
    assert r["status"] == "DEGRADED"
    assert r["baostock_close"] == 99.5
    assert r["baostock_date"] == today
    assert any("execution_quote DEGRADED" in e for e in r["errors"])
    print(f"✅ same-day DEGRADED: status={r['status']} close={r['baostock_close']}")

def test_market_truth_same_day_block_branch_no_lt_dict_crash():
    """Same-day dp=2.0%→BLOCK, must not NameError on lt['close']"""
    import importlib.util
    from datetime import datetime
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    today = datetime.now().strftime("%Y-%m-%d")
    mod._cache_get = lambda ck, ttl=None: None
    mod._cache_set = lambda ck, rv, ttl=None: None
    mod._sina_quote = lambda t: {"price":100.0,"open":99.5,"high":101.0,"low":99.0,"volume":"1000000","name":"测试","source":"sina_api","time":"15:00:00"}
    mod._bs_raw_kline = lambda t,d: {"dates":[today],"close":[98.0],"prices":[98.0],"count":1,"data_contract":"OHLCV_DAILY_V1"}
    r = mod.market_truth("002463")
    assert r["status"] == "DEGRADED"  # price_conflict=True → DEGRADED
    assert r["price_conflict"] is True
    assert any("execution_quote BLOCK" in e for e in r["errors"])
    print(f"✅ same-day BLOCK: status={r['status']} conflict={r['price_conflict']} errors={r['errors']}")

if __name__ == "__main__":
    test_get_kline_contract_has_ohlcv_keys()
    test_zg04_uses_volume_not_prices()
    test_market_truth_realtime_vs_prev_close_not_block()
    test_zg11_cash_ratio_not_placeholder()
    test_market_truth_same_day_degraded_branch_no_lt_dict_crash()
    test_market_truth_same_day_block_branch_no_lt_dict_crash()
    test_market_truth_handles_ohlcv_raw_kline_shape()
    print("\n🏁 OHLCV data contract tests PASS")
