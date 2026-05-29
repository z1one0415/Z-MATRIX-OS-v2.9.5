# allowlist: forbidden-token-definition
from __future__ import annotations
BRD_RESULT_AUDIT_VERSION="V35_BRD_RESULT_AUDIT_V10"
BRD_ROLES=["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","D_REJECT","UNKNOWN"]
DEFAULT_AUDIT_SAFETY={"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,"runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,"audit_only":True}
AUDIT_BLOCKED_FIELDS=["real_trade_allowed","broker_order_allowed","auto_buy_allowed","auto_sell_allowed","auto_position_close_allowed","real_z9_write_allowed","hermes_memory_write_allowed","auto_calibration_allowed","prompt_auto_injection_allowed","system_prompt_write_allowed","runtime_injection_allowed","runtime_enabled","external_api_default_on"]
