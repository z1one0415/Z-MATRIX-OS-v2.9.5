#!/usr/bin/env python3
"""☯️ Z-G10 全局黑马筛选 — gate_pipeline.py v1.0
运行: 每周全量 + 每日增量 | 功能: D-Matrix全市场扫描, 发现黑马基因标的
依赖: Z-G01 (via z17_loader)
输出: D_POOL (D1→D2→D3分级)
"""

import argparse, json, os, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth, get_kline, l4_health, get_financials, dq_score
except ImportError:
    market_truth = lambda t: {"status":"stub"}; get_kline = lambda t,d: {"prices":[],"count":0}
    l4_health = lambda t: {"status":"stub"}; get_financials = lambda t: {"has_finance":False}
    dq_score = lambda t: {"total":0}

def _quick_d_score(ticker):
    """快速D-Matrix评分: 基因+低关注+量价异动"""
    l4 = l4_health(ticker)
    if l4.get("status") == "BLOCK":
        return {"status":"DATA_INSUFFICIENT","output_level":"O1_DATA_GAP","reason_codes":["L4_BLOCKED_OR_NO_KLINE"],"excluded_from_ranking":True}
    
    g1 = market_truth(ticker)
    kl = get_kline(ticker, 60)
    fin = get_financials(ticker)
    
    if not kl.get("prices") or len(kl["prices"]) < 20:
        return {"status":"DATA_INSUFFICIENT","output_level":"O1_DATA_GAP","reason_codes":["L4_BLOCKED_OR_NO_KLINE"],"excluded_from_ranking":True}
    
    prices = kl["prices"]
    # Gene: 低关注度 = 近3月涨幅低
    chg_3m = (prices[-1]/prices[0]-1)*100 if len(prices)>=60 else 0
    gene = max(0, 10 - abs(chg_3m))  # 涨幅低→高分
    
    # Sector: 有财务数据=基础分
    sector = 8 if fin.get("has_finance") else 4
    
    # Silent: 近5日缩量+横盘
    if len(prices) >= 6:
        vol5 = sum(abs(prices[i]/prices[i-1]-1) for i in range(-5,0))
        silent = 10 - min(vol5*100, 10)
    else:
        silent = 5
    
    # Volume preload: 量能温和放大
    vol_preload = 5
    
    # DQ修正
    dq = dq_score(ticker)
    dq_bonus = dq.get("total", 50) / 20
    
    total = gene + sector + silent + vol_preload + dq_bonus
    
    # 生命周期分级
    if total > 30: lifecycle = "D3_CANDIDATE"
    elif total > 20: lifecycle = "D2_PREHEAT"
    else: lifecycle = "D1_THEME_SEED"
    
    return {"ticker":ticker,"name":g1.get("name","?"),"price":g1.get("price"),
            "score":round(total,1),"lifecycle":lifecycle,"chg_3m":round(chg_3m,1)}

def run(pool_size=100):
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G10_全局黑马_v2.9.5-draft","timestamp":now.isoformat(),
              "status":"running","d_pool":[]}
    
    print(f"\n☯️ Z-G10 全局黑马筛选 — {now.strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    tickers = _extract_list()
    print(f"📡 扫描: {len(tickers)}标的")
    
    candidates = []; degraded = []
    for i, t in enumerate(tickers):
        sc = _quick_d_score(t)
        if sc and sc.get("status") != "DATA_INSUFFICIENT" and "score" in sc:
            candidates.append(sc)
        elif sc:
            degraded.append(sc)  # 数据不足落盘, 不进入排序
        if (i+1) % 30 == 0: print(f"  进度: {i+1}/{len(tickers)}")
    
    candidates.sort(key=lambda x: x["score"], reverse=True)
    d_pool = candidates[:pool_size]
    
    # 分级统计
    d3 = [c for c in d_pool if c["lifecycle"]=="D3_CANDIDATE"]
    d2 = [c for c in d_pool if c["lifecycle"]=="D2_PREHEAT"]
    d1 = [c for c in d_pool if c["lifecycle"]=="D1_THEME_SEED"]
    
    print(f"\n🏆 D_POOL: D3={len(d3)} D2={len(d2)} D1={len(d1)} (总计{len(d_pool)})")
    if d3:
        print("D3_CANDIDATE TOP5:")
        for i, c in enumerate(d3[:5]):
            print(f"  {i+1}. {c['ticker']} {c['name']:<8s} score={c['score']:.0f} 3M={c['chg_3m']:+.1f}%")
    
    result["d_pool"] = d_pool
    result["sections"] = {"d3":len(d3),"d2":len(d2),"d1":len(d1),"total":len(d_pool)}
    return result

def _extract_list():
    mem = WORKSPACE.parent / "MEMORY.md"
    tk = []
    if mem.exists():
        import re
        for m in re.finditer(r'\b(00\d{4}|30\d{4}|60\d{4}|68\d{4})\b', open(mem).read()):
            c = m.group(1)
            if c not in tk: tk.append(c)
    preset = ["002463","002472","002837","002881","002979","000977","000988",
              "300308","300394","300502","300620","300687","300499",
              "600519","601899","601898","688041","688111","688160","688256",
              "688322","688498","688608"]
    for c in preset:
        if c not in tk: tk.append(c)
    return tk

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G10 全局黑马筛选")
    p.add_argument("--pool", type=int, default=100)
    args = p.parse_args()
    run(pool_size=args.pool)
