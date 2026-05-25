#!/usr/bin/env python3
"""Z9 Calibration Policy Preview v1.0 — Batch D-4 contract tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime
from pathlib import Path


def _make_empty_backfill_task():
    """构造 outcome_fields 全为 None 的 backfill task (未回填)"""
    return {
        "task_version": "v1.0",
        "task_type": "Z9_OUTCOME_BACKFILL_TASK",
        "task_id": "BF_Q_20260524_235900_000000_20260525_023900",
        "ticker": "002472",
        "outcome_fields": {
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
        },
        "required_market_data": {"real_fetch_allowed": False},
        "idempotency": {"backfill_task_key": "018f5bb8df965e4bf5ea83b47766a85b"},
        "source_queue_item": {},
    }


def _make_filled_backfill_task(t5_return=5.2):
    """构造 outcome_fields 已回填的 backfill task"""
    task = _make_empty_backfill_task()
    task["outcome_fields"]["actual_return_T1"] = 2.1
    task["outcome_fields"]["actual_return_T5"] = t5_return
    task["outcome_fields"]["actual_return_T20"] = None  # 未到 T20
    task["outcome_fields"]["max_drawdown_T5"] = -3.5
    task["outcome_fields"]["max_drawdown_T20"] = None
    task["outcome_fields"]["max_runup_T5"] = 6.8
    task["outcome_fields"]["max_runup_T20"] = None
    task["outcome_fields"]["decision_outcome"] = "CORRECT"
    return task


# ── 1. 核心字段 ──

def test_preview_required_fields():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_empty_backfill_task())
    required = [
        "preview_version", "preview_type", "preview_id", "run_id", "task_id",
        "ticker", "created_at", "source_backfill_task", "idempotency",
        "outcome_summary", "policy_domains", "state", "validation",
        "write_policy", "forbidden_real_trade_checked",
    ]
    for k in required:
        assert k in preview, f"missing top-level field: {k}"
    assert preview["preview_version"] == "v1.0"
    assert preview["preview_type"] == "CALIBRATION_POLICY_PREVIEW"
    assert preview["write_policy"]["ev_write_allowed"] is False
    assert preview["write_policy"]["r_matrix_write_allowed"] is False
    assert preview["write_policy"]["g18_write_allowed"] is False
    assert preview["write_policy"]["z9_write_allowed"] is False
    print("✅ preview: all required fields present")


def test_source_backfill_task_preserved():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_empty_backfill_task())
    sb = preview["source_backfill_task"]
    assert sb["task_id"] == "BF_Q_20260524_235900_000000_20260525_023900"
    assert sb["task_version"] == "v1.0"
    assert sb["backfill_task_key"] == "018f5bb8df965e4bf5ea83b47766a85b"
    print("✅ source_backfill_task: preserved")


# ── 2. 状态机 ──

def test_empty_outcome_awaiting_backfill():
    """outcome_fields 全为 None → AWAITING_BACKFILL"""
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_empty_backfill_task())
    assert preview["state"]["status"] == "AWAITING_BACKFILL"
    assert preview["state"]["ready_for_calibration"] is False
    print("✅ empty outcome: AWAITING_BACKFILL")


def test_filled_outcome_preview_generated():
    """outcome_fields 有值 → POLICY_PREVIEW_GENERATED"""
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_filled_backfill_task())
    assert preview["state"]["status"] == "POLICY_PREVIEW_GENERATED"
    assert preview["state"]["ready_for_calibration"] is True
    print("✅ filled outcome: POLICY_PREVIEW_GENERATED")


# ── 3. Policy domains (三域) ──

def test_policy_domains_structure():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_filled_backfill_task(5.2))
    pd = preview["policy_domains"]
    for domain in ["ev_calibration", "r_matrix_calibration", "g18_rule_calibration"]:
        assert domain in pd, f"missing {domain}"
        d = pd[domain]
        assert "domain" in d
        assert "direction" in d
        assert "confidence" in d
        assert "recommendations" in d
        assert "explanation" in d
    print("✅ policy_domains: all 3 domains present with standard fields")


def test_positive_outcome_generates_strengthen_recommendations():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_filled_backfill_task(5.2))
    ev = preview["policy_domains"]["ev_calibration"]
    assert ev["direction"] == "STRENGTHEN_POSITIVE"
    assert ev["confidence"] == "HIGH"
    assert len(ev["recommendations"]) > 0
    print("✅ +5.2% T5 → STRENGTHEN_POSITIVE, HIGH confidence")


def test_negative_outcome_generates_review_recommendations():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_filled_backfill_task(-5.2))
    ev = preview["policy_domains"]["ev_calibration"]
    assert ev["direction"] == "REVIEW_NEGATIVE"
    assert ev["confidence"] == "HIGH"
    print("✅ -5.2% T5 → REVIEW_NEGATIVE, HIGH confidence")


def test_small_outcome_is_stable():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_filled_backfill_task(0.5))
    ev = preview["policy_domains"]["ev_calibration"]
    assert ev["direction"] == "STABLE"
    assert ev["confidence"] == "LOW"
    print("✅ +0.5% T5 → STABLE, LOW confidence")


def test_rmatrix_accelerating_trend():
    """T1→T5 加速 → MAINTAIN_OR_LIGHTEN"""
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    task = _make_filled_backfill_task(5.2)
    task["outcome_fields"]["actual_return_T1"] = 1.0  # T1=1%, T5=5.2% → 加速
    preview = build_calibration_policy_preview(task)
    rm = preview["policy_domains"]["r_matrix_calibration"]
    assert rm["direction"] == "MAINTAIN_OR_LIGHTEN"
    print("✅ accelerating trend → MAINTAIN_OR_LIGHTEN")


def test_rmatrix_decelerating_trend():
    """T1→T5 减速 → TIGHTEN_EXIT"""
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    task = _make_filled_backfill_task(1.0)
    task["outcome_fields"]["actual_return_T1"] = 5.0  # T1=5%, T5=1% → 减速
    preview = build_calibration_policy_preview(task)
    rm = preview["policy_domains"]["r_matrix_calibration"]
    assert rm["direction"] == "TIGHTEN_EXIT"
    print("✅ decelerating trend → TIGHTEN_EXIT")


def test_g18_positive_outcome_maintain():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_filled_backfill_task(3.0))
    g18 = preview["policy_domains"]["g18_rule_calibration"]
    assert "MAINTAIN" in g18["direction"]
    print("✅ +3% T5 → G18 maintain threshold")


def test_g18_negative_outcome_review():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    task = _make_filled_backfill_task(-4.0)
    task["outcome_fields"]["decision_outcome"] = "INCORRECT"
    preview = build_calibration_policy_preview(task)
    g18 = preview["policy_domains"]["g18_rule_calibration"]
    assert g18["direction"] == "REVIEW_RULES"
    assert g18["confidence"] == "HIGH"
    assert "calibratable_rules" in g18
    print("✅ -4% INCORRECT → REVIEW_RULES, HIGH confidence")


# ── 4. auto_calibration_allowed ──

def test_auto_calibration_allowed_false():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_empty_backfill_task())
    assert preview["validation"]["auto_calibration_allowed"] is False
    # 各 write policy 也必须 False
    assert preview["write_policy"]["ev_write_allowed"] is False
    assert preview["write_policy"]["r_matrix_write_allowed"] is False
    assert preview["write_policy"]["g18_write_allowed"] is False
    print("✅ auto_calibration_allowed: False")


# ── 5. 幂等 ──

def test_calibration_policy_key_stable():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview, make_calibration_policy_key
    task = _make_filled_backfill_task(5.2)
    k1 = make_calibration_policy_key(task)
    k2 = make_calibration_policy_key(task)
    assert k1 == k2
    assert len(k1) == 32
    print(f"✅ calibration_policy_key stable: {k1}")


def test_calibration_policy_key_changes_when_outcome_changes():
    from zmatrix.calibration.z9_calibration_policy import make_calibration_policy_key
    t1 = _make_filled_backfill_task(5.2)
    t2 = _make_filled_backfill_task(-3.0)
    k1 = make_calibration_policy_key(t1)
    k2 = make_calibration_policy_key(t2)
    assert k1 != k2
    print("✅ calibration_policy_key changes with outcome")


# ── 6. 禁止交易 ──

def test_forbidden_outcome_rejected():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    task = _make_empty_backfill_task()
    task["outcome_fields"]["decision_outcome"] = "BUY"
    try:
        build_calibration_policy_preview(task)
        assert False, "BUY should be rejected"
    except ValueError as e:
        assert "BUY" in str(e)
    print("✅ BUY in outcome rejected")


def test_real_fetch_flag_rejected():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    task = _make_empty_backfill_task()
    task["required_market_data"]["real_fetch_allowed"] = True
    try:
        build_calibration_policy_preview(task)
        assert False, "real_fetch_allowed=True should be rejected"
    except ValueError as e:
        assert "real_fetch_allowed" in str(e)
    print("✅ real_fetch_allowed=True rejected")


# ── 7. outcome_summary ──

def test_outcome_summary_not_backfilled():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_empty_backfill_task())
    summary = preview["outcome_summary"]
    assert summary["outcome_status"] == "NOT_BACKFILLED"
    assert summary["t1_return"] is None
    print("✅ outcome_summary: NOT_BACKFILLED")


def test_outcome_summary_backfilled():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_filled_backfill_task(5.2))
    summary = preview["outcome_summary"]
    assert summary["outcome_status"] == "BACKFILLED"
    assert summary["t1_return"] == 2.1
    assert summary["t5_return"] == 5.2
    assert summary["is_positive_t5"] is True
    print("✅ outcome_summary: BACKFILLED with values")


# ── 8. 禁止真实操作全面检查 ──

def test_no_real_ops():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview
    preview = build_calibration_policy_preview(_make_empty_backfill_task())
    raw = json.dumps(preview)
    for token in ["D4_PREVIEW_MODE", "PREVIEW_ONLY", "NO_REAL_WRITE", "DEFERRED_NOT_CONNECTED"]:
        assert token in raw, f"missing safety token: {token}"
    print("✅ no real ops: all safety tokens present")


# ── 9. 报告生成 ──

def test_report_generated():
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview, generate_calibration_report
    p1 = build_calibration_policy_preview(_make_empty_backfill_task())
    p2 = build_calibration_policy_preview(_make_filled_backfill_task(5.2))
    report = generate_calibration_report([p1, p2])
    assert isinstance(report, str)
    assert len(report) > 100
    assert "Calibration Policy Preview Report" in report
    print("✅ report: generated")


# ── 10. G18 集成测试 ──

def test_g18_output_contains_calibration_policy_preview():
    """G18 应包含 calibration_policy_preview"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "zg18", "pipelines/Z-G18_天机引擎/gate_pipeline.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    p = r["predictions"][0]
    assert "z9_calibration_policy_preview" in p
    cp = p["z9_calibration_policy_preview"]
    assert cp is not None
    assert cp["policy_domains"]["ev_calibration"]["domain"] == "EV_CALIBRATION"
    assert cp["write_policy"]["ev_write_allowed"] is False
    assert cp["validation"]["auto_calibration_allowed"] is False
    assert r["sections"]["z9_auto_calibration_allowed"] is False
    print("✅ G18: calibration_policy_preview present, safety gates closed")


