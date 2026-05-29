# allowlist: forbidden-token-definition
from __future__ import annotations
REGIME_SECTOR_ATTRIBUTION_VERSION = "V3512_REGIME_SECTOR_ATTRIBUTION_V10"
DEFAULT_REGIME_SECTOR_SAFETY = {"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,"runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"production_weight_adjustment_allowed":False,"synthetic_sector_index_production_allowed":False,"paper_attribution_only":True}
JOINT_ATTRIBUTION_STATUSES = ["JOINT_ATTRIBUTION_SEPARABLE","WEAKLY_JOINT_SEPARABLE","NOT_JOINT_SEPARABLE","DATA_INSUFFICIENT"]
JOINT_THRESHOLDS = {"min_join_coverage":0.90,"min_segment_count":1000,"min_sector_count":20,"min_good_segment_count":3,"win_rate_spread_threshold":0.08,"median_spread_threshold":1.0,"invalidation_spread_threshold":0.10,"max_top_sector_share":0.30,"max_top_5_sector_share":0.60}
