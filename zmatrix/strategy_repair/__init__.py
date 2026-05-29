# allowlist: forbidden-token-definition
from __future__ import annotations

STRATEGY_REPAIR_VERSION = "V352_STRATEGY_REPAIR_LAB_V10"

DEFAULT_REPAIR_SAFETY = {
 "real_trade_allowed": False, "broker_order_allowed": False,
 "auto_buy_allowed": False, "auto_sell_allowed": False,
 "auto_position_close_allowed": False, "real_z9_write_allowed": False,
 "hermes_memory_write_allowed": False, "auto_calibration_allowed": False,
 "prompt_auto_injection_allowed": False, "system_prompt_write_allowed": False,
 "runtime_injection_allowed": False, "runtime_enabled": False,
 "external_api_default_on": False, "repair_lab_only": True,
}

REPAIR_STATUSES = [
 "REPAIR_CANDIDATE_READY", "REPAIR_CANDIDATE_REJECTED",
 "REPAIR_INSUFFICIENT_SAMPLE", "REPAIR_OVERFIT_RISK",
 "REPAIR_DATA_INTEGRITY_BLOCKED",
]

DEFAULT_REPAIR_HURDLES = {
 "min_sample_count": 5000, "min_active_count": 1000,
 "min_win_rate_delta": 0.03, "min_median_delta": 0.30,
 "max_top_1pct_contribution": 0.50, "must_keep_ready_outcome_rate_above": 0.95,
}
