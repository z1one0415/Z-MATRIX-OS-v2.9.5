#!/usr/bin/env python3
"""Z9 Outcome Backfill Task v1.0 contract tests — D-3 Contract Freeze, no real backfill"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime


def _make_valid_sample():
    return {
        "sample_id": "Z9S_002472_20260522",
        "ticker": "002472",
        "name": "双环传动",
        "sample_version": "v1.0",
        "created_at": "2026-05-22 00:00:00",
        "source_record": {"record_ref": "Z9S_002472_20260522"},
        "decision_snapshot": {
            "entry_intent": "WAIT", "exit_intent": None,
            "paper_action": None, "action_cap": "WAIT",
        },
        "outcome_placeholder": {
            "actual_return_T1": None, "actual_return_T5": None, "actual_return_T20": None,
            "review_status": "WAITING_FOR_FUTURE_MARKET_DATA",
        },
        "prediction": {"probability": 0.75},
        "review_plan": {"needs_future_review": True},
        "calibration_hooks": {},
    }


def test_module_imports():
    from zmatrix.calibration.z9_outcome_backfill_task import (
        build_z9_outcome_backfill_task,
        generate_backfill_task_report,
        HORIZON_MAP,
    )
    assert callable(build_z9_outcome_backfill_task)
    assert callable(generate_backfill_task_report)
    assert len(HORIZON_MAP) == 3
    print("✅ imports + callables verified")


def test_task_required_fields():
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    sample = _make_valid_sample()
    task = build_z9_outcome_backfill_task(sample, ticker="002472", pred_date="2026-05-22")
    for k in ["task_version", "task_type", "task_id", "sample_id", "ticker",
              "task_state", "backfill_spec", "outcome_target", "provenance",
              "write_policy", "forbidden_real_trade_checked"]:
        assert k in task, f"missing {k}"
    assert task["task_version"] == "v1.0"
    assert task["task_type"] == "Z9_OUTCOME_BACKFILL_TASK"
    assert task["write_policy"]["backfill_write_allowed"] is False
    assert task["write_policy"]["z9_write_allowed"] is False
    print("✅ task: all required fields present")


def test_task_no_real_backfill():
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_sample())
    assert task["write_policy"]["backfill_write_allowed"] is False
    assert task["write_policy"]["z9_write_allowed"] is False
    assert "CONTRACT_ONLY" in task["task_state"]["reason"]
    print("✅ no real backfill: CONTRACT_ONLY")


def test_horizon_status_calculations():
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    # 用过去的日期 -> 所有horizon都到期
    sample = _make_valid_sample()
    sample["created_at"] = "2026-05-01 00:00:00"
    task = build_z9_outcome_backfill_task(sample, ticker="002472", pred_date="2026-05-01")
    assert task["backfill_spec"]["backfill_ready"] is True
    assert task["task_state"]["status"] == "PENDING_BACKFILL"
    for h in ["T1", "T5", "T20"]:
        assert task["backfill_spec"]["horizon_details"][h]["is_matured"] is True
    print("✅ horizon: past pred_date → all matured, PENDING_BACKFILL")


def test_horizon_not_matured():
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    # 今天的日期 -> 未来horizon未到期
    today = datetime.now().strftime("%Y-%m-%d")
    task = build_z9_outcome_backfill_task(_make_valid_sample(), pred_date=today)
    assert task["backfill_spec"]["backfill_ready"] is False
    assert task["task_state"]["status"] == "WAITING_FOR_FUTURE_MARKET_DATA"
    for h in ["T1", "T5", "T20"]:
        assert task["backfill_spec"]["horizon_details"][h]["is_matured"] is False
    print("✅ horizon: today → WAITING_FOR_FUTURE_MARKET_DATA")


def test_contains_queue_preview_provenance():
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_sample())
    prov = task["provenance"]["source_queue_item"]
    assert "queue_id" in prov
    assert "queue_type" in prov
    assert "idempotency_key" in prov
    assert "source_record_ref" in prov
    print("✅ provenance: queue item reference present")


def test_outcome_target_template():
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    sample = _make_valid_sample()
    sample["created_at"] = "2026-05-01 00:00:00"
    task = build_z9_outcome_backfill_task(sample, pred_date="2026-05-01")
    ot = task["outcome_target"]
    assert "actual_return_T1" in ot
    assert "actual_return_T5" in ot
    assert "actual_return_T20" in ot
    assert "max_drawdown_T5" in ot
    assert "max_drawdown_T20" in ot
    assert "decision_outcome" in ot
    assert ot["decision_outcome"] == "PENDING_REVIEW"
    print("✅ outcome_target: template fields present")


def test_forbidden_real_trade_rejected():
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    sample = _make_valid_sample()
    sample["decision_snapshot"]["entry_intent"] = "BUY"
    try:
        build_z9_outcome_backfill_task(sample)
        assert False, "BUY should be rejected"
    except ValueError:
        pass
    print("✅ BUY rejected")


def test_outcome_decision_forbidden():
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    sample = _make_valid_sample()
    sample["outcome_placeholder"]["decision_outcome"] = "SELL"
    try:
        build_z9_outcome_backfill_task(sample)
        assert False, "SELL in outcome should be rejected"
    except ValueError:
        pass
    print("✅ SELL in outcome rejected")


def test_report_generated():
    from zmatrix.calibration.z9_outcome_backfill_task import generate_backfill_task_report
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    tasks = [
        build_z9_outcome_backfill_task(_make_valid_sample(), pred_date="2026-05-01"),
        build_z9_outcome_backfill_task(_make_valid_sample(), pred_date=datetime.now().strftime("%Y-%m-%d")),
    ]
    report = generate_backfill_task_report(tasks)
    assert isinstance(report, str)
    assert len(report) > 100
    assert "Z9 Outcome Backfill Task Report" in report
    print("✅ report: generated")


def test_sample_file_workflow():
    """从JSON文件构建task preview（模拟完整G18→D-3流程）"""
    import tempfile
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task

    sample = _make_valid_sample()
    sample["created_at"] = "2026-05-01 00:00:00"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(sample, f)
        tmp_path = f.name

    try:
        with open(tmp_path) as f:
            loaded = json.load(f)
        task = build_z9_outcome_backfill_task(loaded, pred_date="2026-05-01")
        assert task["task_state"]["status"] == "PENDING_BACKFILL"
        assert task["backfill_spec"]["backfill_ready"] is True
    finally:
        os.unlink(tmp_path)

    print("✅ sample file workflow: PENDING_BACKFILL + backfill_ready")


def test_no_real_write():
    """确保产出不含BUY/SELL等字段"""
    from zmatrix.calibration.z9_outcome_backfill_task import build_z9_outcome_backfill_task
    task = build_z9_outcome_backfill_task(_make_valid_sample(), pred_date="2026-05-01")
    raw = json.dumps(task)
    for f in ["BUY", "SELL", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"]:
        assert f not in raw, f"forbidden token found: {f}"
    print("✅ no forbidden real trade tokens")


def test_horizon_map_consistent():
    from zmatrix.calibration.z9_outcome_backfill_task import HORIZON_MAP
    assert HORIZON_MAP["T1"] == 1
    assert HORIZON_MAP["T5"] == 5
    assert HORIZON_MAP["T20"] == 20
    print("✅ HORIZON_MAP: T1=1, T5=5, T20=20")


if __name__ == "__main__":
    test_module_imports()
    test_task_required_fields()
    test_task_no_real_backfill()
    test_horizon_status_calculations()
    test_horizon_not_matured()
    test_contains_queue_preview_provenance()
    test_outcome_target_template()
    test_forbidden_real_trade_rejected()
    test_outcome_decision_forbidden()
    test_report_generated()
    test_sample_file_workflow()
    test_no_real_write()
    test_horizon_map_consistent()
    print("\n🏁 Z9 Outcome Backfill Task v1.0 — all D-3 contract tests PASS")
