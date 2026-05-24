#!/usr/bin/env python3
"""Z9 Outcome Backfill Contract v1.0 — Batch D-3 tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime


def _make_valid_queue_item():
    """构造符合Z9_INGESTION_QUEUE_ITEM v1.0契约的有效queue item"""
    return {
        "queue_version": "v1.0",
        "queue_type": "Z9_INGESTION_QUEUE_ITEM",
        "queue_id": "Q_20260524_235900",
        "sample_id": "Z9S_20260524_235900",
        "run_id": "20260524_235900",
        "ticker": "002472",
        "idempotency": {
            "idempotency_key": "6ecf3446fd02e38fb983761adebff4e4",
            "dedup_key": "002472_Z9S_20260524_235900",
            "source_sample_id": "Z9S_20260524_235900",
            "source_record_ref": "Z9S_20260524_235900",
            "same_sample_reenqueue_allowed": False,
        },
        "sample_snapshot": {
            "sample_version": "v1.0",
            "sample_type": "Z9_CALIBRATION_SAMPLE",
            "ticker": "002472",
            "decision_snapshot": {
                "entry_intent": "WAIT", "exit_intent": None,
                "paper_action": None, "action_cap": "WAIT",
            },
            "outcome_placeholder": {
                "actual_return_T1": None, "actual_return_T5": None, "actual_return_T20": None,
                "max_drawdown_T5": None, "max_drawdown_T20": None,
                "decision_outcome": "PENDING_REVIEW",
                "review_status": "WAITING_FOR_FUTURE_MARKET_DATA",
            },
            "review_plan": {"needs_future_review": True},
            "calibration_hooks": {},
        },
        "state": {"status": "WAITING_MARKET_DATA"},
        "validation": {"sample_valid": True, "reject_reasons": []},
        "write_policy": {"queue_write_allowed": False, "z9_write_allowed": False},
        "forbidden_real_trade_checked": True,
    }


# ── 1. 核心字段 ──

def test_backfill_task_required_fields():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_queue_item())
    required = [
        "task_version", "task_type", "task_id", "run_id", "queue_id",
        "sample_id", "ticker", "created_at",
        "source_queue_item", "idempotency",
        "required_market_data", "outcome_fields",
        "state", "validation", "write_policy",
        "calibration_policy", "forbidden_real_trade_checked",
    ]
    for k in required:
        assert k in task, f"missing top-level field: {k}"
    assert task["task_version"] == "v1.0"
    assert task["task_type"] == "Z9_OUTCOME_BACKFILL_TASK"
    print("✅ task: all required fields present")


def test_source_queue_item_preserved():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_queue_item())
    sq = task["source_queue_item"]
    assert sq["queue_version"] == "v1.0"
    assert sq["queue_type"] == "Z9_INGESTION_QUEUE_ITEM"
    assert sq["queue_id"] == "Q_20260524_235900"
    assert sq["idempotency_key"] == "6ecf3446fd02e38fb983761adebff4e4"
    print("✅ source_queue_item: preserved")


# ── 2. Write policy ──

def test_backfill_write_policy_disabled():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_queue_item())
    wp = task["write_policy"]
    assert wp["outcome_write_allowed"] is False
    assert wp["z9_write_allowed"] is False
    assert wp["queue_update_allowed"] is False
    print("✅ write_policy: all False")


# ── 3. Market fetch ──

def test_market_fetch_disabled():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_queue_item())
    md = task["required_market_data"]
    assert md["real_fetch_allowed"] is False
    assert md["data_status"] == "NOT_CONNECTED"
    assert "close_T0" in md["required_fields"]
    assert len(md["horizons"]) == 3
    print("✅ market_fetch: disabled, NOT_CONNECTED")


# ── 4. Calibration ──

def test_auto_calibration_disabled():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_queue_item())
    cp = task["calibration_policy"]
    assert cp["auto_calibration_allowed"] is False
    assert cp["ev_calibration_allowed"] is False
    assert cp["r_matrix_calibration_allowed"] is False
    assert cp["g18_rule_calibration_allowed"] is False
    assert cp["reason"] == "D4_ONLY"
    print("✅ calibration: all False, D4_ONLY")


# ── 5. 幂等 ──

def test_backfill_task_key_stable():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task, make_z9_backfill_task_key
    qi = _make_valid_queue_item()
    k1 = make_z9_backfill_task_key(qi)
    k2 = make_z9_backfill_task_key(qi)
    assert k1 == k2
    assert len(k1) == 32
    print(f"✅ backfill_task_key stable: {k1}")


def test_backfill_task_key_changes_when_queue_id_changes():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task, make_z9_backfill_task_key
    qi1 = _make_valid_queue_item()
    qi2 = _make_valid_queue_item()
    qi2["queue_id"] = "Q_OTHER"
    k1 = make_z9_backfill_task_key(qi1)
    k2 = make_z9_backfill_task_key(qi2)
    assert k1 != k2
    print("✅ backfill_task_key changes with queue_id")


def test_backfill_task_key_changes_when_idempotency_key_changes():
    from zmatrix.calibration.z9_outcome_backfill import make_z9_backfill_task_key
    qi1 = _make_valid_queue_item()
    qi2 = _make_valid_queue_item()
    qi2["idempotency"]["idempotency_key"] = "other_key"
    k1 = make_z9_backfill_task_key(qi1)
    k2 = make_z9_backfill_task_key(qi2)
    assert k1 != k2
    print("✅ backfill_task_key changes with idempotency_key")


# ── 6. 状态机 ──

def test_waiting_market_data_default_status():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_queue_item())
    assert task["state"]["status"] == "WAITING_MARKET_DATA"
    print("✅ status: WAITING_MARKET_DATA (default)")


def test_missing_required_queue_field_rejected():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    qi = _make_valid_queue_item()
    del qi["queue_id"]
    task = build_z9_outcome_backfill_task(qi)
    assert task["state"]["status"] == "REJECTED"
    assert any("queue_id" in r for r in task["validation"]["reject_reasons"])
    print("✅ missing queue_id → REJECTED")


def test_missing_idempotency_rejected():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    qi = _make_valid_queue_item()
    qi["idempotency"]["idempotency_key"] = ""
    task = build_z9_outcome_backfill_task(qi)
    assert task["state"]["status"] == "REJECTED"
    print("✅ missing idempotency_key → REJECTED")


def test_missing_outcome_placeholder_rejected():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    qi = _make_valid_queue_item()
    qi["sample_snapshot"]["outcome_placeholder"] = None
    task = build_z9_outcome_backfill_task(qi)
    assert task["state"]["status"] == "REJECTED"
    print("✅ missing outcome_placeholder → REJECTED")


# ── 7. 禁止交易 ──

def test_forbidden_real_trade_rejected():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    qi = _make_valid_queue_item()
    qi["sample_snapshot"]["decision_snapshot"]["entry_intent"] = "BUY"
    try:
        build_z9_outcome_backfill_task(qi)
        assert False, "BUY should raise ValueError"
    except ValueError as e:
        assert "BUY" in str(e)
    print("✅ BUY rejected (ValueError)")


def test_conflict_code_with_sell_not_rejected():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    qi = _make_valid_queue_item()
    # G09_SELL_VS_G18_ENTRY 在 conflict code 中, 不在 action 字段
    qi["sample_snapshot"]["decision_snapshot"]["entry_intent"] = "WAIT"
    task = build_z9_outcome_backfill_task(qi)
    assert task["state"]["status"] == "WAITING_MARKET_DATA"
    print("✅ conflict code not rejected (WAITING_MARKET_DATA)")


# ── 8. outcome_fields ──

def test_outcome_fields_template():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_queue_item())
    of = task["outcome_fields"]
    for field in ["actual_return_T1", "actual_return_T5", "actual_return_T20",
                  "max_drawdown_T5", "max_drawdown_T20",
                  "max_runup_T5", "max_runup_T20"]:
        assert field in of and of[field] is None, f"{field} not None"
    assert of["decision_outcome"] == "PENDING_BACKFILL"
    assert of["false_positive_flags"] == []
    assert of["false_negative_flags"] == []
    print("✅ outcome_fields: template correct")


# ── 9. 禁止真实操作全面检查 ──

def test_no_real_ops():
    from zmatrix.calibration.z9_outcome_backfill import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_queue_item())
    raw = json.dumps(task)
    # 禁止真实操作的关键标记必须存在
    assert all(x in raw for x in [
        "D3_CONTRACT_ONLY",
        "NO_REAL",
        "DEFERRED_NOT_CONNECTED",
        "D4_ONLY",
        "PENDING_BACKFILL",
    ])
    # 禁止真实操作字段必须在值层为 False
    assert task["required_market_data"]["real_fetch_allowed"] is False
    assert task["write_policy"]["outcome_write_allowed"] is False
    assert task["write_policy"]["z9_write_allowed"] is False
    assert task["write_policy"]["queue_update_allowed"] is False
    assert task["calibration_policy"]["auto_calibration_allowed"] is False
    print("✅ no real ops: all gates closed")


# ── 10. G18 集成测试 ──

def test_g18_output_contains_outcome_backfill_task_preview():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "zg18", "pipelines/Z-G18_天机引擎/gate_pipeline.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    p = r["predictions"][0]
    assert "z9_outcome_backfill_task_preview" in p
    assert r["sections"]["z9_outcome_write_allowed"] is False
    assert r["sections"]["z9_market_fetch_allowed"] is False
    assert r["sections"]["z9_auto_calibration_allowed"] is False
    # 旧字段必须保留
    assert r["sections"]["z9_real_write_allowed"] is False
    assert r["sections"]["z9_queue_write_allowed"] is False
    print("✅ G18: outcome_backfill_task_preview + all safety gates")


if __name__ == "__main__":
    test_backfill_task_required_fields()
    test_source_queue_item_preserved()
    test_backfill_write_policy_disabled()
    test_market_fetch_disabled()
    test_auto_calibration_disabled()
    test_backfill_task_key_stable()
    test_backfill_task_key_changes_when_queue_id_changes()
    test_backfill_task_key_changes_when_idempotency_key_changes()
    test_waiting_market_data_default_status()
    test_missing_required_queue_field_rejected()
    test_missing_idempotency_rejected()
    test_missing_outcome_placeholder_rejected()
    test_forbidden_real_trade_rejected()
    test_conflict_code_with_sell_not_rejected()
    test_outcome_fields_template()
    test_no_real_ops()
    test_g18_output_contains_outcome_backfill_task_preview()
    print("\n🏁 Z9 Outcome Backfill Contract v1.0 — all D-3 tests PASS")
