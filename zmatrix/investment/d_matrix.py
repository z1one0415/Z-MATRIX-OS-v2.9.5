#!/usr/bin/env python3
"""
☯️ D-Matrix v1.0 — Dark Horse Matrix, 短期黑马/事件矩阵 (v2.9.8-dev)

回答: 这只股票是否值得做短期事件/高弹性纸面观察或小仓试错？
核心: 催化剂, 叙事热度, 资金情绪, 弹性, 泡沫温度, 事件证伪点, 止损纪律
硬规则:
  - 短线票跌破止损, 不许补仓
  - 事件证伪, 退出观察
  - 短线票不得转长期底仓
  - 不得输出 BUY / SELL / AUTO_TRADE
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}


def evaluate_d_matrix(ticker: str, narrative: dict | None = None, event: dict | None = None) -> dict:
    """
    D-Matrix 评估: 短期事件/黑马资格

    参数:
      ticker: 股票代码
      narrative: 叙事数据 (可选, 含 heat/decay/temperature)
      event: 事件数据 (可选, 含催化剂/证伪点)

    返回:
      符合 D-Matrix v1.0 契约的 dict
    """
    now = datetime.now()
    narrative = narrative or {}
    event = event or {}

    # ── 数据提取 ──
    catalyst_score = event.get("catalyst_score") or narrative.get("catalyst_score")
    narrative_heat = narrative.get("narrative_heat") or event.get("narrative_heat")
    narrative_decay = narrative.get("narrative_decay")
    bubble_temperature = narrative.get("bubble_temperature")
    event_validity = event.get("event_validity")
    fund_flow_heat = narrative.get("fund_flow_heat")
    stop_loss_pct = event.get("stop_loss_pct")
    invalidation_condition = event.get("invalidation_condition")

    # ── 数据充足性 ──
    data_fields = [catalyst_score, narrative_heat, event_validity]
    available = sum(1 for f in data_fields if f is not None)
    data_sufficient = available >= 2

    if not data_sufficient:
        return {
            "matrix_id": "D-MATRIX",
            "matrix_version": "v1.0-dark-horse",
            "ticker": ticker,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "DEGRADED",
            "degraded_reason": f"INSUFFICIENT_NARRATIVE_DATA: {available}/3",
            "catalyst_score": catalyst_score,
            "narrative_heat": narrative_heat,
            "narrative_decay": narrative_decay,
            "bubble_temperature": bubble_temperature,
            "event_validity": event_validity,
            "short_event_eligible": False,
            "stop_loss_required": True,
            "cannot_convert_to_base": True,
            "event_invalidation_condition": invalidation_condition,
            "d_action_cap": "WAIT",
            "reasons": ["INSUFFICIENT_NARRATIVE_DATA"],
            "real_trade_allowed": False,
            "forbidden_real_trade_checked": True,
        }

    # ── 评分 ──
    score = 0.0
    if catalyst_score is not None:
        score += catalyst_score * 0.30
    if narrative_heat is not None:
        score += narrative_heat * 0.25
    if fund_flow_heat is not None:
        score += fund_flow_heat * 0.15
    if event_validity is not None:
        score += event_validity * 0.20
    score = min(score, 10.0)

    # ── 扣分项 ──
    traps = []
    if narrative_decay is not None and narrative_decay < 3:
        score -= 1.0
        traps.append("NARRATIVE_DECAYING")
    if bubble_temperature is not None and bubble_temperature > 8:
        score -= 1.5
        traps.append("BUBBLE_OVERHEATED")

    # ── 资格判定 ──
    short_event_eligible = score >= 5.0 and bool(invalidation_condition)
    if short_event_eligible:
        d_action_cap = "PAPER_PROBE"
        reasons = [f"score={score:.1f}, event valid, invalidation set"]
    elif score >= 3.0:
        d_action_cap = "WATCH"
        reasons = [f"score={score:.1f}, marginal event — WATCH only"]
    else:
        d_action_cap = "WAIT"
        reasons = [f"score={score:.1f}, below threshold"]

    if traps:
        reasons.extend(traps)

    # ── 硬规则 ──
    if invalidation_condition and stop_loss_pct is None:
        reasons.append("WARNING: stop_loss_pct not set — required for short events")

    return {
        "matrix_id": "D-MATRIX",
        "matrix_version": "v1.0-dark-horse",
        "ticker": ticker,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "PASS" if short_event_eligible else "DEGRADED",
        "degraded_reason": None if short_event_eligible else "SCORE_OR_INVALIDATION_MISSING",
        "catalyst_score": catalyst_score,
        "narrative_heat": narrative_heat,
        "narrative_decay": narrative_decay,
        "bubble_temperature": bubble_temperature,
        "event_validity": event_validity,
        "short_event_eligible": short_event_eligible,
        "stop_loss_required": True,
        "cannot_convert_to_base": True,
        "event_invalidation_condition": invalidation_condition,
        "d_action_cap": d_action_cap,
        "score_final": round(score, 2),
        "trap_flags": traps,
        "reasons": reasons,
        "real_trade_allowed": False,
        "forbidden_real_trade_checked": True,
    }
