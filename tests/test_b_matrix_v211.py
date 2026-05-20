"""B-Matrix v2.1.1 unit tests — classification, traps, no trade action leak"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.scoring.b_matrix import (
    BMatrixInput, BMatrixResult, BaseType, BRating, BEligibility, evaluate_b_matrix
)


def test_b5_brand_scarcity_classification():
    """高端白酒品牌稀缺→BRAND_SCARCITY_MONOPOLY"""
    stock = BMatrixInput(
        symbol="600519", name="贵州茅台", industry="高端白酒",
        brand_premium_score=9, pricing_power_score=9, supply_constraint_score=9,
        scarcity_durability_score=9, brand_mindshare_score=9,
        channel_health_score=8, dividend_yield=2.5, roic_5y=25,
        gross_margin=80,
    )
    r = evaluate_b_matrix(stock)
    assert r.base_type == BaseType.BRAND_SCARCITY_MONOPOLY, f"got {r.base_type}"
    assert r.matrix == "B_MATRIX"
    assert r.eligibility in {
        BEligibility.B_ELIGIBLE, BEligibility.B_WATCH, BEligibility.B_HOLD, BEligibility.B_REVIEW,
    }
    assert r.score_final >= 0
    assert r.rating in {BRating.A, BRating.B, BRating.C, BRating.D}
    print(f"✅ B5 茅台→{r.base_type.value} eligibility={r.eligibility.value} rating={r.rating.value} score={r.score_final:.1f}")


def test_not_b_matrix_for_st():
    stock = BMatrixInput(symbol="000000", name="ST测试", is_st=True)
    r = evaluate_b_matrix(stock)
    assert r.base_type == BaseType.NOT_B_MATRIX
    assert r.eligibility == BEligibility.B_DISQUALIFIED
    assert r.score_final == 0.0
    print(f"✅ ST→NOT_B_MATRIX / B_DISQUALIFIED")


def test_not_b_matrix_for_suspended():
    stock = BMatrixInput(symbol="000001", name="停牌测试", suspended=True)
    r = evaluate_b_matrix(stock)
    assert r.base_type == BaseType.NOT_B_MATRIX
    assert r.eligibility == BEligibility.B_DISQUALIFIED
    print(f"✅ suspended→NOT_B_MATRIX / B_DISQUALIFIED")


def test_b1_high_dividend_anchor():
    stock = BMatrixInput(symbol="601398", name="工商银行", industry="银行",
                         is_state_owned=True, dividend_yield=5.5,
                         roe_5y=12, debt_ratio=0.85,
                         ocf_3y=[100,110,120], net_profit_3y=[80,85,90])
    r = evaluate_b_matrix(stock)
    assert r.base_type == BaseType.HIGH_DIVIDEND_ANCHOR
    print(f"✅ B1 银行→{r.eligibility.value} score={r.score_final:.1f}")


def test_b3_resource_cash_cow():
    stock = BMatrixInput(symbol="601899", name="紫金矿业", industry="有色金属",
                         cost_curve_score=8, resource_quality_score=8,
                         profit_percentile_5y=0.85, roe_5y=15, debt_ratio=0.42)
    r = evaluate_b_matrix(stock)
    assert r.base_type == BaseType.RESOURCE_CASH_COW
    # B3 cycle detection may lower score
    print(f"✅ B3 资源→{r.eligibility.value} score={r.score_final:.1f} traps={r.trap_flags}")


def test_b4_state_infra_monopoly():
    stock = BMatrixInput(symbol="600900", name="长江电力", industry="能源基础设施",
                         is_state_owned=True, asset_monopoly_score=9,
                         dividend_yield=3.8, ocf_3y=[50,52,55], net_profit_3y=[48,50,52])
    r = evaluate_b_matrix(stock)
    assert r.base_type == BaseType.STATE_INFRA_MONOPOLY
    print(f"✅ B4 垄断→{r.eligibility.value} score={r.score_final:.1f}")


def test_b_matrix_no_trade_action_leak():
    """B-Matrix 禁止输出 BUY/ADD/CLEAR/HEAVY_POSITION"""
    samples = [
        BMatrixInput(symbol="600519", name="茅台", industry="高端白酒",
                     brand_premium_score=9, pricing_power_score=9, supply_constraint_score=9,
                     brand_mindshare_score=9, roic_5y=25, gross_margin=80),
        BMatrixInput(symbol="601398", name="工行", industry="银行",
                     is_state_owned=True, dividend_yield=5.5),
        BMatrixInput(symbol="601899", name="紫金", industry="有色金属",
                     cost_curve_score=8, resource_quality_score=8, profit_percentile_5y=0.85),
    ]
    for s in samples:
        r = evaluate_b_matrix(s)
        r.validate_no_trade_action()  # must not raise
        # Also check output strings
        output = str(r.eligibility.value) + " ".join(r.next_trigger) + " ".join(r.forbidden)
        for forbidden in ("BUY", "ADD", "CLEAR", "HEAVY_POSITION"):
            assert forbidden not in output.split(), f"leaked {forbidden} in {s.symbol}"
    print(f"✅ {len(samples)} samples passed no-trade-action check")


if __name__ == "__main__":
    test_b5_brand_scarcity_classification()
    test_not_b_matrix_for_st()
    test_not_b_matrix_for_suspended()
    test_b1_high_dividend_anchor()
    test_b3_resource_cash_cow()
    test_b4_state_infra_monopoly()
    test_b_matrix_no_trade_action_leak()
    print("\n🏁 B-Matrix v2.1.1 unit tests PASS")
