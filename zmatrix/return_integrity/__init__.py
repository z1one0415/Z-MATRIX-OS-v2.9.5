from __future__ import annotations

RETURN_INTEGRITY_VERSION = "V36_RETURN_INTEGRITY_V10"

DEFAULT_RETURN_INTEGRITY_SAFETY = {
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
 "analysis_only": True,
}

RETURN_OUTLIER_THRESHOLDS = {
 "t5_abs_pct": 50.0,
 "t20_abs_pct": 120.0,
 "t60_abs_pct": 250.0,
 "single_day_jump_pct": 25.0,
 "price_gap_ratio": 0.35,
}

VERDICT_LEVELS = [
 "PERFORMANCE_QUALIFIED",
 "WEAK_RIGHT_TAIL_ONLY",
 "BLOCKED_RETURN_INTEGRITY",
 "BLOCKED_NEGATIVE_MEDIAN",
 "BLOCKED_LOW_WIN_RATE",
 "BLOCKED_OUTLIER_DOMINATED",
 "BLOCKED_INSUFFICIENT_VALID_RETURNS",
]
