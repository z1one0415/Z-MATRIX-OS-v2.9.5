#!/usr/bin/env python3
"""☯️ Z-G13 底仓管理 — v1.0 | 每月+财报后 | B-Matrix+ThesisStop"""
import argparse, json, os, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
MEMORY_MD = WORKSPACE.parent / "MEMORY.md"
sys.path.insert(0, str(WORKSPACE))
try: from pipelines.z17_loader import market_truth, get_financials, dq_score, l4_health
except: market_truth = lambda t: {"status":"stub"}; get_financials = lambda t: {}; dq_score = lambda t: {"total":0}; l4_health = lambda t: {"status":"stub"}

B_TYPES = ["B1高股息压舱石","B2复利再投资","B3资源现金牛","B4垄断基础设施","B5品牌稀缺垄断"]

def _check_thesis(ticker, name):
    """Thesis Stop: 检查底仓逻辑是否证伪"""
    fin = get_financials(ticker)
    dq = dq_score(ticker)
    g1 = market_truth(ticker)
    flags = []
    
    # 检查: 财务数据缺失
    if not fin.get("has_finance"): flags.append("财报数据不可用")
    # 检查: DQ过低
    if dq.get("total", 0) < 60: flags.append(f"DQ={dq['total']}<60, 数据质量恶化")
    # 检查: ST/停牌
    l4 = l4_health(ticker)
    if l4.get("status") == "BLOCK": flags.append(f"L4 BLOCK: {l4.get('errors',['未知'])[0]}")
    
    if len(flags) >= 2:
        return "THESIS_REVIEW_REQUIRED", flags
    elif flags:
        return "THESIS_WATCH", flags
    return "THESIS_INTACT", []

def run():
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G13_底仓管理_v2.9.5-draft","timestamp":now.isoformat()}
    
    print(f"\n☯️ Z-G13 底仓管理 — 每月")
    print("=" * 60)
    
    # 解析持仓
    positions = []
    if MEMORY_MD.exists():
        for m in re.finditer(r'\|\s*([^|]+?)\s+(\d{6})\s*\|\s*([\d,]+股)\s*\|', open(MEMORY_MD).read()):
            positions.append({"name":m.group(1).strip(),"code":m.group(2),"shares":int(m.group(3).replace("股","").replace(",",""))})
    
    if not positions:
        print("⚠️ 无持仓数据")
        return result
    
    print(f"📊 持仓 {len(positions)}只 → Thesis复核")
    
    b_candidates = []
    for p in positions:
        thesis, flags = _check_thesis(p["code"], p["name"])
        icon = "✅" if thesis=="THESIS_INTACT" else ("⚠️" if thesis=="THESIS_WATCH" else "🔴")
        b_type = B_TYPES[len(b_candidates) % 5]  # placeholder classification
        b_candidates.append({"code":p["code"],"name":p["name"],"thesis":thesis,"flags":flags,"b_type":b_type})
        print(f"  {icon} {p['code']} {p['name']:<8s} {thesis} {b_type} {flags if flags else ''}")
    
    result["b_pool"] = b_candidates
    result["sections"] = {"total":len(positions),"intact":sum(1 for c in b_candidates if c["thesis"]=="THESIS_INTACT"),
                         "watch":sum(1 for c in b_candidates if c["thesis"]=="THESIS_WATCH"),
                         "review":sum(1 for c in b_candidates if c["thesis"]=="THESIS_REVIEW_REQUIRED")}
    return result

if __name__ == "__main__":
    run()