# ── 11. example JSON test ──

def test_example_json_exists_and_structure():
    """example 样例文件必须存在且结构正确"""
    example_path = Path("docs/contracts/examples/z9_calibration_policy_preview_v10_example.json")
    assert example_path.exists(), "example JSON file missing"
    data = json.loads(example_path.read_text())
    assert data["preview_version"] == "v1.0"
    for w in ["ev_write_allowed", "r_matrix_write_allowed", "g18_write_allowed", "z9_write_allowed"]:
        assert data["write_policy"][w] is False, f"{w} must be False in example"
    assert data["validation"]["auto_calibration_allowed"] is False
    # 检查三域示例都有 content
    for domain in ["ev_calibration", "r_matrix_calibration", "g18_rule_calibration"]:
        d = data["policy_domains"][domain]
        assert d["direction"] not in (None, ""), f"{domain} direction is empty"
        assert len(d["recommendations"]) > 0, f"{domain} has no recommendations"
    print(f"✅ example JSON: {example_path.name} verified ({len(data['policy_domains'])} domains)")


def test_policy_key_is_32_hex():
    """calibration_policy_key 必须是 32 位 hex"""
    from zmatrix.calibration.z9_calibration_policy import build_calibration_policy_preview, make_calibration_policy_key
    key = make_calibration_policy_key({
        "task_id": "BF_T1", "ticker": "000001",
        "outcome_fields": {"actual_return_T5": 3.0},
    })
    assert len(key) == 32
    assert all(c in "0123456789abcdef" for c in key)
    print(f"✅ policy key: 32-char hex ({key})")


if __name__ == "__main__":
    test_preview_required_fields()
    test_source_backfill_task_preserved()
    test_empty_outcome_awaiting_backfill()
    test_filled_outcome_preview_generated()
    test_policy_domains_structure()
    test_positive_outcome_generates_strengthen_recommendations()
    test_negative_outcome_generates_review_recommendations()
    test_small_outcome_is_stable()
    test_rmatrix_accelerating_trend()
    test_rmatrix_decelerating_trend()
    test_g18_positive_outcome_maintain()
    test_g18_negative_outcome_review()
    test_auto_calibration_allowed_false()
    test_calibration_policy_key_stable()
    test_calibration_policy_key_changes_when_outcome_changes()
    test_forbidden_outcome_rejected()
    test_real_fetch_flag_rejected()
    test_outcome_summary_not_backfilled()
    test_outcome_summary_backfilled()
    test_no_real_ops()
    test_report_generated()
    test_g18_output_contains_calibration_policy_preview()
    test_example_json_exists_and_structure()
    test_policy_key_is_32_hex()
    print("\n🏁 Z9 Calibration Policy Preview v1.0 — all D-4 tests PASS")
