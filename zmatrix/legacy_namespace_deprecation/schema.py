# allowlist: forbidden-token-definition
from __future__ import annotations
LEGACY_NAMESPACE_DEPRECATION_VERSION = "V3519_LEGACY_NAMESPACE_DEPRECATION_GATE_V10"
DEFAULT_DEPRECATION_SAFETY = {"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,"runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"classifier_production_write_allowed":False,"role_definition_production_write_allowed":False,"legacy_runtime_rewrite_allowed":False,"legacy_module_direct_rewrite_allowed":False,"l2_l3_direct_migration_allowed":False,"legacy_namespace_expansion_allowed":False,"paper_only":True}
LEGACY = ["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","D_REJECT","WATCH_ONLY"]
CANONICAL = ["ROLE_CORE","ROLE_ROT","ROLE_HUNT","ROLE_WATCH","ROLE_BLOCK"]
