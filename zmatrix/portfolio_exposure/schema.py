"""Portfolio Exposure Schema — position snapshot fields"""
from __future__ import annotations

EXPOSURE_RECORD_FIELDS = [
    "position_id", "ticker", "role", "weight", "entry_price",
    "current_price", "beta", "sector", "chain", "exposure_ratio",
]

DEFAULT_EXPOSURE_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "auto_sell_allowed": False, "auto_position_close_allowed": False,
    "auto_buy_allowed": False,
    "real_z9_write_allowed": False, "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False,
    "runtime_enabled": False,
}
