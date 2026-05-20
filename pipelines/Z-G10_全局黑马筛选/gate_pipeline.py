#!/usr/bin/env python3
"""☯️ Z-G10 全局黑马筛选 — D-Matrix v2.2 源点雷达
运行: 每日轻量 + 每周全量 | 算法: Gene+Sector+Silent+Micro+SmartMoney+VolPreload+FalsePreheat
"""

import argparse, json, sys, os
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))
os.chdir(str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth, get_kline, l4_health, get_financials, dq_score
except ImportError:
    market_truth = lambda t: {"status":"stub","name":"?"}; get_kline = lambda t,d: {"prices":[],"count":0}
    l4_health = lambda t: {"status":"stub"}; get_financials = lambda t: {"has_finance":False}
    dq_score = lambda t: {"total":0}

def _d_matrix_score(ticker):
    """D-Matrix v2.2 黑马源点雷达评分"""
    l4 = l4_health(ticker)
    if l4.get("status") == "BLOCK":
        return {"status":"BLOCKED","output_level":"O2_DIAGNOSTIC","ticker":ticker,"excluded_from_ranking":True}
    
    g1 = market_truth(ticker)
    kl = get_kline(ticker, 120)
    prices = kl.get("prices", [])
    if len(prices) < 20:
        return {"status":"DATA_INSUFFICIENT","output_level":"O1_DATA_GAP",
                "reason_codes":["KLINE_LT_20D"],"ticker":ticker,"excluded_from_ranking":True}
    
    try:
        from zmatrix.scoring.d_band.d_early_v22_scorer import evaluate_d_early_v22
        # Build OHLCV-enriched payload — missing fields are empty, scorer does coverage discount
        payload = {
            "code": ticker, "name": g1.get("name", ""),
            "sector": g1.get("industry", "") or g1.get("sector", ""),
            "theme": {},
            "prices": prices,
            "market": {
                "dates": kl.get("dates", []),
                "open": kl.get("open", []),
                "high": kl.get("high", []),
                "low": kl.get("low", []),
                "close": kl.get("close", prices),
                "volume": kl.get("volume", []),
                "amount": kl.get("amount", []),
                "prices": prices,
                "data_contract": kl.get("data_contract", ""),
            },
            "silent_accumulation": {
                "prices": prices,
                "volume": kl.get("volume", []),
                "amount": kl.get("amount", []),
            },
            "micro_absorption": {
                "prices": prices,
                "volume": kl.get("volume", []),
                "amount": kl.get("amount", []),
            },
            "volume_price_preload": {
                "prices": prices,
                "volume": kl.get("volume", []),
                "amount": kl.get("amount", []),
            },
        }
        result = evaluate_d_early_v22(payload)
        
        # DEarlyV22Result dataclass → 通过to_dict()获取字段
        if hasattr(result, "to_dict"):
            rd = result.to_dict()
            score = rd.get("final_score", rd.get("raw_score", 0))
            lifecycle = rd.get("stage_hint", rd.get("lifecycle_max", "D1_THEME_SEED"))
            return {
                "ticker":ticker,"name":g1.get("name",""),
                "status":"PASS","score":float(score or 0),
                "raw_score":float(rd.get("raw_score",0) or 0),
                "coverage_ratio":rd.get("coverage_ratio"),
                "lifecycle":lifecycle,
                "allowed_action_max":rd.get("allowed_action_max","WATCH"),
                "details":rd.get("score_breakdown",{}),
                "warnings":rd.get("warnings",[])
            }
        
        if isinstance(result, dict):
            score = result.get("d_score", result.get("total", result.get("final_score", 0)))
            lifecycle = result.get("lifecycle", result.get("stage_hint", "D1_THEME_SEED"))
            return {
                "ticker":ticker,"name":g1.get("name",""),
                "status":"PASS","score":float(score) if score else 0,
                "lifecycle":lifecycle,
                "details":{k:v for k,v in result.items() if k in ("gene_score","sector_score","silent_score")}
            }
        return {"ticker":ticker,"name":g1.get("name",""),"status":"PASS","score":float(result) if result else 0}
    except Exception as e:
        return {"status":"ERROR","ticker":ticker,"error":str(e)[:80],"excluded_from_ranking":True}


def run(pool_size=100):
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G10_全局黑马_v2.9.5-RC","timestamp":now.isoformat(),
              "engine":"D-Matrix v2.2","d_pool":[]}
    
    print(f"\n☯️ Z-G10 全局黑马 (D-Matrix v2.2) — {now.strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    tickers = _scan_list()
    print(f"📡 扫描: {len(tickers)}标的 → Gene(22%)+Sector(18%)+Silent(18%)+SmartMoney(10%)+Micro(10%)+VolPreload(7%)")
    
    candidates = []; degraded = []
    for t in tickers:
        sc = _d_matrix_score(t)
        if not sc: continue
        if sc.get("excluded_from_ranking"):
            degraded.append(sc)
        else:
            candidates.append(sc)
    
    candidates.sort(key=lambda x: x.get("score",0), reverse=True)
    d_pool = candidates[:pool_size]
    
    d3 = [c for c in d_pool if c.get("lifecycle","") == "D3_CANDIDATE"]
    d2 = [c for c in d_pool if c.get("lifecycle","") == "D2_PREHEAT"]
    
    print(f"\n🏆 D_POOL (D-Matrix v2.2): D3={len(d3)} D2={len(d2)} Total={len(d_pool)}")
    if d3:
        for i, c in enumerate(d3[:5]):
            print(f"  {i+1}. {c['ticker']} {c.get('name','?'):<8s} score={c.get('score',0):.0f} {c.get('lifecycle','?')}")
    
    result["d_pool"] = d_pool
    result["sections"] = {"d3":len(d3),"d2":len(d2),"total":len(d_pool),"degraded":len(degraded)}
    return result

def _scan_list():
    tk = []; preset = ["002463","002472","002837","002881","002979","000977","000988",
        "300308","300394","300502","300620","300687","300499",
        "600519","601899","601898","688041","688111","688160","688256","688322","688608"]
    for c in preset:
        if c not in tk: tk.append(c)
    return tk

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G10 全局黑马 (D-Matrix v2.2)")
    p.add_argument("--pool", type=int, default=100)
    args = p.parse_args()
    run(pool_size=args.pool)
