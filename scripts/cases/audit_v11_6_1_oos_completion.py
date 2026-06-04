#!/usr/bin/env python3
"""Audit OOS completion — checks contract purity + label resolution + outcomes."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
ct=json.loads((C/"v11_6_1_oos_completion_contract.json").read_text())
res=json.loads((C/"v11_6_1_oos_due_label_resolution.json").read_text())
out=json.loads((C/"v11_6_1_oos_paper_outcomes.json").read_text())
# Contract purity
has_observations="observations"in ct;has_t20="t20_complete"in ct
contract_pure=ct["status"]=="V11_6_1_OOS_COMPLETION_CONTRACT_BUILT"and not has_observations and not has_t20 and ct["paper_tracking_period_completed"]is False
all_avail=res["all_due_labels_available"]
calc_ok=out["calculated_observation_count"]==ct["required_observation_count"]and out["blocked_observation_count"]==0
ok=contract_pure and all_avail and calc_ok
reasons=[]
if not contract_pure:reasons.append("CONTRACT_NOT_PURE"if has_observations or has_t20 else"CONTRACT_PAPER_TRACKING_SHOULD_BE_FALSE")
if not all_avail:reasons.append("OOS_DUE_LABELS_NOT_AVAILABLE")
if not calc_ok:reasons.append("OOS_CALCULATION_INCOMPLETE")
a=dict(status="V11_6_1_OOS_COMPLETION_AUDIT_PASS"if ok else"V11_6_1_OOS_COMPLETION_AUDIT_BLOCKED",paper_tracking_period_completed=ok,completion_ready_for_v12_gate=ok,contract_purity_ok=contract_pure,blocking_reasons=reasons,ready_for_alpha_claim=False,alpha_validated=False,production="BLOCKED",broker_runtime="BLOCKED",real_trade="BLOCKED")
json.dump(a,open(C/"v11_6_1_oos_completion_audit.json","w"),indent=2)
print(f"Audit: {'PASS' if ok else 'BLOCKED'} contract_pure={contract_pure} avail={all_avail} calc_ok={calc_ok}")
