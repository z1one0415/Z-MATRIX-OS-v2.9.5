"""Z-G13 B-Matrix v2.1.1 integration test — mocked data, no live network"""
import sys, os, tempfile, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_zg13_run_with_mocked_positions():
    """Z-G13 run() with mocked MEMORY + mocked data → outputs b_pool"""
    spec = importlib.util.spec_from_file_location("zg13", "pipelines/Z-G13_底仓管理/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Create temp MEMORY.md with one position
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("| 贵州茅台 600519 | 100股 | 1500 |\n")
        mem_path = f.name
    
    try:
        mod.MEMORY_MD = __import__('pathlib').Path(mem_path)
        mod.market_truth = lambda t: {"status": "PASS", "name": "贵州茅台", "industry": "高端白酒"}
        mod.get_financials = lambda t: {
            "has_finance": True, "industry": "高端白酒",
            "brand_premium_score": 9, "pricing_power_score": 9,
            "supply_constraint_score": 9, "scarcity_durability_score": 9,
            "brand_mindshare_score": 9, "channel_health_score": 8,
            "roic_5y": 25, "dividend_yield": 2.5, "gross_margin": 80,
        }
        mod.dq_score = lambda t: {"total": 90}
        mod.l4_health = lambda t: {"status": "PASS", "errors": []}
        
        r = mod.run()
        
        assert "b_pool" in r, f"missing b_pool: {r.keys()}"
        assert len(r["b_pool"]) == 1, f"expected 1, got {len(r['b_pool'])}"
        b = r["b_pool"][0]
        assert b["base_type"] == "BRAND_SCARCITY_MONOPOLY", f"got {b['base_type']}"
        assert b["eligibility"] in {"B_ELIGIBLE", "B_WATCH", "B_HOLD", "B_REVIEW"}, f"got {b['eligibility']}"
        assert "sections" in r
        assert r["sections"]["total"] == 1
        print(f"✅ Z-G13 run→{b['base_type']} eligibility={b['eligibility']} score={b['score_final']}")
    finally:
        os.unlink(mem_path)


def test_zg13_icon_map_no_attribute_error():
    """BEligibility icon_map must not raise AttributeError (regression for P0-1)"""
    spec = importlib.util.spec_from_file_location("zg13", "pipelines/Z-G13_底仓管理/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Verify the module doesn't reference wrong BEligibility names
    source = open("pipelines/Z-G13_底仓管理/gate_pipeline.py").read()
    # Check no bare .WATCH .HOLD .REVIEW .DISQUALIFIED without B_ prefix
    for bad_name in ["BEligibility.WATCH", "BEligibility.HOLD", "BEligibility.REVIEW", "BEligibility.DISQUALIFIED"]:
        assert bad_name not in source, f"Z-G13 still references {bad_name}"
    print("✅ Z-G13 no bare BEligibility.WATCH/HOLD/REVIEW/DISQUALIFIED")


def test_zg13_run_not_b_matrix_rejected():
    """Z-G13 with ST stock → NOT_B_MATRIX + B_DISQUALIFIED"""
    spec = importlib.util.spec_from_file_location("zg13", "pipelines/Z-G13_底仓管理/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("| ST测试 000000 | 100股 | 500 |\n")
        mem_path = f.name
    
    try:
        mod.MEMORY_MD = __import__('pathlib').Path(mem_path)
        mod.market_truth = lambda t: {"status": "PASS", "name": "ST测试", "is_st": True}
        mod.get_financials = lambda t: {"has_finance": False}
        mod.dq_score = lambda t: {"total": 30}
        mod.l4_health = lambda t: {"status": "PASS", "errors": []}
        
        r = mod.run()
        assert len(r["b_pool"]) == 1
        b = r["b_pool"][0]
        assert b["base_type"] == "NOT_B_MATRIX", f"got {b['base_type']}"
        assert b["eligibility"] == "B_DISQUALIFIED", f"got {b['eligibility']}"
        print(f"✅ ST→NOT_B_MATRIX / B_DISQUALIFIED")
    finally:
        os.unlink(mem_path)


if __name__ == "__main__":
    test_zg13_run_with_mocked_positions()
    test_zg13_icon_map_no_attribute_error()
    test_zg13_run_not_b_matrix_rejected()
    print("\n🏁 Z-G13 B-Matrix integration tests PASS")
