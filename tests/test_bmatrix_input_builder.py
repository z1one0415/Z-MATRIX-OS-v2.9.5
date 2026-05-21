"""BMatrix input builder contract — unified field mapping for G13/G14"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_builder_maps_core_financial_fields():
    from pipelines.bmatrix_input_builder import build_bmatrix_input
    inp = build_bmatrix_input(
        "601398", "工商银行",
        market_truth_fn=lambda t: {"name": "工商银行", "industry": "银行"},
        get_financials_fn=lambda t: {
            "roe_5y_avg": 12.5, "roic_5y": 10.0,
            "pe_ttm": 8.0, "pb": 1.2,
            "dividend_yield": 5.0, "debt_ratio": 0.85,
            "ocf_3y": [100, 110, 120],
            "net_profit_3y": [80, 85, 90],
            "goodwill_ratio": 0.01,
            "financial_coverage_ratio": 0.8,
            "missing_fields": [],
        },
        dq_score_fn=lambda t: {"total": 85},
        l4_health_fn=lambda t: {"status": "PASS"},
    )
    assert inp.goodwill_to_net_assets == 0.01
    assert inp.data_completeness == 0.8
    assert inp.roe_5y == 12.5
    assert inp.pe_ttm == 8.0
    assert inp.extra["financial_missing_fields"] == []
    print(f"✅ core fields: roe={inp.roe_5y} pe={inp.pe_ttm} gw={inp.goodwill_to_net_assets}")


def test_builder_maps_brand_scarcity_fields():
    from pipelines.bmatrix_input_builder import build_bmatrix_input
    inp = build_bmatrix_input(
        "600519", "贵州茅台",
        market_truth_fn=lambda t: {"name": "贵州茅台", "industry": "高端白酒"},
        get_financials_fn=lambda t: {
            "roe_5y_avg": 30.0,
            "brand_premium_score": 9.5,
            "pricing_power_score": 9.0,
            "supply_constraint_score": 9.0,
            "scarcity_durability_score": 9.0,
            "brand_mindshare_score": 9.5,
            "channel_health_score": 8.0,
            "financial_coverage_ratio": 0.6,
            "missing_fields": ["ocf_3y"],
        },
        dq_score_fn=lambda t: {"total": 90},
        l4_health_fn=lambda t: {"status": "PASS"},
    )
    assert inp.brand_premium_score == 9.5
    assert inp.scarcity_durability_score == 9.0
    assert inp.brand_mindshare_score == 9.5
    assert inp.channel_health_score == 8.0
    assert inp.data_completeness == 0.6
    assert inp.extra["financial_missing_fields"] == ["ocf_3y"]
    print(f"✅ B5 fields: brand={inp.brand_premium_score} scarcity={inp.scarcity_durability_score}")


def test_builder_degrades_gracefully_with_empty_financials():
    from pipelines.bmatrix_input_builder import build_bmatrix_input
    inp = build_bmatrix_input(
        "000001", "测试",
        get_financials_fn=lambda t: {"financial_coverage_ratio": 0.0, "missing_fields": ["all"]},
    )
    assert inp.goodwill_to_net_assets is None
    assert inp.data_completeness == 0.0
    print(f"✅ empty financials→coverage=0.0, no crash")


if __name__ == "__main__":
    test_builder_maps_core_financial_fields()
    test_builder_maps_brand_scarcity_fields()
    test_builder_degrades_gracefully_with_empty_financials()
    print("\n🏁 BMatrix input builder tests PASS")
