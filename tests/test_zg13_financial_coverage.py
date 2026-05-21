"""Z-G13 B-Matrix financial coverage contract tests"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_get_financials_returns_bmatrix_v1_contract():
    """get_financials returns FINANCIAL_BMATRIX_V1 shape with all required keys"""
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    required = [
        "symbol", "industry", "has_finance",
        "roe_5y_avg", "roic_5y", "pe_ttm", "pb",
        "debt_ratio", "goodwill_ratio",
        "dividend_yield", "ocf_3y", "net_profit_3y",
        "brand_premium_score", "pricing_power_score", "supply_constraint_score",
        "data_contract", "missing_fields",
    ]
    
    # Don't actually call baostock — just verify the function signature and contract shape
    mod._cache_get = lambda ck, ttl=None: None
    mod._cache_set = lambda ck, rv, ttl=None: None
    orig = mod._bs_finance
    mod._bs_finance = lambda t: {
        "symbol": t, "industry": "银行", "has_finance": True,
        "q1_eps": "1.5", "roe_5y_avg": 12.5, "roic_5y": 10.0,
        "pe_ttm": 8.0, "pb": 1.2,
        "debt_ratio": 0.85, "goodwill_ratio": 0.01,
        "dividend_yield": 5.0,
        "ocf_3y": [100, 110, 120], "net_profit_3y": [80, 85, 90],
        "brand_premium_score": None,
        "pricing_power_score": None, "supply_constraint_score": None,
        "data_contract": "FINANCIAL_BMATRIX_V1",
        "missing_fields": ["brand_premium_score", "pricing_power_score"],
        "cost_curve_score": None, "resource_quality_score": None,
        "scarcity_durability_score": None, "brand_mindshare_score": None,
        "channel_health_score": None, "policy_stability_score": None,
        "asset_monopoly_score": None,
    }
    
    try:
        r = mod.get_financials("002463")
        assert r["data_contract"] == "FINANCIAL_BMATRIX_V1"
        for k in required:
            assert k in r, f"missing key: {k}"
        assert r["missing_fields"] == ["brand_premium_score", "pricing_power_score"]
        assert r["roe_5y_avg"] == 12.5
        assert r["pe_ttm"] == 8.0
        assert r["debt_ratio"] == 0.85
        print(f"✅ FINANCIAL_BMATRIX_V1 contract: {len(r)} fields, missing={len(r['missing_fields'])}")
    finally:
        mod._bs_finance = orig


def test_get_financials_marks_missing_not_fabricates():
    """Missing fields are None, not fabricated"""
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    mod._cache_get = lambda ck, ttl=None: None
    mod._cache_set = lambda ck, rv, ttl=None: None
    orig = mod._bs_finance
    mod._bs_finance = lambda t: {
        "has_finance": False, "industry": "",
        "data_contract": "FINANCIAL_BMATRIX_V1",
        "missing_fields": ["roe_5y_avg", "pe_ttm", "pb", "dividend_yield"],
    }
    
    try:
        r = mod.get_financials("000000")
        assert r["roe_5y_avg"] is None, f"should be None, got {r['roe_5y_avg']}"
        assert r["pe_ttm"] is None
        assert r["dividend_yield"] is None
        assert len(r.get("missing_fields", [])) > 0
        print(f"✅ all missing→None: roe={r['roe_5y_avg']} pe={r['pe_ttm']} div={r['dividend_yield']}")
    finally:
        mod._bs_finance = orig


def test_zg13_outputs_financial_coverage():
    """Z-G13 b_pool item includes financial_coverage_ratio"""
    import tempfile
    spec = importlib.util.spec_from_file_location("zg13", "pipelines/Z-G13_底仓管理/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("| 测试股 002463 | 100股 | 1500 |\n")
        mem_path = f.name
    
    try:
        mod.MEMORY_MD = __import__('pathlib').Path(mem_path)
        mod.market_truth = lambda t: {"status": "PASS", "name": "测试股", "industry": "电子"}
        mod.get_financials = lambda t: {
            "has_finance": True, "industry": "电子",
            "roe_5y_avg": 15.0, "pe_ttm": 20.0, "pb": 3.0,
            "dividend_yield": 1.0, "debt_ratio": 0.35,
            "ocf_3y": [50, 60, 70], "net_profit_3y": [40, 50, 60],
            "data_contract": "FINANCIAL_BMATRIX_V1",
            "missing_fields": ["brand_premium_score"],
            "cost_curve_score": None, "resource_quality_score": None,
            "pricing_power_score": None, "supply_constraint_score": None,
            "roic_5y": None, "gross_margin": None,
        }
        mod.dq_score = lambda t: {"total": 85}
        mod.l4_health = lambda t: {"status": "PASS", "errors": []}
        
        r = mod.run()
        b = r["b_pool"][0]
        assert "financial_coverage_ratio" in b, f"missing coverage: {list(b.keys())}"
        assert "financial_missing_fields" in b
        assert "financial_data_contract" in b
        assert b["financial_data_contract"] == "FINANCIAL_BMATRIX_V1"
        # 1 missing out of 36 ≈ 0.97 coverage, not LOW
        assert b["confidence"] != "LOW_DATA_COVERAGE", f"should not be LOW at {b['financial_coverage_ratio']}"
        print(f"✅ coverage={b['financial_coverage_ratio']} missing={b['financial_missing_fields']} confidence={b['confidence']}")
    finally:
        os.unlink(mem_path)


def test_zg13_low_coverage_marks_degraded():
    """Low financial coverage (<50%) → LOW_DATA_COVERAGE"""
    import tempfile
    spec = importlib.util.spec_from_file_location("zg13", "pipelines/Z-G13_底仓管理/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("| 测试股 002463 | 100股 | 1500 |\n")
        mem_path = f.name
    
    try:
        mod.MEMORY_MD = __import__('pathlib').Path(mem_path)
        mod.market_truth = lambda t: {"status": "PASS", "name": "测试股", "industry": "电子"}
        # Only 2 fields available, everything else missing
        mod.get_financials = lambda t: {
            "has_finance": True, "industry": "电子",
            "data_contract": "FINANCIAL_BMATRIX_V1",
            "missing_fields": [f"field_{i}" for i in range(25)],  # 25 missing out of ~36
        }
        mod.dq_score = lambda t: {"total": 85}
        mod.l4_health = lambda t: {"status": "PASS", "errors": []}
        
        r = mod.run()
        b = r["b_pool"][0]
        assert b["confidence"] == "LOW_DATA_COVERAGE", f"got {b['confidence']} at {b['financial_coverage_ratio']}"
        print(f"✅ LOW_DATA_COVERAGE: coverage={b['financial_coverage_ratio']} confidence={b['confidence']}")
    finally:
        os.unlink(mem_path)



def test_zg13_goodwill_via_unified_builder():
    """BMatrixInput via unified builder maps goodwill_ratio correctly"""
    from pipelines.bmatrix_input_builder import build_bmatrix_input
    inp = build_bmatrix_input(
        "002463", "测试股",
        market_truth_fn=lambda t: {"name": "测试股", "industry": "电子"},
        get_financials_fn=lambda t: {
            "goodwill_ratio": 0.25,
            "financial_coverage_ratio": 0.7,
            "missing_fields": ["roe_5y_avg"],
        },
        dq_score_fn=lambda t: {"total": 80},
        l4_health_fn=lambda t: {"status": "PASS"},
    )
    assert inp.goodwill_to_net_assets == 0.25
    assert inp.data_completeness == 0.7
    assert inp.extra["financial_missing_fields"] == ["roe_5y_avg"]
    print(f"✅ builder: goodwill={inp.goodwill_to_net_assets} coverage={inp.data_completeness}")

if __name__ == "__main__":
    test_get_financials_returns_bmatrix_v1_contract()
    test_get_financials_marks_missing_not_fabricates()
    test_zg13_outputs_financial_coverage()
    test_zg13_low_coverage_marks_degraded()
    test_zg13_goodwill_via_unified_builder()
    print("\n🏁 Z-G13 financial coverage tests PASS")
