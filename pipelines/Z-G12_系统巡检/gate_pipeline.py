#!/usr/bin/env python3
"""☯️ Z-G12 系统巡检 — gate_pipeline.py v1.0
运行: 每周日 + 升级后 | 功能: 扫地僧6模块 + TailRisk + DQ趋势 + Cron健康
依赖: Z-G01 (via z17_loader) + HEARTBEAT.md + cron list
输出: 巡检报告 (6模块状态)
"""

import argparse, json, os, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth, get_sectors, dq_score, l25_macro
except ImportError:
    market_truth = lambda t: {"status":"stub"}; get_sectors = lambda: {"status":"stub"}
    dq_score = lambda t: {"total":0}; l25_macro = lambda: {"filled":0}

def _check_data_sources():
    """检查数据源健康"""
    r = {"sina":"DOWN","baostock":"DOWN","tushare":"DOWN"}
    try:
        g1 = market_truth("002463")
        if g1.get("status") not in ("BLOCK",): r["sina"] = "UP"
        if g1.get("baostock_close"): r["baostock"] = "UP"
    except: pass
    return r

def _count_memory_files():
    """记忆宫殿盘存"""
    root = Path(os.path.expanduser(
        "~/Documents/openclaw memory/openclaw memory/Z2信息熔炉/投资记忆银行"
    ))
    if not root.exists(): return {"root":"MISSING","files":0}
    count = sum(1 for _ in root.rglob("*.md"))
    return {"root":"OK","files":count}

def _check_cron():
    """Cron健康 (通过openclaw cron list)"""
    try:
        r = subprocess.run(["openclaw","cron","list"], capture_output=True, text=True, timeout=5)
        return {"status":"accessible","output_lines":len(r.stdout.splitlines())} if r.returncode==0 else {"status":"error"}
    except:
        return {"status":"unavailable"}

def run():
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G12_系统巡检_v2.9.5-draft","timestamp":now.isoformat(),
              "status":"running","sections":{}}
    
    print(f"\n☯️ Z-G12 系统巡检 — {now.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    checks = {}
    
    # 模块1: 数据源健康
    print("\n🔌 数据源健康:")
    ds = _check_data_sources()
    checks["data_sources"] = ds
    for k, v in ds.items():
        print(f"  {'✅' if v=='UP' else '❌'} {k}: {v}")
    
    # 模块2: 记忆宫殿
    print("\n📁 记忆宫殿:")
    mem = _count_memory_files()
    checks["memory_palace"] = mem
    print(f"  📄 {mem['files']}个文件 | 根: {mem['root']}")
    
    # 模块3: DQ趋势
    print("\n📊 DQ趋势 (样本:002463):")
    dq = dq_score("002463")
    checks["dq_trend"] = {"sample_ticker":"002463","dq":dq.get("total",0)}
    print(f"  DQ={dq.get('total','?')} | {dq.get('status','?')}")
    
    # 模块4: L2.5宏观
    print("\n🌐 L2.5宏观填充:")
    l25 = l25_macro()
    checks["l25"] = l25
    print(f"  {l25.get('filled',0)}/8信息域")
    
    # 模块5: 板块
    print("\n📈 板块数据:")
    sec = get_sectors()
    checks["sectors"] = sec
    print(f"  状态: {sec.get('status','?')}")
    
    # 模块6: Cron (如果可用)
    print("\n⏰ Cron:")
    cron = _check_cron()
    checks["cron"] = cron
    print(f"  状态: {cron.get('status','?')}")
    
    # 总结
    up_count = sum(1 for v in checks.get("data_sources",{}).values() if v=="UP")
    total_ok = (up_count >= 2) and (mem.get("root")=="OK") and (dq.get("total",0)>=60)
    
    print(f"\n{'='*60}")
    print(f"🏁 巡检结论: {'✅ 系统健康' if total_ok else '⚠️ 需要关注'}")
    print(f"   数据源: {up_count}/3在线 | 记忆: {mem['files']}文件 | DQ: {dq.get('total',0)}")
    
    result["sections"] = checks
    result["sections"]["verdict"] = "HEALTHY" if total_ok else "NEEDS_ATTENTION"
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G12 系统巡检")
    args = p.parse_args()
    run()
