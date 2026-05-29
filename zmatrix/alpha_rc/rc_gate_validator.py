# allowlist: forbidden-token-definition
"""RC Gate Validator — aggregate all RC checks for final validation"""
from __future__ import annotations
import json

from zmatrix.alpha_rc.manifest_builder import build_v3_alpha_release_manifest
from zmatrix.alpha_rc.verification_matrix import build_v3_alpha_verification_matrix
from zmatrix.alpha_rc.module_inventory import build_v3_alpha_frozen_module_inventory
from zmatrix.alpha_rc.known_limitations import build_v3_alpha_known_limitations
from zmatrix.integration.readiness_report import build_v3_alpha_readiness_report
from zmatrix.dry_run.rehearsal_report import build_v3_alpha_dry_run_report


_BLOCKED_FIELDS = [
    "real_trade_allowed", "broker_order_allowed", "auto_buy_allowed",
    "auto_sell_allowed", "auto_position_close_allowed", "real_z9_write_allowed",
    "hermes_memory_write_allowed", "auto_calibration_allowed",
    "prompt_auto_injection_allowed", "system_prompt_write_allowed",
    "runtime_injection_allowed", "runtime_enabled", "external_api_default_on",
]


def _check_blocked_fields(prefix: str, record: dict) -> list[str]:
    violations = []
    if not isinstance(record, dict):
        return violations
    for field in _BLOCKED_FIELDS:
        if record.get(field) is True:
            violations.append(f"{prefix}.{field} must be False")
    safety = record.get("safety", {})
    if safety is None:
        safety = {}
    if not isinstance(safety, dict):
        violations.append(f"{prefix}.safety must be dict")
        return violations
    for field in _BLOCKED_FIELDS:
        if safety.get(field) is True:
            violations.append(f"{prefix}.safety.{field} must be False")
    return violations

_RC_GATE_VERSION = "V3_ALPHA_RC_GATE_VALIDATION_V10"


def validate_v3_alpha_rc_gate() -> dict:
    """Validate the full v3.0-alpha RC gate."""
    violations = []

    manifest = build_v3_alpha_release_manifest()
    ver_matrix = build_v3_alpha_verification_matrix()
    inventory = build_v3_alpha_frozen_module_inventory()
    limitations = build_v3_alpha_known_limitations()
    readiness = build_v3_alpha_readiness_report()
    dry_run = build_v3_alpha_dry_run_report()

    # Check readiness
    if readiness.get("overall_status") != "READY_FOR_ALPHA":
        violations.append(f"readiness status={readiness.get('overall_status')} != READY_FOR_ALPHA")
    if readiness.get("alpha_runtime_allowed") is True:
        violations.append("readiness alpha_runtime_allowed must be False")

    # Check dry-run
    if dry_run.get("overall_status") != "PASS":
        violations.append(f"dry-run status={dry_run.get('overall_status')} != PASS")
    if dry_run.get("runtime_enabled") is True:
        violations.append("dry-run runtime_enabled must be False")

    # Check manifest
    if manifest.get("runtime_enabled") is True:
        violations.append("manifest runtime_enabled must be False")

    # Check verification matrix
    if not ver_matrix.get("all_required_present"):
        violations.append("verification matrix not all present")

    # Check inventory: 8 core packages
    if len(inventory.get("frozen_modules", [])) < 8:
        violations.append(f"inventory has {len(inventory.get('frozen_modules', []))} modules, expected >=8")

    # Check known limitations
    if len(limitations.get("limitations", [])) < 10:
        violations.append(f"known limitations has {len(limitations.get('limitations', []))} items, expected >=10")

    # Check all safety
    for field in ["runtime_enabled", "real_trade_allowed", "broker_order_allowed",
                  "hermes_memory_write_allowed", "real_z9_write_allowed",
                  "auto_calibration_allowed", "prompt_auto_injection_allowed",
                  "system_prompt_write_allowed"]:
        safety = manifest.get("safety", {})
        if not isinstance(safety, dict):
            safety = {}
        if safety.get(field) is True:
            violations.append(f"manifest.safety.{field} must be False")

    # Recursive safety check on all RC outputs
    for name, obj in {
        "manifest": manifest,
        "verification_matrix": ver_matrix,
        "module_inventory": inventory,
        "known_limitations": limitations,
        "readiness_report": readiness,
        "dry_run_report": dry_run,
    }.items():
        violations.extend(_check_blocked_fields(name, obj))

    return {
        "rc_gate_version": _RC_GATE_VERSION,
        "blocked_fields_checked": list(_BLOCKED_FIELDS),
        "pass": len(violations) == 0,
        "violations": violations,
        "manifest": manifest,
        "verification_matrix": ver_matrix,
        "module_inventory": inventory,
        "known_limitations": limitations,
        "readiness_report": readiness,
        "dry_run_report": dry_run,
        "runtime_enabled": False,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "hermes_memory_write_allowed": False,
        "real_z9_write_allowed": False,
        "auto_calibration_allowed": False,
        "prompt_auto_injection_allowed": False,
        "system_prompt_write_allowed": False,
    }
