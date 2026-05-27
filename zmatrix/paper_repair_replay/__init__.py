from __future__ import annotations
PAPER_REPAIR_REPLAY_VERSION = "V353_PAPER_REPAIR_REPLAY_V10"
DEFAULT_REPAIR_REPLAY_SAFETY = {"real_trade_allowed": False, "broker_order_allowed": False, "auto_buy_allowed": False, "auto_sell_allowed": False, "auto_position_close_allowed": False, "real_z9_write_allowed": False, "hermes_memory_write_allowed": False, "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False, "system_prompt_write_allowed": False, "runtime_injection_allowed": False, "runtime_enabled": False, "external_api_default_on": False, "paper_repair_replay_only": True}
REPAIR_REPLAY_STATUSES = ["REPAIRED_REPLAY_READY", "BLOCKED_REPLAY_DATA_MISSING", "BLOCKED_PRICE_PATH_MISSING", "BLOCKED_LOOKAHEAD_RISK", "BLOCKED_NO_REPAIRABLE_ACTIONS"]
