"""Portfolio Exposure Policy — validate exposure records"""
from __future__ import annotations

_BLOCKED_FIELDS = [
    "real_trade_allowed", "broker_order_allowed", "auto_sell_allowed",
    "auto_position_close_allowed", "auto_buy_allowed",
    "real_z9_write_allowed", "hermes_memory_write_allowed",
    "auto_calibration_allowed", "prompt_auto_injection_allowed",
    "runtime_enabled",
]


def assert_no_real_trade_effects(record: dict) -> list[str]:
    violations = []
    for field in _BLOCKED_FIELDS:
        if record.get(field) is True:
            violations.append(f"{field} must be False")
    safety = record.get("safety", {})
    if not isinstance(safety, dict):
        violations.append("safety must be dict")
        safety = {}
    for field in _BLOCKED_FIELDS:
        if safety.get(field) is True:
            violations.append(f"safety.{field} must be False")
    return violations


def validate_exposure_record(record: dict) -> list[str]:
    violations = []
    if not record.get("ticker"):
        violations.append("ticker required")
    return violations + assert_no_real_trade_effects(record)
