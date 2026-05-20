#!/usr/bin/env python3
"""☯️ Z-G09 全局轮动筛选 — R-Matrix OscillationKing v1.1 Type B优先版
运行: 每周全量 + 每日增量 | 算法: Type B上升通道 + 残差均值回归 + 熊陷阱 + 波动锥 (Type A水平震荡待补)
"""

import argparse, json, sys, os
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))
os.chdir(str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth, get_kline, l4_health
except ImportError:
    market_truth = lambda t: {"status":"stub","name":"?"}; get_kline = lambda t,d: {"prices":[],"count":0}
    l4_health = lambda t: {"status":"stub"}

def _r_matrix_score(ticker):
    """R-Matrix OscillationKing v1.1 Type B优先版 评分"""
    g1 = market_truth(ticker)
    l4 = l4_health(ticker)
    if g1.get("status") == "BLOCK" or l4.get("status") == "BLOCK":
        return {"status":"BLOCKED","output_level":"O2_DIAGNOSTIC","ticker":ticker,"excluded_from_ranking":True}
    
    kl = get_kline(ticker, 250)
    prices = kl.get("prices", [])
    if len(prices) < 60:
        return {"status":"DATA_INSUFFICIENT","output_level":"O1_DATA_GAP",
                "reason_codes":["KLINE_LT_60D"],"ticker":ticker,"excluded_from_ranking":True}
    
    try:
        from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_b_rising_channel
        result = rank_type_b_rising_channel(ticker, g1.get("name",""), prices)
        return {
            "ticker":ticker,"name":g1.get("name",""),
            "status":"PASS",
            "score":result.score,
            "role":result.role,
            "oscillation_type":result.oscillation_type,
            "allowed_action":result.allowed_action,
            "next_trigger":result.next_trigger,
            "diagnostics":result.diagnostics if hasattr(result,"diagnostics") else {}
        }
    except Exception as e:
        return {"status":"ERROR","ticker":ticker,"error":str(e)[:80],"excluded_from_ranking":True}


def run(pool_size=80):
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G09_全局轮动_v2.9.5-RC","timestamp":now.isoformat(),
              "engine":"OscillationKing v1.1","sections":{},"r_pool":[]}
    
    print(f"\n☯️ Z-G09 全局轮动 (OscillationKing v1.1) — {now.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    tickers = _scan_list()
    print(f"📡 扫描: {len(tickers)}标的 → Type B上升通道 + 残差均值回归 + BearTrap + VolCone")
    
    candidates = []; degraded = []
    for t in tickers:
        sc = _r_matrix_score(t)
        if not sc: continue
        if sc.get("excluded_from_ranking"):
            degraded.append(sc)
        else:
            candidates.append(sc)
    
    candidates.sort(key=lambda x: x.get("score",0), reverse=True)
    r_pool = candidates[:pool_size]
    
    print(f"\n🏆 R_POOL (OscillationKing v1.1): {len(r_pool)}/{len(tickers)}入选, {len(degraded)}数据不足/DEGRADED")
    for i, c in enumerate(r_pool[:10]):
        print(f"  {i+1:2d}. {c['ticker']} {c.get('name','?'):<8s} score={c.get('score',0):.1f} {c.get('oscillation_type','?')} {c.get('allowed_action','?')}")
    
    result["r_pool"] = r_pool
    result["sections"]["summary"] = {"scanned":len(tickers),"pool_size":len(r_pool),"degraded":len(degraded)}
    return result

def _scan_list():
    tk = []; preset = ["002463","002472","002837","002881","002979","000977","000988",
        "300308","300394","300502","300620","300687","300499",
        "600519","601899","601898","688041","688111","688160","688256","688322","688608","688981"]
    for c in preset:
        if c not in tk: tk.append(c)
    return tk

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G09 全局轮动 (OscillationKing v1.1)")
    p.add_argument("--pool", type=int, default=80)
    args = p.parse_args()
    run(pool_size=args.pool)
