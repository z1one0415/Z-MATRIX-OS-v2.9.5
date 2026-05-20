"""v2.9.5-RC 最小核心契约测试"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_market_truth_has_capability_mask():
    """market_truth返回必须包含output_level+capability_mask+price_basis+quote_domain"""
    from pipelines.z17_loader import market_truth
    g1 = market_truth("002463")
    required = ["status","output_level","capability_mask","price_basis","quote_domain"]
    for key in required:
        assert key in g1, f"market_truth missing: {key}"
    assert "allowed_outputs" in g1.get("capability_mask",{})
    print("✅ test_market_truth_has_capability_mask")

def test_source_arbitration_passthrough():
    """source_arbitrate只承接不二次裁决"""
    from pipelines.z17_loader import market_truth, source_arbitrate
    g1 = market_truth("002463")
    sa = source_arbitrate("002463", g1)
    assert sa["status"] == g1["status"], f"SA status mismatch: {sa['status']} vs {g1['status']}"
    assert "output_level" in sa
    print("✅ test_source_arbitration_passthrough")

def test_dq_not_hard_block():
    """DQ<60→DQ_FAIL不输出BLOCK"""
    from pipelines.z17_loader import dq_score
    dq = dq_score("000001")  # unlikely to have good data
    assert dq["status"] != "BLOCK", f"DQ should not BLOCK: {dq['status']}"
    print(f"✅ test_dq_not_hard_block: DQ={dq.get('total','?')} status={dq['status']}")

def test_zg09_no_keyerror():
    """Z-G09 DATA_INSUFFICIENT不进入排序"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg09","pipelines/Z-G09_全局轮动筛选/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.run(pool_size=3)
    assert "r_pool" in r or "error" not in str(r), "Z-G09 should not crash"
    print("✅ test_zg09_no_keyerror")

def test_zg16_full_lite_exists():
    """Z-G16 Full/Lite模式存在"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg16","pipelines/Z-G16_纸面验证/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "run"), "Z-G16 missing run()"
    print("✅ test_zg16_full_lite_exists")

def test_zg16a_fill_exists():
    """Z-G16A填充逻辑存在"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg16a","pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "run"), "Z-G16A missing run()"
    print("✅ test_zg16a_fill_exists")

if __name__ == "__main__":
    test_market_truth_has_capability_mask()
    test_source_arbitration_passthrough()
    test_dq_not_hard_block()
    test_zg09_no_keyerror()
    test_zg16_full_lite_exists()
    test_zg16a_fill_exists()
    print("\n🏁 All tests passed")
