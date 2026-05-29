# allowlist: forbidden-token-definition
from __future__ import annotations
SECTOR_CLOCK_FOUNDATION_VERSION = "V359_SECTOR_CLOCK_FOUNDATION_V10"
DEFAULT_SECTOR_CLOCK_SAFETY = {"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,"runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"production_weight_adjustment_allowed":False,"synthetic_sector_index_production_allowed":False,"foundation_only":True}
SECTOR_PHASES = ["SECTOR_ADVANCE","SECTOR_RANGE","SECTOR_RETREAT","SECTOR_CRASH","SECTOR_CLIMAX","UNKNOWN_SECTOR_PHASE"]
CLOCK_DEFAULT_TTL = {"B":30,"R":5,"D":1}
DECAY_HALF_LIFE = {"B":30,"R":5,"D":1}
