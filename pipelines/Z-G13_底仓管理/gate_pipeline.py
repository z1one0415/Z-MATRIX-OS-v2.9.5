#!/usr/bin/env python3
"""☯️ Z-G13 底仓管理 — v2.1.1 | 每月+财报后 | B-Matrix v2.1.1 五类底仓资格闸门"""
import argparse, json, os, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
MEMORY_MD = WORKSPACE.parent / "MEMORY.md"
sys.path.insert(0, str(WORKSPACE))
try: from pipelines.z17_loader import market_truth, get_financials, dq_score, l4_health
except: market_truth = lambda t: {"status":"stub"}; get_financials = lambda t: {}; dq_score = lambda t: {"total":0}; l4_health = lambda t: {"status":"stub"}

try:
    from zmatrix.scoring.b_matrix import BMatrixInput, BMatrixResult, BaseType, BRating, BEligibility, evaluate_b_matrix
    _B_MATRIX_LOADED = True
except ImportError as e:
    _B_MATRIX_LOADED = False
    _B_IMPORT_ERR = str(e)


def _build_bmatrix_input(ticker, name):
    """Build BMatrixInput from available data sources. Fields absent from
    get_financials default to None — B-Matrix pricers degrade gracefully."""
    g1 = market_truth(ticker)
    fin = get_financials(ticker)
    dq = dq_score(ticker)
    l4 = l4_health(ticker)

    return BMatrixInput(
        symbol=ticker,
        name=name or g1.get("name",""),
        industry=g1.get("industry", fin.get("industry", "")),
        is_state_owned=fin.get("is_state_owned", g1.get("is_state_owned", False)),
        is_market_leader=g1.get("is_market_leader", False),
        is_st=g1.get("is_st", False),
        suspended=l4.get("status") == "BLOCK",
        delisting_risk=bool(l4.get("delisting_risk")),
        # Profitability
        roe_5y=fin.get("roe_5y_avg"),
        roe_trend=fin.get("roe_trend"),
        roic_5y=fin.get("roic_5y"),
        roic_trend=fin.get("roic_trend"),
        gross_margin=fin.get("gross_margin"),
        # Valuation
        pe_ttm=fin.get("pe_ttm"),
        pb=fin.get("pb"),
        profit_percentile_5y=fin.get("profit_percentile_5y"),
        # Balance sheet
        debt_ratio=fin.get("debt_ratio"),
        goodwill_to_net_assets=fin.get("goodwill_to_net_assets"),
        # Dividend
        dividend_yield=fin.get("dividend_yield"),
        dividend_years_stable=fin.get("dividend_years_stable"),
        dividends_paid_2y=fin.get("dividends_paid_2y"),
        capex_2y=fin.get("capex_2y"),
        ocf_2y=fin.get("ocf_2y"),
        # Time-series
        ocf_3y=fin.get("ocf_3y"),
        net_profit_3y=fin.get("net_profit_3y"),
        # Qualitative
        policy_stability_score=fin.get("policy_stability_score"),
        asset_monopoly_score=fin.get("asset_monopoly_score"),
        cost_curve_score=fin.get("cost_curve_score"),
        resource_quality_score=fin.get("resource_quality_score"),
        # Brand scarcity (B5)
        brand_premium_score=fin.get("brand_premium_score"),
        pricing_power_score=fin.get("pricing_power_score"),
        supply_constraint_score=fin.get("supply_constraint_score"),
    )


def _check_thesis(ticker, name):
    """Thesis Stop: 检查底仓逻辑是否证伪"""
    fin = get_financials(ticker)
    dq = dq_score(ticker)
    l4 = l4_health(ticker)
    flags = []
    if not fin.get("has_finance"): flags.append("财报数据不可用")
    if dq.get("total", 0) < 60: flags.append(f"DQ={dq['total']}<60, 数据质量恶化")
    if l4.get("status") == "BLOCK": flags.append(f"L4 BLOCK: {l4.get('errors',['未知'])[0]}")
    if len(flags) >= 2: return "THESIS_REVIEW_REQUIRED", flags
    elif flags: return "THESIS_WATCH", flags
    return "THESIS_INTACT", []


