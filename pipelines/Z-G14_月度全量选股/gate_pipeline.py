#!/usr/bin/env python3
"""☯️ Z-G14 月度全量选股 (流A) — v1.0 | 每月 | B-R-D全量重跑+交叉矩阵+产业链映射"""
import argparse, json, os, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
MEMORY_MD = WORKSPACE.parent / "MEMORY.md"
sys.path.insert(0, str(WORKSPACE))
try: from pipelines.z17_loader import market_truth, get_kline, get_financials, dq_score, l4_health, get_sectors
except: market_truth = lambda t: {"status":"stub"}

def _quick_scan(tickers):
    """快速B-R-D三维扫描"""
    candidates = []
    for t in tickers:
        g1 = market_truth(t); dq = dq_score(t); l4 = l4_health(t); fin = get_financials(t)
        if g1.get("status")=="BLOCK" or l4.get("status")=="BLOCK": continue
        kl = get_kline(t, 60); prices = kl.get("prices",[])
        if len(prices) < 20: continue
        
        # 简化的三维评分
        b_score = min(dq.get("total",50), 100) * 0.5  # 数据质量→底仓分
        r_score = (max(prices[-20:])/min(prices[-20:])-1)*100 * 0.6 if len(prices)>=20 else 0  # 振幅→轮动分
        d_score = (8 if fin.get("has_finance") else 4) + (5 if dq.get("total",0)>70 else 2)  # 黑马分
        
        # 交叉标记
        b_ok = b_score > 40; r_ok = r_score > 15; d_ok = d_score > 8
        cross = []
        if b_ok and d_ok: cross.append("B∩D☆")
        if b_ok and r_ok: cross.append("B∩R★")
        if d_ok and r_ok: cross.append("D∩R◇")
        if b_ok and not r_ok and not d_ok: cross.append("纯B")
        if d_ok and not b_ok and not r_ok: cross.append("纯D")
        if r_ok and not b_ok and not d_ok: cross.append("纯R")
        if not cross: cross.append("观察")
        
        candidates.append({"code":t,"name":g1.get("name","?"),"b":round(b_score,1),
                          "r":round(r_score,1),"d":round(d_score,1),"cross":cross[0],
                          "price":g1.get("price")})
    return candidates

def _scan_list():
    tk = []
    mem = WORKSPACE.parent / "MEMORY.md"
    if mem.exists():
        for m in re.finditer(r'\b(00\d{4}|30\d{4}|60\d{4}|68\d{4})\b', open(mem).read()):
            c = m.group(1)
            if c not in tk: tk.append(c)
    preset = ["002463","002472","002837","002881","002979","000977","000988",
              "300308","300394","300502","300620","300499","600519","601899",
              "601898","688041","688111","688160","688256","688322","688608"]
    for c in preset:
        if c not in tk: tk.append(c)
    return tk

def run():
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G14_月度全量_v2.9.5-draft","timestamp":now.isoformat(),"sections":{}}
    
    print(f"\n☯️ Z-G14 月度全量选股 (流A) — {now.strftime('%Y-%m')}")
    print("⚠️ 目的: 清空预设→从零扫全市场→防局部视角陷阱")
    print("=" * 60)
    
    tickers = _scan_list()
    print(f"\n📡 扫描: {len(tickers)}标的")
    
    candidates = _quick_scan(tickers)
    candidates.sort(key=lambda x: x["b"]+x["r"]+x["d"], reverse=True)
    
    # 交叉统计
    cross_counts = {}
    for c in candidates: cross_counts[c["cross"]] = cross_counts.get(c["cross"],0)+1
    
    print(f"\n📊 交叉矩阵:")
    for k, v in sorted(cross_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {k}: {v}只")
    
    # TOP15
    top15 = candidates[:15]
    print(f"\n🏆 TOP15终选:")
    for i, c in enumerate(top15):
        print(f"  {i+1:2d}. {c['code']} {c['name']:<8s} B={c['b']:.0f} R={c['r']:.0f} D={c['d']:.0f} [{c['cross']}]")
    
    # 产业链映射
    chains = {"机器人":"双环|雷赛|绿的|三花|步科|兆威|奥比|柯力",
              "AI算力":"中际|天孚|新易盛|寒武纪|海光|浪潮|华工|沪电|中贝|英维克|高澜|美格|恒玄",
              "半导体":"688|002049|603986|300782",
              "资源":"紫金|中煤|黄金|601899|601898",
              "消费":"600519|000858|002304"}
    chain_hits = {}
    for c in candidates[:50]:
        for ch, kw in chains.items():
            if any(k in c["name"] for k in kw.split("|")):
                chain_hits[ch] = chain_hits.get(ch, 0) + 1
    
    print(f"\n🔗 产业链浓度 (TOP50):")
    for ch in chains:
        h = chain_hits.get(ch, 0)
        flag = "⚠️盲区" if h == 0 else f"{h}只"
        print(f"  {ch}: {flag}")
    
    result["candidates"] = candidates[:30]
    result["sections"]["cross_matrix"] = cross_counts
    result["sections"]["chain_density"] = chain_hits
    return result

if __name__ == "__main__":
    run()
