#!/usr/bin/env python3
"""
☯️ Z9 Outcome Backfill Contract v1.0 — Batch D-3

功能:
  1. 将 Z9_INGESTION_QUEUE_ITEM 转换为 Z9_OUTCOME_BACKFILL_TASK preview
  2. 定义 T1/T5/T20 outcome backfill task schema、回填字段、状态机、数据需求
  3. 只做契约预览，不真实执行回填

输入: Z9_INGESTION_QUEUE_ITEM v1.0
输出: Z9_OUTCOME_BACKFILL_TASK v1.0

边界:
  - 不真实写 Z9
  - 不真实写 queue
  - 不真实拉行情
  - 不真实 outcome 回填
  - 不自动校准参数
  - 不真实交易
"""
from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any

# ── 常量 ──
ALLOWED_BACKFILL_STATUSES = [
    "WAITING_MARKET_DATA",
    "READY_FOR_BACKFILL",
    "BACKFILLED_PREVIEW",
    "REJECTED",
]

REQUIRED_QUEUE_FIELDS = [
    "queue_id",
    "sample_id",
    "ticker",
]

REQUIRED_NESTED = [
    ("idempotency", "idempotency_key"),
    ("idempotency", "dedup_key"),
    ("sample_snapshot", "outcome_placeholder"),
]

_FORBIDDEN_ACTIONS = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE",
                      "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}

OUTCOME_FIELD_NAMES = [
    "actual_return_T1", "actual_return_T5", "actual_return_T20",
    "max_drawdown_T5", "max_drawdown_T20",
    "max_runup_T5", "max_runup_T20",
    "decision_outcome", "rule_hit_accuracy",
    "false_positive_flags", "false_negative_flags",
]


def make_z9_backfill_task_key(queue_item: dict) -> str:
    """生成 backfill_task_key — 幂等, 随 queue_id / idempotency_key 变化"""
    queue_id = queue_item.get("queue_id", "")
    sample_id = queue_item.get("sample_id", "")
    ticker = queue_item.get("ticker", "")
    idem = queue_item.get("idempotency", {}) or {}
    idempotency_key = idem.get("idempotency_key", "")
    raw = queue_id + sample_id + ticker + idempotency_key
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def _check_forbidden_in_sample(snapshot: dict):
    """检查 sample_snapshot 内 action 字段是否有禁止交易"""
    fields_to_check = [
        snapshot.get("decision_snapshot", {}).get("entry_intent"),
        snapshot.get("decision_snapshot", {}).get("exit_intent"),
        snapshot.get("decision_snapshot", {}).get("paper_action"),
        snapshot.get("decision_snapshot", {}).get("action_cap"),
    ]
    for val in fields_to_check:
        if val and val in _FORBIDDEN_ACTIONS:
            raise ValueError(f"forbidden real trade in backfill task: {val}")


def build_z9_outcome_backfill_task(
    queue_item: dict,
    *,
    task_id: str | None = None,
    run_id: str | None = None,
) -> dict:
    """
    将 Z9_INGESTION_QUEUE_ITEM 转换为 Z9_OUTCOME_BACKFILL_TASK preview.

    参数:
      queue_item: Z9_INGESTION_QUEUE_ITEM dict
      task_id: 可选，覆盖自动生成的 task_id
      run_id: 可选，覆盖自动生成的 run_id

    返回:
      符合 Z9_OUTCOME_BACKFILL_TASK v1.0 契约的 dict
    """
    now = datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S_%f")
    queue_id = queue_item.get("queue_id", "")
    sample_id = queue_item.get("sample_id", "UNKNOWN")
    ticker = queue_item.get("ticker", "UNKNOWN")
    run_id = run_id or now.strftime("%Y%m%d_%H%M%S")
    task_id = task_id or f"BF_{queue_id}_{ts}"

    snapshot = queue_item.get("sample_snapshot", {}) or {}
    idem = queue_item.get("idempotency", {}) or {}

    # ── 禁止交易检查 ──
    _check_forbidden_in_sample(snapshot)

    # ── 必要字段验证 ──
    reject_reasons = []
    for field in REQUIRED_QUEUE_FIELDS:
        if not queue_item.get(field):
            reject_reasons.append(f"MISSING_REQUIRED_FIELD:{field}")

    for parent, child in REQUIRED_NESTED:
        parent_val = queue_item.get(parent)
        if not isinstance(parent_val, dict) or not parent_val.get(child):
            reject_reasons.append(f"MISSING_REQUIRED_FIELD:{parent}.{child}")

    # ── 幂等 key ──
    backfill_task_key = make_z9_backfill_task_key(queue_item)

    # ── 状态机 ──
    if reject_reasons:
        status = "REJECTED"
        reason = "; ".join(reject_reasons)
    else:
        status = "WAITING_MARKET_DATA"
        reason = "D3_CONTRACT_ONLY_NO_REAL_MARKET_FETCH"

    # ── outcome 预设骨架 ──
    outcome_fields = {
        "actual_return_T1": None,
        "actual_return_T5": None,
        "actual_return_T20": None,
        "max_drawdown_T5": None,
        "max_drawdown_T20": None,
        "max_runup_T5": None,
        "max_runup_T20": None,
        "decision_outcome": "PENDING_BACKFILL",
        "rule_hit_accuracy": None,
        "false_positive_flags": [],
        "false_negative_flags": [],
    }

    return {
        "task_version": "v1.0",
        "task_type": "Z9_OUTCOME_BACKFILL_TASK",
        "task_id": task_id,
        "run_id": run_id,
        "queue_id": queue_id,
        "sample_id": sample_id,
        "ticker": ticker,
        "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "source_queue_item": {
            "queue_version": queue_item.get("queue_version"),
            "queue_type": queue_item.get("queue_type"),
            "queue_id": queue_id,
            "idempotency_key": idem.get("idempotency_key", ""),
            "dedup_key": idem.get("dedup_key", ""),
        },
        "idempotency": {
            "backfill_task_key": backfill_task_key,
            "source_queue_id": queue_id,
            "source_sample_id": sample_id,
            "source_queue_idempotency_key": idem.get("idempotency_key", ""),
            "same_task_recreate_allowed": False,
        },
        "required_market_data": {
            "horizons": ["T1", "T5", "T20"],
            "required_fields": [
                "close_T0", "close_T1", "close_T5", "close_T20",
                "low_T5", "low_T20", "high_T5", "high_T20",
            ],
            "data_status": "NOT_CONNECTED",
            "real_fetch_allowed": False,
        },
        "outcome_fields": outcome_fields,
        "state": {
            "status": status,
            "allowed_statuses": ALLOWED_BACKFILL_STATUSES,
            "reason": reason,
        },
        "validation": {
            "queue_item_valid": not reject_reasons,
            "reject_reasons": reject_reasons,
            "ready_for_real_backfill": False,
            "requires_future_market_data": True,
        },
        "write_policy": {
            "outcome_write_allowed": False,
            "z9_write_allowed": False,
            "queue_update_allowed": False,
            "write_status": "DEFERRED_NOT_CONNECTED",
            "reason": "D3_OUTCOME_BACKFILL_CONTRACT_ONLY_NO_REAL_WRITE",
        },
        "calibration_policy": {
            "auto_calibration_allowed": False,
            "ev_calibration_allowed": False,
            "r_matrix_calibration_allowed": False,
            "g18_rule_calibration_allowed": False,
            "reason": "D4_ONLY",
        },
        "forbidden_real_trade_checked": True,
    }
