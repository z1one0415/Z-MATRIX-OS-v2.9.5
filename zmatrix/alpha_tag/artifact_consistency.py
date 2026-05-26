"""Artifact Consistency — validate release artifacts match builder outputs"""
from __future__ import annotations
import json
from pathlib import Path

from zmatrix.alpha_rc.manifest_builder import build_v3_alpha_release_manifest
from zmatrix.alpha_rc.verification_matrix import build_v3_alpha_verification_matrix
from zmatrix.alpha_rc.module_inventory import build_v3_alpha_frozen_module_inventory
from zmatrix.alpha_tag.schemas import TAG_GATE_REQUIRED_ARTIFACTS, TAG_GATE_REQUIRED_VERIFY_SCRIPTS

_ROOT = Path(__file__).resolve().parent.parent.parent


def validate_alpha_rc_artifact_consistency() -> dict:
    """Validate that release artifacts match builder outputs and all files exist."""
    violations = []

    # Check all required artifacts exist
    missing_artifacts = []
    for path in TAG_GATE_REQUIRED_ARTIFACTS:
        if not (_ROOT / path).exists():
            missing_artifacts.append(path)
    if missing_artifacts:
        violations.append(f"missing artifacts: {missing_artifacts}")

    # Check all verify scripts exist
    missing_scripts = []
    for path in TAG_GATE_REQUIRED_VERIFY_SCRIPTS:
        if not (_ROOT / path).exists():
            missing_scripts.append(path)
    if missing_scripts:
        violations.append(f"missing verify scripts: {missing_scripts}")

    # Check JSON artifacts match builder outputs
    json_ok = True
    json_checks = [
        ("v3_alpha_release_manifest_v10.json", build_v3_alpha_release_manifest()),
        ("v3_alpha_verification_matrix_v10.json", build_v3_alpha_verification_matrix()),
        ("v3_alpha_frozen_module_inventory_v10.json", build_v3_alpha_frozen_module_inventory()),
    ]
    for fname, builder_output in json_checks:
        path = _ROOT / "release" / "alpha_rc" / fname
        if path.exists():
            try:
                artifact_data = json.loads(path.read_text(encoding="utf-8"))
                if artifact_data != builder_output:
                    violations.append(f"{fname}: artifact does not match builder output")
                    json_ok = False
            except Exception:
                violations.append(f"{fname}: failed to parse JSON")
                json_ok = False
        else:
            violations.append(f"{fname}: file missing")
            json_ok = False

    return {
        "artifact_consistency_version": "V3_ALPHA_ARTIFACT_CONSISTENCY_V10",
        "pass": len(violations) == 0,
        "violations": violations,
        "checked_artifacts": list(TAG_GATE_REQUIRED_ARTIFACTS),
        "checked_verify_scripts": list(TAG_GATE_REQUIRED_VERIFY_SCRIPTS),
        "json_artifacts_match_builders": json_ok,
        "git_tag_execute_allowed": False,
        "git_push_tags_allowed": False,
        "real_trade_allowed": False,
        "runtime_enabled": False,
    }
