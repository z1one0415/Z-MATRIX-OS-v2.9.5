# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.return_integrity.schema import DEFAULT_RETURN_INTEGRITY_SAFETY, RETURN_OUTLIER_THRESHOLDS

def classify_return_sanity(outcome: dict) -> dict:
    flags = []
    t5 = outcome.get("actual_return_t5")
    t20 = outcome.get("actual_return_t20")
    t60 = outcome.get("actual_return_t60")
    if t5 is not None and abs(float(t5)) > RETURN_OUTLIER_THRESHOLDS["t5_abs_pct"]:
        flags.append("T5_RETURN_OUTLIER")
    if t20 is not None and abs(float(t20)) > RETURN_OUTLIER_THRESHOLDS["t20_abs_pct"]:
        flags.append("T20_RETURN_OUTLIER")
    if t60 is not None and abs(float(t60)) > RETURN_OUTLIER_THRESHOLDS["t60_abs_pct"]:
        flags.append("T60_RETURN_OUTLIER")
    if outcome.get("outcome_status") != "READY":
        flags.append("OUTCOME_NOT_READY")
    return {"sanity_version": "RETURN_SANITY_GUARD_V10", "paper_id": outcome.get("paper_id"), "ticker": outcome.get("ticker"), "flags": flags, "is_outlier": any("OUTLIER" in x for x in flags), "is_usable_for_robust_metrics": outcome.get("outcome_status") == "READY", "safety": dict(DEFAULT_RETURN_INTEGRITY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
