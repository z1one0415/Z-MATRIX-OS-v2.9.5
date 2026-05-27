from __future__ import annotations
import json
from pathlib import Path
from zmatrix.paper_repair_replay.schema import DEFAULT_REPAIR_REPLAY_SAFETY

def load_paper_repair_dataset(*, replay_path: str = "runtime_reports/v35_brd_strategy_replay_result.json") -> dict:
    path = Path(replay_path)
    if not path.exists():
        return {"dataset_status": "BLOCKED_REPLAY_DATA_MISSING", "paper_actions": [], "outcomes": [], "joined": [], "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
    replay = json.loads(path.read_text(encoding="utf-8"))
    actions, outcomes = [], []
    for daily in replay.get("daily_results", []):
        actions.extend(daily.get("paper_actions", []))
        outcomes.extend(daily.get("outcomes", []))
    outcome_by_id = {o.get("paper_id"): o for o in outcomes}
    joined = []
    for a in actions:
        pid = a.get("paper_id"); o = outcome_by_id.get(pid, {})
        if a.get("paper_action") in ("NO_ACTION", "DATA_GAP", None): continue
        joined.append({"paper_id": pid, "ticker": a.get("ticker"), "role": a.get("role"), "paper_action": a.get("paper_action"), "entry_date": a.get("entry_date") or a.get("replay_date"), "entry_price": a.get("entry_price"), "max_loss_plan": a.get("max_loss_plan"), "invalidation_condition": a.get("invalidation_condition"), "source_brd_result": a.get("source_brd_result", {}), "baseline_outcome_status": o.get("outcome_status"), "baseline_return_t5": o.get("actual_return_t5"), "baseline_return_t20": o.get("actual_return_t20"), "baseline_return_t60": o.get("actual_return_t60"), "baseline_invalidation_triggered": o.get("invalidation_triggered"), "baseline_max_adverse_excursion_pct": o.get("max_adverse_excursion_pct")})
    return {"dataset_version": "V353_PAPER_REPAIR_DATASET_V10", "dataset_status": "READY" if joined else "BLOCKED_NO_REPAIRABLE_ACTIONS", "paper_action_count": len(actions), "outcome_count": len(outcomes), "repairable_count": len(joined), "joined": joined, "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
