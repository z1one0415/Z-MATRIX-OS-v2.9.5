"""Outcome Linker v3.2 — connect paper action to P2 outcome backfill"""
from __future__ import annotations
from zmatrix.brd_replay.forward_price_loader import load_forward_price_path
from zmatrix.paper_outcome.outcome_backfill_runner import run_outcome_backfill

def build_outcome_for_paper_action(*, paper_action, local_data_root, benchmark_code=None, max_horizon=60):
    if paper_action.get("paper_action") in ("NO_ACTION","DATA_GAP"):
        return {"paper_id":paper_action.get("paper_id"),"ticker":paper_action.get("ticker"),
                "outcome_status":"NO_ACTION","reason":paper_action.get("paper_action"),
                "real_trade_allowed":False,"broker_order_allowed":False}
    ticker = paper_action.get("ticker")
    entry_date = paper_action.get("entry_date") or paper_action.get("replay_date")
    path = load_forward_price_path(ticker=ticker,entry_date=entry_date,local_data_root=local_data_root,max_horizon=max_horizon)
    if path.get("status") != "READY":
        return {"paper_id":paper_action.get("paper_id"),"ticker":ticker,
                "outcome_status":"INSUFFICIENT_DATA","reason":path.get("status"),
                "real_trade_allowed":False,"broker_order_allowed":False}
    outcome = run_outcome_backfill(paper_entry=paper_action, price_path=path["price_path"])
    outcome["source_paper_action"] = {"paper_id":paper_action.get("paper_id"),
        "role":paper_action.get("role"),"paper_action":paper_action.get("paper_action"),
        "brd_score":paper_action.get("brd_score")}
    outcome["real_trade_allowed"] = False; outcome["broker_order_allowed"] = False
    return outcome
