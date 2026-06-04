#!/usr/bin/env python3
"""V11.6.1 Completion Chain."""
import subprocess,json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
S=["build_v11_6_1_oos_completion_contract.py","build_v11_6_closeout.py","check_v12_alpha_operating_loop_entry_gate.py"]
ok=True
for s in S:
    r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK' if r.returncode==0 else 'FAIL'}: {s} {r.stdout.strip()[:80]}")
    if r.returncode!=0:ok=False
ct=json.loads((C/"v11_6_1_oos_completion_contract.json").read_text())
g=json.loads((C/"v12_alpha_operating_loop_entry_gate.json").read_text())
print(f"OOS done={ct['paper_tracking_period_completed']} V12={g['status']} reasons={g['blocking_reasons']}")
