# allowlist: forbidden-token-definition
"""Alpha RC schemas — version, components, frozen range, safety"""
from __future__ import annotations

ALPHA_RC_VERSION = "V3_ALPHA_RC_V10"

FROZEN_VERSION_RANGE = [
    "v2.9.10-dev", "v2.9.11-dev", "v2.9.12-dev",
    "v2.9.13-dev", "v2.9.14-dev", "v2.9.15-dev",
    "v2.9.16-dev", "v2.9.17-dev",
]

ALPHA_RC_COMPONENTS = [
    "Workspace Alignment & Pipeline Census",
    "EventStore & Unified Event Ledger",
    "Hermes Memory Kernel Preview",
    "Approval-Required Reflection Loop",
    "Prompt Hot-Patching Middleware Preview",
    "Tail-Risk Autonomic Gates Preview",
    "v3.0-alpha Integration Readiness Gate",
    "v3.0-alpha Dry-Run Rehearsal",
]

ALPHA_RC_FORBIDDEN_CAPABILITIES = [
    "real_trade", "broker_order", "auto_buy", "auto_sell",
    "auto_position_close", "real_z9_write", "hermes_memory_write",
    "auto_calibration", "prompt_auto_injection", "system_prompt_write",
    "runtime_prompt_injection", "external_api_default_on",
]

DEFAULT_ALPHA_RC_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "auto_buy_allowed": False, "auto_sell_allowed": False,
    "auto_position_close_allowed": False, "real_z9_write_allowed": False,
    "hermes_memory_write_allowed": False, "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False, "system_prompt_write_allowed": False,
    "runtime_injection_allowed": False, "runtime_enabled": False,
    "external_api_default_on": False, "rc_packaging_only": True,
}
