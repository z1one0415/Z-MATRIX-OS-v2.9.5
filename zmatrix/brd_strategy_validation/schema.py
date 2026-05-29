# allowlist: forbidden-token-definition
from __future__ import annotations
BRD_5Y_VALIDATION_VERSION = "BRD_5Y_HISTORICAL_VALIDATION_V10"
DEFAULT_VALIDATION_SAFETY = {
    "real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,
    "auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,
    "hermes_memory_write_allowed":False,"auto_calibration_allowed":False,
    "prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,
    "runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,
    "historical_validation_only":True,
}
VALIDATION_HORIZONS = ["t5","t20","t60"]
BRD_ROLES = ["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","D_REJECT","UNKNOWN"]
