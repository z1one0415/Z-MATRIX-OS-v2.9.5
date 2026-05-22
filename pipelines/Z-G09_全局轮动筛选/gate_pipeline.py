#!/usr/bin/env python3
"""☯️ Z-G09 全局轮动筛选 — R-Matrix v1.2 双周期三模式

波动天王(日线): Type A水平箱体震荡 + Type B上升通道震荡 + DFA/Hurst + 支撑阻力 + BearTrap + VolCone
轮动天王(月线): RISING/HORIZONTAL/DECLINING + 月线β + 通道位置 + HARVEST/HOLD/WATCH_ENTRY/AVOID

运行: 每周全量 + 每日增量
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
    if g1.get("status")=="BLOCK" or l4.get("status")=="BLOCK":
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
        best = type_a if type_a.score >= type_b.score else type_b
        return {
            "ticker":ticker,"name":g1.get("name",""),
            "status":"PASS","score":best.score,
            "oscillation_type":best.oscillation_type,
            "allowed_action":best.allowed_action,
            "subtype_scores":{"type_a_horizontal":type_a.score,"type_b_rising_channel":type_b.score},
            "diagnostics":getattr(best,"diagnostics",{}),
        }
    except Exception as e:
        return {"status":"ERROR","ticker":ticker,"error":str(e)[:80],"excluded_from_ranking":True}


def run(pool_size=80, universe="A_SHARE_ALL", allow_fallback=True, enable_monthly=True):
    """Z-G09 R-Matrix v1.2 — 双周期轮动筛选

    universe: 股票池来源 (A_SHARE_ALL/INDEX_300/INDEX_500/INDEX_1000/WATCHLIST/PRESET_DEV/FILE)
    allow_fallback: A_SHARE_ALL不可用时是否降级到INDEX_BASKET
    enable_monthly: 是否启用月度轮动天王扫描
    """
    from pipelines.universe_provider import load_universe

    now = datetime.now(timezone(timedelta(hours=8)))
    uni = load_universe(source=universe, allow_fallback=allow_fallback,
                       min_count=4000 if universe=="A_SHARE_ALL" else None)
    is_global = uni.get("is_global", False)
    sig = "Z-G09_R-Matrix_v1.2" if is_global else "Z-G09_R-Matrix_non_global"

    result = {"pipeline_signature":sig,"timestamp":now.isoformat(),
              "engine":"R-Matrix v1.2 双周期","sections":{},"r_pool":[],
              "universe_contract":uni,"warnings":[]}

    if uni["status"] == "DATA_GAP":
        result["status"] = "DATA_GAP"
        result["reason"] = "UNIVERSE_NOT_AVAILABLE"
        return result
    if not is_global:
        result["warnings"].append("NON_GLOBAL_UNIVERSE")

    tickers = uni["tickers"]
    print(f"\n☯️ Z-G09 R-Matrix v1.2 — {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"    Universe: {uni['source']} {uni['count']}只 is_global={is_global}")
    print(f"    双周期: 波动天王(日线Type A/B) + 轮动天王(月线RISING/HORIZONTAL/DECLINING)")
    print("=" * 60)

    # ═══ 波动天王: 日线Type A/B ═══
    print(f"\n📡 [波动天王] 日线扫描: {len(tickers)}标的 → Type A水平震荡 + Type B上升通道")
    candidates = []; degraded = []
    for t in tickers:
        sc = _r_matrix_score(t)
        if not sc: continue
        if sc.get("excluded_from_ranking"):
            degraded.append(sc)
        else:
            candidates.append(sc)

    candidates.sort(key=lambda x: x.get("score",0), reverse=True)
    daily_pool = candidates[:pool_size]

    print(f"\n🏆 波动天王: {len(daily_pool)}/{len(tickers)}入选, {len(degraded)}数据不足")
    for i, c in enumerate(daily_pool[:10]):
        action_map = {"HARVEST":"🔴收割","WATCH":"🟡观察","WAIT":"⏳等待","PAPER_PROBE":"🟣试探"}
        act = action_map.get(c.get("allowed_action","?"),"❓")
        print(f"  {i+1:2d}. {c['ticker']} {c.get('name','?'):<8s} {c.get('score',0):.1f}分 {c.get('oscillation_type','?')} {act}")

    result["r_pool"] = daily_pool
    result["sections"]["daily_oscillation_king"] = {"scanned":len(tickers),"pool_size":len(daily_pool),"degraded":len(degraded)}

    # ═══ 轮动天王: 月线分类 ═══
    if enable_monthly:
        print(f"\n📡 [轮动天王] 月线扫描: {len(tickers)}标的 → RISING/HORIZONTAL/DECLINING")
        try:
            from pipelines.Z-G09_全局轮动筛选.rotation_scan import scan_monthly_rotation
            monthly = scan_monthly_rotation(tickers)
            # Build name map from daily candidates
            name_map = {c["ticker"]:c.get("name","?") for c in candidates + degraded if "ticker" in c}
            for m in monthly:
                if m["ticker"] in name_map:
                    m["name"] = name_map[m["ticker"]]

            types = {"RISING":0,"HORIZONTAL":0,"DECLINING":0,"DATA_INSUFFICIENT":0}
            for m in monthly:
                types[m["type"]] = types.get(m["type"],0) + 1
            print(f"  🔺RISING:{types['RISING']} ➖HORIZONTAL:{types['HORIZONTAL']} 🔻DECLINING:{types['DECLINING']}")

            result["sections"]["monthly_rotation_king"] = {
                "summary": types,
                "details": sorted(monthly, key=lambda x: x.get("beta_norm",0), reverse=True),
            }
        except Exception as e:
            print(f"  ⚠️ 轮动天王: {e}")
            result["sections"]["monthly_rotation_king"] = {"error": str(e)[:120]}

    result["sections"]["summary"] = {
        "daily_pool_size": len(daily_pool),
        "monthly_rising": types.get("RISING",0) if enable_monthly else 0,
        "monthly_horizontal": types.get("HORIZONTAL",0) if enable_monthly else 0,
        "monthly_declining": types.get("DECLINING",0) if enable_monthly else 0,
    }
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G09 R-Matrix v1.2 双周期轮动")
    p.add_argument("--pool", type=int, default=80)
    p.add_argument("--universe", default="A_SHARE_ALL",
                   choices=["A_SHARE_ALL","INDEX_300","INDEX_500","INDEX_1000","WATCHLIST","PRESET_DEV","FILE"])
    p.add_argument("--allow-fallback", action="store_true")
    p.add_argument("--no-monthly", action="store_true", help="跳过月线轮动天王")
    args = p.parse_args()
    run(pool_size=args.pool, universe=args.universe, allow_fallback=args.allow_fallback,
        enable_monthly=not args.no_monthly)
