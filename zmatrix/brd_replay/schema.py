from __future__ import annotations
BRD_REPLAY_VERSION = "BRD_HISTORICAL_REPLAY_V10"
BRD_ROLES = ["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","D_REJECT","WATCH_ONLY","DATA_GAP"]
BRD_DECISIONS = ["PAPER_ACTION","WATCH_ONLY","REJECT","DATA_GAP"]
DEFAULT_BRD_REPLAY_SAFETY = {
    "real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,
    "auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,
    "hermes_memory_write_allowed":False,"auto_calibration_allowed":False,
    "prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,
    "runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,
    "historical_replay_only":True,
}
