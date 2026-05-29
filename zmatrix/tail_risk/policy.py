# allowlist: forbidden-token-definition
"""Tail-Risk Policy — validate results, decisions, downgrades, safety"""
from __future__ import annotations

from zmatrix.tail_risk.schemas import TAIL_RISK_DECISION, ACTION_DOWNGRADE

_BLOCKED_FIELDS = [
    "real_trade_allowed", "broker_order_allowed", "auto_buy_allowed",
    "auto_sell_allowed", "auto_cancel_allowed", "auto_position_close_allowed",
    "real_z9_write_allowed", "hermes_memory_write_allowed",
    "auto_calibration_allowed", "prompt_auto_injection_allowed",
]


def assert_no_real_trade_effects(record: dict) -> list[str]:
    """Check top-level and safety nested for all blocked fields."""
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


def validate_tail_risk_result(result: dict) -> list[str]:
    violations = []
    if not result.get("gate_id"):
        violations.append("gate_id required")
    if result.get("decision") not in TAIL_RISK_DECISION:
        violations.append(f"invalid decision: {result.get('decision')}")
    if result.get("action_downgrade") not in ACTION_DOWNGRADE:
        violations.append(f"invalid action_downgrade: {result.get('action_downgrade')}")
    severe = result.get("decision") in ("HIBERNATE", "FREEZE", "ISOLATE")
    if severe and result.get("requires_human_review") is not True:
        violations.append("HIBERNATE/FREEZE/ISOLATE requires human review")
    return violations + assert_no_real_trade_effects(result)


def validate_action_downgrade(result: dict) -> list[str]:
    violations = []
    downgrade = result.get("action_downgrade")
    if downgrade not in ACTION_DOWNGRADE:
        violations.append(f"invalid action_downgrade: {downgrade}")
    return violations + assert_no_real_trade_effects(result)
