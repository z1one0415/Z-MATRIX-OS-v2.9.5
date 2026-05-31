#!/usr/bin/env python3
"""V6-D: Build closeout only if all audits pass."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
val=json.loads((C/"v6b_price_only_factor_values.json").read_text())
pkt=json.loads((C/"v6b_factor_snapshot_packet.json").read_text())
leak=json.loads((C/"v6b_factor_leakage_audit.json").read_text())
cov=json.loads((C/"v6b_factor_coverage_audit.json").read_text())
snap_ok=pkt["status"]=="V6B_FACTOR_SNAPSHOT_PACKET_BUILT"
leak_ok=leak["leakage_safe"]
cov_ok=cov["coverage"]>=0.95
inp_ok=leak.get("input_date_violations",-1)==0
all_ok=snap_ok and leak_ok and cov_ok and inp_ok
co={"status":"CASE_EXPANSION_V6D_PRICE_ONLY_FACTOR_CALCULATION_CONFIRMED" if all_ok else "CASE_EXPANSION_V6D_BLOCKED_AUDIT_FAILURE",
    "v6b_factor_values_calculated":True,"snapshot_packet_built":snap_ok,
    "factor_count":val["factor_count"],"core_12_cases":val["core_12_cases"],
    "as_of_date_count":val["as_of_date_count"],"factor_records":cov["valid_records"],
    "leakage_audit_pass":leak_ok,"coverage_audit_pass":cov_ok,
    "future_data_violations":leak["future_data_violations"],
    "input_date_violations":leak.get("input_date_violations",0),
    "alpha_claim_count":leak.get("alpha_claim_violations",0),
    "ready_for_factor_validation":False,"ready_for_v7_validation_entry":all_ok,
    "buy_sell_instruction_count":0,"council_investment_verdict":"BLOCKED_UNTIL_FACTOR_VALIDATION",
    "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
(C/"v6d_price_only_factor_closeout.json").write_text(json.dumps(co,indent=2,ensure_ascii=False))
print(f"Closeout: {co['status']}")
