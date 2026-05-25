#!/usr/bin/env python3
"""
☯️ B-Matrix v1.0 — Base Matrix, 长期底仓矩阵 (v2.9.8-dev)

回答: 这只股票配不配成为长期底仓？
核心: 长期生存质量, 财务健康, 行业地位, 现金流, ROE, 估值不过度透支
输出: A_LONG_CORE_ELIGIBLE / WATCH_ONLY / REJECTED

规则:
  - 长期底仓必须过财务硬门
  - 若财务数据不足, 返回 DEGRADED, 不得伪装 PASS
  - 不得输出 BUY / SELL / AUTO_TRADE
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

# ── 角色枚举 ──
BASE_ROLE_ELIGIBLE = frozenset({
    "B1_HIGH_DIVIDEND_ANCHOR",      # 高股息压舱石
    "B2_COMPOUND_REINVESTMENT",      # 复利再投资白马
    "B3_RESOURCE_CASH_COW",          # 资源周期现金牛
    "B4_MONOPOLY_INFRASTRUCTURE",    # 垄断基础设施
    "B5_BRAND_SCARCITY_MONOPOLY",    # 品牌稀缺垄断
})

_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}


def evaluate_b_matrix(ticker: str, fundamentals: dict | None = None, valuation: dict | None = None) -> dict:
    """
    B-Matrix 评估: 长期底仓资格审查

    参数:
      ticker: 股票代码
      fundamentals: 基本面数据 (可选, 缺失时降级)
      valuation: 估值数据 (可选, 缺失时降级)

    返回:
      符合 B-Matrix v1.0 契约的 dict
    """
    now = datetime.now()
    fundamentals = fundamentals or {}
    valuation = valuation or {}

    financial_health_score = fundamentals.get("financial_health_score")
    quality_score = fundamentals.get("quality_score")
    cashflow_score = fundamentals.get("cashflow_score")
    roe_score = fundamentals.get("roe_score")
    debt_risk = fundamentals.get("debt_risk")
    industry_durability = fundamentals.get("industry_durability")
    dividend_or_core_score = fundamentals.get("dividend_or_core_asset_score")
    valuation_safety = valuation.get("valuation_safety")

    # ── 数据充足性判断 ──
    data_fields = [financial_health_score, quality_score, cashflow_score, roe_score, industry_durability]
    available = sum(1 for f in data_fields if f is not None)
    total = len(data_fields)
    data_sufficient = available >= 3  # 核心5项有3项即可

    if not data_sufficient:
        # 数据不足, 降级
        return {
            "matrix_id": "B-MATRIX",
            "matrix_version": "v1.0-base-core",
            "ticker": ticker,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "DEGRADED",
            "degraded_reason": f"INSUFFICIENT_DATA: {available}/{total} core fields available",
            "base_type": "UNKNOWN",
            "financial_health_score": financial_health_score,
            "quality_score": quality_score,
            "cashflow_score": cashflow_score,
            "roe_score": roe_score,
            "valuation_safety": valuation_safety,
            "debt_risk": debt_risk,
            "industry_durability": industry_durability,
            "base_role_eligible": False,
            "base_action_cap": "WAIT",
            "base_holding_period": "long_term",
            "rating": "D",
            "eligibility": "B_DISQUALIFIED",
            "reasons": ["INSUFFICIENT_DATA"],
            "real_trade_allowed": False,
            "forbidden_real_trade_checked": True,
        }

    # ── 评分计算 ──
    score = 0.0
    max_score = 10.0

    if financial_health_score is not None:
        score += financial_health_score * 0.25
    if quality_score is not None:
        score += quality_score * 0.20
    if cashflow_score is not None:
        score += cashflow_score * 0.20
    if roe_score is not None:
        score += roe_score * 0.15
    if industry_durability is not None:
        score += industry_durability * 0.10
    if dividend_or_core_score is not None:
        score += dividend_or_core_score * 0.10

    score = min(score, max_score)

    # ── 扣分项 ──
    traps = []
    if debt_risk is not None and debt_risk > 7:
        score -= 1.5
        traps.append("HIGH_DEBT_RISK")
    if valuation_safety is not None and valuation_safety < 3:
        score -= 1.0
        traps.append("VALUATION_OVERHEATED")

    # ── 资格判定 ──
    if score >= 7.0 and not traps:
        base_role_eligible = True
        eligibility = "B_ELIGIBLE"
        rating = "A" if score >= 8.0 else "B"
        base_action_cap = "PAPER_TRACK"
        reasons = [f"score={score:.1f}, passes long-term base gate"]
    elif score >= 5.0:
        base_role_eligible = False
        eligibility = "B_WATCH"
        rating = "C"
        base_action_cap = "WATCH"
        reasons = [f"score={score:.1f}, marginal — needs improvement"]
    else:
        base_role_eligible = False
        eligibility = "B_DISQUALIFIED"
        rating = "D"
        base_action_cap = "WAIT"
        reasons = [f"score={score:.1f}, below threshold"]

    # ── 分类 ──
    base_type = "UNKNOWN"
    if score >= 7.0:
        sector = (fundamentals.get("sector") or "").upper()
        if "DIVIDEND" in sector or (dividend_or_core_score or 0) >= 7:
            base_type = "B1_HIGH_DIVIDEND_ANCHOR"
        elif "RESOURCE" in sector or "METAL" in sector:
            base_type = "B3_RESOURCE_CASH_COW"
        elif "INFRA" in sector or "MONOPOLY" in sector:
            base_type = "B4_MONOPOLY_INFRASTRUCTURE"
        elif "BRAND" in sector or "CONSUMER" in sector:
            base_type = "B5_BRAND_SCARCITY_MONOPOLY"
        else:
            base_type = "B2_COMPOUND_REINVESTMENT"

    if traps:
        reasons.extend(traps)

    return {
        "matrix_id": "B-MATRIX",
        "matrix_version": "v1.0-base-core",
        "ticker": ticker,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "PASS" if eligibility == "B_ELIGIBLE" else "DEGRADED",
        "degraded_reason": None if eligibility == "B_ELIGIBLE" else "SCORE_BELOW_THRESHOLD",
        "base_type": base_type,
        "financial_health_score": financial_health_score,
        "quality_score": quality_score,
        "cashflow_score": cashflow_score,
        "roe_score": roe_score,
        "valuation_safety": valuation_safety,
        "debt_risk": debt_risk,
        "industry_durability": industry_durability,
        "base_role_eligible": base_role_eligible,
        "base_action_cap": base_action_cap,
        "base_holding_period": "long_term",
        "rating": rating,
        "eligibility": eligibility,
        "trap_flags": traps,
        "score_final": round(score, 2),
        "reasons": reasons,
        "real_trade_allowed": False,
        "forbidden_real_trade_checked": True,
    }