def run():
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G13_底仓管理_v2.9.5-draft","timestamp":now.isoformat()}

    print(f"\n☯️ Z-G13 底仓管理 — 每月 B-Matrix v2.1.1 五类底仓资格闸门")
    print("=" * 60)

    if not _B_MATRIX_LOADED:
        print(f"🔴 B-Matrix v2.1.1 加载失败: {_B_IMPORT_ERR}")
        result["status"] = "B_MATRIX_UNAVAILABLE"
        return result

    positions = []
    if MEMORY_MD.exists():
        for m in re.finditer(r'\|\s*([^|]+?)\s+(\d{6})\s*\|\s*([\d,]+股)\s*\|', open(MEMORY_MD).read()):
            positions.append({"name":m.group(1).strip(),"code":m.group(2),"shares":int(m.group(3).replace("股","").replace(",",""))})

    if not positions:
        print("⚠️ 无持仓数据")
        return result

    print(f"📊 持仓 {len(positions)}只 → B-Matrix v2.1.1 五类资格闸门 + Thesis复核\n")

    # Type legend
    B_TYPE_MAP = {
        BaseType.HIGH_DIVIDEND_ANCHOR: "B1高股息压舱石",
        BaseType.COMPOUNDING_QUALITY: "B2复利再投资",
        BaseType.RESOURCE_CASH_COW: "B3资源现金牛",
        BaseType.STATE_INFRA_MONOPOLY: "B4垄断基础设施",
        BaseType.BRAND_SCARCITY_MONOPOLY: "B5品牌稀缺垄断",
        BaseType.NOT_B_MATRIX: "🚫 非B-Matrix",
    }

    b_results = []
    for p in positions:
        # Build input + run B-Matrix v2.1.1
        stock = _build_bmatrix_input(p["code"], p["name"])
        bm = evaluate_b_matrix(stock)
        
        # Thesis check
        thesis, tflags = _check_thesis(p["code"], p["name"])
        
        # Traps summary
        trap_summary = bm.trap_flags if bm.trap_flags else []
        
        icon_map = {
            BEligibility.B_ELIGIBLE: "🟢",
            BEligibility.B_WATCH: "🟡",
            BEligibility.B_ACCUMULATION_CANDIDATE: "🟣",
            BEligibility.B_HOLD: "🔵",
            BEligibility.B_REVIEW: "🟠",
            BEligibility.B_DISQUALIFIED: "🔴",
        }
        icon = icon_map.get(bm.eligibility, "❓")

        print(f"  {icon} {p['code']} {p['name']:<8s}| {B_TYPE_MAP[bm.base_type]:<14s}| "
              f"评分{bm.score_final:.1f}({bm.rating.value})| {bm.eligibility.value:<14s}| "
              f"Thesis:{thesis} {'⚠️'+','.join(tflags) if tflags else ''}")
        if trap_summary:
            print(f"     🚩 Traps: {', '.join(trap_summary)}")
        
        b_results.append({
            "code": p["code"], "name": p["name"],
            "base_type": bm.base_type.value,
            "score_raw": round(bm.score_raw, 2),
            "score_final": round(bm.score_final, 2),
            "rating": bm.rating.value,
            "eligibility": bm.eligibility.value,
            "traps": bm.trap_flags,
            "thesis": thesis,
            "thesis_flags": tflags,
        })

    # Summary
    types = {bm["base_type"] for bm in b_results}
    eligible = sum(1 for bm in b_results if bm["eligibility"] == "B_ELIGIBLE")
    print(f"\n📊 底仓小结: {len(b_results)}只 | 类型{len(types)}种 | B_ELIGIBLE {eligible}只 | "
          f"B_WATCH {sum(1 for b in b_results if b['eligibility']=='B_WATCH')} | "
          f"B_HOLD {sum(1 for b in b_results if b['eligibility']=='B_HOLD')} | "
          f"B_REVIEW {sum(1 for b in b_results if b['eligibility']=='B_REVIEW')} | "
          f"DISQ {sum(1 for b in b_results if b['eligibility']=='B_DISQUALIFIED')}")

    result["b_pool"] = b_results
    result["sections"] = {
        "total": len(b_results),
        "types_count": len(types),
        "eligible": eligible,
        "watch": sum(1 for b in b_results if b["eligibility"] == "B_WATCH"),
        "accumulation_candidate": sum(1 for b in b_results if b["eligibility"] == "B_ACCUMULATION_CANDIDATE"),
        "hold": sum(1 for b in b_results if b["eligibility"] == "B_HOLD"),
        "review": sum(1 for b in b_results if b["eligibility"] == "B_REVIEW"),
        "disqualified": sum(1 for b in b_results if b["eligibility"] == "B_DISQUALIFIED"),
    }
    return result

if __name__ == "__main__":
    run()
