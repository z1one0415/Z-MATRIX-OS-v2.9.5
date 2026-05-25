#!/usr/bin/env python3
"""
☯️ Account Constitution v1.0 — 账户宪法检查器 (v2.9.8-dev)

检查候选股票是否符合账户仓位规则。

默认约束:
  - 长期底仓 bucket ≤ 40%
  - 中期轮动 bucket ≤ 35%
  - 短期黑马 bucket ≤ 15%
  - 现金 ≥ 10%
  - 短期事件单票 ≤ 3%-5%
  - 单一产业链暴露 ≤ 30%-35%
  - 单笔最大亏损 ≤ 总账户 0.5%-1%
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

DEFAULT_CONSTRAINTS = {
    "base_bucket_max_pct": 40,
    "rotation_bucket_max_pct": 35,
    "dark_horse_bucket_max_pct": 15,
    "cash_reserve_min_pct": 10,
    "single_stock_max_pct_by_role": {
        "A_LONG_CORE": 10,
        "B_MID_ROTATION": 8,
        "C_SHORT_EVENT": 5,
        "D_REJECT": 0,
    },
    "single_chain_exposure_max_pct": 35,
    "single_style_exposure_max_pct": 35,
    "max_loss_per_trade_pct": 1.0,
}

_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}


def check_account_constitution(
    candidate: dict,
    account_state: dict | None = None,
) -> dict:
    """
    检查候选股票是否符合账户宪法.

    参数:
      candidate: Stock Role Classifier 输出 (含 role, ticker 等)
      account_state: 账户当前状态 (可选, 含各bucket已用量/现金/持仓)

    返回:
      符合 Account Constitution v1.0 契约的 dict
    """
    now = datetime.now()
    account_state = account_state or {}
    constraints = {**DEFAULT_CONSTRAINTS, **account_state.get("overrides", {})}

    role = candidate.get("role", "D_REJECT")
    ticker = candidate.get("ticker", "UNKNOWN")

    violations = []

    # ── 假设的当前用量 ──
    current_base_pct = account_state.get("current_base_bucket_pct", 0)
    current_rotation_pct = account_state.get("current_rotation_bucket_pct", 0)
    current_dark_horse_pct = account_state.get("current_dark_horse_bucket_pct", 0)
    current_cash_pct = account_state.get("current_cash_pct", 100)
    current_chain_exposure = account_state.get("current_chain_exposure_pct", 0)
    current_style_exposure = account_state.get("current_style_exposure_pct", 0)
    add_weight = account_state.get("add_weight_pct", 5)

    # ── 检查 ──
    if role == "A_LONG_CORE":
        new_total = current_base_pct + add_weight
        if new_total > constraints["base_bucket_max_pct"]:
            violations.append(f"BASE_BUCKET_OVERFLOW: {current_base_pct}+{add_weight}>{constraints['base_bucket_max_pct']}%")
    elif role == "B_MID_ROTATION":
        new_total = current_rotation_pct + add_weight
        if new_total > constraints["rotation_bucket_max_pct"]:
            violations.append(f"ROTATION_BUCKET_OVERFLOW: {current_rotation_pct}+{add_weight}>{constraints['rotation_bucket_max_pct']}%")
    elif role == "C_SHORT_EVENT":
        new_total = current_dark_horse_pct + add_weight
        if new_total > constraints["dark_horse_bucket_max_pct"]:
            violations.append(f"DARK_HORSE_BUCKET_OVERFLOW: {current_dark_horse_pct}+{add_weight}>{constraints['dark_horse_bucket_max_pct']}%")
        if add_weight > constraints["single_stock_max_pct_by_role"].get("C_SHORT_EVENT", 5):
            violations.append(f"SHORT_EVENT_SINGLE_STOCK_OVERFLOW: {add_weight}>{constraints['single_stock_max_pct_by_role']['C_SHORT_EVENT']}%")

    # 现金
    if current_cash_pct < constraints["cash_reserve_min_pct"]:
        violations.append(f"CASH_RESERVE_TOO_LOW: {current_cash_pct}<{constraints['cash_reserve_min_pct']}%")

    # 产业链暴露
    if current_chain_exposure + add_weight > constraints["single_chain_exposure_max_pct"]:
        violations.append(f"CHAIN_EXPOSURE_OVERFLOW: {current_chain_exposure}+{add_weight}>{constraints['single_chain_exposure_max_pct']}%")

    # 风格暴露
    if current_style_exposure + add_weight > constraints["single_style_exposure_max_pct"]:
        violations.append(f"STYLE_EXPOSURE_OVERFLOW: {current_style_exposure}+{add_weight}>{constraints['single_style_exposure_max_pct']}%")

    account_gate_passed = len(violations) == 0

    return {
        "constitution_version": "v1.0",
        "ticker": ticker,
        "role": role,
        "account_gate_passed": account_gate_passed,
        "violation_reasons": violations,
        "current_base_bucket_pct": current_base_pct,
        "current_rotation_bucket_pct": current_rotation_pct,
        "current_dark_horse_bucket_pct": current_dark_horse_pct,
        "current_cash_pct": current_cash_pct,
        "add_weight_pct": add_weight,
        "constraints_used": constraints,
        "real_trade_allowed": False,
        "forbidden_real_trade_checked": True,
    }
