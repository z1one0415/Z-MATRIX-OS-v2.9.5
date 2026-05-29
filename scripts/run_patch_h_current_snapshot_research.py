#!/usr/bin/env python3
# allowlist: forbidden-token-definition
"""PATCH-H: B-Matrix Current Snapshot Research Mode — 81 candidate profiles"""
from __future__ import annotations
import json, csv, argparse
from pathlib import Path
from collections import Counter, defaultdict
from zmatrix.patch_a.b_matrix_foundation import score_b_matrix

def _f(x,d=None):
    try: return d if x in (None,"") else float(x)
    except: return d

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-root",default=".")
    ap.add_argument("--output",default="runtime_reports/v3520_patch_h_current_snapshot_research.json")
    args=ap.parse_args()

    # Load financials
    fd=Path(args.data_root)/"data"/"fundamentals"; tr=defaultdict(list)
    for p in fd.glob("*_fin.csv"):
        tk=p.stem.replace("_fin","").zfill(6)
        with open(p,encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                ann=str(r.get("ann_date","")).replace("-","")[:8]
                if ann: tr[tk]=({"ann_date":ann,"gross_margin":_f(r.get("gross_margin")),"roe":_f(r.get("roe") or r.get("roe_yearly")),"debt_ratio_raw":_f(r.get("debt_to_assets")),"netprofit_yoy":_f(r.get("netprofit_yoy")),"revenue_yoy":_f(r.get("or_yoy")),"eps":_f(r.get("eps")),"bps":_f(r.get("bps")),"ocfps":_f(r.get("ocfps")),"fcff":_f(r.get("fcff"))})
                break
    tr=dict(tr)

    # Load names + sectors
    names={}; sp=Path(args.data_root)/"data"/"tushare"/"stock_basic.csv"
    if sp.exists():
        with open(sp,encoding="utf-8-sig") as f:
            for r in csv.DictReader(f): names[str(r.get("ts_code","")).split(".")[0].zfill(6)]=r.get("name","")
    sm={}; mp=Path(args.data_root)/"data"/"metadata"/"sector_mapping_v3510.csv"
    if mp.exists():
        with open(mp,encoding="utf-8-sig") as f:
            for r in csv.DictReader(f): sm[r.get("ticker","")]=r.get("sector","")

    from scripts.run_patch_e_critical_data_completion import build_industry_percentile_v2
    pct=build_industry_percentile_v2(args.data_root)

    def _close(tk,dt):
        p=Path(args.data_root)/"data"/"price_bars"/f"{tk}.csv"
        if not p.exists(): return None
        t=str(dt).replace("-","")[:8]
        with open(p,encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                if str(r.get("trade_date") or r.get("date","")).replace("-","")[:8]==t: return _f(r.get("close"))
        return None

    # Score all
    all_r=[]
    for tk in tr:
        r=tr[tk]; ip=pct.get(tk,{})
        close=_close(tk,r["ann_date"]) or _close(tk,"20260526")
        eps=r["eps"]; bps=r["bps"]; oc=r["ocfps"]; fc=r["fcff"]
        pe=close/eps if close and eps and eps>0 else None
        pb=close/bps if close and bps and bps>0 else None
        raw_d=r["debt_ratio_raw"]
        debt=raw_d/100 if raw_d is not None and raw_d>5 else raw_d
        bf={"gross_margin":r["gross_margin"],"roe":r["roe"],"net_profit_yoy":r["netprofit_yoy"],"revenue_yoy":r["revenue_yoy"],"debt_ratio":debt,"ocf":oc,"ocf_to_np":oc/eps if oc and eps and eps>0 else None,"fcf_proxy":fc,"pe_ttm":pe,"pb":pb,"industry_percentile_roe":ip.get("industry_percentile_roe"),"industry_percentile_growth":ip.get("industry_percentile_growth")}
        res=score_b_matrix(financial_facts=bf,valuation_facts=bf,industry_facts=bf)
        if res["base_role_eligible"]:
            tier="B_CORE_STRONG" if res["b_score"]>=80 else "B_CORE_WATCH"
            all_r.append({"ticker":tk,"name":names.get(tk,""),"sector":sm.get(tk,"?"),"b_score":res["b_score"],"tier":tier,"roe":r["roe"],"gross_margin":r["gross_margin"],"netprofit_yoy":r["netprofit_yoy"],"revenue_yoy":r["revenue_yoy"],"debt_ratio":debt,"ocfps":oc,"pe_ttm":pe,"pb":pb,"industry_roe_pct":ip.get("industry_percentile_roe")})
    all_r.sort(key=lambda x:-x["b_score"])

    tc=Counter(r["tier"] for r in all_r); sc=Counter(r["sector"] for r in all_r)
    report={"report_version":"V3520_PATCH_H_CURRENT_SNAPSHOT_V10","mode":"CURRENT_SNAPSHOT_RESEARCH_ONLY","H1_boundary":{"mode":"CURRENT_SNAPSHOT_ONLY","historical_pit":"BLOCKED_DATA_INSUFFICIENT","production":"BLOCKED"},"H2_candidates":all_r,"H3_tiers":dict(tc),"H4_sectors":dict(sc.most_common(20)),"H5_trust":{"current_snapshot":"T2","historical":"BLOCKED","production":False},"total_scored":len(tr),"eligible_count":len(all_r),"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False}

    out=Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    print(f"\n  H1: {len(all_r)} candidates / {len(tr)} scored")
    print(f"  H3: STRONG={tc.get('B_CORE_STRONG',0)} WATCH={tc.get('B_CORE_WATCH',0)}")
    print(f"  H4: {sc.most_common(8)}")
    print(f"\n  Top candidates:")
    for r in all_r[:20]:
        pe_val = r.get("pe_ttm")
        n=(r["name"] or r["ticker"])[:10]
        pe_str=f"{pe_val:.0f}" if pe_val else "-"
        b=r["b_score"]; ro=r.get("roe") or 0; db=r.get("debt_ratio") or 0; tr=r["tier"]; se=r["sector"]; tk=r["ticker"]; n=(r.get("name") or tk)[:10]; pe_str=f"{r.get("pe_ttm"):.0f}" if r.get("pe_ttm") else "-"
        print(f"  {tk:<8} {n:<10} {b:>5.1f} PE={pe_str:>5} ROE={ro:>5.1f}% Debt={db:.2f} {tr:<16} {se}")
    print("PATCH-H complete")

if __name__=="__main__": main()
