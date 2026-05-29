# allowlist: forbidden-token-definition
"""Forbidden Capability Audit — check all 4 registries for safety boundaries"""
from __future__ import annotations

from zmatrix.integration.schemas import (
    ALPHA_FORBIDDEN_CAPABILITIES, ALPHA_REQUIRED_PIPELINES,
    ALPHA_REQUIRED_WORKFLOWS, ALPHA_REQUIRED_GATES,
)
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
from zmatrix.architecture.gate_registry import GATE_REGISTRY


def audit_forbidden_capabilities() -> dict:
    """Audit all 4 registries for safety boundaries."""
    violations = []

    # === PIPELINE_REGISTRY ===
    for pid in ALPHA_REQUIRED_PIPELINES:
        p = PIPELINE_REGISTRY.get(pid)
        if p is None:
            violations.append(f"{pid}: missing pipeline")
            continue
        fc = set(p.get("forbidden_capabilities", []))
        missing = sorted(ALPHA_FORBIDDEN_CAPABILITIES - fc)
        # Z-V3AlphaReadinessGate must cover all forbidden caps
        if pid == "Z-V3AlphaReadinessGate" and missing:
            violations.append(f"{pid}: missing forbidden_capabilities {missing}")

    # Z-EventStore specific
    es = PIPELINE_REGISTRY.get("Z-EventStore", {})
    es_fc = es.get("forbidden_capabilities", [])
    if "real_z9_write" not in es_fc:
        violations.append("Z-EventStore: missing real_z9_write forbidden")
    if "hermes_memory_write" not in es_fc:
        violations.append("Z-EventStore: missing hermes_memory_write forbidden")

    # Z-HermesMemoryKernel
    hk = PIPELINE_REGISTRY.get("Z-HermesMemoryKernel", {})
    hk_fc = hk.get("forbidden_capabilities", [])
    for cap in ["hermes_memory_write", "auto_calibration", "prompt_auto_injection"]:
        if cap not in hk_fc:
            violations.append(f"Z-HermesMemoryKernel: missing {cap} forbidden")

    # Z-ApprovalReflectionLoop
    ar = PIPELINE_REGISTRY.get("Z-ApprovalReflectionLoop", {})
    ar_fc = ar.get("forbidden_capabilities", [])
    for cap in ["hermes_memory_write", "auto_calibration", "prompt_auto_injection"]:
        if cap not in ar_fc:
            violations.append(f"Z-ApprovalReflectionLoop: missing {cap} forbidden")

    # Z-PromptMiddlewarePreview
    pm = PIPELINE_REGISTRY.get("Z-PromptMiddlewarePreview", {})
    pm_fc = pm.get("forbidden_capabilities", [])
    for cap in ["runtime_prompt_injection", "system_prompt_write", "prompt_auto_injection"]:
        if cap not in pm_fc:
            violations.append(f"Z-PromptMiddlewarePreview: missing {cap} forbidden")

    # Z-TailRiskAutonomicGates
    tr = PIPELINE_REGISTRY.get("Z-TailRiskAutonomicGates", {})
    tr_fc = tr.get("forbidden_capabilities", [])
    for cap in ["broker_order", "auto_sell", "auto_buy", "real_trade"]:
        if cap not in tr_fc:
            violations.append(f"Z-TailRiskAutonomicGates: missing {cap} forbidden")

    # === WORKFLOW_DAG_REGISTRY ===
    for wid in ALPHA_REQUIRED_WORKFLOWS:
        w = WORKFLOW_DAG_REGISTRY.get(wid)
        if w is None:
            violations.append(f"{wid}: missing workflow")
            continue
        if "required_gates" not in w:
            violations.append(f"{wid}: missing required_gates")
        wg = set(w.get("required_gates", []))
        if "safety.no_real_trade" not in wg:
            violations.append(f"{wid}: missing safety.no_real_trade gate")

    # === SHARED_SKILL_REGISTRY ===
    for pid in ALPHA_REQUIRED_PIPELINES:
        p = PIPELINE_REGISTRY.get(pid, {})
        for skill in p.get("allowed_skills", []):
            if skill == "safety.no_real_trade":
                continue
            if skill not in SHARED_SKILL_REGISTRY:
                violations.append(f"{pid}: skill {skill} not registered")

    # === GATE_REGISTRY ===
    for gate in ALPHA_REQUIRED_GATES:
        if gate not in GATE_REGISTRY:
            violations.append(f"missing gate: {gate}")

    return {
        "audit_version": "FORBIDDEN_CAPABILITY_AUDIT_V10",
        "checked_registries": [
            "PIPELINE_REGISTRY", "WORKFLOW_DAG_REGISTRY",
            "SHARED_SKILL_REGISTRY", "GATE_REGISTRY",
        ],
        "forbidden_capabilities": sorted(ALPHA_FORBIDDEN_CAPABILITIES),
        "violations": violations,
        "pass": len(violations) == 0,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "auto_calibration_allowed": False,
        "prompt_auto_injection_allowed": False,
    }
