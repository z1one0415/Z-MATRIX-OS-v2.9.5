#!/usr/bin/env python3
"""V11.6.1 OOS Completion Chain."""
import subprocess,json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
S=["build_v11_6_1_oos_completion_contract.py","resolve_v11_6_1_oos_due_labels.py","calculate_v11_6_1_oos_paper_outcomes.py","audit_v11_6_1_oos_completion.py","build_v11_6_closeout.py","check_v12_alpha_operating_loop_entry_gate.py"]
ok=True
for s in S:
    r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK' if r.returncode==0 else 'FAIL'}: {s} {r.stdout.strip()[:80]}")
    if r.returncode!=0:ok=False
audit=json.loads((C/"v11_6_1_oos_completion_audit.json").read_text())
g=json.loads((C/"v12_alpha_operating_loop_entry_gate.json").read_text())
r={"status":"V11_6_1_OOS_COMPLETION_CHAIN_PASS"if audit["paper_tracking_period_completed"]else"V11_6_1_OOS_COMPLETION_CHAIN_PASS_BLOCKED_BY_LABELS","steps_returncode_pass":ok,"paper_tracking_period_completed":audit["paper_tracking_period_completed"],"v12_gate_status":g["status"],"v12_blocking_reasons":g["blocking_reasons"],"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(r,open(C/"v11_6_1_oos_completion_chain.json","w"),indent=2)
print(f"OOS Chain: {r['status']} tracking_done={audit['paper_tracking_period_completed']}")
