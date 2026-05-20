"""Global pipelines universe contract — no hardcoded presets, all use UniverseProvider"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_zg09_no_hardcoded_preset():
    source = open("pipelines/Z-G09_全局轮动筛选/gate_pipeline.py", encoding="utf-8").read()
    assert "preset = [" not in source, "Z-G09 still has hardcoded preset"
    assert "load_universe" in source, "Z-G09 does not use UniverseProvider"
    print("✅ Z-G09: no preset, uses load_universe")


def test_zg10_no_hardcoded_preset():
    source = open("pipelines/Z-G10_全局黑马筛选/gate_pipeline.py", encoding="utf-8").read()
    assert "preset = [" not in source, "Z-G10 still has hardcoded preset"
    assert "load_universe" in source, "Z-G10 does not use UniverseProvider"
    print("✅ Z-G10: no preset, uses load_universe")


def test_zg14_no_memory_preset_strict_fail_closed():
    source = open("pipelines/Z-G14_月度全量选股/gate_pipeline.py", encoding="utf-8").read()
    assert "preset = [" not in source, "Z-G14 still has hardcoded preset"
    assert "allow_fallback=False" in source, "Z-G14 should not allow fallback"
    assert "Z-G14 requires A_SHARE_ALL" in source, "Z-G14 missing fail-closed sanity check"
    assert "load_universe" in source, "Z-G14 does not use UniverseProvider"
    print("✅ Z-G14: no preset, allow_fallback=False, fail-closed, uses load_universe")


def test_zg09_zg10_zg14_output_universe_contract():
    """All three pipelines include universe_contract in their result dict"""
    for code, path in [("Z-G09", "pipelines/Z-G09_全局轮动筛选/gate_pipeline.py"),
                        ("Z-G10", "pipelines/Z-G10_全局黑马筛选/gate_pipeline.py"),
                        ("Z-G14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")]:
        source = open(path, encoding="utf-8").read()
        assert "universe_contract" in source, f"{code} missing universe_contract in output"
    print("✅ Z-G09/Z-G10/Z-G14 all output universe_contract")


def test_zg14_returns_data_gap_when_universe_unavailable():
    """Z-G14 returns DATA_GAP when universe fails (strict fail-closed)"""
    spec = importlib.util.spec_from_file_location("zg14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)

    # Inject load_universe to simulate failure BEFORE pipeline loads
    import pipelines.universe_provider as up
    orig = up.load_universe
    up.load_universe = lambda **kw: {
        "status": "DATA_GAP", "source": "A_SHARE_ALL", "tickers": [], "count": 0,
        "is_global": False, "universe_level": "FULL_MARKET",
        "fallback_used": False, "warnings": ["mock gap"],
    }
    try:
        spec.loader.exec_module(mod)
        r = mod.run()
        assert r["status"] == "DATA_GAP", f"expected DATA_GAP got {r.get('status')}"
        assert r["candidates"] == []
        assert r["sections"]["universe"]["status"] == "REJECTED"
        print(f"✅ Z-G14 universe fail→DATA_GAP candidates=[]")
    finally:
        up.load_universe = orig


def test_zg09_non_global_marks_warning():
    """Z-G09 with non-global universe adds NON_GLOBAL_UNIVERSE warning"""
    spec = importlib.util.spec_from_file_location("zg09", "pipelines/Z-G09_全局轮动筛选/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    
    import pipelines.universe_provider as up
    orig = up.load_universe
    up.load_universe = lambda **kw: {
        "status": "PASS", "source": "WATCHLIST", "tickers": ["002463", "601899"], "count": 2,
        "is_global": False, "universe_level": "WATCHLIST",
        "fallback_used": False, "warnings": [],
    }
    try:
        spec.loader.exec_module(mod)
        mod.market_truth = lambda t: {"status": "PASS", "name": "测试"}
        mod.l4_health = lambda t: {"status": "PASS"}
        mod.get_kline = lambda t, d: {"prices": [10]*300, "count": 300}
        r = mod.run(pool_size=80, universe="WATCHLIST")
        assert "NON_GLOBAL_UNIVERSE" in r.get("warnings", [])
        assert r["pipeline_signature"] == "Z-G09_R-Matrix_non_global_universe"
        print(f"✅ Z-G09 WATCHLIST: sig={r['pipeline_signature']} warnings={r['warnings']}")
    finally:
        up.load_universe = orig


if __name__ == "__main__":
    test_zg09_no_hardcoded_preset()
    test_zg10_no_hardcoded_preset()
    test_zg14_no_memory_preset_strict_fail_closed()
    test_zg09_zg10_zg14_output_universe_contract()
    test_zg14_returns_data_gap_when_universe_unavailable()
    test_zg09_non_global_marks_warning()
    print("\n🏁 global pipelines universe contract tests PASS")
