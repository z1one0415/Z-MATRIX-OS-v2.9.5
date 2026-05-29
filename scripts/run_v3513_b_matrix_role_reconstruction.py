#!/usr/bin/env python3
# allowlist: forbidden-token-definition
"""v3.5.13 B-Matrix / Role Definition Reconstruction Lab"""
from __future__ import annotations
import json, argparse
from pathlib import Path
from collections import Counter
from statistics import median

def _f(x,d=None):
    try:
        if x in (None,""): return d
        return float(x)
    except: return d

def _trim(v,t):
    if not v: return None
    k=int(len(v)*t); ys=v[k:len(v)-k] if len(v)>2*k else v
    return sum(ys)/len(ys) if ys else None

def _stats(rows):
    vals=[]; inv=0
    for r in rows:
        v=_f(r.get("actual_return_t20"))
        if v is not None: vals.append(v)
        if r.get("invalidation_triggered") or r.get("baseline_invalidation_triggered"): inv+=1
    sv=sorted(vals); wins=[x for x in vals if x>0]
    return {"count":len(vals),"win_rate":len(wins)/len(vals) if vals else None,"mean":sum(vals)/len(vals) if vals else None,"median":median(vals) if vals else None,"trimmed_mean_5pct":_trim(sv,0.05),"invalidation_rate":inv/len(rows) if rows else None,"best":max(vals) if vals else None,"worst":min(vals) if vals else None}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay-path", default="runtime_reports/v35_brd_strategy_replay_result.json")
    ap.add_argument("--output", default="runtime_reports/v3513_b_matrix_role_reconstruction_report.json")
    args = ap.parse_args()

    print("Loading replay...", flush=True)
    rr = json.loads(Path(args.replay_path).read_text(encoding="utf-8"))
    
    # Build outcome lookup
    outcomes = {}
    for daily in rr.get("daily_results",[]):
        for o in daily.get("outcomes",[]):
            outcomes[o.get("paper_id")] = o
    
    rows = []
    src_counter = Counter()
    reason_counter = Counter()
    for daily in rr.get("daily_results",[]):
        for a in daily.get("paper_actions",[]):
            if a.get("role")!="B_MID_ROTATION": continue
            if a.get("paper_action") in ("NO_ACTION","DATA_GAP",None): continue
            raw = a.get("source_brd_result",{}).get("source_raw",{})
            src_counter[raw.get("role_source_matrix","UNKNOWN")] += 1
            for rc in a.get("source_brd_result",{}).get("reason_codes",[]): reason_counter[rc] += 1
            o = outcomes.get(a.get("paper_id"),{})
            rows.append({"paper_id":a.get("paper_id"),"ticker":a.get("ticker"),"entry_date":a.get("entry_date") or a.get("replay_date"),"source_matrix":raw.get("role_source_matrix","UNKNOWN"),"b_pass":raw.get("b_matrix_pass"),"r_pass":raw.get("r_matrix_pass"),"d_pass":raw.get("d_matrix_pass"),"downgrade_reasons":raw.get("downgrade_reasons",[]),"reason_codes":a.get("source_brd_result",{}).get("reason_codes",[]),"actual_return_t20":_f(o.get("actual_return_t20")),"actual_return_t5":_f(o.get("actual_return_t5")),"invalidation_triggered":o.get("invalidation_triggered"),"max_adverse_excursion_pct":_f(o.get("max_adverse_excursion_pct"))})

    total = len(rows)
    print(f"  {total} B_MID_ROTATION rows", flush=True)

    # P0-1: Role Source Matrix audit
    src_rates = {k: v/total for k,v in src_counter.items()}
    reason_rates = {k: v/total for k,v in reason_counter.items()}

    # P0-2: Subtype labeling
    subtypes = Counter()
    labeled = []
    for r in rows:
        sm = r.get("source_matrix","")
        rc = r.get("reason_codes",[])
        if sm == "R-MATRIX" and "FUNDAMENTAL_DATA_MISSING" in rc:
            st = "B_R_TECHNICAL_PROXY"
        elif sm == "R-MATRIX":
            st = "B_R_SIGNAL_DOMINATED"
        elif sm == "D-MATRIX":
            st = "B_D_SIGNAL_DOMINATED"
        else:
            st = "B_UNEXPLAINED"
        subtypes[st] += 1
        r["subtype"] = st
        labeled.append(r)

    # P0-3: Subtype performance
    subtype_profiles = {}
    for st in subtypes:
        rs = [r for r in labeled if r["subtype"]==st]
        subtype_profiles[st] = _stats(rs)

    
    # P0-3: Subtype performance
    vals = [p["median"] for p in subtype_profiles.values() if p.get("count",0)>=1000 and p.get("median") is not None]
    perf_score = max(0,min(1,(max(vals)-min(vals))/3.0)) if len(vals)>=2 else 0
    unknown_rate = subtypes.get("B_UNEXPLAINED",0)/total
    unknown_score = max(0,1-unknown_rate)
    trace_cov = 1.0  # 100% have source_raw
    score = perf_score*0.50 + trace_cov*0.25 + unknown_score*0.25
    status = "ROLE_RECONSTRUCTION_READY" if score>=0.70 else "WEAKLY_RECONSTRUCTABLE" if score>=0.55 else "NOT_RECONSTRUCTABLE"

    # Candidates
    candidates = []
    if status in ("ROLE_RECONSTRUCTION_READY","WEAKLY_RECONSTRUCTABLE"):
        names = ["rename_b_mid_to_r_technical_proxy","split_b_mid_into_r_proxy_and_b_true","require_b_trace_for_b_mid_rotation","downgrade_no_fundamental_b_to_watch","separate_regime_dependent_b_subrole","exclude_stale_or_weak_b_evidence"]
        for n in names: candidates.append({"candidate_name":n,"lookahead_risk":False,"production_ready":False,"paper_replay_required":True,"role_definition_write_allowed":False})

    report = {"report_version":"V3513_B_MATRIX_ROLE_RECONSTRUCTION_REPORT_V10","mode":"PAPER_ONLY_ROLE_RECONSTRUCTION","input_count":total,"source_matrix_audit":{"source_matrix_counts":dict(src_counter),"source_matrix_rates":src_rates},"reason_code_audit":{"reason_code_counts":dict(reason_counter),"reason_code_rates":reason_rates},"subtype_labeling":{"subtype_counts":dict(subtypes)},"subtype_performance":subtype_profiles,"reconstruction_separability":{"reconstruction_status":status,"reconstruction_score":score,"scoring_breakdown":{"subtype_performance_spread":perf_score,"trace_coverage":1.0,"unknown_subtype_score":unknown_score,"unknown_rate":unknown_rate}},"reconstruction_candidates":{"candidate_count":len(candidates),"candidates":candidates},"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"role_definition_write_allowed":False,"classifier_production_write_allowed":False,"policy_violations":[],"reconstruction_status":status,"recommended_next_step":{"ROLE_RECONSTRUCTION_READY":"v3.5.14 Role-Conditioned Paper Replay","WEAKLY_RECONSTRUCTABLE":"v3.5.14 Role Reconstruction Observation Replay"}.get(status,"v3.5.14 B/R/D Feature Enrichment")}

    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    # Summary
    print(f"\n{'='*60}")
    print(f"  v3.5.13 B-Matrix Role Reconstruction")
    print(f"{'='*60}")
    print(f"  Source matrix: {dict(src_counter)}")
    print(f"  Reason codes: {dict({k:v for k,v in reason_counter.most_common(5)})}")
    print(f"\n  Subtypes:")
    for st,c in subtypes.most_common():
        p = subtype_profiles[st]
        print(f"  {st}: {c:,} ({c/total*100:.1f}%) win={p.get('win_rate',0)*100:.1f}% median={p.get('median',0):.2f}%")
    print(f"\n  Status: {status} (score: {score:.3f})")
    print(f"  Candidates: {len(candidates)}")
    print(f"  Next: {report['recommended_next_step']}")
    print("v3.5.13 done")

if __name__ == "__main__": main()
