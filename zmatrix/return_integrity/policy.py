# allowlist: forbidden-token-definition
from __future__ import annotations

BLOCKED_FIELDS = [
    "real_trade_allowed", "broker_order_allowed", "auto_buy_allowed",
    "auto_sell_allowed", "auto_position_close_allowed", "real_z9_write_allowed",
    "hermes_memory_write_allowed", "auto_calibration_allowed",
    "prompt_auto_injection_allowed", "system_prompt_write_allowed",
    "runtime_injection_allowed", "runtime_enabled", "external_api_default_on",
]

def validate_return_integrity_report(record: dict) -> list[str]:
    errors = []
    if not isinstance(record, dict):
        return ["record must be dict"]
    for field in BLOCKED_FIELDS:
        if record.get(field) is True:
            errors.append(f"{field} must be False")
    safety = record.get("safety", {})
    if safety and not isinstance(safety, dict):
        errors.append("safety must be dict")
        return errors
    for field in BLOCKED_FIELDS:
        if isinstance(safety, dict) and safety.get(field) is True:
            errors.append(f"safety.{field} must be False")
    return errors
