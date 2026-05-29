# allowlist: forbidden-token-definition
from __future__ import annotations
ENTRY_QUALITY_REPAIR_VERSION = "V355_ENTRY_QUALITY_REPAIR_V10"
DEFAULT_ENTRY_REPAIR_SAFETY = {"real_trade_allowed": False, "broker_order_allowed": False, "auto_buy_allowed": False, "auto_sell_allowed": False, "auto_position_close_allowed": False, "real_z9_write_allowed": False, "hermes_memory_write_allowed": False, "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False, "system_prompt_write_allowed": False, "runtime_injection_allowed": False, "runtime_enabled": False, "external_api_default_on": False, "paper_repair_only": True}
ENTRY_ARCHETYPES = ["QUALITY_ROTATION", "DOWNTREND_BOUNCE_TRAP", "HIGH_VOLATILITY_NOISE", "LOW_VOLUME_WEAKNESS", "OVEREXTENDED_RIGHT_TAIL", "UNKNOWN_ENTRY_ARCHETYPE"]
CANDIDATE_STATUSES = ["CANDIDATE_READY_FOR_OBSERVATION", "CANDIDATE_READY_FOR_PAPER_REPLAY", "CANDIDATE_REJECTED_OVERFIT_RISK", "CANDIDATE_REJECTED_LOW_SAMPLE", "CANDIDATE_REJECTED_NO_IMPROVEMENT"]
DEFAULT_ENTRY_REPAIR_HURDLES = {"min_kept_count": 5000, "min_kept_rate": 0.20, "min_win_rate_delta": 0.03, "min_median_delta": 0.30, "min_trimmed_mean_delta": 0.10, "max_top_1pct_contribution": 0.50}
