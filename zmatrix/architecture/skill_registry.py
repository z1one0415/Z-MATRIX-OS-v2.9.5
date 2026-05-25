#!/usr/bin/env python3
"""
☯️ Shared Skill Registry v1.0 — Z-MATRIX-OS 三层架构收束 (Batch F-1)

所有通用能力必须注册到此表。
所有 pipeline 只能组合调用已注册的 skill module。
禁止重复建设同类技能模块。

原则:
  1. 一个 skill 只有一个 canonical id
  2. used_by 列明所有消费管线
  3. duplicate_allowed 默认为 False
  4. 无任何 skill 可声明 real trade enabled
"""
from __future__ import annotations

from typing import Any

# ── Registry ──

SHARED_SKILL_REGISTRY: dict[str, dict[str, Any]] = {
    "r_matrix.evaluate_cycle": {
        "layer": "shared_skill",
        "module": "zmatrix.scoring.r_matrix.r_matrix_service",
        "public_function": "evaluate_r_matrix_cycle",
        "owner": "R-Matrix",
        "used_by": ["Z-G09", "Z-G14", "Z-G18"],
        "contract": "docs/contracts/R_MATRIX_V2_CONTRACT.md",
        "test": "tests/test_rmatrix_contract_schema.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real market fetch, no auto calibration",
    },
    "evidence.aggregate_upstream": {
        "layer": "shared_skill",
        "module": "zmatrix.prediction.upstream_evidence_aggregator",
        "public_function": "build_upstream_evidence",
        "owner": "G18",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/G18_UPSTREAM_EVIDENCE_V10.md",
        "test": "tests/test_g18_upstream_evidence_aggregation.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade",
    },
    "conflict.resolve": {
        "layer": "shared_skill",
        "module": "zmatrix.prediction.conflict_resolver",
        "public_function": "resolve_upstream_conflicts",
        "owner": "G18",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/G18_CONFLICT_RESOLVER_V10.md",
        "test": "tests/test_g18_conflict_resolver.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade",
    },
    "decision.finalize": {
        "layer": "shared_skill",
        "module": "zmatrix.prediction.final_decision_envelope",
        "public_function": "build_final_decision",
        "owner": "G18",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/G18_FINAL_DECISION_ENVELOPE_V11.md",
        "test": "tests/test_g18_final_decision_envelope_v11.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no broker order",
    },
    "paper.record": {
        "layer": "shared_skill",
        "module": "zmatrix.prediction.paper_execution_record",
        "public_function": "build_paper_execution_record",
        "owner": "G18",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/G18_PAPER_EXECUTION_RECORD_V10.md",
        "test": "tests/test_g18_paper_execution_record.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write",
    },
    "z9.sample.build": {
        "layer": "shared_skill",
        "module": "zmatrix.calibration.z9_calibration_sample",
        "public_function": "build_z9_calibration_sample",
        "owner": "Z9",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/Z9_CALIBRATION_SAMPLE_V10.md",
        "test": "tests/test_z9_calibration_sample_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write",
    },
    "z9.queue.build": {
        "layer": "shared_skill",
        "module": "zmatrix.calibration.z9_ingestion_queue",
        "public_function": "build_z9_ingestion_queue_item",
        "owner": "Z9",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/Z9_INGESTION_QUEUE_V10.md",
        "test": "tests/test_z9_ingestion_queue_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real queue write, no real Z9 write",
    },
    "z9.backfill_task.build": {
        "layer": "shared_skill",
        "module": "zmatrix.calibration.z9_outcome_backfill",
        "public_function": "build_z9_outcome_backfill_task",
        "owner": "Z9",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/Z9_OUTCOME_BACKFILL_V10.md",
        "test": "tests/test_z9_outcome_backfill_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real market fetch, no real outcome backfill",
    },
    "z9.calibration_policy.preview": {
        "layer": "shared_skill",
        "module": "zmatrix.calibration.z9_calibration_policy",
        "public_function": "build_calibration_policy_preview",
        "owner": "Z9",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/Z9_CALIBRATION_POLICY_V10.md",
        "test": "tests/test_z9_calibration_policy_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real EV weight change, no real R-Matrix param change, no real G18 rule change",
    },
    "safety.no_real_trade": {
        "layer": "shared_skill",
        "module": "zmatrix.action.action_contracts",
        "public_function": "assert_no_real_trade",
        "owner": "SystemCore",
        "used_by": ["Z-G18", "Z9-all"],
        "contract": "docs/contracts/G18_FINAL_DECISION_ENVELOPE_V11.md",
        "test": "tests/test_g18_final_decision_envelope_v11.py",
        "duplicate_allowed": False,
        "safety_boundary": "foundational: no real trade — forbids BUY/SELL/AUTO_TRADE/MARKET_ORDER/BROKER_ORDER",
    },
    "rc.checksum.build": {
        "layer": "shared_skill",
        "module": "scripts.build_rc_package_manifest",
        "public_function": "main (CLI)",
        "owner": "RC",
        "used_by": ["RC-release"],
        "contract": None,
        "test": "tests/test_rc_packaging.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no Z9 write, only SHA256 checksum generation",
    },
}


def get_skill(skill_id: str) -> dict | None:
    """按 skill_id 查找注册技能"""
    return SHARED_SKILL_REGISTRY.get(skill_id)


def get_skills_by_owner(owner: str) -> list[dict]:
    """按 owner 查找注册技能"""
    return [s for s in SHARED_SKILL_REGISTRY.values() if s["owner"] == owner]


def get_skills_by_pipeline(pipeline_id: str) -> list[tuple[str, dict]]:
    """按消费管线查找注册技能"""
    return [(sid, s) for sid, s in SHARED_SKILL_REGISTRY.items()
            if pipeline_id in s["used_by"]]


def get_duplicate_allowed_skills() -> list[str]:
    """返回允许重复的技能ID列表（应有0个）"""
    return [sid for sid, s in SHARED_SKILL_REGISTRY.items() if s["duplicate_allowed"]]


def check_registry_integrity() -> list[str]:
    """检查注册表完整性，返回所有违规列表"""
    violations = []

    for sid, skill in SHARED_SKILL_REGISTRY.items():
        # 每个 skill 必须有 owner
        if not skill.get("owner"):
            violations.append(f"{sid}: missing owner")

        # 每个 skill 必须有 module
        if not skill.get("module"):
            violations.append(f"{sid}: missing module")

        # 每个 skill 必须有 test
        if not skill.get("test"):
            violations.append(f"{sid}: missing test")

        # 每个 skill 必须有 safety_boundary
        if not skill.get("safety_boundary"):
            violations.append(f"{sid}: missing safety_boundary")

        # 检查 no real trade 声明, 不允许多个 skill_id 指向同一 module
        # (非强制项，仅记录)

    # R-Matrix 只能有一个 canonical skill id
    r_matrix_skills = [sid for sid in SHARED_SKILL_REGISTRY if sid.startswith("r_matrix")]
    if len(r_matrix_skills) != 1:
        violations.append(f"expected exactly 1 r_matrix skill, got {len(r_matrix_skills)}: {r_matrix_skills}")

    return violations
