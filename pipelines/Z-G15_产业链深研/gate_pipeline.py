#!/usr/bin/env python3
"""☯️ Z-G15 产业链深研 — v1.0 | 按需 | V3证据分层+8硬门+催化剂日历"""
import argparse, json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))
try: from pipelines.z17_loader import market_truth, get_financials, get_kline, dq_score, l4_health
except: market_truth = lambda t: {"status":"stub"}

def run(tickers=None):
    now = datetime.now(timezone(timedelta(hours=8)))
    tickers = tickers or ["002463"]
    result = {"pipeline_signature":"Z-G15_产业链深研_v2.9.5-draft","timestamp":now.isoformat(),"analyses":[]}
    
    print(f"\n☯️ Z-G15 产业链深研 — {', '.join(tickers)}")
    print("=" * 60)
    
    for t in tickers:
        g1 = market_truth(t); dq = dq_score(t); l4 = l4_health(t); fin = get_financials(t); kl = get_kline(t, 120)
        
        print(f"\n📋 {t} {g1.get('name','?')}")
        print(f"  价格: {g1.get('price','?')} | DQ: {dq.get('total',0)} | L4: {l4.get('status','?')}")
        
        # V3证据分层
        evidence = {
            "A_确证": [],
            "B_佐证": [],
            "C_传闻": [],
            "D_风险": []
        }
        
        if dq.get("total",0) > 70: evidence["A_确证"].append(f"数据质量DQ={dq['total']}")
        if fin.get("has_finance"): evidence["A_确证"].append(f"Q1EPS={fin.get('q1_eps','?' )}")
        if kl.get("count",0) > 60: evidence["B_佐证"].append(f"K线充足({kl['count']}日)")
        if fin.get("industry"): evidence["B_佐证"].append(f"行业:{fin['industry']}")
        if l4.get("status")=="BLOCK": evidence["D_风险"].append(f"L4 BLOCK: {l4.get('errors',['?'])[0]}")
        
        print("  证据分层:")
        for level, items in evidence.items():
            if items: print(f"    {level}: {'; '.join(items)}")
        
        # 8硬门
        gates = {
            "ROE": "待拉取" if not fin.get("has_finance") else "有Q1数据",
            "OCF/NI": "待拉取",
            "毛利率趋势": "待拉取",
            "负债率": "待拉取",
            "分红": "待拉取",
            "估值分位": f"DQ={dq.get('total',0)}",
            "产业链位置": fin.get("industry","待拉取"),
            "催化剂日程": "见EventCalendar"
        }
        print("  8硬门:")
        for k, v in gates.items(): print(f"    {k}: {v}")
        
        # 催化剂
        catalysts = [{"date":"5/20","event":"FOMC纪要","relevance":"高(宏观)"},
                     {"date":"5/20盘后","event":"英伟达Q1财报","relevance":"高(AI链)"}]
        print("  催化剂:")
        for c in catalysts: print(f"    {c['date']} {c['event']} ({c['relevance']})")
        
        result["analyses"].append({"ticker":t,"evidence":evidence,"gates":gates,"catalysts":catalysts})
    
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G15 产业链深研")
    p.add_argument("--tickers", type=str, default="", help="逗号分隔")
    args = p.parse_args()
    tk = [t.strip() for t in args.tickers.split(",") if t.strip()] if args.tickers else None
    run(tickers=tk)
