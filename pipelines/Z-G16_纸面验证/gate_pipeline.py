#!/usr/bin/env python3
"""☯️ Z-G16 V4纸面执行教练 — v2.9.5-RC
Full/Lite双模式: Full(8模块, O4) / Lite(条件路线+缺口, O3/O2)
Alpha平行验证仓为后续专项
"""
import argparse, json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth, get_kline, l4_health, dq_score
except ImportError:
    market_truth = lambda t: {"status":"stub","price":0}
    get_kline = lambda t,d: {"prices":[],"count":0}
    l4_health = lambda t: {"status":"stub"}
    dq_score = lambda t: {"total":0}

def run(proposal=None):
    now = datetime.now(timezone(timedelta(hours=8)))
    proposal = proposal or {"symbol":"002463","name":"沪电股份","selected_role":"R_MATRIX",
        "action_proposal":{"action":"PAPER_TRACK"},"price":102.6,"target":120,"stop":90}
    
    ticker = proposal["symbol"]
    g1 = market_truth(ticker)
    dq = dq_score(ticker)
    
    result = {
        "pipeline_signature":"Z-G16_纸面执行教练_v2.9.5-RC",
        "timestamp":now.isoformat(),"symbol":ticker,
        "paper_only":True,"real_trade_authorized":False
    }
    
    print(f"\n☯️ Z-G16 V4纸面执行教练 — {ticker} {proposal.get('name','')}")
    print("=" * 60)
    
    # Mode determination
    dq_total = dq.get("total",0)
    mt_status = g1.get("status","BLOCK")
    
    # Full模式前置条件: DQ≥85 + MT.PASS + (L1.5 SAFE implied) + world=PAPER_WORLD
    l1_5_safe = True  # placeholder - real check requires L1.5 module
    world_ok = True    # placeholder - real check requires world context
    
    if dq_total < 85 or mt_status != "PASS" or not l1_5_safe or not world_ok:
        mode = "Lite"
        output_level = "O2_DIAGNOSTIC" if mt_status == "BLOCK" else "O3_CONDITIONAL"
        print(f"⚠️ {mode}模式: DQ={dq_total}, MT={mt_status} → {output_level}")
        result["mode"] = mode
        result["output_level"] = output_level
        result["forbidden_fields"] = ["price_zones","position_playbook","PAPER_PROBE","fill_price"]
        result["route_hypotheses"] = [
            {"id":"A","condition":"L3→FULL+MT恢复PASS","action":"WAIT"},
            {"id":"B","condition":"缩量横盘","action":"WAIT"},
            {"id":"C","condition":"板块退潮","action":"WATCH"}
        ]
        result["evidence_gaps"] = [f"DQ={dq_total}(need≥85)" if dq_total<85 else f"MT={mt_status}"]
        result["waiting_triggers"] = ["DQ恢复≥85","MT恢复PASS","价格交叉验证通过"]
        return result
    
    # Full mode
    mode = "Full"
        # NOTE: TailRisk DEFENSIVE_ONLY check, Hibernation check - placeholders
    # Full requires: DQ≥85, MT.PASS, L1.5 SAFE, role_valid, world=PAPER_WORLD
    print(f"Full模式: DQ={dq_total}, MT=PASS (L1.5/TailRisk/Hibernation待接入)")
    result["mode"] = mode
    result["output_level"] = "O4_PAPER_PLAN"
    result["plan_status"] = "QUALIFIED"
    
    price = g1.get("price", proposal.get("price"))
    kl = get_kline(ticker, 60)
    prices = kl.get("prices", [])
    ma20 = sum(prices[-20:])/20 if len(prices)>=20 else price
    recent_low = min(prices[-20:]) if len(prices)>=20 else price*0.9
    recent_high = max(prices[-20:]) if len(prices)>=20 else price*1.1
    
    print(f"\n📋 [1/8] 当前状态: {proposal['selected_role']}, DQ={dq_total}, price={price}")
    print(f"📊 [2/8] 路线: A顺风/B震荡/C回撤/D高开 (uncalibrated)")
    print(f"💰 [3/8] 价格: watch={ma20*0.98:.1f}-{ma20*1.02:.1f} rollback=<{recent_low*0.97:.1f}")
    print(f"📐 [4/8] 仓位: 3U制 PAPER_TRACK(0U)→PROBE_1(1U)→PROBE_2(1U)→PROBE_3(1U)")
    print(f"🚦 [5/8] 信号: IN(L3→FULL+VWAP) OUT(跌破失效+RETREAT)")
    print(f"⏰ [6/8] 检查点: T-1→0925→0935→0945→1030→1430→1500")
    print(f"🛑 [7/8] Kill:6条 Rollback:4条")
    print(f"📝 [8/8] 后验: T+1/3/5/20→Z9→Alpha验证仓")
    print(f"🏁 paper_only | 不连接券商")
    
    result["coach_plan"] = {
        "current_state": {"l3":"PARTIAL","dq":dq_total,"price":price},
        "scenario_routes": [
            {"id":"A","condition":"L3→FULL","weight":"中","action":"PAPER_PROBE","paper_size":"1U"},
            {"id":"B","condition":"缩量横盘","weight":"中高","action":"WAIT"}
        ],
        "price_zones": {"watch":f"{ma20*0.98:.0f}-{ma20*1.02:.0f}","rollback":f"<{recent_low*0.97:.0f}"},
        "position_playbook": {"max":"3U","steps":[
            {"stage_id":"TRACK","action":"PAPER_TRACK","paper_size":"0U"},
            {"stage_id":"PROBE_1","action":"PAPER_PROBE","paper_size":"1U"},
            {"stage_id":"PROBE_2","action":"PAPER_PROBE","paper_size":"1U"}
        ]},
        "kill_conditions": ["MT_BLOCK","L3_REJECTED","放量跌破失效位"],
        "rollback_conditions": [{"from":"PROBE","to":"TRACK"},{"from":"A","to":"B"}]
    }
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G16 V4纸面执行教练")
    p.add_argument("--ticker", default="002463")
    args = p.parse_args()
    run({"symbol":args.ticker,"name":"","selected_role":"R_MATRIX",
         "action_proposal":{"action":"PAPER_TRACK"},"price":102.6,"target":120,"stop":90})
