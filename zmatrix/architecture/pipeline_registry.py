#!/usr/bin/env python3
"""
☯️ Pipeline Registry v1.0 — Z-MATRIX-OS 三层架构第二层 (Batch F-2)

三层架构:
  Layer 3: System Control (控制器)
  Layer 2: Pipeline Application (管线组合应用层) ← 本注册表
  Layer 1: Shared Skill Module (通用技能层)

原则:
  1. 每条 pipeline 只能在 allowed_skills 中调用技能
  2. allowed_skills 必须全部存在于 SHARED_SKILL_REGISTRY
  3. pipeline 不得私造同类技能模块
  4. forbidden_capabilities 声明 pipeline 禁止的能力
"""
from __future__ import annotations

from typing import Any

PIPELINE_REGISTRY: dict[str, dict[str, Any]] = {
    "Z-G18": {
        "layer": "pipeline_application",
        "pipeline_path": "pipelines/Z-G18_天机引擎/gate_pipeline.py",
        "purpose": "Build G18 paper prediction and full Z9 preview chain",
        "allowed_skills": [
            "r_matrix.evaluate_cycle",
            "evidence.aggregate_upstream",
            "conflict.resolve",
            "decision.finalize",
            "paper.record",
            "z9.sample.build",
            "z9.queue.build",
            "z9.backfill_task.build",
            "z9.calibration_policy.preview",
            "safety.no_real_trade",
            "investment.role_review.build",
        ],
        "required_gates": [
            "safety.no_real_trade",
            "contract.validation",
            "z9.preview_only",
            "investment.role_review.required",
        ],
        "forbidden_capabilities": [
            "real_trade",
            "broker_order",
            "real_z9_write",
            "real_market_fetch",
            "auto_calibration",
        ],
        "owner": "G18",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
    "RC-release": {
        "layer": "pipeline_application",
        "pipeline_path": "scripts/verify_rc_candidate.sh",
        "purpose": "Verify release candidate package and safety boundaries",
        "allowed_skills": [
            "rc.checksum.build",
        ],
        "required_gates": [
            "rc.packaging",
            "rc.verification",
            "safety.boundary_scan",
        ],
        "forbidden_capabilities": [
            "real_trade",
            "real_z9_write",
            "real_market_fetch",
            "auto_calibration",
        ],
        "owner": "RC",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
    "Z-G09": {
        "layer": "pipeline_application",
        "pipeline_path": "pipelines/Z-G09_全局轮动筛选/gate_pipeline.py",
        "purpose": "R-Matrix cycle four-king rotation scan",
        "allowed_skills": [
            "r_matrix.evaluate_cycle",
        ],
        "required_gates": [
            "r_matrix.cycle_valid",
        ],
        "forbidden_capabilities": [
            "real_trade",
            "real_z9_write",
            "real_market_fetch",
            "auto_calibration",
        ],
        "owner": "R-Matrix",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
    "Z-G14": {
        "layer": "pipeline_application",
        "pipeline_path": "pipelines/Z-G14_月度全量选股/gate_pipeline.py",
        "purpose": "Monthly full-market sweep with R-Matrix cycle scan",
        "allowed_skills": [
            "r_matrix.evaluate_cycle",
        ],
        "required_gates": [
            "r_matrix.cycle_valid",
        ],
        "forbidden_capabilities": [
            "real_trade",
            "real_z9_write",
            "real_market_fetch",
            "auto_calibration",
        ],
        "owner": "R-Matrix",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
    "Z-InvestmentRoleReview": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix.investment.investment_role_workflow",
        "purpose": "Run complete B/R/D investment role review before any paper record",
        "allowed_skills": [
            "b_matrix.evaluate_base",
            "r_matrix.evaluate_cycle",
            "d_matrix.evaluate_event",
            "stock_role.classify",
            "account.constitution.check",
            "portfolio.exposure.analyze",
            "pre_trade.checklist.validate",
            "investment.role_review.build",
            "chain_force.evaluate_10x5",
            "sector_stage.detect",
            "financial.health_gate",
            "z8.position_control",
            "g17.manual_veto.preview",
            "safety.no_real_trade",
        ],
        "required_gates": [
            "b_matrix.base_valid",
            "d_matrix.event_valid",
            "stock_role.classification_valid",
            "account.constitution.valid",
            "portfolio.exposure.valid",
            "pre_trade.checklist.complete",
            "chain_force.valid",
            "sector_stage.valid",
            "financial.health_valid",
            "z8.position_control.valid",
            "investment.role_review.required",
            "safety.no_real_trade",
            "human.final_override.required",
        ],
        "forbidden_capabilities": [
            "real_trade", "real_z9_write", "real_market_fetch", "auto_calibration",
            "convert_to_base", "long_hold",
        ],
        "owner": "SystemCore",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
}


def get_pipeline(pipeline_id: str) -> dict | None:
    return PIPELINE_REGISTRY.get(pipeline_id)


def get_allowed_skills(pipeline_id: str) -> list[str]:
    p = get_pipeline(pipeline_id)
    return list(p["allowed_skills"]) if p else []


def check_pipeline_registry_integrity() -> list[str]:
    """检查 Pipeline Registry 完整性，返回违规列表"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY

    violations = []

    for pid, pipeline in PIPELINE_REGISTRY.items():
        # layer 必须正确
        if pipeline.get("layer") != "pipeline_application":
            violations.append(f"{pid}: layer != pipeline_application")

        # 必须有 pipeline_path
        if not pipeline.get("pipeline_path"):
            violations.append(f"{pid}: missing pipeline_path")

        # 必须有 owner
        if not pipeline.get("owner"):
            violations.append(f"{pid}: missing owner")

        # forbidden_capabilities 必须包含 no-real-ops
        fc = pipeline.get("forbidden_capabilities", [])
        for required in ["real_trade", "real_z9_write", "real_market_fetch", "auto_calibration"]:
            if required not in fc:
                violations.append(f"{pid}: forbidden_capabilities missing {required}")

        # allowed_skills 必须全部存在于 SHARED_SKILL_REGISTRY
        for skill_id in pipeline.get("allowed_skills", []):
            if skill_id not in SHARED_SKILL_REGISTRY:
                violations.append(f"{pid}: allowed_skill '{skill_id}' not in SHARED_SKILL_REGISTRY")

    return violations


def check_pipeline_skills_registered() -> list[str]:
    """返回所有 pipeline 使用的 skill 中未被 SHARED_SKILL_REGISTRY 注册的"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY

    unregistered = []
    for pid, pipeline in PIPELINE_REGISTRY.items():
        for skill_id in pipeline.get("allowed_skills", []):
            if skill_id not in SHARED_SKILL_REGISTRY:
                unregistered.append(f"{pid} -> {skill_id}")
    return unregistered
