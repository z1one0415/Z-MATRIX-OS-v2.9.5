"""Forbidden Capability Audit — check all registries for safety boundaries"""
from __future__ import annotations

from zmatrix.integration.schemas import ALPHA_FORBIDDEN_CAPABILITIES
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY


def audit_forbidden_capabilities() -> dict:
    """Audit that all v3.0 pipelines forbid required capabilities."""
    violations = []

    # Z-EventStore
    es = PIPELINE_REGISTRY.get("Z-EventStore", {})
    es_fc = es.get("forbidden_capabilities", [])
    if "real_z9_write" not in es_fc:
        violations.append("Z-EventStore missing real_z9_write forbidden")
    if "hermes_memory_write" not in es_fc:
        violations.append("Z-EventStore missing hermes_memory_write forbidden")

    # Z-HermesMemoryKernel
    hk = PIPELINE_REGISTRY.get("Z-HermesMemoryKernel", {})
    hk_fc = hk.get("forbidden_capabilities", [])
    if "hermes_memory_write" not in hk_fc:
        violations.append("Z-HermesMemoryKernel missing hermes_memory_write forbidden")
    if "auto_calibration" not in hk_fc:
        violations.append("Z-HermesMemoryKernel missing auto_calibration forbidden")
    if "prompt_auto_injection" not in hk_fc:
        violations.append("Z-HermesMemoryKernel missing prompt_auto_injection forbidden")

    # Z-ApprovalReflectionLoop
    ar = PIPELINE_REGISTRY.get("Z-ApprovalReflectionLoop", {})
    ar_fc = ar.get("forbidden_capabilities", [])
    for cap in ["hermes_memory_write", "auto_calibration", "prompt_auto_injection"]:
        if cap not in ar_fc:
            violations.append(f"Z-ApprovalReflectionLoop missing {cap} forbidden")

    # Z-PromptMiddlewarePreview
    pm = PIPELINE_REGISTRY.get("Z-PromptMiddlewarePreview", {})
    pm_fc = pm.get("forbidden_capabilities", [])
    for cap in ["runtime_prompt_injection", "system_prompt_write", "prompt_auto_injection"]:
        if cap not in pm_fc:
            violations.append(f"Z-PromptMiddlewarePreview missing {cap} forbidden")

    # Z-TailRiskAutonomicGates
    tr = PIPELINE_REGISTRY.get("Z-TailRiskAutonomicGates", {})
    tr_fc = tr.get("forbidden_capabilities", [])
    for cap in ["broker_order", "auto_sell", "auto_buy", "real_trade"]:
        if cap not in tr_fc:
            violations.append(f"Z-TailRiskAutonomicGates missing {cap} forbidden")

    # Check all alpha pipelines have forbidden_capabilities field
    from zmatrix.integration.schemas import ALPHA_REQUIRED_PIPELINES
    for pid in ALPHA_REQUIRED_PIPELINES:
        p = PIPELINE_REGISTRY.get(pid, {})
        if "forbidden_capabilities" not in p:
            violations.append(f"{pid}: missing forbidden_capabilities field")

    return {
        "audit_version": "FORBIDDEN_CAPABILITY_AUDIT_V10",
        "checked_registries": ["PIPELINE_REGISTRY"],
        "forbidden_capabilities": sorted(ALPHA_FORBIDDEN_CAPABILITIES),
        "violations": violations,
        "pass": len(violations) == 0,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "auto_calibration_allowed": False,
        "prompt_auto_injection_allowed": False,
    }
