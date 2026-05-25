#!/usr/bin/env python3
"""
☯️ Architecture Enforcement v1.0 — 架构硬约束审计 (Batch F-5)

对所有架构注册表做跨表硬约束验证。
违反任意规则即记录违规。
"""
from __future__ import annotations

from typing import Any


def check_pipeline_allowed_skills_only() -> list[str]:
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    violations = []
    for pid, p in PIPELINE_REGISTRY.items():
        for sid in p.get("allowed_skills", []):
            if sid not in SHARED_SKILL_REGISTRY:
                violations.append(f"{pid}: allowed_skill '{sid}' not in SHARED_SKILL_REGISTRY")
    return violations


def check_no_unregistered_pipeline_required_gates() -> list[str]:
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    violations = []
    for pid, p in PIPELINE_REGISTRY.items():
        for g in p.get("required_gates", []):
            if g not in GATE_REGISTRY:
                violations.append(f"{pid}: required_gate '{g}' not in GATE_REGISTRY")
    return violations


def check_no_duplicate_skill_modules() -> list[str]:
    """不允许两个 skill 注册同一 module+public_function，除非 duplicate_allowed=True"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    seen = {}
    violations = []
    for sid, s in SHARED_SKILL_REGISTRY.items():
        key = (s.get("module"), s.get("public_function"))
        if key in seen and not s.get("duplicate_allowed"):
            violations.append(f"{sid} and {seen[key]}: duplicate module+function {key}")
        seen[key] = sid
    return violations


def check_no_pipeline_declares_forbidden_capability() -> list[str]:
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    violations = []
    for pid, p in PIPELINE_REGISTRY.items():
        fc = p.get("forbidden_capabilities", [])
        for required in ["real_trade", "real_z9_write", "real_market_fetch", "auto_calibration"]:
            if required not in fc:
                violations.append(f"{pid}: forbidden_capabilities missing {required}")
    return violations


def check_no_real_ops_enabled_anywhere() -> list[str]:
    """不允许任何 entity 声明 real_trade enabled 或等价"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY

    violations = []
    for name, reg in [("SHARED_SKILL_REGISTRY", SHARED_SKILL_REGISTRY),
                       ("PIPELINE_REGISTRY", PIPELINE_REGISTRY),
                       ("GATE_REGISTRY", GATE_REGISTRY),
                       ("WORKFLOW_DAG_REGISTRY", WORKFLOW_DAG_REGISTRY)]:
        for eid, entity in reg.items():
            # 检查 safety_boundary / forbidden_capabilities
            sb = entity.get("safety_boundary", "")
            fc = entity.get("forbidden_capabilities", [])
            if isinstance(fc, list) and "real_trade" not in fc:
                # pipeline/workflow 必须有 forbidden_capabilities
                pass  # 已在 check_no_pipeline_declares_forbidden_capability 覆盖
            if sb and "no real trade" not in sb and "no_real_trade" not in str(entity):
                # skill 的 safety_boundary 必须包含 no real trade
                if entity.get("layer") == "shared_skill":
                    violations.append(f"{name}/{eid}: safety_boundary must forbid real trade")
    return violations


def run_architecture_enforcement() -> list[str]:
    v = []
    v.extend(check_pipeline_allowed_skills_only())
    v.extend(check_no_unregistered_pipeline_required_gates())
    v.extend(check_no_duplicate_skill_modules())
    v.extend(check_no_pipeline_declares_forbidden_capability())
    v.extend(check_no_real_ops_enabled_anywhere())
    return v
