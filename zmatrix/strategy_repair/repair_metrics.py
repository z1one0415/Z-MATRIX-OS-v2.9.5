from __future__ import annotations
from zmatrix.return_integrity.robust_metrics import build_robust_return_metrics

def build_repair_metrics(*, joined: list[dict], horizon: str = "t20") -> dict:
    outcomes = []
    key = f"actual_return_{horizon.lower()}"
    for x in joined or []:
        outcomes.append({"paper_id": x.get("paper_id"), "ticker": x.get("ticker"), "outcome_status": x.get("outcome_status"), key: x.get(key), "actual_return_t5": x.get("actual_return_t5"), "actual_return_t20": x.get("actual_return_t20"), "actual_return_t60": x.get("actual_return_t60")})
    return build_robust_return_metrics(outcomes=outcomes, horizon=horizon)
