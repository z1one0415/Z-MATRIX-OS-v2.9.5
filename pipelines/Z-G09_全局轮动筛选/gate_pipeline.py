#!/usr/bin/env python3
"""☯️ Z-G09 全局轮动筛选 — R-Matrix OscillationKing v1.1 Type A/B 双模式
运行: 每周全量 + 每日增量 | 算法: Type A水平箱体震荡 + Type B上升通道震荡 + DFA/Hurst + 支撑阻力 + BearTrap + VolCone
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
    """R-Matrix OscillationKing v1.1 Type A/B 双模式 评分"""
    g1 = market_truth(ticker)
    l4 = l4_health(ticker)
    if g1.get("status") == "BLOCK" or l4.get("status") == "BLOCK":
        return {"status":"BLOCKED","output_level":"O2_DIAGNOSTIC","ticker":ticker,"excluded_from_ranking":True}
    
    kl = get_kline(ticker, 500)
    prices = kl.get("prices", [])
    if len(prices) < 260:
        return {"status":"DATA_INSUFFICIENT","output_level":"O1_DATA_GAP",
                "reason_codes":["KLINE_LT_260D"],"ticker":ticker,"excluded_from_ranking":True}
    
    try:
        from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal, rank_type_b_rising_channel
        type_a = rank_type_a_horizontal(ticker, g1.get("name",""), prices)
        type_b = rank_type_b_rising_channel(ticker, g1.get("name",""), prices)
        best = max([type_a, type_b], key=lambda r: r.score)
        return {
            "ticker":ticker,"name":g1.get("name",""),
            "status":"PASS",
            "score":best.score,
            "oscillation_type":best.oscillation_type,
            "allowed_action":best.allowed_action,
            "next_trigger":best.next_trigger,
            "diagnostics":best.diagnostics,
            "subtype_scores":{"type_a_horizontal":type_a.score,"type_b_rising_channel":type_b.score},
            "subtype_actions":{"type_a_horizontal":type_a.allowed_action,"type_b_rising_channel":type_b.allowed_action}
        }
    except Exception as e:
        return {"status":"ERROR","ticker":ticker,"error":str(e)[:80],"excluded_from_ranking":True}


def run(pool_size=80, universe="A_SHARE_ALL", allow_fallback=True):
    """Z-G09 R-Matrix OscillationKing v1.1
    universe: A_SHARE_ALL/INDEX_300/INDEX_500/INDEX_1000/WATCHLIST/PRESET_DEV/FILE"""
    from pipelines.universe_provider import load_universe
    
    now = datetime.now(timezone(timedelta(hours=8)))
    uni = load_universe(source=universe, allow_fallback=allow_fallback,
                       min_count=4000 if universe=="A_SHARE_ALL" else None)
    is_global = uni.get("is_global", False)
    sig = "Z-G09_R-Matrix_v2.9.5-RC" if is_global else "Z-G09_R-Matrix_non_global_universe"
    
    result = {"pipeline_signature":sig,"timestamp":now.isoformat(),
              "engine":"OscillationKing v1.1","sections":{},"r_pool":[],
              "universe_contract":uni,"warnings":[]}
    
    if uni["status"] == "DATA_GAP":
        result["status"] = "DATA_GAP"
        result["reason"] = "UNIVERSE_NOT_AVAILABLE"
        return result
    if not is_global:
        result["warnings"].append("NON_GLOBAL_UNIVERSE")
    
    tickers = uni["tickers"]
    print(f"\n☯️ Z-G09 筛选 (OscillationKing v1.1) — {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"    Universe: {uni['source']} {uni['count']}只 is_global={is_global}")
    print("=" * 60)
    print(f"📡 扫描: {len(tickers)}标的 → Type A水平震荡 + Type B上升通道 + OscillationKing双模式")
    
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

# _scan_list() removed — use pipelines.universe_provider.load_universe() instead

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G09 R-Matrix OscillationKing v1.1")
    p.add_argument("--pool", type=int, default=80)
    p.add_argument("--universe", default="A_SHARE_ALL",
                   choices=["A_SHARE_ALL","INDEX_300","INDEX_500","INDEX_1000","WATCHLIST","PRESET_DEV","FILE"])
    p.add_argument("--allow-fallback", action="store_true")
    args = p.parse_args()
    run(pool_size=args.pool, universe=args.universe, allow_fallback=args.allow_fallback)
