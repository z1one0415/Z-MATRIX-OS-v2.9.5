#!/usr/bin/env python3
"""V12-Prep Full Chain Runner — enhanced semantic checks."""
import subprocess, json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
S=["build_v11_6_closeout.py","build_v11_7_closeout.py","build_v11_8_closeout.py","build_v11_9_closeout.py","check_v12_alpha_operating_loop_entry_gate.py","build_v12_entry_gate_recheck_report.py"]
ok=True
for s in S:
    r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK' if r.returncode==0 else 'FAIL'}: {s} {r.stdout.strip()[:80]}")
    if r.returncode!=0:ok=False
g=json.loads((C/"v12_alpha_operating_loop_entry_gate.json").read_text())
blocked="BLOCKED"in g.get("status","")
reasons=g.get("blocking_reasons",[])
if blocked:
    status_ok=True;reasons_ok=len(reasons)>0
    ready_ok=g["ready_for_alpha_operating_loop"]is False
    research_ok=g["research_only"]is False
else:
    status_ok="RESEARCH_ONLY_ALLOWED"in g["status"]
    ready_ok=g["ready_for_alpha_operating_loop"]is True
    research_ok=g["research_only"]is True
    reasons_ok=len(reasons)==0
safety_ok=(g["production"]=="BLOCKED"and g["broker_runtime"]=="BLOCKED"and g["real_trade"]=="BLOCKED"and not g["ready_for_alpha_claim"]and not g["alpha_validated"])
gate_consistent=status_ok and ready_ok and research_ok and reasons_ok
chain_ok=ok and gate_consistent
r2={"status":"V12_PREP_FULL_REPRODUCIBLE_CHAIN_PASS"if chain_ok else"V12_PREP_FULL_REPRODUCIBLE_CHAIN_BLOCKED","steps_returncode_pass":ok,"gate_logic_consistent":gate_consistent,"gate_ready_semantics_ok":ready_ok,"gate_research_only_semantics_ok":research_ok,"safety_blocked":safety_ok,"v12_gate_status":g["status"],"blocking_reasons":reasons,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(r2,open(C/"v12_prep_full_reproducible_chain.json","w"),indent=2)
print(f"Chain: {r2['status']} gate_ok={gate_consistent} ready_ok={ready_ok} research_ok={research_ok} safety={safety_ok}")
