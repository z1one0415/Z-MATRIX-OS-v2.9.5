"""Alpha Tag Gate schemas — version, tag target, required artifacts"""
from __future__ import annotations

ALPHA_TAG_GATE_VERSION = "V3_ALPHA_TAG_GATE_V10"

TARGET_TAG = "v3.0-alpha-rc1"

TAG_GATE_MODE = "TAG_REVIEW_ONLY"

TAG_GATE_REQUIRED_ARTIFACTS = [
    "release/alpha_rc/v3_alpha_release_manifest_v10.json",
    "release/alpha_rc/v3_alpha_verification_matrix_v10.json",
    "release/alpha_rc/v3_alpha_frozen_module_inventory_v10.json",
    "release/alpha_rc/v3_alpha_known_limitations_v10.md",
    "release/alpha_rc/v3_alpha_operator_runbook_v10.md",
    "release/alpha_rc/v3_alpha_pre_tag_checklist_v10.md",
    "release/alpha_rc/README.md",
]

TAG_GATE_REQUIRED_VERIFY_SCRIPTS = [
    "scripts/verify_workspace_alignment_candidate.sh",
    "scripts/verify_event_store_candidate.sh",
    "scripts/verify_hermes_memory_candidate.sh",
    "scripts/verify_approval_loop_candidate.sh",
    "scripts/verify_prompt_middleware_candidate.sh",
    "scripts/verify_tail_risk_candidate.sh",
    "scripts/verify_v3_alpha_readiness_candidate.sh",
    "scripts/verify_v3_alpha_dry_run_candidate.sh",
    "scripts/verify_v3_alpha_rc_candidate.sh",
]

DEFAULT_TAG_GATE_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "auto_buy_allowed": False, "auto_sell_allowed": False,
    "auto_position_close_allowed": False, "real_z9_write_allowed": False,
    "hermes_memory_write_allowed": False, "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False, "system_prompt_write_allowed": False,
    "runtime_injection_allowed": False, "runtime_enabled": False,
    "external_api_default_on": False,
    "git_tag_execute_allowed": False, "git_push_tags_allowed": False,
    "tag_review_only": True,
}
