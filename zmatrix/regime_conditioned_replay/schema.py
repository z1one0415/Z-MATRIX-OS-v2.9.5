# allowlist: forbidden-token-definition
from __future__ import annotations
REGIME_REPLAY_VERSION = "V357_REGIME_CONDITIONED_REPLAY_V10"
DEFAULT_REGIME_REPLAY_SAFETY = {"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,"runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,"paper_replay_only":True}
REGIME_POLICY_STATUSES = ["POLICY_READY_FOR_OBSERVATION","POLICY_REJECTED_NO_IMPROVEMENT","POLICY_REJECTED_LOW_SAMPLE","POLICY_REJECTED_OUTLIER_DOMINATED","POLICY_REJECTED_OPPORTUNITY_LOSS"]
DEFAULT_REGIME_REPLAY_HURDLES = {"min_kept_count":5000,"min_kept_rate":0.20,"min_win_rate_delta_vs_raw":0.03,"min_median_delta_vs_raw":0.30,"min_trimmed_mean_delta_vs_raw":0.10,"max_top_1pct_contribution":0.50,"max_opportunity_loss_rate":0.70,"must_improve_vs_mechanical_stop":True}
