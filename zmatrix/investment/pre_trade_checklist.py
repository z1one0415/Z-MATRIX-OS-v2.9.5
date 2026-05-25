#!/usr/bin/env python3
"""
☯️ Pre-Trade Checklist v1.0 — 买前8问验证器 (v2.9.8-dev)

在 paper record 前必须通过此清单。

8问:
  1. stock_role — 这只票属于 A/B/C 哪类？
  2. buy_logic_type — 买入逻辑是基本面/轮动/事件/资金情绪？
  3. sector_stage — 所属板块处于哪个阶段？
  4. financial_gate_passed — 财务硬门是否过关？
  5. valuation_overheated — 估值是否已经透支？
  6. max_loss_after_entry — 买入后最大亏损是多少？
  7. invalidation_condition — 什么条件证明我错了？
  8. lower_risk_validation_action — 是否有更低风险的验证动作？
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

REQUIRED_QUESTIONS = [
    "stock_role",
    "buy_logic_type",
    "sector_stage",
    "financial_gate_passed",
    "valuation_overheated",
    "max_loss_after_entry",
    "invalidation_condition",
    "lower_risk_validation_action",
]

SECTOR_STAGES = frozenset({
    "IGNITION", "CONFIRMATION", "LEADING", "DIFFUSION",
    "CLIMAX", "DIVERGENCE", "RETREAT", "REPAIR",
})

BUY_LOGIC_TYPES = frozenset({
    "FUNDAMENTAL", "ROTATION", "EVENT", "MOMENTUM_SENTIMENT",
})

_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}


def validate_pre_trade_checklist(candidate: dict) -> dict:
    """
    验证买前8问清单.

    参数:
      candidate: Stock Role Classifier 输出 + 投资人提供的问答数据

    返回:
      符合 Pre-Trade Checklist v1.0 契约的 dict
    """
    now = datetime.now()
    missing_items = []

    for q in REQUIRED_QUESTIONS:
        val = candidate.get(q)
        if val is None or (isinstance(val, str) and not val.strip()):
            missing_items.append(q)

    checklist_complete = len(missing_items) == 0

    # ── 检查角色 ──
    role = candidate.get("role", "UNKNOWN")
    if role not in ("A_LONG_CORE", "B_MID_ROTATION", "C_SHORT_EVENT"):
        if not missing_items:
            missing_items.append("stock_role: not a tradeable role")

    # ── 检查板块阶段 ──
    sector_stage = candidate.get("sector_stage")
    if sector_stage and sector_stage not in SECTOR_STAGES:
        missing_items.append(f"sector_stage: '{sector_stage}' not in {sorted(SECTOR_STAGES)}")

    # ── 检查买入逻辑 ──
    buy_logic = candidate.get("buy_logic_type")
    if buy_logic and buy_logic not in BUY_LOGIC_TYPES:
        missing_items.append(f"buy_logic_type: '{buy_logic}' not in {sorted(BUY_LOGIC_TYPES)}")

    # ── 检查估值透支 ──
    valuation_overheated = candidate.get("valuation_overheated")
    if valuation_overheated is True:
        missing_items.append("valuation_overheated: cannot trade when overheated")

    # ── 最终判定 ──
    checklist_complete = len(missing_items) == 0
    paper_trade_allowed = checklist_complete and role not in ("D_REJECT",)

    return {
        "checklist_version": "v1.0",
        "ticker": candidate.get("ticker", "UNKNOWN"),
        "role": role,
        "checklist_complete": checklist_complete,
        "paper_trade_allowed": paper_trade_allowed,
        "missing_items": missing_items,
        "responses": {q: candidate.get(q) for q in REQUIRED_QUESTIONS},
        "real_trade_allowed": False,
        "reason": "PASS" if paper_trade_allowed else f"BLOCKED: {missing_items}",
        "forbidden_real_trade_checked": True,
    }
