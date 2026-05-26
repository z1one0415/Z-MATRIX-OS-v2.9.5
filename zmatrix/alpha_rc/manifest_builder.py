"""Manifest Builder — build v3.0-alpha release manifest"""
from __future__ import annotations

from zmatrix.alpha_rc.schemas import (
    ALPHA_RC_VERSION, FROZEN_VERSION_RANGE,
    ALPHA_RC_COMPONENTS, DEFAULT_ALPHA_RC_SAFETY,
)

_REQUIRED_VERIFY_SCRIPTS = [
    "scripts/verify_workspace_alignment_candidate.sh",
    "scripts/verify_event_store_candidate.sh",
    "scripts/verify_hermes_memory_candidate.sh",
    "scripts/verify_approval_loop_candidate.sh",
    "scripts/verify_prompt_middleware_candidate.sh",
    "scripts/verify_tail_risk_candidate.sh",
    "scripts/verify_v3_alpha_readiness_candidate.sh",
    "scripts/verify_v3_alpha_dry_run_candidate.sh",
]


def build_v3_alpha_release_manifest() -> dict:
    return {
        "manifest_version": "V3_ALPHA_RELEASE_MANIFEST_V10",
        "rc_version": ALPHA_RC_VERSION,
        "mode": "RELEASE_CANDIDATE_PACKAGING_ONLY",
        "base_branch": "v2.9.17-dev",
        "target_tag_candidate": "v3.0-alpha-rc1",
        "frozen_version_range": list(FROZEN_VERSION_RANGE),
        "components": list(ALPHA_RC_COMPONENTS),
        "required_verify_scripts": list(_REQUIRED_VERIFY_SCRIPTS),
        "release_artifacts": [
            "release/alpha_rc/v3_alpha_release_manifest_v10.json",
            "release/alpha_rc/v3_alpha_verification_matrix_v10.json",
            "release/alpha_rc/v3_alpha_frozen_module_inventory_v10.json",
            "release/alpha_rc/v3_alpha_known_limitations_v10.md",
            "release/alpha_rc/v3_alpha_operator_runbook_v10.md",
            "release/alpha_rc/v3_alpha_pre_tag_checklist_v10.md",
            "release/alpha_rc/README.md",
        ],
        "safety": dict(DEFAULT_ALPHA_RC_SAFETY),
        "runtime_enabled": False,
        "real_trade_allowed": False,
    }
