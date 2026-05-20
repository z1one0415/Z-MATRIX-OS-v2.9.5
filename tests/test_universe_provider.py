"""UniverseProvider contract tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_preset_dev_is_not_global():
    from pipelines.universe_provider import load_universe
    uni = load_universe("PRESET_DEV")
    assert uni["status"] == "PASS"
    assert uni["is_global"] is False
    assert uni["universe_level"] == "DEV_SAMPLE"
    assert uni["as_of"] == "static"
    assert "DEV_SAMPLE_NOT_GLOBAL" in uni["warnings"]
    print(f"✅ PRESET_DEV: is_global={uni['is_global']} level={uni['universe_level']}")


def test_watchlist_is_not_global():
    from pipelines.universe_provider import load_universe
    uni = load_universe("WATCHLIST")
    assert uni["is_global"] is False
    assert uni["universe_level"] == "WATCHLIST"
    assert "as_of" in uni
    print(f"✅ WATCHLIST: is_global={uni['is_global']} count={uni['count']}")


def test_unknown_source_returns_data_gap():
    from pipelines.universe_provider import load_universe
    uni = load_universe("NONEXISTENT_SOURCE")
    assert uni["status"] == "DATA_GAP"
    print(f"✅ unknown source→DATA_GAP")


def test_a_share_all_data_gap_with_fallback_false():
    """When baostock + cache both fail and allow_fallback=False → DATA_GAP"""
    import pipelines.universe_provider as up
    orig = up._a_share_all
    up._a_share_all = lambda allow_fallback: {
        "status": "DATA_GAP", "source": "A_SHARE_ALL", "tickers": [], "count": 0,
        "is_global": False, "universe_level": "FULL_MARKET",
        "fallback_used": False, "warnings": ["mock failure"],
    }
    try:
        uni = up.load_universe("A_SHARE_ALL", allow_fallback=False, min_count=4000)
        assert uni["status"] == "DATA_GAP"
        assert uni["is_global"] is False
        print(f"✅ A_SHARE_ALL no-fallback→DATA_GAP")
    finally:
        up._a_share_all = orig


def test_as_of_contract_exists_for_all_local_sources():
    from pipelines.universe_provider import load_universe
    for src in ["PRESET_DEV", "WATCHLIST"]:
        uni = load_universe(src)
        assert "as_of" in uni, f"{src} missing as_of"
    print("✅ as_of present for PRESET_DEV + WATCHLIST")


def test_universe_contract_has_required_fields():
    from pipelines.universe_provider import load_universe
    uni = load_universe("PRESET_DEV")
    required = ["status", "source", "tickers", "count", "is_global",
                "universe_level", "fallback_used", "warnings"]
    for k in required:
        assert k in uni, f"missing required field: {k}"
    print(f"✅ all {len(required)} required fields present")



def test_a_share_all_fallback_index_basket_not_killed_by_min_count():
    """A_SHARE_ALL fail + allow_fallback=True + index basket → DEGRADED, not DATA_GAP"""
    import pipelines.universe_provider as up
    orig_a = up._bs_all_stock
    orig_cache = up._read_cache
    orig_index = up._index_basket
    
    up._bs_all_stock = lambda today: []
    up._read_cache = lambda path, max_age_days: (None, None)
    up._index_basket = lambda src: {
        "status": "PASS", "source": src,
        "tickers": ["000001", "000002", "600000"],
        "count": 3, "is_global": False, "universe_level": src,
        "fallback_used": False, "warnings": [],
    }
    try:
        uni = up.load_universe("A_SHARE_ALL", allow_fallback=True, min_count=4000)
        assert uni["status"] == "DEGRADED", f"expected DEGRADED got {uni['status']}"
        assert uni["is_global"] is False
        assert uni["universe_level"] == "INDEX_BASKET"
        assert uni["fallback_used"] is True
        assert uni["count"] == 3
        print(f"✅ fallback index basket→DEGRADED (not DATA_GAP)")
    finally:
        up._bs_all_stock = orig_a
        up._read_cache = orig_cache
        up._index_basket = orig_index

if __name__ == "__main__":
    test_preset_dev_is_not_global()
    test_watchlist_is_not_global()
    test_unknown_source_returns_data_gap()
    test_as_of_contract_exists_for_all_local_sources()
    test_universe_contract_has_required_fields()
    test_a_share_all_data_gap_with_fallback_false()
    test_a_share_all_fallback_index_basket_not_killed_by_min_count()
    print("\n🏁 UniverseProvider tests PASS")
