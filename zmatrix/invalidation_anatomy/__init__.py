from __future__ import annotations
INVALIDATION_ANATOMY_VERSION = "V354_INVALIDATION_ANATOMY_LAB_V10"
DEFAULT_INVALIDATION_ANATOMY_SAFETY = {"real_trade_allowed": False, "broker_order_allowed": False, "auto_buy_allowed": False, "auto_sell_allowed": False, "auto_position_close_allowed": False, "real_z9_write_allowed": False, "hermes_memory_write_allowed": False, "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False, "system_prompt_write_allowed": False, "runtime_injection_allowed": False, "runtime_enabled": False, "external_api_default_on": False, "anatomy_only": True}
INVALIDATION_PATH_TYPES = ["TRUE_BREAKDOWN", "FAST_RECOVERY", "SLOW_RECOVERY", "MARKET_BETA_SHAKEOUT", "STOCK_SPECIFIC_DAMAGE", "HIGH_VOLATILITY_WINNER", "UNKNOWN_PATH"]
SEPARABILITY_STATUSES = ["SEPARABLE", "WEAKLY_SEPARABLE", "NOT_SEPARABLE", "DATA_INSUFFICIENT"]
DEFAULT_ANATOMY_THRESHOLDS = {"trigger_loss_pct": -8.0, "fast_recovery_days": 5, "fast_recovery_level_pct": -4.0, "slow_recovery_level_pct": 0.0, "true_breakdown_t20_pct": -8.0, "high_vol_winner_t20_pct": 20.0, "stock_specific_underperform_pct": -5.0, "separable_score": 0.65, "weakly_separable_score": 0.55}
