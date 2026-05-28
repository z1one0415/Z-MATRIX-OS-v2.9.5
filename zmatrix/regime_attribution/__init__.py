from __future__ import annotations
REGIME_ATTRIBUTION_VERSION = "V356_MARKET_REGIME_ATTRIBUTION_V10"
DEFAULT_REGIME_ATTRIBUTION_SAFETY = {"real_trade_allowed": False,"broker_order_allowed": False,"auto_buy_allowed": False,"auto_sell_allowed": False,"auto_position_close_allowed": False,"real_z9_write_allowed": False,"hermes_memory_write_allowed": False,"auto_calibration_allowed": False,"prompt_auto_injection_allowed": False,"system_prompt_write_allowed": False,"runtime_injection_allowed": False,"runtime_enabled": False,"external_api_default_on": False,"attribution_only": True}
MARKET_REGIMES = ["BULL_TREND","RANGE_BOUND","BEAR_TREND","LIQUIDITY_EXPANSION","LIQUIDITY_CONTRACTION","HIGH_VOLATILITY","LOW_VOLATILITY","UNKNOWN_MARKET_REGIME"]
SECTOR_PHASES = ["SECTOR_ADVANCE","SECTOR_RANGE","SECTOR_RETREAT","SECTOR_CLIMAX","SECTOR_CRASH","UNKNOWN_SECTOR_PHASE"]
REGIME_SEPARABILITY_STATUSES = ["REGIME_SEPARABLE","WEAKLY_REGIME_SEPARABLE","NOT_REGIME_SEPARABLE","DATA_INSUFFICIENT"]
DEFAULT_REGIME_THRESHOLDS = {"min_feature_ready_rate":0.70,"min_group_sample":1000,"regime_separable_score":0.65,"weakly_regime_separable_score":0.55,"min_win_rate_delta":0.03,"min_median_delta":0.30,"max_top_1pct_contribution":0.50}
