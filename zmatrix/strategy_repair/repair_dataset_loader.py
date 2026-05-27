from __future__ import annotations
import json
from pathlib import Path
from zmatrix.strategy_repair.schema import DEFAULT_REPAIR_SAFETY

def load_repair_dataset(*, replay_path: str = "runtime_reports/v35_brd_strategy_replay_result.json") -> dict:
    path = Path(replay_path)
    if not path.exists():
        return {"dataset_status": "BLOCKED_REPLAY_RESULT_MISSING", "paper_actions": [], "outcomes": [], "joined": [], "safety": dict(DEFAULT_REPAIR_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
    replay = json.loads(path.read_text(encoding="utf-8"))
    paper_actions, outcomes = [], []
    for daily in replay.get("daily_results", []):
        paper_actions.extend(daily.get("paper_actions", []))
        outcomes.extend(daily.get("outcomes", []))
    outcome_by_id = {o.get("paper_id"): o for o in outcomes}
    joined = []
    for a in paper_actions:
        pid = a.get("paper_id")
        o = outcome_by_id.get(pid, {})
        joined.append({"paper_id": pid, "ticker": a.get("ticker"), "role": a.get("role"), "paper_action": a.get("paper_action"), "entry_date": a.get("entry_date") or a.get("replay_date"), "sector_phase": a.get("sector_phase"), "source_brd_result": a.get("source_brd_result", {}), "outcome_status": o.get("outcome_status"), "actual_return_t5": o.get("actual_return_t5"), "actual_return_t20": o.get("actual_return_t20"), "actual_return_t60": o.get("actual_return_t60"), "max_adverse_excursion_pct": o.get("max_adverse_excursion_pct"), "invalidation_triggered": o.get("invalidation_triggered")})
    return {"dataset_version": "V352_REPAIR_DATASET_V10", "dataset_status": "READY" if joined else "BLOCKED_EMPTY_DATASET", "paper_action_count": len(paper_actions), "outcome_count": len(outcomes), "joined_count": len(joined), "paper_actions": paper_actions, "outcomes": outcomes, "joined": joined, "safety": dict(DEFAULT_REPAIR_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
