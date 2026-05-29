# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.paper_repair_replay.invalidation_rule_extractor import extract_invalidation_rule
from zmatrix.paper_repair_replay.price_path_replay import load_price_path_with_dates
from zmatrix.paper_repair_replay.invalidation_exit_simulator import simulate_invalidation_exit
from zmatrix.paper_repair_replay.schema import DEFAULT_REPAIR_REPLAY_SAFETY

def build_repaired_outcomes(*, joined: list[dict], data_root: str = ".", horizon_days: int = 20, max_items: int | None = None) -> dict:
    rows = []
    items = joined[:max_items] if max_items else joined
    for action in items:
        rule = extract_invalidation_rule(action=action)
        path = load_price_path_with_dates(ticker=action.get("ticker"), entry_date=action.get("entry_date"), data_root=data_root, max_days=max(80, horizon_days + 5))
        sim = simulate_invalidation_exit(action=action, price_path=path, rule=rule, horizon_days=horizon_days)
        rows.append({"paper_id": action.get("paper_id"), "ticker": action.get("ticker"), "role": action.get("role"), "baseline_return_t20": action.get("baseline_return_t20"), "baseline_invalidation_triggered": action.get("baseline_invalidation_triggered"), "rule": rule, "price_path_status": path.get("path_status"), "simulation": sim})
    ready = [r for r in rows if r.get("simulation", {}).get("simulation_status") == "READY"]
    return {"repaired_outcomes_version": "V353_REPAIRED_OUTCOMES_V10", "input_count": len(items), "ready_count": len(ready), "ready_rate": len(ready) / len(items) if items else None, "rows": rows, "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
