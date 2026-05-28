#!/usr/bin/env python3
"""v3.5.14 Role Replay & Namespace Migration"""
from __future__ import annotations
import json, argparse
from pathlib import Path
from collections import Counter
from statistics import median

LEGACY_TO_NEW = {"A_LONG_CORE":"ROLE_CORE","B_MID_ROTATION":"ROLE_ROT","C_SHORT_EVENT":"ROLE_HUNT","D_REJECT":"ROLE_BLOCK","WATCH_ONLY":"ROLE_WATCH"}
def _f(x,d=None):
    try:
        if x in (None,""): return d
        return float(x)
    except: return d
def _t(v,t):
    if not v: return None
    k=int(len(v)*t); ys=v[k:len(v)-k] if len(v)>2*k else v
    return sum(ys)/len(ys) if ys else None
def _stats(rows):
    vals=[]; inv=0
    for r in rows:
        v=_f(r.get("actual_return_t20"))
        if v is not None: vals.append(v)
        if r.get("invalidation_triggered"): inv+=1
    sv=sorted(vals); wins=[x for x in vals if x>0]
    return {"count":len(vals),"win_rate":len(wins)/len(vals) if vals else None,"mean":sum(vals)/len(vals) if vals else None,"median":median(vals) if vals else None,"trimmed_mean_5pct":_t(sv,0.05),"invalidation_rate":inv/len(rows) if rows else None,"best":max(vals) if vals else None,"worst":min(vals) if vals else None}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay-path", default="runtime_reports/v35_brd_strategy_replay_result.json")
    ap.add_argument("--output", default="runtime_reports/v3514_role_replay_namespace_migration_report.json")
    args = ap.parse_args()

    print("Loading replay...", flush=True)
    rr = json.loads(Path(args.replay_path).read_text(encoding="utf-8"))
    outcomes = {}
    for d in rr.get("daily_results",[]):
        for o in d.get("outcomes",[]): outcomes[o.get("paper_id")] = o

    rows = []
    for d in rr.get("daily_results",[]):
        for a in d.get("paper_actions",[]):
            o = outcomes.get(a.get("paper_id"),{})
            legacy = a.get("role","UNKNOWN")
            new_role = LEGACY_TO_NEW.get(legacy,"ROLE_WATCH")
            raw = a.get("source_brd_result",{}).get("source_raw",{})
            source = raw.get("role_source_matrix") or raw.get("b_matrix_pass") or raw.get("r_matrix_pass") or ""
            rows.append({"paper_id":a.get("paper_id"),"ticker":a.get("ticker"),"legacy_role":legacy,"new_role":new_role,"source_matrix":source,"b_pass":raw.get("b_matrix_pass"),"r_pass":raw.get("r_matrix_pass"),"d_pass":raw.get("d_matrix_pass"),"actual_return_t20":_f(o.get("actual_return_t20")),"invalidation_triggered":o.get("invalidation_triggered"),"paper_action":a.get("paper_action")})

    # P0: Count by new role
    role_counts = Counter()
    source_counts = Counter()
    role_source = {}
    for r in rows:
        role_counts[r["new_role"]] += 1
        src = "MATRIX_R_ROTATION" if r.get("r_pass") else "MATRIX_B_BASE" if r.get("b_pass") else "MATRIX_D_DARK_HORSE" if r.get("d_pass") else "NONE"
        source_counts[src] += 1
        role_source.setdefault(r["new_role"],Counter())[src] += 1

    # Performance by new role
    perf = {}
    for role in role_counts:
        rs = [r for r in rows if r["new_role"]==role]
        perf[role] = _stats(rs)

    # Transitions
    trans = Counter()
    for r in rows: trans[(r["legacy_role"],r["new_role"])] += 1

    # Audit
    mismatch = 0; total_source = len(rows)
    for r in rows:
        nr = r["new_role"]; src = "MATRIX_R_ROTATION" if r.get("r_pass") else "NONE"
        if nr=="ROLE_ROT" and "R_ROTATION" not in src: mismatch += 1

    status = "ROLE_REPLAY_READY"
    if mismatch/total_source > 0.05: status = "ROLE_REPLAY_WARNING_SOURCE_MISMATCH"

    report = {"report_version":"V3514_ROLE_REPLAY_NAMESPACE_MIGRATION_REPORT_V10","mode":"PAPER_ONLY_ROLE_NAMESPACE_MIGRATION","input_count":len(rows),"role_mapping":{"new_role_counts":dict(role_counts)},"role_source_audit":{"source_counts":dict(source_counts),"role_source_counts":{k:dict(v) for k,v in role_source.items()},"source_mismatch_count":mismatch,"source_mismatch_rate":mismatch/total_source if total_source else 0,"source_audit_status":"PASS" if mismatch==0 else "SOURCE_MISMATCH_WARNING"},"role_performance":perf,"transition_matrix":{"transitions":[{"legacy":k[0],"new":k[1],"count":v} for k,v in trans.most_common()]},"role_replay_status":status,"recommended_next_step":"v3.5.15 Role Taxonomy Closeout / Classifier v2 Paper Adapter" if status=="ROLE_REPLAY_READY" else "v3.5.15 Role Source Trace Repair","production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"classifier_production_write_allowed":False,"role_definition_production_write_allowed":False,"policy_violations":[]}

    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    print(f"\n{'='*60}")
    print("  v3.5.14 Role Replay & Namespace Migration")
    print(f"{'='*60}")
    print(f"  Input: {len(rows):,} rows")
    print(f"\n  Role Counts:")
    for role,c in role_counts.most_common():
        p = perf.get(role,{})
        print(f"  {role}: {c:,} win={_f(p.get('win_rate'),0)*100:.1f}% median={_f(p.get('median'),0):.2f}%")
    print(f"\n  Source Counts: {dict(source_counts)}")
    print(f"  Mismatch: {mismatch} ({mismatch/total_source*100:.1f}%)")
    print(f"  Status: {status}")
    print(f"  Next: {report['recommended_next_step']}")
    print("v3.5.14 done")

if __name__ == "__main__": main()
