"""Paper Action Builder v3.2 — B/R/D result → paper action (no real trade)"""
from __future__ import annotations
import hashlib

_ROLE_ACTION_MAP = {"A_LONG_CORE":"PAPER_WATCH_CORE","B_MID_ROTATION":"PAPER_WATCH_ROTATION",
                     "C_SHORT_EVENT":"PAPER_WATCH_EVENT","D_REJECT":"NO_ACTION","UNKNOWN":"WATCH_ONLY"}

def build_paper_action_from_brd(*, replay_date, ticker, brd_result, price_snapshot, sector_phase=None):
    role = brd_result.get("role","UNKNOWN")
    hard_gate_passed = bool(brd_result.get("hard_gate_passed",False))
    entry_price = float(price_snapshot.get("close",0) or 0)
    paper_action = _ROLE_ACTION_MAP.get(role,"WATCH_ONLY")
    if not hard_gate_passed: paper_action = "NO_ACTION"
    if role == "D_REJECT": paper_action = "NO_ACTION"
    if entry_price <= 0: paper_action = "DATA_GAP"
    seed = f"{replay_date}|{ticker}|{role}|{paper_action}"
    paper_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    h = 60 if role=="A_LONG_CORE" else (20 if role=="B_MID_ROTATION" else 5)
    return {"paper_action_version":"BRD_PAPER_ACTION_V10","mode":"PAPER_ONLY",
            "paper_id":paper_id,"replay_date":replay_date,"entry_date":replay_date,
            "ticker":ticker,"role":role,"paper_action":paper_action,
            "entry_price":entry_price,"target_horizon":h,
            "brd_score":float(brd_result.get("brd_score",0)or 0),
            "hard_gate_passed":hard_gate_passed,"max_loss_plan":12.0 if role=="A_LONG_CORE" else (8.0 if role=="B_MID_ROTATION" else 5.0),
            "source_brd_result":brd_result,"real_trade_allowed":False,"broker_order_allowed":False,
            "auto_buy_allowed":False,"auto_sell_allowed":False}
