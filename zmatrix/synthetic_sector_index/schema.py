# allowlist: forbidden-token-definition
from __future__ import annotations
SYNTHETIC_SECTOR_INDEX_VERSION = "V3511_SYNTHETIC_SECTOR_INDEX_V10"
DEFAULT_SYNTHETIC_SECTOR_SAFETY = {"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,"runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"production_weight_adjustment_allowed":False,"synthetic_sector_index_production_allowed":False,"paper_only_sector_index":True}
SECTOR_PHASES = ["SECTOR_ADVANCE","SECTOR_RANGE","SECTOR_RETREAT","SECTOR_CRASH","SECTOR_CLIMAX","UNKNOWN_SECTOR_PHASE"]
MIN_ACTIVE_MEMBERS = 3; MIN_ACTIVE_MEMBER_RATIO = 0.30; BASE_INDEX_VALUE = 1000.0
