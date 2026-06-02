#!/usr/bin/env python3
"""Audit: decay semantics propagated through all V10 layers."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
REQUIRED=["decay_pattern","decay_pattern_basis","rankic_direction","raw_rankic_trend"]
def main():
    missing={f:[] for f in REQUIRED}; raw_leaks=[]
    # V9 decay
    d9=json.loads((C/"v9_factor_decay_analysis.json").read_text())
    for r in d9["decay_results"]:
        for f in REQUIRED:
            if f not in r: missing[f].append(f"v9.{r['factor_id']}")
        dp=r.get("decay_pattern","")
        if dp in ("MONOTONIC_INCREASING","MONOTONIC_DECREASING"): raw_leaks.append(f"v9.{r['factor_id']}={dp}")
    # V10 input pack
    inp=json.loads((C/"v10_council_input_pack.json").read_text())
    for pf in inp.get("promoted_factors",[]):
        for f in REQUIRED:
            if f not in pf: missing[f].append(f"inp.{pf['factor_id']}")
        dp=pf.get("decay_pattern","")
        if dp in ("MONOTONIC_INCREASING","MONOTONIC_DECREASING"): raw_leaks.append(f"inp.{pf['factor_id']}={dp}")
    # Council review
    cr=json.loads((C/"v10_research_council_review.json").read_text())
    for rv in cr.get("reviews",[]):
        ev=rv.get("evidence",{})
        for f in REQUIRED:
            if f not in ev: missing[f].append(f"cr.{rv['factor_id']}")
        dp=ev.get("decay_pattern","")
        if dp in ("MONOTONIC_INCREASING","MONOTONIC_DECREASING"): raw_leaks.append(f"cr.{rv['factor_id']}={dp}")
    # DA
    da=json.loads((C/"v10_devil_advocate_review.json").read_text())
    for fr in da.get("factor_failure_reviews",[]):
        ev=fr.get("evidence",{})
        for f in REQUIRED:
            if f not in ev: missing[f].append(f"da.{fr['factor_id']}")
        dp=ev.get("decay_pattern","")
        if dp in ("MONOTONIC_INCREASING","MONOTONIC_DECREASING"): raw_leaks.append(f"da.{fr['factor_id']}={dp}")
    # Thesis
    tp=json.loads((C/"v10_candidate_factor_thesis_pack.json").read_text())
    for c in tp.get("candidates",[]):
        ev=c.get("supporting_evidence",{})
        for f in REQUIRED:
            if f not in ev: missing[f].append(f"tp.{c['factor_id']}")
        dp=ev.get("decay_pattern","")
        if dp in ("MONOTONIC_INCREASING","MONOTONIC_DECREASING"): raw_leaks.append(f"tp.{c['factor_id']}={dp}")
    all_ok=all(len(v)==0 for v in missing.values()) and len(raw_leaks)==0
    audit={"status":"V10_DECAY_SEMANTIC_PROPAGATION_PASS" if all_ok else "V10_DECAY_SEMANTIC_PROPAGATION_FAIL","checked_layers":["v9_decay","v10_input_pack","v10_council_review","v10_devil_advocate","v10_candidate_thesis"],**{f"missing_{k}":v for k,v in missing.items()},"raw_monotonic_leaks":raw_leaks,"ready_for_v11_paper_watchlist":all_ok}
    json.dump(audit,open(C/"v10_decay_semantic_propagation_audit.json","w"),indent=2)
    print(f"Semantic audit: {'PASS' if all_ok else 'FAIL'} | missing={ {k:len(v) for k,v in missing.items()} } | raw_leaks={len(raw_leaks)}")
if __name__=="__main__": main()
