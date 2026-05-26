"""Readiness Report — aggregate all checks and produce final readiness status"""
from __future__ import annotations

from zmatrix.integration.readiness_map import build_v3_alpha_readiness_map
from zmatrix.integration.capability_audit import audit_forbidden_capabilities
from zmatrix.integration.workflow_alignment import audit_workflow_alignment
from zmatrix.integration.event_chain_validator import (
    build_sample_v3_alpha_event_chain, validate_v3_alpha_event_chain,
)
from zmatrix.integration.safety_matrix import build_cross_layer_safety_matrix


def build_v3_alpha_readiness_report() -> dict:
    """Aggregate all readiness checks and produce a final report."""
    readiness_map = build_v3_alpha_readiness_map()
    capability_audit = audit_forbidden_capabilities()
    workflow_alignment = audit_workflow_alignment()
    event_chain = build_sample_v3_alpha_event_chain()
    event_chain_validation = validate_v3_alpha_event_chain(event_chain)
    safety_matrix = build_cross_layer_safety_matrix()

    blocking_issues = []
    warnings = []

    if not capability_audit.get("pass", False):
        blocking_issues.append(f"capability_audit: {len(capability_audit.get('violations', []))} violations")
    if not workflow_alignment.get("pass", False):
        blocking_issues.append(f"workflow_alignment: missing pipelines={workflow_alignment.get('missing_pipelines')} workflows={workflow_alignment.get('missing_workflows')}")
    if not event_chain_validation.get("pass", False):
        blocking_issues.append(f"event_chain: {len(event_chain_validation.get('violations', []))} violations")
    if not safety_matrix.get("pass", False):
        blocking_issues.append(f"safety_matrix: {len(safety_matrix.get('violations', []))} violations")

    missing_pips = readiness_map.get("missing_pipelines", [])
    if missing_pips:
        warnings.append(f"missing pipelines: {missing_pips}")
    missing_gates = readiness_map.get("missing_gates", [])
    if missing_gates:
        warnings.append(f"missing required gates: {len(missing_gates)} items")

    if blocking_issues:
        overall_status = "BLOCKED"
    elif warnings:
        overall_status = "NEEDS_REVIEW"
    else:
        overall_status = "READY_FOR_ALPHA"

    return {
        "report_version": "V3_ALPHA_READINESS_REPORT_V10",
        "overall_status": overall_status,
        "ready_for_alpha": overall_status == "READY_FOR_ALPHA",
        "alpha_runtime_allowed": False,
        "real_trade_allowed": False,
        "summary": {
            "capability_audit_pass": capability_audit.get("pass"),
            "workflow_alignment_pass": workflow_alignment.get("pass"),
            "event_chain_validation_pass": event_chain_validation.get("pass"),
            "safety_matrix_pass": safety_matrix.get("pass"),
            "blocking_issue_count": len(blocking_issues),
            "warning_count": len(warnings),
        },
        "readiness_map": readiness_map,
        "capability_audit": capability_audit,
        "workflow_alignment": workflow_alignment,
        "event_chain_validation": event_chain_validation,
        "safety_matrix": safety_matrix,
        "blocking_issues": blocking_issues,
        "warnings": warnings,
        "next_recommended_step": "Proceed to alpha integration validation" if overall_status == "READY_FOR_ALPHA" else "Resolve blocking issues before alpha",
    }
