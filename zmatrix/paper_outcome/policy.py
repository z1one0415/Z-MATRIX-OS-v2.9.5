"""Paper Outcome Policy — validate records and safety"""
from __future__ import annotations

from zmatrix.paper_outcome.schema import OUTCOME_STATUS

_BLOCKED_FIELDS = [
    "real_trade_allowed", "broker_order_allowed", "auto_sell_allowed",
    "auto_position_close_allowed", "real_z9_write_allowed",
    "hermes_memory_write_allowed", "auto_calibration_allowed",
    "prompt_auto_injection_allowed", "runtime_enabled",
]


def assert_no_real_trade_effects(record: dict) -> list[str]:
    violations = []
    for field in _BLOCKED_FIELDS:
        if record.get(field) is True:
            violations.append(f"top-level {field} must be False")
    safety = record.get("safety", {})
    if not isinstance(safety, dict):
        violations.append("safety must be dict")
        safety = {}
    for field in _BLOCKED_FIELDS:
        if safety.get(field) is True:
            violations.append(f"safety.{field} must be False")
    return violations


def validate_outcome_record(record: dict) -> list[str]:
    violations = []
    if not record.get("paper_id"):
        violations.append("paper_id required")
    if not record.get("ticker"):
        violations.append("ticker required")
    if record.get("outcome_status") not in OUTCOME_STATUS:
        violations.append(f"invalid status: {record.get('outcome_status')}")
    return violations + assert_no_real_trade_effects(record)
