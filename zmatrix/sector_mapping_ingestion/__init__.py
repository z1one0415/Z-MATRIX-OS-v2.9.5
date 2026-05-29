# allowlist: forbidden-token-definition
from __future__ import annotations
SECTOR_MAPPING_INGESTION_VERSION = "V3510_SECTOR_MAPPING_INGESTION_V10"
DEFAULT_SECTOR_MAPPING_SAFETY = {"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,"runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"production_weight_adjustment_allowed":False,"synthetic_sector_index_production_allowed":False,"ingestion_only":True}
MAPPING_STATUS = ["READY","PARTIAL","DATA_INSUFFICIENT","BLOCKED_POLICY_VIOLATION"]
TICKER_FIELDS = ["ts_code","ticker","symbol","code","股票代码"]
NAME_FIELDS = ["name","stock_name","股票名称"]
SECTOR_FIELDS = ["sector","sector_code","industry","sw_industry","申万行业","中信行业","同花顺行业"]
THEME_FIELDS = ["concept","theme","concept_name","概念","主题"]
MARKET_FIELDS = ["market","exchange","list_board"]
LIST_DATE_FIELDS = ["list_date","ipo_date","上市日期"]
MIN_READY_TICKERS = 5000; MIN_READY_COVERAGE = 0.90; MIN_PARTIAL_COVERAGE = 0.30
