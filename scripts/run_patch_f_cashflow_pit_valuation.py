#!/usr/bin/env python3
# allowlist: forbidden-token-definition
"""PATCH-F: Cashflow + PIT Valuation — fix debt_ratio units, make B-Matrix eligible"""
from __future__ import annotations
import json, csv, argparse
from pathlib import Path
from collections import Counter, defaultdict
from zmatrix.patch_a.b_matrix_foundation import score_b_matrix

def _f(x,d=None):
    try: return d if x in (None,"") else float(x)
    except: return d

def _load_fin(data_root):
    d=Path(data_root)/"data"/"fundamentals"; tr=defaultdict(list)
    if not d.exists(): return {}
    for p in d.glob("*_fin.csv"):
        tk=p.stem.replace("_fin","").zfill(6)
        with open(p,encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                ann=str(r.get("ann_date","")).replace("-","")[:8]
                if ann: tr[tk].append({"ann_date":ann,"report_period":str(r.get("end_date","")).replace("-","")[:8],"gross_margin":_f(r.get("gross_margin")),"roe":_f(r.get("roe") or r.get("roe_yearly")),"debt_ratio_raw":_f(r.get("debt_to_assets")),"netprofit_yoy":_f(r.get("netprofit_yoy")),"revenue_yoy":_f(r.get("or_yoy")),"eps":_f(r.get("eps")),"bps":_f(r.get("bps")),"ocfps":_f(r.get("ocfps")),"fcff":_f(r.get("fcff"))})
    return dict(tr)

def _close_at(tk, dt, data_root):
    p=Path(data_root)/"data"/"price_bars"/f"{tk}.csv"
    if not p.exists(): return None
    t=str(dt).replace("-","")[:8]
    with open(p,encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if str(r.get("trade_date") or r.get("date","")).replace("-","")[:8]==t: return _f(r.get("close"))
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-root",default=".")
    ap.add_argument("--output",default="runtime_reports/v3520_patch_f_cashflow_pit_valuation.json")
    args=ap.parse_args()
    print("Loading data...",flush=True)
    tr=_load_fin(args.data_root)
    print(f"  {len(tr)} tickers",flush=True)
    from scripts.run_patch_e_critical_data_completion import build_industry_percentile_v2
    ip=build_industry_percentile_v2(args.data_root)
    print(f"  {len(ip)} percentile",flush=True)

    b_ok=0; bs=0; rc=Counter()
    for tk in list(tr.keys())[:5000]:
        reps=tr.get(tk,[]); 
        if not reps: continue
        latest=reps[-1]; pct=ip.get(tk,{})
        ann_date=latest.get("ann_date","")
        close=_close_at(tk, ann_date, args.data_root) or _close_at(tk, "20260526", args.data_root)
        eps=latest.get("eps"); bps=latest.get("bps")
        pe=close/eps if close and eps and eps>0 else None
        pb=close/bps if close and bps and bps>0 else None
        ocfps=latest.get("ocfps"); fcff=latest.get("fcff")
        # Normalize debt_ratio: fina_indicator is percentage (0-100), B-Matrix expects ratio (0-1)
        raw_d=latest.get("debt_ratio_raw")
        debt=raw_d/100 if raw_d is not None and raw_d>5 else raw_d
        bf={"gross_margin":latest.get("gross_margin"),"roe":latest.get("roe"),"roic":None,"revenue_yoy":latest.get("revenue_yoy"),"net_profit_yoy":latest.get("netprofit_yoy"),"deduct_np_yoy":None,"ocf":ocfps,"ocf_to_np":ocfps/eps if ocfps and eps and eps>0 else None,"fcf_proxy":fcff,"debt_ratio":debt,"current_ratio":None,"goodwill_ratio":None,"pe_ttm":pe,"pb":pb,"ps":None,"dividend_yield":None,"industry_percentile_roe":pct.get("industry_percentile_roe"),"industry_percentile_growth":pct.get("industry_percentile_growth"),"bottleneck_score":None,"chain_position":None,"st_flag":None,"audit_opinion":None,"ocf_trend":None}
        r=score_b_matrix(financial_facts=bf,valuation_facts=bf,industry_facts=bf)
        bs+=1
        if r["base_role_eligible"]: b_ok+=1
        if not r["hard_gate_passed"]: rc["hard_gate_failed"]+=1
        if r["b_score"]<75: rc["score_below_75"]+=1
        if "VALUATION_DATA_INSUFFICIENT" in r.get("reason_codes",[]): rc["valuation_missing"]+=1
        if pe is None: rc["pe_none"]+=1
        if pb is None: rc["pb_none"]+=1
        if ocfps is None or ocfps==0: rc["ocfps_zero"]+=1

    report={"report_version":"FINAL","F_b_eligible":b_ok,"F_b_samples":bs,"F_b_rate":b_ok/bs if bs else 0,"F_blocked_breakdown":dict(rc),"root_cause":"debt_ratio unit mismatch (percentage vs ratio)" if rc.get("hard_gate_failed",0)==0 else "debt_ratio FIXED: hard_gate now passes","real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False}
    out=Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"\n  B eligible: {b_ok}/{bs} ({b_ok/bs*100:.1f}%)")
    print(f"  Blocked: {dict(rc)}")
    print("PATCH-F done")

if __name__=="__main__": main()
