# allowlist: forbidden-token-definition
from __future__ import annotations
import json
from pathlib import Path
from zmatrix.entry_quality_repair.schema import DEFAULT_ENTRY_REPAIR_SAFETY

def load_entry_repair_dataset(*, replay_path: str = "runtime_reports/v35_brd_strategy_replay_result.json", role_filter: str = "B_MID_ROTATION") -> dict:
    path = Path(replay_path)
    if not path.exists(): return {"dataset_status":"BLOCKED_REPLAY_RESULT_MISSING","joined":[],"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_ENTRY_REPAIR_SAFETY)}
    replay = json.loads(path.read_text(encoding="utf-8"))
    actions, outcomes = [], []
    for daily in replay.get("daily_results",[]):
        actions.extend(daily.get("paper_actions",[]))
        outcomes.extend(daily.get("outcomes",[]))
    outcome_by_id = {o.get("paper_id"): o for o in outcomes}
    joined = []
    for a in actions:
        if a.get("role") != role_filter: continue
        if a.get("paper_action") in ("NO_ACTION","DATA_GAP",None): continue
        pid = a.get("paper_id"); o = outcome_by_id.get(pid,{})
        if o.get("outcome_status") != "READY": continue
        joined.append({"paper_id":pid,"ticker":a.get("ticker"),"role":a.get("role"),"paper_action":a.get("paper_action"),"entry_date":a.get("entry_date") or a.get("replay_date"),"entry_price":a.get("entry_price"),"sector_phase":a.get("sector_phase"),"source_brd_result":a.get("source_brd_result",{}),"actual_return_t5":o.get("actual_return_t5"),"actual_return_t20":o.get("actual_return_t20"),"actual_return_t60":o.get("actual_return_t60"),"invalidation_triggered":o.get("invalidation_triggered"),"max_adverse_excursion_pct":o.get("max_adverse_excursion_pct")})
    return {"dataset_version":"V355_ENTRY_REPAIR_DATASET_V10","dataset_status":"READY" if joined else "BLOCKED_EMPTY_B_ROTATION","role_filter":role_filter,"joined_count":len(joined),"joined":joined,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_ENTRY_REPAIR_SAFETY)}
