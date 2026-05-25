"""Lightweight Backtest v1.0"""
from __future__ import annotations
import statistics

def calc_return(ep, ex):
    if ep and ex and ep>0: return round((ex/ep-1)*100,2)
    return None

def calc_max_drawdown(prices):
    if not prices or len(prices)<2: return None
    peak=prices[0]; mdd=0.0
    for p in prices: peak=max(peak,p); dd=(peak-p)/peak*100; mdd=max(mdd,dd)
    return round(mdd,2)

def calc_win_rate(returns):
    v=[r for r in returns if r is not None]
    return round(sum(1 for r in v if r>0)/len(v)*100,1) if v else 0.0

def calc_avg(v):
    vv=[x for x in v if x is not None]
    return round(sum(vv)/len(vv),2) if vv else None

def calc_median(v):
    vv=[x for x in v if x is not None]
    return round(statistics.median(vv),2) if vv else None

def _entry_outcome(e, bars, offset):
    idx=0
    for i,b in enumerate(bars):
        if b.get("date","")[:10]>=e.get("entry_date","")[:10]: idx=i; break
    if idx+offset>=len(bars): return None,None
    try:
        ep=float(e.get("entry_price",0))
        ex=float(bars[idx+offset].get("adj_close",bars[idx+offset].get("close",0)))
        seg=[float(bars[j].get("adj_close",bars[j].get("close",0))) for j in range(idx,idx+offset+1)]
        return calc_return(ep,ex),calc_max_drawdown(seg)
    except: return None,None

def run_lightweight_role_backtest(paper_entries, price_bars_by_ticker):
    groups={}; [groups.setdefault(e.get("role","UNKNOWN"),[]).append(e) for e in paper_entries]
    ALL_ROLES=["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT"]
    results={}
    all_t20s,all_t60s,all_dd20s,all_dd60s=[],[],[],[]
    for role in ALL_ROLES+["ALL"]:
        entries=groups.get(role,[])
        t20s,t60s,dd20s,dd60s=[],[],[],[]
        for e in entries:
            bars=price_bars_by_ticker.get(e.get("ticker",""),[])
            if not bars: continue
            r20,dd20=_entry_outcome(e,bars,20); r60,dd60=_entry_outcome(e,bars,60)
            if r20 is not None: t20s.append(r20);dd20s.append(dd20)
            if r60 is not None: t60s.append(r60);dd60s.append(dd60)
        if role!="ALL":
            results[role]={"count":len(entries),"win_rate_t20":calc_win_rate(t20s),"avg_return_t20":calc_avg(t20s),"median_return_t20":calc_median(t20s),"avg_max_drawdown_t20":calc_avg(dd20s),"win_rate_t60":calc_win_rate(t60s),"avg_return_t60":calc_avg(t60s),"avg_max_drawdown_t60":calc_avg(dd60s)}
        all_t20s.extend(t20s);all_t60s.extend(t60s);all_dd20s.extend(dd20s);all_dd60s.extend(dd60s)
    results["ALL"]={"count":sum(len(groups.get(r,[])) for r in ALL_ROLES),"win_rate_t20":calc_win_rate(all_t20s),"avg_return_t20":calc_avg(all_t20s),"median_return_t20":calc_median(all_t20s),"avg_max_drawdown_t20":calc_avg(all_dd20s),"win_rate_t60":calc_win_rate(all_t60s),"avg_return_t60":calc_avg(all_t60s),"avg_max_drawdown_t60":calc_avg(all_dd60s)}
    return results
