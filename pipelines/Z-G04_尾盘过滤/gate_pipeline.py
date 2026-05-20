#!/usr/bin/env python3
"""☯️ Z-G04 尾盘过滤 — gate_pipeline.py v1.0
运行: 14:30监控/15:00最终判定 | 目标: 防尾盘画图与假预热
依赖: Z-G01 (via z17_loader) + D-Matrix false_preheat逻辑
输出: FalsePreheat告警 / SmartMoneyTailGrab / L3尾盘确认
"""

import argparse, json, os, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth, get_kline
except ImportError:
    market_truth = lambda t: {"status":"stub","price":0}
    get_kline = lambda t,d: {"prices":[],"count":0}

def _tail_30min_analysis(ticker):
    """尾盘30分钟特征分析"""
    g1 = market_truth(ticker)
    kl = get_kline(ticker, 20)
    
    if not g1.get("price") or not kl.get("prices") or len(kl["prices"]) < 2:
        return {"type": "DATA_INCOMPLETE", "ticker": ticker}
    
    today_chg = (g1["price"] / g1.get("open", g1["price"]) - 1) * 100 if g1.get("open") else 0
    prices = kl["prices"]
    # Use OHLCV volume field when available, fall back to price-based proxy
    volumes = kl.get("volume", [])
    if len(volumes) >= 5:
        avg_vol_5d = sum(volumes[-5:-1]) / 4
        today_vol = volumes[-1]
        vol_source = "daily_ohlcv"
    elif len(prices) >= 5:
        # Fallback: price-based proxy (degraded, not real volume)
        avg_vol_5d = sum(prices[-5:-1]) / 4 if len(prices) >= 6 else prices[-2]
        today_vol = prices[-1]
        vol_source = "price_proxy_DEGRADED"
    else:
        return {"type": "DATA_INCOMPLETE", "ticker": ticker, "reason": "NO_VOLUME_DATA"}
    
    vol_ratio = today_vol / avg_vol_5d if avg_vol_5d > 0 else 1
    data_contract = kl.get("data_contract", "UNKNOWN")
    
    if today_chg > 3 and vol_ratio < 0.7:
        return {"type": "FALSE_PREHEAT", "ticker": ticker,
                "reason": f"缩量尾盘拉升 (+{today_chg:.1f}%, 量比{vol_ratio:.1f}x)",
                "action": "冷却3交易日, 禁止生命周期升级",
                "data_contract": data_contract, "volume_source": vol_source}
    if today_chg > 2 and vol_ratio > 1.5:
        return {"type": "SMART_MONEY_TAIL", "ticker": ticker,
                "reason": f"放量逆势抢筹 (+{today_chg:.1f}%, 量比{vol_ratio:.1f}x)",
                "action": "次日观察优先级, 需L3确认",
                "data_contract": data_contract, "volume_source": vol_source}
    
    return {"type": "NORMAL", "ticker": ticker, "reason": "尾盘无异常",
            "data_contract": data_contract, "volume_source": vol_source}

def run(tickers=None, mode="tail_filter"):
    """Z-G04 主管线"""
    now = datetime.now(timezone(timedelta(hours=8)))
    today = now.strftime("%Y-%m-%d")
    
    result = {
        "pipeline_signature": "Z-G04_尾盘过滤_v2.9.5-draft",
        "timestamp": now.isoformat(), "date": today,
        "mode": mode, "status": "running", "sections": {}, "errors": []
    }
    
    # 默认扫描MEMORY.md中的观察标的
    tickers = tickers or _extract_watchlist()
    
    print(f"\n☯️ Z-G04 尾盘过滤 — {today} 14:30")
    print("=" * 60)
    
    # 1. 运行状态
    print(f"\n📡 [1/4] 扫描范围: {len(tickers)}标的")
    status = {"tickers_scanned": len(tickers), "time": now.strftime("%H:%M:%S"),
              "filter": "FalsePreheat + SmartMoneyTail + 尾盘画图"}
    result["sections"]["运行状态"] = status
    
    # 2. 尾盘分析
    print(f"\n🔍 [2/4] 尾盘30分钟分析:")
    analyses = []
    false_count = 0; smart_count = 0
    for t in tickers:
        a = _tail_30min_analysis(t)
        analyses.append(a)
        if a["type"] == "FALSE_PREHEAT":
            false_count += 1
            print(f"  ❌ {t}: FALSE_PREHEAT — {a['reason']}")
        elif a["type"] == "SMART_MONEY_TAIL":
            smart_count += 1
            print(f"  🔍 {t}: SMART_MONEY — {a['reason']} (次日观察)")
        elif a["type"] == "NORMAL":
            pass  # 正常不打印
        else:
            print(f"  ⚠️ {t}: {a['type']}")
    result["sections"]["尾盘分析"] = analyses
    
    # 3. D-Matrix Lifecycle Cap
    print(f"\n📋 [3/4] 生命周期封顶:")
    caps = []
    for a in analyses:
        if a["type"] == "FALSE_PREHEAT":
            caps.append({"ticker": a["ticker"], "max_lifecycle": "D2_PREHEAT",
                         "reason": "FalsePreheat触发, 禁止升至D3", "cooldown_days": 3})
            print(f"  🔒 {a['ticker']}: lifecycle≤D2, 冷却3日")
        elif a["type"] == "SMART_MONEY_TAIL":
            caps.append({"ticker": a["ticker"], "max_lifecycle": "D3_CANDIDATE (需次日验证)",
                         "reason": "SmartMoney尾盘, 次日L3确认后方可升"})
    if not caps:
        caps.append({"ticker": "—", "max_lifecycle": "无限制", "reason": "今日尾盘无异常"})
        print(f"  ✅ 无需要封顶的标的")
    result["sections"]["生命周期封顶"] = caps
    
    # 4. 结论
    print(f"\n📊 [4/4] 尾盘裁决:")
    summary = {
        "false_preheat_count": false_count,
        "smart_money_count": smart_count,
        "normal_count": len(analyses) - false_count - smart_count,
        "rule": "FalsePreheat→冷却3日 | SmartMoney→次日验证 | Normal→正常流程"
    }
    print(f"  FalsePreheat: {false_count}只 | SmartMoney: {smart_count}只 | 正常: {summary['normal_count']}只")
    result["sections"]["尾盘裁决"] = summary
    
    return result

def _extract_watchlist():
    mem = WORKSPACE.parent / "MEMORY.md"
    tk = []
    if mem.exists():
        import re
        for m in re.finditer(r'\b(00\d{4}|30\d{4}|60\d{4}|68\d{4})\b', open(mem).read()):
            c = m.group(1)
            if c not in tk: tk.append(c)
    return tk[:10] or ["002463","688608"]

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G04 尾盘过滤")
    p.add_argument("--tickers", type=str, default="", help="逗号分隔代码")
    args = p.parse_args()
    tk = [t.strip() for t in args.tickers.split(",") if t.strip()] if args.tickers else None
    run(tickers=tk)
