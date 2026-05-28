#!/usr/bin/env python3
"""v3.5.18 Classifier v2 Paper Replay"""
from __future__ import annotations
import json, argparse
from pathlib import Path
from collections import Counter
from statistics import median

L2C = {"A_LONG_CORE":"ROLE_CORE","B_MID_ROTATION":"ROLE_ROT","C_SHORT_EVENT":"ROLE_HUNT","WATCH_ONLY":"ROLE_WATCH","D_REJECT":"ROLE_BLOCK"}
EXPECTED_SRC = {"ROLE_CORE":"MATRIX_B_BASE","ROLE_ROT":"MATRIX_R_ROTATION","ROLE_HUNT":"MATRIX_D_DARK_HORSE","ROLE_WATCH":"UNKNOWN","ROLE_BLOCK":"NONE"}

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

def _pass(m): return (m or {}).get("status")=="PASS" or (m or {}).get("matrix_status")=="PASS"

def _classify_v2(row):
    raw = row.get("source_brd_result",{}).get("source_raw",{})
    b = raw.get("b_matrix") or {}; r = raw.get("r_matrix") or {}; d = raw.get("d_matrix") or {}
    bp = _pass(b) or raw.get("b_matrix_pass"); rp = _pass(r) or raw.get("r_matrix_pass"); dp = _pass(d) or raw.get("d_matrix_pass")
    if bp and rp: role="ROLE_CORE"; src="MATRIX_B_BASE"
    elif bp: role="ROLE_CORE"; src="MATRIX_B_BASE"
    elif rp and not bp: role="ROLE_ROT"; src="MATRIX_R_ROTATION"
    elif dp: role="ROLE_HUNT"; src="MATRIX_D_DARK_HORSE"
    else: role="ROLE_BLOCK"; src="NONE"
    return role, src

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--replay-path",default="runtime_reports/v35_brd_strategy_replay_result.json"); ap.add_argument("--output",default="runtime_reports/v3518_classifier_v2_paper_replay_report.json")
    args=ap.parse_args()

    print("Loading replay...",flush=True)
    rr=json.loads(Path(args.replay_path).read_text(encoding="utf-8"))
    outcomes={}
    for d in rr.get("daily_results",[]):
        for o in d.get("outcomes",[]): outcomes[o.get("paper_id")]=o

    rows=[]
    for d in rr.get("daily_results",[]):
        for a in d.get("paper_actions",[]):
            o=outcomes.get(a.get("paper_id"),{})
            rows.append({"paper_id":a.get("paper_id"),"ticker":a.get("ticker"),"legacy_role":a.get("role"),"source_brd_result":a.get("source_brd_result",{}),"actual_return_t20":_f(o.get("actual_return_t20")),"invalidation_triggered":o.get("invalidation_triggered")})

    print(f"  {len(rows)} rows",flush=True)

    # Run classifier v2
    print("Running classifier v2...",flush=True)
    role_counts=Counter(); source_counts=Counter(); transitions=Counter(); mismatches=[]; trace_ready=0; replay_rows=[]
    for r in rows:
        role,src=_classify_v2(r); trace_ready+=1
        r["classifier_v2_role"]=role; r["classifier_v2_source_matrix"]=src; r["classifier_v2_production_ready"]=False
        role_counts[role]+=1; source_counts[src]+=1
        legacy=r["legacy_role"]; expected=L2C.get(legacy,"ROLE_WATCH"); transitions[(legacy,role)]+=1
        if expected!=role: mismatches.append({"paper_id":r["paper_id"],"ticker":r["ticker"],"legacy_role":legacy,"expected":expected,"actual":role,"v2_source":src})
        replay_rows.append(r)

    # Source mismatch
    src_mismatch=[]; src_total=len(replay_rows)
    for r in replay_rows:
        role=r["classifier_v2_role"]; expected_src=EXPECTED_SRC.get(role,"UNKNOWN"); actual_src=r["classifier_v2_source_matrix"]
        if expected_src!=actual_src and role not in ("ROLE_WATCH","ROLE_BLOCK"):
            src_mismatch.append({"paper_id":r["paper_id"],"ticker":r["ticker"],"role":role,"expected":expected_src,"actual":actual_src})

    # Performance by canonical role
    perf={}; 
    for role in role_counts:
        rs=[r for r in replay_rows if r["classifier_v2_role"]==role]; perf[role]=_stats(rs)

    # Delta
    rd_rate=len(mismatches)/src_total if src_total else 0; sm_rate=len(src_mismatch)/src_total if src_total else 0
    tc = trace_ready / len(rows) if len(rows) else 0
    warnings=[]
    if rd_rate>0.03: warnings.append("ROLE_DELTA_RATE_HIGH")
    if sm_rate>0.01: warnings.append("SOURCE_MISMATCH_RATE_HIGH")
    status="CLASSIFIER_V2_REPLAY_READY" if not warnings else "CLASSIFIER_V2_REPLAY_WARNING_BEHAVIOR_DELTA"

    report={"report_version":"V3518_CLASSIFIER_V2_PAPER_REPLAY_REPORT_V10","mode":"PAPER_ONLY_CLASSIFIER_V2_REPLAY","dataset":{"row_count":len(rows)},"matrix_trace":{"trace_coverage":tc},"classifier_v2_runner":{"classifier_v2_role_counts":dict(role_counts),"classifier_v2_source_counts":dict(source_counts)},"legacy_vs_v2_comparison":{"role_delta_count":len(mismatches),"role_delta_rate":rd_rate,"transitions":[{"legacy":k[0],"v2":k[1],"count":v} for k,v in transitions.most_common()]},"canonical_role_performance":perf,"role_source_stability_audit":{"source_mismatch_count":len(src_mismatch),"source_mismatch_rate":sm_rate},"replay_delta_summary":{"warnings":warnings,"delta_status":"PASS" if not warnings else "WARNING"},"classifier_v2_replay_status":status,"recommended_next_step":"v3.5.19 Legacy Namespace Deprecation Gate" if status=="CLASSIFIER_V2_REPLAY_READY" else "v3.5.19 Behavior Delta Attribution","production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"classifier_production_write_allowed":False,"role_definition_production_write_allowed":False,"legacy_runtime_rewrite_allowed":False,"legacy_module_direct_rewrite_allowed":False,"l2_l3_direct_migration_allowed":False,"policy_violations":[]}

    out=Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    print(f"\n  v3.5.18 Classifier v2 Paper Replay")
    print(f"  Rows: {len(rows):,}")
    print(f"  Role counts: {dict(role_counts)}")
    print(f"  Source counts: {dict(source_counts)}")
    print(f"  Role delta: {len(mismatches)} ({rd_rate*100:.1f}%)")
    print(f"  Source mismatch: {len(src_mismatch)} ({sm_rate*100:.1f}%)")
    print(f"\n  Canonical Performance:")
    for role in ["ROLE_CORE","ROLE_ROT","ROLE_HUNT","ROLE_WATCH","ROLE_BLOCK"]:
        p=perf.get(role)
        if p and p.get("count",0)>0:
            print(f"  {role}: {p['count']:,} win={p['win_rate']*100:.1f}% median={p['median']:.2f}%")
    print(f"\n  Status: {status}")
    print(f"  Next: {report['recommended_next_step']}")
    print("v3.5.18 done")

if __name__=="__main__": main()
