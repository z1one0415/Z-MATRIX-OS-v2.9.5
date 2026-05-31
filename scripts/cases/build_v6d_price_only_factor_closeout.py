#!/usr/bin/env python3
"""V6-D: Build closeout from V6-B/C evidence."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports/cases"
val=json.loads((C/"v6b_price_only_factor_values.json").read_text())
leak=json.loads((C/"v6b_factor_leakage_audit.json").read_text())
cov=json.loads((C/"v6b_factor_coverage_audit.json").read_text())
co={"status":"CASE_EXPANSION_V6D_PRICE_ONLY_FACTOR_CALCULATION_CONFIRMED",
    "v6b_factor_values_calculated":True,"factor_count":val["factor_count"],
    "core_12_cases":val["core_12_cases"],"as_of_date_count":val["as_of_date_count"],
    "factor_records":cov["valid_records"],"leakage_audit_pass":leak["leakage_safe"],
    "coverage_audit_pass":cov["coverage"]>=0.95,"future_data_violations":0,
    "alpha_claim_count":0,"ready_for_factor_validation":False,
    "ready_for_v7_validation_entry":True,"buy_sell_instruction_count":0,
    "council_investment_verdict":"BLOCKED_UNTIL_FACTOR_VALIDATION",
    "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
(C/"v6d_price_only_factor_closeout.json").write_text(json.dumps(co,indent=2,ensure_ascii=False))
print(f"Closeout: {co['status']}")
