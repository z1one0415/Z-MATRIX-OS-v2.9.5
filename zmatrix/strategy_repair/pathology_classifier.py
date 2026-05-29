# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.strategy_repair.schema import DEFAULT_REPAIR_SAFETY

def classify_sample_pathology(*, sample: dict, horizon: str = "t20") -> dict:
    key = f"actual_return_{horizon.lower()}"
    ret = sample.get(key)
    role = sample.get("role")
    action = sample.get("paper_action")
    mae = sample.get("max_adverse_excursion_pct")
    invalidated = sample.get("invalidation_triggered") is True
    tags = []
    if action in ("NO_ACTION", "DATA_GAP", None):
        tags.append("NO_ACTION")
    if sample.get("outcome_status") == "READY" and action not in ("NO_ACTION", "DATA_GAP", None):
        tags.append("READY_ACTIVE")
    if ret is not None:
        r = float(ret)
        if r < 0: tags.append("NEGATIVE_RETURN")
        if r > 120: tags.append("EXTREME_RIGHT_TAIL")
        if r < -50: tags.append("EXTREME_LEFT_TAIL")
    if invalidated: tags.append("INVALIDATED")
    if mae is not None and float(mae) < -10: tags.append("HIGH_MAE")
    if role == "B_MID_ROTATION" and ret is not None and float(ret) < 0: tags.append("B_ROTATION_LOSER")
    return {"pathology_version": "V352_SAMPLE_PATHOLOGY_V10", "paper_id": sample.get("paper_id"), "ticker": sample.get("ticker"), "role": role, "paper_action": action, "return": ret, "tags": tags, "safety": dict(DEFAULT_REPAIR_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}

def classify_dataset_pathology(*, joined: list[dict], horizon: str = "t20") -> dict:
    rows = [classify_sample_pathology(sample=x, horizon=horizon) for x in joined or []]
    tag_counts = {}
    for r in rows:
        for t in r.get("tags", []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    return {"pathology_report_version": "V352_PATHOLOGY_REPORT_V10", "sample_count": len(rows), "tag_counts": tag_counts, "rows": rows[:200], "real_trade_allowed": False, "broker_order_allowed": False}
