"""Verification Matrix — build v3.0-alpha verification matrix"""
from __future__ import annotations

from zmatrix.alpha_rc.schemas import FROZEN_VERSION_RANGE, ALPHA_RC_COMPONENTS

_VERIFY_MAP = {
    "v2.9.10-dev": ("Workspace Alignment & Pipeline Census", "scripts/verify_workspace_alignment_candidate.sh"),
    "v2.9.11-dev": ("EventStore & Unified Event Ledger", "scripts/verify_event_store_candidate.sh"),
    "v2.9.12-dev": ("Hermes Memory Kernel Preview", "scripts/verify_hermes_memory_candidate.sh"),
    "v2.9.13-dev": ("Approval-Required Reflection Loop", "scripts/verify_approval_loop_candidate.sh"),
    "v2.9.14-dev": ("Prompt Hot-Patching Middleware Preview", "scripts/verify_prompt_middleware_candidate.sh"),
    "v2.9.15-dev": ("Tail-Risk Autonomic Gates Preview", "scripts/verify_tail_risk_candidate.sh"),
    "v2.9.16-dev": ("v3.0-alpha Integration Readiness Gate", "scripts/verify_v3_alpha_readiness_candidate.sh"),
    "v2.9.17-dev": ("v3.0-alpha Dry-Run Rehearsal", "scripts/verify_v3_alpha_dry_run_candidate.sh"),
}

_CRITICAL_TESTS = {
    "v2.9.10-dev": ["test_workspace_layout", "test_pipeline_census"],
    "v2.9.11-dev": ["test_event_ids", "test_event_schema", "test_event_store_local", "test_event_lineage"],
    "v2.9.12-dev": ["test_core_memory", "test_working_context", "test_learned_heuristics", "test_prompt_patch_preview"],
    "v2.9.13-dev": ["test_approval_request", "test_approval_decision", "test_approval_policy"],
    "v2.9.14-dev": ["test_prompt_patch_request", "test_prompt_middleware_renderer", "test_prompt_middleware_policy"],
    "v2.9.15-dev": ["test_limit_down_blackhole", "test_tail_risk_controller", "test_tail_risk_policy"],
    "v2.9.16-dev": ["test_integration_readiness_map", "test_integration_capability_audit", "test_integration_event_chain_validator"],
    "v2.9.17-dev": ["test_v3_alpha_dry_run_rehearsal", "test_v3_alpha_dry_run_validator"],
}


def build_v3_alpha_verification_matrix() -> dict:
    rows = []
    for ver in FROZEN_VERSION_RANGE:
        info = _VERIFY_MAP.get(ver, ("unknown", ""))
        tests = _CRITICAL_TESTS.get(ver, [])
        rows.append({
            "component": info[0],
            "version": ver,
            "verify_script": info[1],
            "critical_tests": tests,
            "status": "FROZEN_PASS",
            "runtime_allowed": False,
            "real_trade_allowed": False,
        })

    return {
        "matrix_version": "V3_ALPHA_VERIFICATION_MATRIX_V10",
        "rows": rows,
        "required_scripts": [info[1] for info in _VERIFY_MAP.values()],
        "required_tests": [t for tests in _CRITICAL_TESTS.values() for t in tests],
        "all_required_present": len(rows) == len(FROZEN_VERSION_RANGE),
        "runtime_enabled": False,
        "real_trade_allowed": False,
    }
