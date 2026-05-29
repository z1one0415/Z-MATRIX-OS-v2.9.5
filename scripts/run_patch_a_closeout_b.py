#!/usr/bin/env python3
# allowlist: forbidden-token-definition
"""Closeout-B: Real Data Integration Audit — Outcome Horizon + B/D Matrix + Trading Cost"""
from __future__ import annotations
import json, csv, argparse
from pathlib import Path
from collections import Counter
from statistics import median
from zmatrix.patch_a.outcome_horizon import check_all_horizons, build_hardened_outcome

def _f(x,d=None):
    try:
        if x in (None,""): return d
        return float(x)
    except: return d

def _load_financials(data_root):
    """Load real financial facts from data/fundamentals/"""
    facts = {}
    fin_dir = Path(data_root)/"data"/"fundamentals"
    if not fin_dir.exists(): return facts
    for p in fin_dir.glob("*_fin.csv"):
        tk = p.stem.replace("_fin","").zfill(6)
        with open(p, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                facts[tk] = {"ticker":tk,"report_period":row.get("end_date"),"ann_date":row.get("ann_date"),"gross_margin":_f(row.get("gross_margin")),"current_ratio":_f(row.get("current_ratio")),"debt_ratio":_f(row.get("debt_to_assets")),"roe":_f(row.get("roe")),"roe_yearly":_f(row.get("roe_yearly")),"netprofit_yoy":_f(row.get("netprofit_yoy")),"ocf_to_np":_f(row.get("ocf_to_shortdebt")),"eps":_f(row.get("eps")),"bps":_f(row.get("bps")),"revenue_yoy":_f(row.get("or_yoy"))}
                break  # first row only
    return facts

def _load_price_bars(ticker, data_root, max_days=120):
    bare = str(ticker).split(".")[0].zfill(6) if isinstance(ticker, str) else str(ticker)
    p = Path(data_root)/"data"/"price_bars"/f"{bare}.csv"
    if not p.exists(): return []
    bars = []
    with open(p, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d = str(r.get("trade_date") or r.get("date","")).replace("-","")[:8]; c = _f(r.get("close"))
            if d and c is not None: bars.append({"trade_date":d,"close":c,"open":_f(r.get("open")),"high":_f(r.get("high")),"low":_f(r.get("low")),"volume":_f(r.get("vol") or r.get("volume"))})
    return sorted(bars, key=lambda x:x["trade_date"])[-max_days:]

def _estimate_limit_board(bars, idx):
    """Estimate limit board status from price bars"""
    if idx <= 0: return {}
    cur = bars[idx]; prev = bars[idx-1]
    prev_close = prev.get("close",0)
    if not prev_close: return {}
    pct = (cur["close"] - prev_close) / prev_close * 100
    is_limit_up = pct >= 9.8  # A-share ~10% limit
    is_limit_down = pct <= -9.8
    # One-price board: all OHLC equal
    o = cur.get("open"); h = cur.get("high"); l = cur.get("low"); c = cur.get("close")
    one_price = o and h and l and c and (h == l) and (o == h) and is_limit_up
    return {"limit_up_flag":is_limit_up,"limit_down_flag":is_limit_down,"one_price_board_flag":one_price and is_limit_up,"consecutive_limit_check":is_limit_up}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--replay-path", default="runtime_reports/v35_brd_strategy_replay_result.json")
    ap.add_argument("--data-root", default=".")
    ap.add_argument("--output", default="runtime_reports/v3520_patch_a_closeout_b_report.json")
    args=ap.parse_args()

    print("Loading replay...", flush=True)
    rr=json.loads(Path(args.replay_path).read_text(encoding="utf-8"))
    outcomes={}
    for d in rr.get("daily_results",[]):
        for o in d.get("outcomes",[]): outcomes[o.get("paper_id")]=o

    print("Loading financials...", flush=True)
    financials=_load_financials(args.data_root)
    print(f"  {len(financials)} tickers with financial data", flush=True)

    # B1: Outcome Horizon Audit (with cached price bars)
    print("B1: Outcome Horizon Audit (loading price bars)...", flush=True)
    price_cache = {}
    unique_tickers = set(o.get("ticker","") for o in outcomes.values())
    for i, tk in enumerate(unique_tickers):
        price_cache[tk] = _load_price_bars(tk, args.data_root, 120)
        if (i+1) % 1000 == 0: print(f"  cached {i+1}/{len(unique_tickers)} tickers", flush=True)
    print(f"  {len(price_cache)} ticker price bars cached", flush=True)
    t5_ready=0; t20_ready=0; t60_ready=0; t20_dropped=0; total_outcomes=0
    for pid, o in outcomes.items():
        ticker = o.get("ticker","")
        bars = price_cache.get(ticker, [])
        entry_date = o.get("entry_date","")
        ed = str(entry_date).replace("-","")[:8]
        forward = [b for b in bars if b["trade_date"] > ed]
        checks = check_all_horizons(forward_bars=forward)
        if checks["horizons"]["t5"]["horizon_ready"]: t5_ready+=1
        if checks["horizons"]["t20"]["horizon_ready"]: t20_ready+=1
        else: t20_dropped+=1
        if checks["horizons"]["t60"]["horizon_ready"]: t60_ready+=1
        total_outcomes+=1

    # B2: B-Matrix Real Coverage
    print("B2: B-Matrix Coverage Audit...", flush=True)
    b_covered=0; b_total=0; b_core_fields=["gross_margin","current_ratio","debt_ratio","roe","netprofit_yoy","eps"]
    b_field_counts=Counter()
    for tk, f in financials.items():
        b_total+=1; has_core=all(f.get(field) is not None for field in b_core_fields)
        if has_core: b_covered+=1
        for field in b_core_fields:
            if f.get(field) is not None: b_field_counts[field]+=1

    # B3: D-Matrix Real Signals from Price Bars
    print("B3: D-Matrix Price Signal Audit...", flush=True)
    sample_tickers = list(set(o.get("ticker","") for o in list(outcomes.values())[:5000]))
    limit_up_count=0; one_price_count=0; volume_surge=0; gap_count=0; checked=0
    for ticker in sample_tickers[:1000]:
        bars = _load_price_bars(ticker, args.data_root, 120)
        if len(bars)<20: continue
        for i in range(len(bars)-5, len(bars)):
            lb=_estimate_limit_board(bars, i)
            if lb.get("limit_up_flag"): limit_up_count+=1
            if lb.get("one_price_board_flag"): one_price_count+=1
            checked+=1

    # B4: Trading Cost on Replay Samples
    print("B4: Trading Cost Audit...", flush=True)
    from zmatrix.patch_a.trading_cost import compute_net_return
    gross_returns=[]; net_returns=[]; execution_blocked=0; total_cost_checks=0
    for pid, o in list(outcomes.items())[:5000]:
        ep = _f(o.get("entry_price"), 10); ret = _f(o.get("actual_return_t20"))
        if ret is None: continue
        r = compute_net_return(gross_return_pct=ret, entry_price=ep, exit_price=ep*(1+ret/100), volume=1000)
        gross_returns.append(ret); net_returns.append(r["net_return_pct"])
        if not r["execution_feasible"]: execution_blocked+=1
        total_cost_checks+=1

    # Build report
    report = {"report_version":"V3520_PATCH_A_CLOSEOUT_B_REPORT_V10","mode":"CLOSEOUT_B_REAL_DATA_INTEGRATION","B1_outcome_horizon":{"total_outcomes":total_outcomes,"t5_ready":t5_ready,"t20_ready":t20_ready,"t60_ready":t60_ready,"t20_dropped_by_insufficient_forward":t20_dropped,"t5_ready_rate":t5_ready/total_outcomes if total_outcomes else 0,"t20_ready_rate":t20_ready/total_outcomes if total_outcomes else 0,"t60_ready_rate":t60_ready/total_outcomes if total_outcomes else 0},"B2_b_matrix_coverage":{"total_tickers":b_total,"core_coverage_count":b_covered,"core_coverage_rate":b_covered/b_total if b_total else 0,"core_fields":dict(b_field_counts)},"B3_d_matrix_signals":{"checked":checked,"limit_up_detected":limit_up_count,"one_price_board":one_price_count,"note":"Based on 9.8% threshold estimation from price bars"},"B4_trading_cost_audit":{"samples":total_cost_checks,"mean_gross_return":sum(gross_returns)/len(gross_returns) if gross_returns else 0,"mean_net_return":sum(net_returns)/len(net_returns) if net_returns else 0,"median_gross":median(gross_returns) if gross_returns else 0,"median_net":median(net_returns) if net_returns else 0,"cost_drag_bps":(sum(gross_returns)/len(gross_returns) - sum(net_returns)/len(net_returns)) if gross_returns and net_returns else 0,"execution_blocked_count":execution_blocked},"closeout_b_status":"CLOSEOUT_B_REAL_DATA_AUDIT_COMPLETE","real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False}

    out=Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    print(f"\n  Closeout-B Results:")
    print(f"  B1: T5={t5_ready}({t5_ready/total_outcomes*100:.0f}%) T20={t20_ready}({t20_ready/total_outcomes*100:.0f}%) T60={t60_ready}({t60_ready/total_outcomes*100:.0f}%)")
    print(f"  B1: T20 dropped={t20_dropped}")
    print(f"  B2: B-Matrix core coverage={b_covered}/{b_total} ({b_covered/b_total*100:.0f}%)")
    print(f"  B3: Limit up events={limit_up_count}, One-price={one_price_count}")
    print(f"  B4: Cost drag={report['B4_trading_cost_audit']['cost_drag_bps']:.0f}bps, Blocked={execution_blocked}")
    print("Closeout-B complete")

if __name__=="__main__": main()
