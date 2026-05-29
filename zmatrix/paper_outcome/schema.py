# allowlist: forbidden-token-definition
"""Paper Outcome Schema — unified outcome record fields and safety"""
from __future__ import annotations

OUTCOME_RECORD_FIELDS = [
    "paper_id", "ticker", "entry_date", "entry_price", "paper_action",
    "target_horizon", "max_loss_plan", "invalidation_condition",
    "actual_return_t5", "actual_return_t20", "actual_return_t60",
    "max_drawdown_t20", "max_drawdown_t60",
    "outcome_status", "error_type", "review_note",
]

OUTCOME_STATUS = frozenset({"PENDING", "INSUFFICIENT_DATA", "READY", "INVALIDATED"})

DEFAULT_OUTCOME_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "auto_sell_allowed": False, "auto_position_close_allowed": False,
    "real_z9_write_allowed": False, "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False,
    "external_api_default_on": False, "runtime_enabled": False,
}
