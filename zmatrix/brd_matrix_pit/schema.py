from __future__ import annotations
BRD_MATRIX_PIT_VERSION = "BRD_MATRIX_PIT_PRECOMPUTE_V10"
MATRIX_STATUS = ["PASS","FAIL","WATCH","INSUFFICIENT_DATA"]
DEFAULT_BRD_MATRIX_PIT_SAFETY = {
    "real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,
    "auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,
    "hermes_memory_write_allowed":False,"auto_calibration_allowed":False,
    "prompt_auto_injection_allowed":False,"system_prompt_write_allowed":False,
    "runtime_injection_allowed":False,"runtime_enabled":False,"external_api_default_on":False,
    "pit_matrix_precompute_only":True,
}
B_MATRIX_REQUIRED_FIELDS = ["status","base_role_eligible","reason_codes","quality_score","growth_score","valuation_score","financial_hard_gate_passed"]
R_MATRIX_REQUIRED_FIELDS = ["status","r_action_cap","cycle_score","momentum_score","trend_score","sector_phase","reason_codes"]
D_MATRIX_REQUIRED_FIELDS = ["status","short_event_eligible","event_score","short_momentum_score","risk_score","reason_codes"]
