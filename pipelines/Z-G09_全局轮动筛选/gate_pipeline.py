#!/usr/bin/env python3
"""☯️ Z-G09 R-Matrix v2.0 — 四天王全周期轮动筛选

冲动天王(日线): Type A水平箱体 + Type B上升通道 — 日内超买超卖警报
波动天王(5日): BOX箱体震荡 — 周级低买高卖 (17% BOX optimal)
律动天王(周线): BOX/TREND — 中线摆动交易 (30% BOX)
轮动天王(双周): RISING/HORIZONTAL/DECLINING — 轮动选股entry (13% BOX, 3x月线)

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


def _read_positions():
    """读取MEMORY.md持仓 → {ticker: {shares, cost}}"""
    mem = WORKSPACE.parent / "MEMORY.md"
    if not mem.exists(): return {}
    import re
    pos = {}
    for m in re.finditer(r'\|\s*([^|]+?)\s+(\d{6})\s*\|\s*([\d,]+股)\s*\|\s*([\d.]+)\s*\|', open(mem).read()):
        code = m.group(2)
        shares = int(m.group(3).replace("股","").replace(",",""))
        cost = float(m.group(4))
        pos[code] = {"shares": shares, "cost": cost, "name": m.group(1).strip()}
    return pos

def _anchor_to_cost(ticker, channel_position, channel_type, action, positions, current_price=None):
    """成本锚定: 将绝对通道位置转化为相对成本的建议。
    
    Returns {action_anchored, cost_pct, rationale}
    """
    if ticker not in positions: return {"action_anchored": action, "cost_pct": None, "rationale": "无持仓"}
    
    pos = positions[ticker]
    cost = pos["cost"]
    price = current_price or (cost * (1 + channel_position * 0.3))  # fallback estimate
    
    cost_pct = round((price / cost - 1) * 100, 1)
    
    # 锚定逻辑:
    if cost_pct > 20:
        rationale = f"浮盈{cost_pct:+.1f}%, 通道{channel_position:.2f}, 建议部分止盈"
        action_anchored = "PARTIAL_HARVEST"
    elif cost_pct > 5:
        if channel_position > 0.75:
            rationale = f"浮盈{cost_pct:+.1f}%, 但通道偏高({channel_position:.2f}), 不加仓, 持有观察"
            action_anchored = "HOLD_PROFIT"
        else:
            rationale = f"浮盈{cost_pct:+.1f}%, 通道合理, 持有"
            action_anchored = "HOLD"
    elif cost_pct > -5:
        if channel_position < 0.35:
            rationale = f"成本附近({cost_pct:+.1f}%), 通道低位, 可考虑小加仓"
            action_anchored = "CONSIDER_ADD"
        else:
            rationale = f"成本附近({cost_pct:+.1f}%), 通道中位, 持有等待"
            action_anchored = "HOLD"
    elif cost_pct > -15:
        rationale = f"浮亏{cost_pct:+.1f}%, 通道{channel_position:.2f}, 不加仓不止损, 等反弹"
        action_anchored = "HOLD_LOSS"
    else:
        rationale = f"浮亏{cost_pct:+.1f}%, 深度亏损, 需评估是否止损"
        action_anchored = "REVIEW_STOP"
    
    return {"action_anchored": action_anchored, "cost_pct": cost_pct, "cost": cost, "shares": pos["shares"], "rationale": rationale}


KINGS = {
    "impulse":  {"name":"冲动天王","scale":"日线","window":500,"desc":"日内超买超卖"},
    "oscillation": {"name":"波动天王","scale":"5日线","window":50,"desc":"周级箱体低买高卖"},
    "rhythm":   {"name":"律动天王","scale":"周线","window":26,"desc":"中线摆动"},
    "rotation": {"name":"轮动天王","scale":"双周线","window":30,"desc":"轮动选股entry"},
}

def _impulse_score(ticker):
    """冲动天王: 日线 Type A/B"""
    g1 = market_truth(ticker); l4 = l4_health(ticker)
    if g1.get("status")=="BLOCK" or l4.get("status")=="BLOCK":
        return {"status":"BLOCKED","ticker":ticker}
    kl = get_kline(ticker, 500); prices = kl.get("prices",[])
    if len(prices) < 260:
        return {"status":"DATA_INSUFFICIENT","ticker":ticker}
    try:
        from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal, rank_type_b_rising_channel
        a = rank_type_a_horizontal(ticker, g1.get("name",""), prices)
        b = rank_type_b_rising_channel(ticker, g1.get("name",""), prices)
        best = a if a.score >= b.score else b
        return {"ticker":ticker,"name":g1.get("name","?"),"status":"PASS","score":best.score,
                "type":best.oscillation_type,"action":best.allowed_action}
    except Exception as e:
        return {"status":"ERROR","ticker":ticker,"error":str(e)[:80]}

# _rhythm_scan removed — use rotation_scan.py + rhythm_king_weekly.py instead

def run(pool_size=80, universe="A_SHARE_ALL", allow_fallback=True,
        kings_enabled="all"):
    """Z-G09 R-Matrix v2.0 — 四天王全周期

    kings_enabled: all | impulse_only | oscillation+rhythm | comma-separated
    """
    from pipelines.universe_provider import load_universe
    now = datetime.now(timezone(timedelta(hours=8)))
    uni = load_universe(source=universe, allow_fallback=allow_fallback,
                       min_count=4000 if universe=="A_SHARE_ALL" else None)
    is_global = uni.get("is_global",False)
    tickers = uni["tickers"]

    result = {"pipeline_signature":"Z-G09_R-Matrix_v2.0_四天王","timestamp":now.isoformat(),
              "universe_contract":uni,"sections":{},"warnings":[]}
    if uni["status"]=="DATA_GAP": result["status"]="DATA_GAP"; return result

    print(f"\n☯️ Z-G09 R-Matrix v2.0 四天王 — {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Universe: {uni['source']} {uni['count']}只")
    kings_list = kings_enabled.split(",") if kings_enabled!="all" else ["impulse","oscillation","rhythm","rotation"]
    print(f"   启用: {', '.join(KINGS[k]['name'] for k in kings_list if k in KINGS)}")
    print("="*60)

    # ═══ R-Matrix v2.0 unified service — single truth source ═══
    from zmatrix.scoring.r_matrix.r_matrix_service import evaluate_r_matrix_cycle
    positions = _read_positions()
    
    print(f"\n📡 R-Matrix v2.0: {len(tickers)}只 → 四天王周期扫描")
    
    resonance_pool = []
    for t in tickers:
        try:
            kl = get_kline(t, 500)
            prices = kl.get("prices", [])
            if len(prices) < 60:
                continue
            g1 = market_truth(t)
            pos_data = positions.get(t)
            if pos_data:
                pos_data = {"shares": pos_data["shares"], "cost": pos_data["cost"],
                            "price": g1.get("price", pos_data["cost"])}
            r = evaluate_r_matrix_cycle(t, prices=prices, position=pos_data)
            r["name"] = g1.get("name", "?")
            resonance_pool.append(r)
        except Exception as e:
            result["warnings"].append(f"{t}: {str(e)[:60]}")
    
    resonance_pool.sort(key=lambda x: (len(x.get("hard_blocks",[]))==0, x.get("r_score",0)), reverse=True)
    result["r_pool"] = resonance_pool[:pool_size]
    
    statuses = {"PASS":0,"DEGRADED":0,"DATA_GAP":0,"ERROR":0}
    for r in resonance_pool: statuses[r.get("status","?")] = statuses.get(r.get("status","?"),0)+1
    print(f"  PASS={statuses['PASS']} DEGRADED={statuses['DEGRADED']} DATA_GAP={statuses['DATA_GAP']}")
    print(f"  STRONG={sum(1 for r in resonance_pool if r.get('r_resonance_status')=='CYCLE_RESONANCE_STRONG')} BLOCKED={sum(1 for r in resonance_pool if r.get('hard_blocks'))}")
    
    result["sections"]["four_king_resonance"] = {
        "pool_size": len(result["r_pool"]),
        "scanned": len(tickers),
        "statuses": statuses,
    }
    
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G09 R-Matrix v2.0 四天王")
    p.add_argument("--pool",type=int,default=80)
    p.add_argument("--universe",default="A_SHARE_ALL")
    p.add_argument("--kings",default="all",help="impulse,oscillation,rhythm,rotation or all")
    args = p.parse_args()
    run(pool_size=args.pool,universe=args.universe,kings_enabled=args.kings)
