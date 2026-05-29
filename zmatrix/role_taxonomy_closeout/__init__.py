# allowlist: forbidden-token-definition
from __future__ import annotations
ROLE_TAXONOMY_CLOSEOUT_VERSION = "V3515_ROLE_TAXONOMY_CLOSEOUT_V10"
DEFAULT_ROLE_TAXONOMY_SAFETY = {"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,"runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"classifier_production_write_allowed":False,"role_definition_production_write_allowed":False,"legacy_runtime_rewrite_allowed":False,"paper_adapter_only":True}
LEGACY_TO_CANONICAL_ROLE = {"A_LONG_CORE":"ROLE_CORE","B_MID_ROTATION":"ROLE_ROT","C_SHORT_EVENT":"ROLE_HUNT","D_REJECT":"ROLE_BLOCK","WATCH_ONLY":"ROLE_WATCH"}
CANONICAL_TO_LEGACY_ROLE = {"ROLE_CORE":"A_LONG_CORE","ROLE_ROT":"B_MID_ROTATION","ROLE_HUNT":"C_SHORT_EVENT","ROLE_BLOCK":"D_REJECT","ROLE_WATCH":"WATCH_ONLY"}
EXPECTED_ROLE_SOURCE = {"ROLE_CORE":["MATRIX_B_BASE"],"ROLE_ROT":["MATRIX_R_ROTATION"],"ROLE_HUNT":["MATRIX_D_DARK_HORSE"],"ROLE_WATCH":["MATRIX_B_BASE","MATRIX_R_ROTATION","MATRIX_D_DARK_HORSE","UNKNOWN"],"ROLE_BLOCK":["NONE","UNKNOWN"]}
CANONICAL_ACTIONS = {"ROLE_CORE":"ACTION_HOLD_CORE","ROLE_ROT":"ACTION_PAPER_ROT","ROLE_HUNT":"ACTION_PAPER_HUNT","ROLE_WATCH":"ACTION_WATCH_ONLY","ROLE_BLOCK":"ACTION_BLOCK"}
LEGACY_LOCKED_MODULES = ["account_constitution.py","pre_trade_checklist.py","z8_position_control.py","brd_result_audit"]
