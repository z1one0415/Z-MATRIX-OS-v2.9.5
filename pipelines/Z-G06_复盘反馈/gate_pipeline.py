#!/usr/bin/env python3
"""☯️ Z-G06 复盘反馈 — gate_pipeline.py
运行: 每日 16:00 盘后 | 依赖: Z-G01 (via z17_loader)
输出: 5段报告 (运行状态/准确率/模式检测/Z9归因/Hermes学习)
"""

import argparse, json, os, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEMORY_MD = WORKSPACE.parent / "MEMORY.md"
REPORT_ROOT = Path(os.path.expanduser(
    "~/Documents/openclaw memory/openclaw memory/Z2信息熔炉/投资记忆银行"
))

# Z-G01
try:
    from pipelines.z17_loader import market_truth, get_kline
except ImportError:
    market_truth = lambda t: {"status": "stub"}
    get_kline = lambda t, d: {"prices": [], "count": 0}

def run(predictions_file=None, tickers=None, mode="daily"):
    now = datetime.now(timezone(timedelta(hours=8)))
    today = now.strftime("%Y-%m-%d")
    
    result = {
        "pipeline_signature": "Z-G06_复盘反馈_v2.9.5-draft",
        "timestamp": now.isoformat(), "date": today,
        "status": "running", "sections": {}, "errors": []
    }
    
    print(f"\n☯️ Z-G06 复盘反馈 — {today} 16:00")
    print("=" * 60)
    
    # 1. 运行状态
    print("\n📡 [1/5] 运行状态:")
    status = {"date": today, "mode": mode, "data_sources": {}, "gate_status": {}}
    
    tickers = tickers or _extract_watchlist()
    for t in tickers[:5]:
        g1 = market_truth(t)
        status["gate_status"][t] = g1.get("status", "?")
    status["tracked_count"] = len(tickers)
    print(f"  追踪标的: {len(tickers)} | 数据可用: {sum(1 for v in status['gate_status'].values() if v=='PASS')}")
    result["sections"]["运行状态"] = status
    
    # 2. 准确率追踪
    print("\n📊 [2/5] 准确率追踪:")
    accuracy = _compute_accuracy(today)
    for k, v in accuracy["summary"].items():
        print(f"  {k}: {v}")
    result["sections"]["准确率追踪"] = accuracy
    
    # 3. 模式检测
    print("\n🔍 [3/5] 模式检测:")
    patterns = _detect_patterns(tickers, today)
    for p in patterns:
        print(f"  [{p['type']}] {p['ticker']}: {p['reason'][:60]}")
    print(f"  共{len(patterns)}条异常模式")
    result["sections"]["模式检测"] = patterns
    
    # 4. Z9归因
    print("\n🎯 [4/5] Z9归因:")
    attribution = _z9_attribute(patterns, accuracy)
    print(f"  主要偏差: {attribution.get('primary_bias','—')}")
    print(f"  驱动因子: {attribution.get('driver','—')}")
    result["sections"]["Z9归因"] = attribution
    
    # 5. Hermes学习
    print("\n🧠 [5/5] Hermes学习输入:")
    learning = _hermes_input(attribution, patterns)
    print(f"  教训: {learning.get('lesson','—')}")
    print(f"  Memory候选: {len(learning.get('memory_candidates',[]))}条")
    result["sections"]["Hermes学习输入"] = learning
    
    # 落盘
    outdir = REPORT_ROOT / "超级预测系统" / "复盘记录"
    outdir.mkdir(parents=True, exist_ok=True)
    jpath = outdir / f"{today}_复盘反馈_Z-G06.json"
    with open(jpath, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n📄 {jpath}")
    
    return result

def _extract_watchlist():
    """从MEMORY.md提取观察标的"""
    tk = []
    if MEMORY_MD.exists():
        text = open(MEMORY_MD).read()
        import re
        for m in re.finditer(r'\b(00\d{4}|30\d{4}|60\d{4}|68\d{4})\b', text):
            code = m.group(1)
            if code not in tk:
                tk.append(code)
    return tk[:10]

def _compute_accuracy(today):
    """计算今日预测准确率"""
    return {
        "summary": {
            "总预测数": "待积累",
            "正确数": "—",
            "拒绝率": "—",
            "遗漏因子": "—",
            "平均滑点": "—",
        },
        "calibrated": False,
        "min_samples_for_z9": 50,
        "current_samples": 0
    }

def _detect_patterns(tickers, today):
    """检测异常模式: REJECTION/MISSED/SLIPPAGE"""
    patterns = []
    for t in tickers[:5]:
        kl = get_kline(t, 5)
        if kl.get("prices") and len(kl["prices"]) >= 2:
            prices = kl["prices"]
            chg = (prices[-1]/prices[-2]-1)*100
            if chg > 9.5:
                patterns.append({"type":"SLIPPAGE","ticker":t,"reason":f"+{chg:.1f}%涨停, 可能存在买入滑点"})
            elif chg < -9.5:
                patterns.append({"type":"REJECTION","ticker":t,"reason":f"{chg:.1f}%跌停, 前日预测可能被市场否定"})
    if not patterns:
        patterns.append({"type":"NORMAL","ticker":"—","reason":"今日无显著异常模式"})
    return patterns

def _z9_attribute(patterns, accuracy):
    return {
        "primary_bias": "数据不足, 待≥50样本",
        "driver": "—",
        "calibration_note": "uncalibrated",
        "total_patterns": len(patterns)
    }

def _hermes_input(attribution, patterns):
    return {
        "lesson": "样本积累中, Z9未启用自动学习",
        "memory_candidates": [
            {"type": p["type"], "ticker": p["ticker"], "note": p["reason"][:50]}
            for p in patterns if p["type"] != "NORMAL"
        ],
        "approval_required": True
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G06 复盘反馈")
    p.add_argument("--tickers", type=str, default="", help="逗号分隔代码")
    p.add_argument("--mode", default="daily")
    args = p.parse_args()
    tk = [t.strip() for t in args.tickers.split(",") if t.strip()] if args.tickers else None
    run(tickers=tk, mode=args.mode)
