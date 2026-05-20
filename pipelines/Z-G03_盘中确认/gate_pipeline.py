#!/usr/bin/env python3
"""☯️ Z-G03 盘中确认 — gate_pipeline.py v1.0
运行: 09:25-10:30 | 检查点: 0925竞价/0935承接/0945确认/1030过期
依赖: Z-G01 (via z17_loader)
输出: 5段报告 (运行状态/竞价数据/L3确认/准确率/天师解读)
"""

import argparse, json, os, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth, get_kline, get_sectors
except ImportError:
    market_truth = lambda t: {"status":"stub","price":0}
    get_kline = lambda t,d: {"prices":[],"count":0}
    get_sectors = lambda: {"status":"stub"}

def _auction_snapshot(ticker):
    """拉取竞价数据 (09:25集合竞价后)"""
    g1 = market_truth(ticker)
    if g1.get("status") == "BLOCK":
        return {"error": "no_data", "status": "BLOCK"}
    return {
        "ticker": ticker,
        "name": g1.get("name","?"),
        "open": g1.get("open"),
        "price": g1.get("price"),
        "high": g1.get("high"),
        "low": g1.get("low"),
        "prev_close": g1.get("baostock_close"),
        "gap_pct": round((g1.get("open",0)/g1.get("baostock_close",1)-1)*100, 2) if g1.get("baostock_close") else None,
        "source": g1.get("source",""),
        "time": g1.get("time",""),
    }

def _vwap_check(ticker):
    """VWAP站稳检测 — 日内VWAP近似 (high+low+close)/3 vs price"""
    g1 = market_truth(ticker)
    if g1.get("price") and g1.get("high") and g1.get("low"):
        vwap_est = (g1["high"] + g1["low"] + g1["price"]) / 3
        if g1["price"] >= vwap_est:
            return "ABOVE_VWAP"
    return "BELOW_VWAP"

def _volume_ratio(ticker):
    """量比 = 今日成交量 / 5日均量 (OHLCV daily volume)"""
    kl = get_kline(ticker, 20)
    volumes = kl.get("volume", [])
    if len(volumes) >= 6:
        avg = sum(volumes[-6:-1]) / 5
        today = volumes[-1]
        return round(today / avg, 2) if avg > 0 else 1.0
    # Fallback to neutral when no OHLCV volume
    return 1.0

def run(tickers=None, mode="confirm"):
    """Z-G03 主管线"""
    now = datetime.now(timezone(timedelta(hours=8)))
    today = now.strftime("%Y-%m-%d")
    
    result = {
        "pipeline_signature": "Z-G03_盘中确认_v2.9.5-draft",
        "timestamp": now.isoformat(), "date": today,
        "mode": mode, "status": "running", "sections": {}, "errors": []
    }
    
    tickers = tickers or ["002472","002463","688608"]
    
    print(f"\n☯️ Z-G03 盘中确认 — {today} {now.strftime('%H:%M')}")
    print("=" * 60)
    
    # 1. 运行状态
    print("\n📡 [1/5] 运行状态:")
    status = {
        "truth_gate": "PASS",
        "auction_time": now.strftime("%H:%M"),
        "confirmation_chain": "L2.5→L3→竞价→VWAP",
        "tracked_count": len(tickers),
        "sector_snapshot": get_sectors(),
    }
    print(f"  竞价时间: {status['auction_time']} | 追踪: {len(tickers)}标的")
    result["sections"]["运行状态"] = status
    
    # 2. 竞价数据
    print(f"\n📊 [2/5] 竞价数据:")
    auction = []
    for t in tickers:
        snap = _auction_snapshot(t)
        auction.append(snap)
        if snap.get("gap_pct") is not None:
            icon = "🟢" if snap["gap_pct"] > 0 else "🔴"
            print(f"  {icon} {t} {snap.get('name','?'):<8s} 开{snap.get('open','?'):.2f} 现{snap.get('price','?'):.2f}"
                  f" 缺口{snap['gap_pct']:+.2f}%")
    result["sections"]["竞价数据"] = auction
    
    # 3. L3确认
    print(f"\n🔍 [3/5] L3确认结果:")
    l3 = []
    for t in tickers:
        g1 = market_truth(t)
        vwap = _vwap_check(t)
        vr = _volume_ratio(t)
        verdict = "UNCERTAIN"
        if vwap == "ABOVE_VWAP" and vr > 0.8:
            verdict = "CONFIRMED"
        elif vwap == "BELOW_VWAP" or vr < 0.5:
            verdict = "REJECTED"
        
        entry = {
            "ticker": t, "name": g1.get("name","?"),
            "price": g1.get("price"), "vwap_status": vwap,
            "volume_ratio": vr, "verdict": verdict,
            "action": "WATCH" if verdict == "CONFIRMED" else "WAIT"
        }
        l3.append(entry)
        icon = "✅" if verdict == "CONFIRMED" else ("❌" if verdict == "REJECTED" else "⏳")
        print(f"  {icon} {t}: {verdict} (VWAP={vwap} 量比={vr:.1f}x) → {entry['action']}")
    result["sections"]["L3确认结果"] = l3
    
    # 4. 准确率
    accuracy = {"notes": "盘中确认实时记录, 盘后由Z-G06汇总校准"}
    result["sections"]["准确率记录"] = accuracy
    
    # 5. 天师解读
    confirmed = [e for e in l3 if e["verdict"] == "CONFIRMED"]
    rejected = [e for e in l3 if e["verdict"] == "REJECTED"]
    
    print(f"\n🎓 [5/5] 天师解读:")
    print(f"  确认: {len(confirmed)}只 | 否决: {len(rejected)}只 | 待定: {len(l3)-len(confirmed)-len(rejected)}只")
    if confirmed:
        print(f"  → 可WATCH: {', '.join(e['ticker'] for e in confirmed)}")
    if rejected:
        print(f"  → 不追: {', '.join(e['ticker'] for e in rejected)}")
    print(f"  ⚠️ 盘中确认仅输出WATCH/WAIT, 不输出买入")
    
    result["sections"]["天师解读"] = {
        "confirmed_count": len(confirmed),
        "rejected_count": len(rejected),
        "rule": "盘中确认只决定观察优先级, 不决定买入"
    }
    
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G03 盘中确认")
    p.add_argument("--tickers", type=str, default="", help="逗号分隔代码")
    p.add_argument("--mode", default="confirm", choices=["confirm","quick"])
    args = p.parse_args()
    tk = [t.strip() for t in args.tickers.split(",") if t.strip()] if args.tickers else None
    run(tickers=tk, mode=args.mode)
