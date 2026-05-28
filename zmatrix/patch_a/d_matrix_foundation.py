"""PATCH-A-4: D-Matrix Data Foundation — 事件+价量+资金+涨停+热度+可交易性六层事实"""
from __future__ import annotations

D_MATRIX_SCORING = {"event_catalyst":{"weight":25,"fields":["event_evidence_level","event_recency_hours","catalyst_strength"]},"price_volume_anomaly":{"weight":25,"fields":["return_1d","return_3d","return_5d","volume_ratio_5d","turnover_rate","amplitude","volatility_expansion"]},"fund_flow_lhb":{"weight":20,"fields":["main_net_inflow","large_order_net_inflow","lhb_buy_amount","lhb_sell_amount"]},"theme_resonance":{"weight":15,"fields":["theme_heat_score","theme_rank_change","sector_momentum","concept_board_strength"]},"tradability":{"weight":10,"fields":["tradability_status","limit_up_flag","limit_down_flag","consecutive_limit_up_count","suspension_flag"]},"risk_penalty":{"weight":5,"fields":["rumor_risk","failed_limit_up_flag","one_price_board_flag","liquidity_capacity_status"]}}

D_EVENT_EVIDENCE_LEVELS = {"A":{"description":"官方公告/财报/交易所披露","allowed_for_hunt":True,"weight":1.0},"B":{"description":"权威媒体/产业链实锤","allowed_for_hunt":True,"weight":0.8},"C":{"description":"普通媒体/机构解读","allowed_for_hunt":True,"weight":0.5},"D":{"description":"社媒传闻/题材炒作","allowed_for_hunt":False,"weight":0.0}}

D_HARD_GATES = {"suspension":{"action":"BLOCK","reason":"停牌"},"st_flag":{"action":"BLOCK","reason":"ST风险"},"one_price_board_buy":{"action":"WATCH_ONLY","reason":"一字涨停买不进"},"one_price_board_sell":{"action":"BLOCK","reason":"一字跌停卖不出"},"extreme_volume_shrink":{"action":"BLOCK","reason":"连续极端缩量"},"liquidity_insufficient":{"action":"BLOCK","reason":"流动性不足"},"event_evidence_d":{"action":"WATCH_ONLY","reason":"事件证据D级"}}

def score_d_matrix(*, event_facts: dict, price_facts: dict, flow_facts: dict, theme_facts: dict, tradability_facts: dict) -> dict:
    all_facts = {**event_facts, **price_facts, **flow_facts, **theme_facts, **tradability_facts}
    scores = {}; reasons = []; risk_flags = []; total = 0
    for module, cfg in D_MATRIX_SCORING.items():
        ms = 0; mc = 0
        for f in cfg["fields"]:
            v = all_facts.get(f)
            if v is not None: ms += _d_field_score(f, v); mc += 1
        w = cfg["weight"]
        raw = ms / max(1, mc) if mc > 0 else 0
        scores[module] = {"raw_score": raw, "weighted_score": raw * w / 100, "fields_available": mc}
        total += raw * w / 100

    tradable = _check_tradability(tradability_facts, event_facts, risk_flags)
    resonance = _check_resonance(scores)
    event_level = event_facts.get("event_evidence_level", "D")
    d_score = round(total, 1)
    eligible = d_score >= 80 and tradable and resonance and D_EVENT_EVIDENCE_LEVELS.get(event_level, {}).get("allowed_for_hunt", False)
    return {"status":"PASS" if eligible else "DATA_INSUFFICIENT" if d_score < 50 else "FAIL","short_event_eligible":eligible,"d_score":d_score,"event_score":scores.get("event_catalyst",{}).get("raw_score"),"price_volume_score":scores.get("price_volume_anomaly",{}).get("raw_score"),"fund_flow_score":scores.get("fund_flow_lhb",{}).get("raw_score"),"theme_heat_score":scores.get("theme_resonance",{}).get("raw_score"),"tradability_status":"TRADABLE" if tradable else "BLOCKED","risk_flags":risk_flags,"reason_codes":reasons,"pit_safe":True}

def _d_field_score(field, value):
    try: v = float(value) if not isinstance(value, str) else 0
    except: v = 0
    if field in ("event_evidence_level",): return D_EVENT_EVIDENCE_LEVELS.get(str(value),{}).get("weight",0) * 100
    if field in ("return_1d","return_3d","return_5d"): return min(100, max(0, 50 + v * 5))
    if field in ("volume_ratio_5d",): return min(100, max(0, v * 50))
    if field in ("turnover_rate",): return min(100, max(0, v * 5))
    if field in ("amplitude","volatility_expansion"): return min(100, max(0, v * 10))
    if field in ("main_net_inflow","large_order_net_inflow","lhb_buy_amount"): return min(100, max(0, 50 + v * 0.1))
    if field in ("theme_heat_score","sector_momentum","concept_board_strength"): return min(100, max(0, v))
    if field in ("tradability_status",): return 100 if str(value) == "TRADABLE" else 0
    if field in ("limit_up_flag","limit_down_flag","suspension_flag","one_price_board_flag"): return 0 if value else 100
    if field in ("rumor_risk","failed_limit_up_flag"): return -20 if value else 0
    if field in ("liquidity_capacity_status",): return 100 if str(value) == "ADEQUATE" else 0
    return 50

def _check_tradability(tradability, event, risk_flags):
    if tradability.get("suspension_flag"): risk_flags.append("SUSPENSION"); return False
    if tradability.get("limit_up_flag") and tradability.get("one_price_board_flag"): risk_flags.append("ONE_PRICE_BOARD_BUY"); return False
    if tradability.get("limit_down_flag"): risk_flags.append("LIMIT_DOWN"); return False
    if tradability.get("liquidity_capacity_status") == "INSUFFICIENT": risk_flags.append("LIQUIDITY_INSUFFICIENT"); return False
    if event.get("event_evidence_level") == "D": risk_flags.append("EVENT_EVIDENCE_D"); return False
    return True

def _check_resonance(scores):
    active = sum(1 for m, s in scores.items() if s.get("raw_score", 0) >= 50 and m != "risk_penalty")
    return active >= 2
