#!/usr/bin/env python3
"""Audit forward label alignment for V11.5 portfolio simulation."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases";L=W/"runtime_reports/cases/v8_large_data"
sn=json.loads((C/"v11_paper_signal_snapshot.json").read_text())
lb=json.loads((L/"v8_forward_return_labels.json").read_text())
lab={}
for l in lb["labels"]:lab[(l["as_of_date"],l["ticker"],l["horizon"])]=l
eligible=[s for s in sn["snapshots"]if s.get("rankic_direction")in("NEGATIVE","POSITIVE")and s.get("favored_bucket_size",0)>0]
expected=0;found=0
for s in eligible:
    for hn in["T20","T60"]:
        for bkt in["favored_bucket","comparison_bucket"]:
            for tk in s.get(bkt,[]):expected+=1
            if(s["as_of_date"],tk,hn)in lab:found+=1
ready=expected>0 and found==expected
a={"status":"V11_5_FORWARD_LABEL_ALIGNMENT_PASS"if ready else"V11_5_FORWARD_LABEL_ALIGNMENT_BLOCKED","expected_label_count":expected,"found_label_count":found,"missing_label_count":expected-found,"coverage":round(found/expected,4)if expected else 0,"ready_for_portfolio_simulation":ready}
json.dump(a,open(C/"v11_5_forward_label_alignment_audit.json","w"),indent=2)
print(f"Label alignment: {'PASS' if ready else 'BLOCKED'} | missing={expected-found}")
