#!/usr/bin/env python3
"""Audit: all 4 V10 upstream JSONs must have explicit safety + alpha fields."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
FILES=["v10_council_input_pack","v10_research_council_review","v10_devil_advocate_review","v10_candidate_factor_thesis_pack"]
SAFETY=["production","broker_runtime","real_trade"]
ALPHA=["ready_for_alpha_claim","alpha_validated"]
def main():
    safety_miss=[]; safety_unblocked=[]; alpha_miss=[]; alpha_true=[]
    for fn in FILES:
        p=C/(fn+".json")
        if not p.exists(): safety_miss.append(f"{fn}.FILE_MISSING"); continue
        d=json.loads(p.read_text())
        for f in SAFETY:
            if f not in d: safety_miss.append(f"{fn}.{f}")
            elif d[f]!="BLOCKED": safety_unblocked.append(f"{fn}.{f}={d[f]}")
        for f in ALPHA:
            if f not in d: alpha_miss.append(f"{fn}.{f}")
            elif d[f] is True: alpha_true.append(f"{fn}.{f}=True")
    ok=len(safety_miss)==0 and len(safety_unblocked)==0 and len(alpha_miss)==0 and len(alpha_true)==0
    audit=dict(status="V10_UPSTREAM_SAFETY_ALPHA_AUDIT_PASS" if ok else "V10_UPSTREAM_SAFETY_ALPHA_AUDIT_FAIL",checked_sources=FILES,safety_missing_fields=safety_miss,safety_unblocked_fields=safety_unblocked,alpha_missing_fields=alpha_miss,alpha_true_fields=alpha_true,ready_for_v11_gate=ok)
    json.dump(audit,open(C/"v10_upstream_safety_alpha_audit.json","w"),indent=2)
    print(f"Audit: {'PASS' if ok else 'FAIL'} | safety_miss={len(safety_miss)} alpha_miss={len(alpha_miss)}")
if __name__=="__main__": main()
