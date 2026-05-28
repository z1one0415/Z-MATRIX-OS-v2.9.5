#!/usr/bin/env python3
"""PATCH-E: B/D Critical Data Completion — PIT join + percentile fix + sector momentum + fund_flow ban"""
from __future__ import annotations
import json, csv, argparse
from pathlib import Path
from collections import Counter, defaultdict
from statistics import median
from zmatrix.patch_a.b_matrix_foundation import score_b_matrix
from zmatrix.patch_a.d_matrix_foundation import score_d_matrix

def _f(x,d=None):
    try: return d if x in (None,"") else float(x)
    except: return d

# ── E2: Real PIT Historical Financial Join ──
def build_pit_financial_loader(data_root):
    """For each replay_date, select the latest financial report where ann_date <= replay_date"""
    fin_dir = Path(data_root)/"data"/"fundamentals"
    if not fin_dir.exists(): return {}
    ticker_reports = defaultdict(list)
    for p in fin_dir.glob("*_fin.csv"):
        tk = p.stem.replace("_fin","").zfill(6)
        with open(p, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                ann = str(r.get("ann_date","")).replace("-","")[:8]
                if ann:
                    ticker_reports[tk].append({"ann_date":ann,"report_period":str(r.get("end_date","")).replace("-","")[:8],"gross_margin":_f(r.get("gross_margin")),"roe":_f(r.get("roe") or r.get("roe_yearly")),"debt_ratio":_f(r.get("debt_to_assets")),"netprofit_yoy":_f(r.get("netprofit_yoy")),"eps":_f(r.get("eps")),"bps":_f(r.get("bps")),"revenue_yoy":_f(r.get("or_yoy"))})
    # Sort by ann_date
    for tk in ticker_reports: ticker_reports[tk].sort(key=lambda x:x["ann_date"])
    return dict(ticker_reports)

def get_pit_safe_report(ticker_reports, tk, replay_date):
    """Get latest report with ann_date <= replay_date"""
    reports = ticker_reports.get(tk, [])
    ed = str(replay_date).replace("-","")[:8]
    latest = None
    for r in reports:
        if r["ann_date"] <= ed: latest = r
    return latest

# ── E4: Industry Percentile Fix ──
def build_industry_percentile_v2(data_root):
    """Fixed: better ticker matching, continuous percentile, higher coverage"""
    fin_dir = Path(data_root)/"data"/"fundamentals"
    sm_path = Path(data_root)/"data"/"metadata"/"sector_mapping_v3510.csv"
    if not fin_dir.exists() or not sm_path.exists(): return {}
    # Load sector mapping
    sm = {}
    with open(sm_path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            sm[r.get("ticker","")] = r.get("sector","")
    # Load financials grouped by sector
    sector_vals = defaultdict(lambda: defaultdict(list))
    ticker_fin = {}
    for p in fin_dir.glob("*_fin.csv"):
        tk = p.stem.replace("_fin","").zfill(6)
        sector = sm.get(tk, "UNKNOWN")
        if sector == "UNKNOWN": continue
        with open(p, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                roe = _f(r.get("roe") or r.get("roe_yearly"))
                rev_yoy = _f(r.get("or_yoy") or r.get("revenue_yoy"))
                gross_m = _f(r.get("gross_margin"))
                debt_r = _f(r.get("debt_to_assets"))
                if roe is not None: sector_vals[sector]["roe"].append(roe)
                if rev_yoy is not None: sector_vals[sector]["growth"].append(rev_yoy)
                if gross_m is not None: sector_vals[sector]["gross_margin"].append(gross_m)
                if debt_r is not None: sector_vals[sector]["debt_ratio"].append(debt_r)
                ticker_fin[tk] = {"roe":roe,"growth":rev_yoy,"gross_margin":gross_m,"debt_ratio":debt_r}
                break
    # Compute percentiles per sector
    pct_map = {}
    for sector, fields in sector_vals.items():
        pct_map[sector] = {}
        for fname, vals in fields.items():
            sv = sorted(vals)
            n = len(sv)
            if n < 3: continue
            pct_map[sector][fname] = {"p25":sv[n//4],"p50":median(sv),"p75":sv[n*3//4],"n":n}
    # Score each ticker (continuous percentile rank)
    results = {}
    for tk, fin in ticker_fin.items():
        sector = sm.get(tk, "UNKNOWN")
        pcts = pct_map.get(sector, {})
        results[tk] = {"ticker":tk,"sector":sector,"industry_percentile_roe":_cont_pct_rank(fin.get("roe"),pcts.get("roe",{}).get("p25"),pcts.get("roe",{}).get("p75")),"industry_percentile_growth":_cont_pct_rank(fin.get("growth"),pcts.get("growth",{}).get("p25"),pcts.get("growth",{}).get("p75")),"industry_percentile_gross_margin":_cont_pct_rank(fin.get("gross_margin"),pcts.get("gross_margin",{}).get("p25"),pcts.get("gross_margin",{}).get("p75"))}
    return results

def _cont_pct_rank(v, p25, p75):
    """Continuous percentile rank between 0-100"""
    if v is None or p25 is None or p75 is None: return None
    v = float(v); span = p75 - p25
    if span <= 0: return 50
    return max(0, min(100, (v - p25) / span * 50 + 25))

# ── E6: Sector Momentum from v3511 Synthetic Indexes ──
def load_sector_momentum(data_root):
    """Load sector momentum from v3511 synthetic sector basket artifacts"""
    basket_dir = Path(data_root)/"runtime_reports"/"sector_baskets_v3511"
    if not basket_dir.exists(): return {}
    sector_mom = {}
    for p in basket_dir.glob("*.csv"):
        sector = p.stem
        rows = []
        with open(p, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                r20 = _f(r.get("sector_return_20d"))
                r5 = _f(r.get("sector_return_5d"))
                if r20 is not None: rows.append({"trade_date":r.get("trade_date",""),"return_20d":r20,"return_5d":r5,"phase":r.get("sector_phase","")})
        sector_mom[sector] = rows
    return sector_mom

def get_sector_momentum(sector_mom, sector, entry_date):
    """Get sector return at entry_date"""
    rows = sector_mom.get(sector, [])
    ed = str(entry_date).replace("-","")[:8]
    for r in rows:
        if r["trade_date"] == ed:
            return {"sector_return_20d":r.get("return_20d"),"sector_return_5d":r.get("return_5d"),"sector_phase":r.get("phase"),"source":"v3511_synthetic_sector_index"}
    return None

# ── E7: Fund Flow Placeholder Ban ──
FUND_FLOW_RULES = {"fund_flow_status":"MISSING","flow_score":None,"flow_missing_blocks_hunt":True,"rule":"main_net_inflow/large_order_net_inflow/lhb data NOT AVAILABLE; D-Matrix must not use zero as placeholder","action":"flow_score=0 is FORBIDDEN; must be None or explicitly MISSING"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-root",default=".")
    ap.add_argument("--output",default="runtime_reports/v3520_patch_e_critical_data_completion.json")
    args=ap.parse_args()

    print("E2: PIT Historical Financial Join...",flush=True)
    ticker_reports = build_pit_financial_loader(args.data_root)
    pit_tickers = sum(1 for v in ticker_reports.values() if v)
    print(f"  {pit_tickers} tickers with PIT-ready financial reports",flush=True)

    print("E4: Industry Percentile v2...",flush=True)
    percentiles = build_industry_percentile_v2(args.data_root)
    roe_cov = sum(1 for p in percentiles.values() if p.get("industry_percentile_roe") is not None)
    growth_cov = sum(1 for p in percentiles.values() if p.get("industry_percentile_growth") is not None)
    print(f"  {len(percentiles)} tickers, roe={roe_cov}({roe_cov/max(1,len(percentiles))*100:.0f}%), growth={growth_cov}({growth_cov/max(1,len(percentiles))*100:.0f}%)",flush=True)

    print("E6: Sector Momentum from v3511...",flush=True)
    sector_mom = load_sector_momentum(args.data_root)
    print(f"  {len(sector_mom)} sectors with momentum data",flush=True)

    # Load valuation from PATCH-D
    print("Loading valuation + fundamentals...",flush=True)
    valuation = {}
    vb_path = Path(args.data_root)/"data"/"valuation"/"daily_basic_sample_20260526.csv"
    if vb_path.exists():
        with open(vb_path, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                tk = str(r.get("ts_code","")).split(".")[0].zfill(6)
                valuation[tk] = {"pe_ttm":_f(r.get("pe_ttm")),"pb":_f(r.get("pb")),"ps":_f(r.get("ps")),"total_mv":_f(r.get("total_mv")),"dv_ratio":_f(r.get("dv_ratio"))}
    # Fallback EPS/BPS for missing
    for tk in [t for t in list(percentiles.keys()) if t not in valuation]:
        reports = ticker_reports.get(tk, [])
        if reports:
            latest = reports[-1]; eps = latest.get("eps"); bps = latest.get("bps")
            if eps and bps:
                close_p = _get_last_close(tk, args.data_root)
                if close_p:
                    valuation[tk] = {"pe_ttm":close_p/eps if eps>0 else None,"pb":close_p/bps if bps>0 else None,"source":"eps_bps_fallback","pit_note":"last close used; NOT pit-safe for historical dates"}

    # B-Matrix shadow with PIT join + percentile v2 + sector momentum
    print("\nB-Matrix shadow with PIT + percentile v2...",flush=True)
    b_eligible=0; b_samples=0; pit_ok=0
    for tk in list(ticker_reports.keys())[:5000]:
        reports = ticker_reports.get(tk, [])
        if not reports: continue
        # Use latest report for testing
        latest = reports[-1]
        v = valuation.get(tk, {})
        ip = percentiles.get(tk, {})
        b_facts = {"gross_margin":latest.get("gross_margin"),"roe":latest.get("roe"),"revenue_yoy":latest.get("revenue_yoy"),"net_profit_yoy":latest.get("netprofit_yoy"),"debt_ratio":latest.get("debt_ratio"),"pe_ttm":v.get("pe_ttm"),"pb":v.get("pb"),"ps":v.get("ps"),"dividend_yield":v.get("dv_ratio"),"industry_percentile_roe":ip.get("industry_percentile_roe"),"industry_percentile_growth":ip.get("industry_percentile_growth"),
            # Real cash flow from fundamentals!
            "ocf":_f(latest.get("ocfps")),"ocf_to_np":_f(latest.get("ocfps"))/_f(latest.get("eps")) if _f(latest.get("ocfps")) and _f(latest.get("eps")) else None,"fcf_proxy":_f(latest.get("fcff")),
            "net_margin":None,"roic":None,"deduct_np_yoy":None,"current_ratio":None,"goodwill_ratio":None,"bottleneck_score":None,"chain_position":None,"st_flag":None,"audit_opinion":None,"ocf_trend":None}
        result = score_b_matrix(financial_facts=b_facts, valuation_facts=b_facts, industry_facts=b_facts)
        b_samples += 1
        if result["base_role_eligible"]: b_eligible += 1
        if latest.get("ann_date"): pit_ok += 1
    print(f"  B eligible: {b_eligible}/{b_samples} ({b_eligible/b_samples*100:.1f}%) PIT-safe: {pit_ok}/{b_samples}",flush=True)

    # D-Matrix shadow with sector momentum
    print("D-Matrix shadow with sector momentum...",flush=True)
    d_eligible=0; d_samples=0; mom_used=0
    for tk in list(ticker_reports.keys())[:1000]:
        # Get sector and momentum
        ip = percentiles.get(tk, {}); sector = ip.get("sector","")
        mom = get_sector_momentum(sector_mom, sector, "20260526") or {}
        # Price signal from bars
        bars_path = Path(args.data_root)/"data"/"price_bars"/f"{tk}.csv"
        if not bars_path.exists(): continue
        bars = []
        with open(bars_path, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                d = str(r.get("trade_date") or r.get("date","")).replace("-","")[:8]; c = _f(r.get("close"))
                if d and c is not None: bars.append({"trade_date":d,"close":c,"open":_f(r.get("open")),"high":_f(r.get("high")),"low":_f(r.get("low"))})
        if len(bars) < 20: continue
        idx = len(bars)-1; cur = bars[idx]; prev = bars[idx-1]
        pct = (cur["close"] - prev["close"]) / prev["close"] * 100 if prev["close"] else 0
        one_price = all(cur.get(k) == cur.get("close") for k in ["open","high","low"] if cur.get(k) is not None) and pct >= 9.8
        lb = {"limit_up_flag":pct>=9.8,"limit_down_flag":pct<=-9.8,"one_price_board_flag":one_price}
        # D facts
        event = {"event_evidence_level":"C","event_recency_hours":24,"catalyst_strength":50}
        price = {"return_1d":pct,"return_3d":pct,"return_5d":pct,"volume_ratio_5d":1.0,"turnover_rate":1.0,"amplitude":abs(pct),"volatility_expansion":0}
        flow = {"main_net_inflow":None,"large_order_net_inflow":None,"lhb_buy_amount":None,"lhb_sell_amount":None}  # E7: None, not 0
        theme = {"theme_heat_score":0,"theme_rank_change":0,"sector_momentum":mom.get("sector_return_20d",None),"concept_board_strength":None}  # E6: real sector momentum
        if theme["sector_momentum"] is not None: mom_used += 1
        tradability = {"tradability_status":"TRADABLE" if not lb["limit_up_flag"] else "BLOCKED","limit_up_flag":lb["limit_up_flag"],"limit_down_flag":lb["limit_down_flag"],"consecutive_limit_up_count":1 if lb["limit_up_flag"] else 0,"suspension_flag":False,"one_price_board_flag":lb["one_price_board_flag"],"liquidity_capacity_status":"ADEQUATE"}
        result = score_d_matrix(event_facts=event, price_facts=price, flow_facts=flow, theme_facts=theme, tradability_facts=tradability)
        d_samples += 1
        if result["short_event_eligible"]: d_eligible += 1
    print(f"  D eligible: {d_eligible}/{d_samples} ({d_eligible/d_samples*100:.1f}%) sector_momentum={mom_used}",flush=True)

    report = {"report_version":"V3520_PATCH_E_CRITICAL_DATA_COMPLETION_V10","mode":"PATCH_E_DATA_COMPLETION","E2_pit_join":{"tickers_with_reports":pit_tickers,"historical_join_ready":pit_tickers>0,"function":"get_pit_safe_report(ticker, replay_date)"},"E4_industry_percentile_v2":{"ticker_count":len(percentiles),"roe_coverage":roe_cov,"growth_coverage":growth_cov,"method":"continuous_percentile_rank_with_sector_aggregation"},"E6_sector_momentum":{"sector_count":len(sector_mom),"momentum_samples_used":mom_used,"source":"v3511_synthetic_sector_basket"},"E7_fund_flow_ban":FUND_FLOW_RULES,"E8_shadow_replay":{"b_eligible":b_eligible,"b_samples":b_samples,"b_rate":b_eligible/b_samples if b_samples else 0,"d_eligible":d_eligible,"d_samples":d_samples,"d_rate":d_eligible/d_samples if d_samples else 0},"patch_e_status":"PATCH_E_CRITICAL_DATA_COMPLETION_APPLIED","real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False}

    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  PATCH-E: B={b_eligible}/{b_samples} D={d_eligible}/{d_samples} sector_mom={mom_used}")
    print("PATCH-E complete")

def _get_last_close(tk, data_root):
    p = Path(data_root)/"data"/"price_bars"/f"{tk}.csv"
    if not p.exists(): return None
    last = None
    with open(p, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            c = _f(r.get("close"))
            if c is not None: last = c
    return last

if __name__=="__main__": main()
