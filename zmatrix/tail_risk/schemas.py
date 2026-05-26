"""Tail-Risk schemas — states, gate types, decisions, safety defaults"""
from __future__ import annotations

TAIL_RISK_STATE = frozenset({
    "NORMAL", "CAUTION", "STRESS", "CRASH", "HIBERNATE", "WAKEUP_PROBATION",
})

TAIL_RISK_GATE_TYPES = frozenset({
    "LIMIT_DOWN_BLACKHOLE", "DOMESTIC_LIQUIDITY_CRASH", "HIBERNATE_MODE",
    "WAKEUP_PROBATION", "D_MATRIX_FREEZE", "BMO_RISK_ISOLATION_UNIT",
})

ACTION_DOWNGRADE = frozenset({
    "ENTER_TO_WAIT", "ADD_TO_HOLD", "HOLD_TO_REVIEW", "REVIEW_TO_FREEZE",
    "FREEZE_TO_HIBERNATE", "RISK_ISOLATE", "NO_ACTION",
})

TAIL_RISK_DECISION = frozenset({
    "ALLOW", "WARN", "DOWNGRADE", "FREEZE", "HIBERNATE", "ISOLATE",
})

TAIL_RISK_RESULT_FIELDS = [
    "gate_id", "gate_type", "state", "decision", "action_downgrade",
    "reason", "evidence", "affected_roles", "affected_tickers",
    "freeze_new_entries", "allow_existing_position_review",
    "requires_human_review", "safety",
]

DEFAULT_TAIL_RISK_SAFETY = {
    "real_trade_allowed": False,
    "broker_order_allowed": False,
    "auto_buy_allowed": False,
    "auto_sell_allowed": False,
    "auto_cancel_allowed": False,
    "auto_position_close_allowed": False,
    "real_z9_write_allowed": False,
    "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False,
    "external_api_default_on": False,
    "local_event_write_allowed": True,
}
