"""PATCH-A-6: Parameter Trust Map"""
from __future__ import annotations

TRUST_LEVELS = {0: "T0_ENGINEERING_DEFAULT", 1: "T1_HISTORICAL_SAMPLE", 2: "T2_TEMPORAL_SPLIT", 3: "T3_SECTOR_SPLIT", 4: "T4_OUT_OF_SAMPLE", 5: "T5_PAPER_LIVE_SHADOW"}

def classify_parameter_trust(*, param_name: str, has_historical_validation: bool, has_temporal_split: bool, has_sector_split: bool, has_out_of_sample: bool, has_live_shadow: bool) -> dict:
    level = 0
    if has_historical_validation: level = 1
    if has_temporal_split and level >= 1: level = 2
    if has_sector_split and level >= 2: level = 3
    if has_out_of_sample and level >= 3: level = 4
    if has_live_shadow and level >= 4: level = 5
    production_allowed = level >= 4
    return {"param_name": param_name, "trust_level": level, "trust_label": TRUST_LEVELS[level], "production_allowed": production_allowed, "requires_validation": level < 4}

def build_parameter_trust_map() -> dict:
    params = {"b_matrix_score_weights": classify_parameter_trust(param_name="b_matrix_score_weights", has_historical_validation=True, has_temporal_split=False, has_sector_split=False, has_out_of_sample=False, has_live_shadow=False), "d_matrix_score_weights": classify_parameter_trust(param_name="d_matrix_score_weights", has_historical_validation=False, has_temporal_split=False, has_sector_split=False, has_out_of_sample=False, has_live_shadow=False), "trading_cost_commission": classify_parameter_trust(param_name="trading_cost_commission", has_historical_validation=False, has_temporal_split=False, has_sector_split=False, has_out_of_sample=False, has_live_shadow=False), "slippage_model": classify_parameter_trust(param_name="slippage_model", has_historical_validation=False, has_temporal_split=False, has_sector_split=False, has_out_of_sample=False, has_live_shadow=False), "invalidation_threshold": classify_parameter_trust(param_name="invalidation_threshold", has_historical_validation=True, has_temporal_split=False, has_sector_split=False, has_out_of_sample=False, has_live_shadow=False), "regime_policy_weights": classify_parameter_trust(param_name="regime_policy_weights", has_historical_validation=True, has_temporal_split=False, has_sector_split=False, has_out_of_sample=False, has_live_shadow=False)}
    return {"map_version": "PATCH_A_PARAMETER_TRUST_MAP_V10", "parameters": params, "summary": {"t0_count": sum(1 for p in params.values() if p["trust_level"] == 0), "t1_count": sum(1 for p in params.values() if p["trust_level"] == 1), "t2_count": sum(1 for p in params.values() if p["trust_level"] == 2), "t3_count": sum(1 for p in params.values() if p["trust_level"] == 3), "t4_plus_count": sum(1 for p in params.values() if p["trust_level"] >= 4), "production_ready_params": sum(1 for p in params.values() if p["production_allowed"]), "recommendation": "ALL parameters currently T0-T1; NO parameter ready for production; ALL require out-of-sample validation before T4/T5 claim"}}
