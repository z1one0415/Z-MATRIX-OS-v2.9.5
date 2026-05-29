# allowlist: forbidden-token-definition
"""Dry-Run schemas — steps, safety defaults"""
from __future__ import annotations

DRY_RUN_VERSION = "V3_ALPHA_DRY_RUN_REHEARSAL_V10"

DRY_RUN_STEPS = [
    "PaperLedgerEvent",
    "OutcomeBackfillEvent",
    "MemoryCandidatePreview",
    "ApprovalRequest",
    "HumanApprovalDecision",
    "PromptPatchRequest",
    "PromptRenderPreview",
    "TailRiskControllerPreview",
    "V3AlphaReadinessReport",
]

DEFAULT_DRY_RUN_SAFETY = {
    "real_trade_allowed": False,
    "broker_order_allowed": False,
    "auto_buy_allowed": False,
    "auto_sell_allowed": False,
    "auto_position_close_allowed": False,
    "real_z9_write_allowed": False,
    "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False,
    "system_prompt_write_allowed": False,
    "runtime_injection_allowed": False,
    "runtime_enabled": False,
    "external_api_default_on": False,
    "dry_run_only": True,
}
