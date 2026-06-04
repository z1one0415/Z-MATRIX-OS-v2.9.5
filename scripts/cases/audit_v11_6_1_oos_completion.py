#!/usr/bin/env python3
"""Audit OOS completion."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
res=json.loads((C/"v11_6_1_oos_due_label_resolution.json").read_text())
out=json.loads((C/"v11_6_1_oos_paper_outcomes.json").read_text())
all_avail=res["all_due_labels_available"]
calc_ok=out["calculated_observation_count"]==out["observation_count"]and out["blocked_observation_count"]==0
ok=all_avail and calc_ok
a=dict(status="V11_6_1_OOS_COMPLETION_AUDIT_PASS"if ok else"V11_6_1_OOS_COMPLETION_AUDIT_BLOCKED",paper_tracking_period_completed=ok,completion_ready_for_v12_gate=ok,blocking_reasons=[]if ok else["OOS_DUE_LABELS_NOT_AVAILABLE"],ready_for_alpha_claim=False,alpha_validated=False,production="BLOCKED",broker_runtime="BLOCKED",real_trade="BLOCKED")
json.dump(a,open(C/"v11_6_1_oos_completion_audit.json","w"),indent=2)
print(f"Audit: {'PASS' if ok else 'BLOCKED'} avail={all_avail} calc_ok={calc_ok}")
