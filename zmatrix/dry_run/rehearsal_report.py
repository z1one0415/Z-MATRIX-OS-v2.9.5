"""Rehearsal Report — aggregate dry-run rehearsal + validation into final report"""
from __future__ import annotations

from zmatrix.dry_run.rehearsal_runner import build_v3_alpha_dry_run_rehearsal
from zmatrix.dry_run.rehearsal_validator import validate_v3_alpha_dry_run_rehearsal


def build_v3_alpha_dry_run_report() -> dict:
    """Build the v3.0-alpha dry-run report."""
    rehearsal = build_v3_alpha_dry_run_rehearsal()
    validation = validate_v3_alpha_dry_run_rehearsal(rehearsal)

    blocking_issues = []
    if not validation.get("pass", False):
        blocking_issues.append(f"validation: {len(validation.get('violations', []))} violations")

    return {
        "report_version": "V3_ALPHA_DRY_RUN_REPORT_V10",
        "overall_status": "PASS" if not blocking_issues else "BLOCKED",
        "dry_run_pass": len(blocking_issues) == 0,
        "runtime_enabled": False,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "hermes_memory_write_allowed": False,
        "real_z9_write_allowed": False,
        "prompt_auto_injection_allowed": False,
        "system_prompt_write_allowed": False,
        "summary": {
            "rehearsal_steps_count": len(rehearsal.get("steps", [])),
            "lineage_count": len(rehearsal.get("lineage", [])),
            "validation_pass": validation.get("pass"),
        },
        "rehearsal": rehearsal,
        "validation": validation,
        "blocking_issues": blocking_issues,
    }
