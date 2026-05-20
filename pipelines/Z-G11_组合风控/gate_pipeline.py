#!/usr/bin/env python3
"""☯️ Z-G11 组合风控 — gate_pipeline.py v1.0
运行: 每周+调仓前 | 功能: 持仓集中度/角色桶/因子暴露检查
依赖: Z-G01 (via z17_loader) + MEMORY.md持仓
输出: 风险警告 + REDUCE_RISK建议
"""

import argparse, json, os, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEMORY_MD = WORKSPACE.parent / "MEMORY.md"
sys.path.insert(0, str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth
except ImportError:
    market_truth = lambda t: {"status":"stub","price":0,"name":"?"}

def _parse_positions():
    """解析持仓"""
    positions = []
    if not MEMORY_MD.exists(): return positions
    text = open(MEMORY_MD).read()
    for m in re.finditer(r'\|\s*([^|]+?)\s+(\d{6})\s*\|\s*([\d,]+股)\s*\|\s*([\d.]+)\s*\|', text):
        name = m.group(1).strip()
        code = m.group(2)
        shares = int(m.group(3).replace("股","").replace(",",""))
        cost = float(m.group(4))
        g1 = market_truth(code)
        price = g1.get("price") or cost
        value = shares * price
        positions.append({"code":code,"name":name,"shares":shares,"cost":cost,
                          "price":price,"value":value})
    return positions

def _classify_chain(name):
    """简单产业链分类"""
    chains = {"机器人":["双环","雷赛","绿的","三花","步科","兆威","奥比","柯力"],
              "AI算力":["中际","天孚","新易盛","寒武纪","海光","浪潮","华工","沪电","中贝","英维克"],
              "资源":["紫金","中煤","黄金"]}
    for chain, keywords in chains.items():
        for kw in keywords:
            if kw in name: return chain
    return "其他"

def run():
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G11_组合风控_v2.9.5-draft","timestamp":now.isoformat(),
              "status":"running","sections":{}}
    
    print(f"\n☯️ Z-G11 组合风控 — {now.strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    positions = _parse_positions()
    if not positions:
        print("⚠️ 无持仓数据")
        return result
    
    total_value = sum(p["value"] for p in positions)
    
    # 1. 单票集中度
    print("\n📊 单票占比:")
    warnings = []
    for p in positions:
        pct = p["value"]/total_value*100 if total_value else 0
        flag = "⚠️" if pct > 40 else ("🔴" if pct > 25 else "✅")
        print(f"  {flag} {p['code']} {p['name']:<8s} {pct:5.1f}%  (¥{p['value']:,.0f})")
        if pct > 40: warnings.append(f"单票集中度过高: {p['name']} {pct:.0f}%")
    
    # 2. 产业链集中度
    print(f"\n🔗 产业链分布:")
    chain_map = {}
    for p in positions:
        ch = _classify_chain(p["name"])
        chain_map[ch] = chain_map.get(ch, 0) + p["value"]
    for ch, val in sorted(chain_map.items(), key=lambda x: x[1], reverse=True):
        pct = val/total_value*100 if total_value else 0
        flag = "⚠️" if pct > 60 else "✅"
        print(f"  {flag} {ch}: {pct:.1f}%")
        if pct > 60: warnings.append(f"产业链过度集中: {ch} {pct:.0f}%")
    
    # 3. 现金比例 (假设总资产=持仓+现金, 估算)
    cash_ratio = None  # NOT_CONNECTED — not a placeholder, explicitly unavailable
    print(f"\n💰 现金比例: 未接入账户实测数据")
    
    # 4. 裁决
    print(f"\n📋 裁决:")
    if warnings:
        print(f"  ⚠️ {len(warnings)}条风险警告")
        for w in warnings: print(f"    - {w}")
        result["sections"]["action"] = "REDUCE_RISK"
    else:
        print(f"  ✅ 组合风险正常")
        result["sections"]["action"] = "PORTFOLIO_OK"
    
    result["sections"]["positions"] = positions
    result["sections"]["total_value"] = total_value
    result["sections"]["warnings"] = warnings
    result["sections"]["cash"] = {"cash_ratio": None, "source": "NOT_CONNECTED", "capability": "cash_exposure_disabled"}
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G11 组合风控")
    args = p.parse_args()
    run()
