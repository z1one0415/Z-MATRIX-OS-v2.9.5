# allowlist: forbidden-token-definition
from __future__ import annotations
GOVERNANCE_CLOSEOUT_VERSION = "V357_GOVERNANCE_POOL_RESILIENCE_V10"
DEFAULT_GOVERNANCE_SAFETY = {"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,"runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"z9_auto_calibration_write_allowed":False,"g18_conflict_resolver_write_allowed":False,"o3_conditional_runtime_enabled":False,"governance_audit_only":True}
GOVERNANCE_STATUSES = ["GOVERNANCE_PASS","GOVERNANCE_BLOCKED_YAML_MUTATION","GOVERNANCE_BLOCKED_PARAMETER_WRITE","GOVERNANCE_BLOCKED_POOL_RESILIENCE","GOVERNANCE_WARNING_CLOCK_ALIGNMENT","GOVERNANCE_WARNING_CONFLICT_RISK","GOVERNANCE_DATA_INSUFFICIENT"]
POOL_RESILIENCE_THRESHOLDS = {"min_daily_pool_size":20,"min_window_pool_size":100,"max_zero_pool_day_rate":0.05,"max_small_pool_day_rate":0.20,"min_kept_rate_preferred":0.60,"min_kept_rate_hard":0.20}
MATRIX_CLOCK_THRESHOLDS = {"b_matrix_ttl_days":30,"r_matrix_ttl_days":5,"d_matrix_ttl_days":1,"max_cross_clock_gap_days":30}
