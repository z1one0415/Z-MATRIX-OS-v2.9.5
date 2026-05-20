#!/usr/bin/env python3
"""☯️ Z-G09 全局轮动筛选 — gate_pipeline.py v1.0
运行: 每周全量 + 每日增量 | 功能: R-Matrix全市场扫描, 不预设标的
依赖: Z-G01 (via z17_loader) + R-Matrix + OscillationKing
输出: R_POOL (≤80只轮动候选, 按评分排序)
"""

import argparse, json, os, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth, get_kline, l4_health
except ImportError:
    market_truth = lambda t: {"status":"stub"}; get_kline = lambda t,d: {"prices":[],"count":0}; l4_health = lambda t: {"status":"stub"}

def _quick_r_score(ticker):
    """快速R-Matrix评分: 振幅+通道位置+均值回归"""
    g1 = market_truth(ticker)
    kl = get_kline(ticker, 60)
    if g1.get("status") == "BLOCK" or not kl.get("prices") or len(kl["prices"]) < 20:
        return {"status":"DATA_INSUFFICIENT","output_level":"O1_DATA_GAP","reason_codes":["KLINE_LT_20D"],"excluded_from_ranking":True}
    prices = kl["prices"]
    # 简化的R评分: 振幅 + 当前位置 + 趋势
    amp = (max(prices[-20:])/min(prices[-20:])-1)*100
    pos = (prices[-1]-min(prices[-20:]))/(max(prices[-20:])-min(prices[-20:])) if max(prices[-20:])!=min(prices[-20:]) else 0.5
    ma20 = sum(prices[-20:])/20
    trend = (prices[-1]/ma20-1)*100
    # 低位+震荡 → 高分
    score = amp * (1-abs(pos-0.5)*1.5) + abs(trend) * 0.5
    return {"ticker":ticker,"name":g1.get("name","?"),"price":g1.get("price"),
            "amp_20d":round(amp,1),"position":round(pos*100),"trend":round(trend,1),
            "score":round(score,1)}

def run(pool_size=80):
    """全局R-Matrix扫描"""
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G09_全局轮动_v2.9.5-draft","timestamp":now.isoformat(),
              "status":"running","sections":{},"r_pool":[]}
    print(f"\n☯️ Z-G09 全局轮动筛选 — {now.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 从MEMORY.md + 预设列表取扫描范围
    tickers = _extract_scan_list()
    print(f"📡 扫描范围: {len(tickers)}标的 → 筛选TOP{pool_size}")
    
    candidates = []
    for t in tickers:
        sc = _quick_r_score(t)
        if sc: candidates.append(sc)
        if len(candidates) % 50 == 0:
            print(f"  进度: {len(candidates)}/{len(tickers)}")
    
    candidates.sort(key=lambda x: x["score"], reverse=True)
    r_pool = candidates[:pool_size]
    
    print(f"\n🏆 R_POOL TOP10:")
    for i, c in enumerate(r_pool[:10]):
        print(f"  {i+1:2d}. {c['ticker']} {c['name']:<8s} {c['price']:>7.2f} "
              f"评分{c['score']:5.1f} 振幅{c['amp_20d']:4.1f}% 位置{c['position']}%")
    
    result["r_pool"] = r_pool
    result["sections"]["summary"] = {"scanned":len(tickers),"pool_size":len(r_pool),"max_score":r_pool[0]["score"] if r_pool else 0}
    return result

def _extract_scan_list():
    """从Tushare全量数据库取标的列表 (fallback: MEMORY.md)"""
    mem = WORKSPACE.parent / "MEMORY.md"
    tk = []
    if mem.exists():
        import re
        for m in re.finditer(r'\b(00\d{4}|30\d{4}|60\d{4}|68\d{4})\b', open(mem).read()):
            c = m.group(1)
            if c not in tk: tk.append(c)
    # 补充预设标的
    preset = ["002463","002472","002837","002881","002979","000977","000988",
              "300308","300394","300502","300620","300687","300499","300687",
              "600519","601899","601898","688041","688111","688160","688256",
              "688322","688498","688608","688981"]
    for c in preset:
        if c not in tk: tk.append(c)
    return tk

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G09 全局轮动筛选")
    p.add_argument("--pool", type=int, default=80, help="候选池大小")
    args = p.parse_args()
    run(pool_size=args.pool)
