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

    # ── Load rotation scan (before all kings) ──
    import importlib.util
    spec = importlib.util.spec_from_file_location("rotscan",
        str(Path(__file__).parent / "rotation_scan.py"))
    rotscan = importlib.util.module_from_spec(spec); spec.loader.exec_module(rotscan)

    # ═══ 冲动天王: 日线 Type A/B ═══
    if "impulse" in kings_list:
        print(f"\n⚡ [冲动天王] {KINGS['impulse']['desc']} | {len(tickers)}只")
        imp = rotscan.scan_impulse_king(tickers)
        daily = sorted(imp, key=lambda x: x.get("score",0), reverse=True)[:pool_size]
        print(f"  入选: {len(daily)}只 (TypeA={sum(1 for c in daily if 'HORIZONTAL' in str(c.get('type','')))} TypeB={sum(1 for c in daily if 'RISING' in str(c.get('type','')))})")
        result["sections"]["impulse_king"] = {"pool":daily,"scanned":len(tickers),"pool_size":len(daily)}

    # ═══ 波动/律动/轮动: via rotation_scan + rhythm_king_weekly ═══
    for king_key in ["oscillation","rhythm","rotation"]:
        if king_key not in kings_list: continue
        cfg = KINGS[king_key]
        print(f"\n📡 [{cfg['name']}] {cfg['desc']} | {cfg['scale']} window={cfg['window']} | {len(tickers)}只")
        try:
            if king_key == "oscillation":
                r = rotscan.scan_oscillation_king(tickers)
            elif king_key == "rhythm":
                r = rotscan.scan_rhythm_king(tickers)
            else:
                r = rotscan.scan_rotation_king(tickers)

            box = [x for x in r if x["type"]=="BOX"]
            up = [x for x in r if x["type"]=="TREND_UP"]
            down = [x for x in r if x["type"]=="TREND_DOWN"]
            entries = [x for x in r if x["position"]<0.35]
            
            print(f"  BOX={len(box)}({len(box)*100//max(len(r),1)}%) UP={len(up)} DOWN={len(down)} ENTRY={len(entries)}")
            if entries:
                tops = sorted(entries,key=lambda x:x["position"])[:4]
                print(f"  🟢entry: "+", ".join(f"{x['ticker']}({x['position']:.2f})" for x in tops))
            
            result["sections"][f"{king_key}_king"] = {"summary":{"BOX":len(box),"UP":len(up),"DOWN":len(down),"ENTRY":len(entries)},"details":r}
        except Exception as e:
            result["sections"][f"{king_key}_king"] = {"error":str(e)[:120]}

    # ═══ 四王共振 + r_pool ═══
    from zmatrix.scoring.r_matrix.cycle_four_king_resonance import evaluate_cycle_four_king
    per_ticker = {}
    for king_key in ["impulse","oscillation","rhythm","rotation"]:
        section = result["sections"].get(f"{king_key}_king", {})
        details = section.get("details", section.get("pool", []))
        for d in details:
            t = d.get("ticker","")
            if t not in per_ticker: per_ticker[t] = {}
            per_ticker[t][king_key] = d
    
    resonance_pool = []
    for ticker, kings in per_ticker.items():
        r = evaluate_cycle_four_king(
            kings.get("impulse"), kings.get("oscillation"),
            kings.get("rhythm"), kings.get("rotation"))
        r["ticker"] = ticker
        # Anchor to portfolio positions
        # Cost-anchored sell decision
        pos_data = _read_positions()
        r["cost_anchor"] = _anchor_to_cost(ticker, r.get("rhythm",{}).get("position",0.5) if r.get("rhythm") else 0.5,
                                           r.get("rhythm",{}).get("type","?"), r["entry_action_cap"], pos_data)
        if ticker in pos_data:
            from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision
            p = pos_data[ticker]
            price = market_truth(ticker).get("price") or p["cost"]
            r["sell_decision"] = evaluate_position_sell_decision(
                ticker=ticker, shares=p["shares"], cost=p["cost"], current_price=price, resonance=r)
        else:
            r["sell_decision"] = {"position_action":"NO_POSITION","sell_ratio":0,"reason_codes":["NO_HOLDING"]}
        resonance_pool.append(r)
    
    resonance_pool.sort(key=lambda x: (len(x["hard_blocks"])==0, x["resonance_score"]), reverse=True)
    result["r_pool"] = resonance_pool[:pool_size]
    result["sections"]["four_king_resonance"] = {
        "pool_size": len(result["r_pool"]),
        "scanned": len(tickers),
        "resonance_strong": sum(1 for r in resonance_pool if r["resonance_status"]=="CYCLE_RESONANCE_STRONG"),
        "blocked": sum(1 for r in resonance_pool if r["hard_blocks"]),
    }
    
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G09 R-Matrix v2.0 四天王")
    p.add_argument("--pool",type=int,default=80)
    p.add_argument("--universe",default="A_SHARE_ALL")
    p.add_argument("--kings",default="all",help="impulse,oscillation,rhythm,rotation or all")
    args = p.parse_args()
    run(pool_size=args.pool,universe=args.universe,kings_enabled=args.kings)
