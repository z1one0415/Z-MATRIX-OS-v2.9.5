from __future__ import annotations
from zmatrix.return_integrity.return_sanity_guard import classify_return_sanity

def build_outlier_attribution(*, outcomes: list[dict], paper_actions: list[dict], horizon: str = "t20", top_n: int = 30) -> dict:
    key = f"actual_return_{horizon.lower()}"
    action_by_id = {a.get("paper_id"): a for a in paper_actions or []}
    ready = [o for o in outcomes or [] if o.get("outcome_status") == "READY" and o.get(key) is not None]
    ranked = sorted(ready, key=lambda x: float(x.get(key)), reverse=True)
    winners = ranked[:top_n]
    losers = list(reversed(ranked[-top_n:]))

    def enrich(o):
        action = action_by_id.get(o.get("paper_id"), {})
        return {"paper_id": o.get("paper_id"), "ticker": o.get("ticker") or action.get("ticker"), "role": action.get("role"), "paper_action": action.get("paper_action"), "entry_date": action.get("entry_date"), "return": o.get(key), "actual_return_t5": o.get("actual_return_t5"), "actual_return_t20": o.get("actual_return_t20"), "actual_return_t60": o.get("actual_return_t60"), "max_adverse_excursion_pct": o.get("max_adverse_excursion_pct"), "invalidation_triggered": o.get("invalidation_triggered"), "sanity": classify_return_sanity(o)}

    return {"attribution_version": "OUTLIER_ATTRIBUTION_V10", "horizon": horizon.upper(), "top_winners": [enrich(o) for o in winners], "top_losers": [enrich(o) for o in losers], "real_trade_allowed": False, "broker_order_allowed": False}
