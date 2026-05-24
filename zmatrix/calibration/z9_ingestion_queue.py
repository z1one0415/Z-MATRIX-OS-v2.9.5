"""Z9 Ingestion Queue v1.0 — contract freeze only, no real DB write."""
from __future__ import annotations
from datetime import datetime
import hashlib

ALLOWED_STATUSES = ["PENDING_REVIEW", "WAITING_MARKET_DATA", "READY_FOR_REVIEW", "REJECTED"]
_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}


def make_z9_queue_idempotency_key(sample: dict) -> str:
    raw = str(sample.get("sample_id", "")) + str(sample.get("ticker", "")) + \
          str(sample.get("sample_version", "")) + str(sample.get("source_record", {}).get("record_ref", ""))
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def _get(obj, key, default=None):
    if isinstance(obj, dict): return obj.get(key, default)
    return getattr(obj, key, default)


def build_z9_ingestion_queue_item(sample: dict, *, queue_id: str | None = None, enqueue_run_id: str | None = None) -> dict:
    queue_id = queue_id or f"Q_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    enqueue_run_id = enqueue_run_id or datetime.now().strftime('%Y%m%d_%H%M%S')
    sample_id = sample.get("sample_id", "UNKNOWN")
    ticker = sample.get("ticker", "UNKNOWN")

    # Forbidden check on action fields only
    ds = sample.get("decision_snapshot", {}) or {}
    for fld in [ds.get("entry_intent"), ds.get("exit_intent"), ds.get("paper_action"), ds.get("action_cap")]:
        if fld and fld in _FORBIDDEN:
            raise ValueError(f"forbidden real trade in queue item: {fld}")

    # Validation
    reject_reasons = []
    if not sample.get("sample_id"): reject_reasons.append("MISSING_REQUIRED_FIELD:sample_id")
    if not sample.get("ticker"): reject_reasons.append("MISSING_REQUIRED_FIELD:ticker")
    if not sample.get("source_record"): reject_reasons.append("MISSING_REQUIRED_FIELD:source_record")

    # Status resolution
    status = "PENDING_REVIEW"
    if reject_reasons:
        status = "REJECTED"
    else:
        review_status = (sample.get("outcome_placeholder") or {}).get("review_status")
        if review_status == "WAITING_FOR_FUTURE_MARKET_DATA":
            status = "WAITING_MARKET_DATA"

    # source_record_ref from nested source_record
    source_record = sample.get("source_record") or {}
    source_record_ref = source_record.get("record_ref", "")

    return {
        "queue_version": "v1.0",
        "queue_type": "Z9_INGESTION_QUEUE_ITEM",
        "queue_id": queue_id,
        "sample_id": sample_id,
        "run_id": enqueue_run_id,
        "ticker": ticker,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "idempotency": {
            "idempotency_key": make_z9_queue_idempotency_key(sample),
            "dedup_key": f"{ticker}_{sample_id}",
            "source_sample_id": sample_id,
            "source_record_ref": source_record_ref,
            "same_sample_reenqueue_allowed": False,
        },
        "state": {"status": status, "allowed_statuses": ALLOWED_STATUSES, "reason": "D2_QUEUE_CONTRACT_ONLY_NO_REAL_WRITE" if not reject_reasons else "; ".join(reject_reasons)},
        "sample_snapshot": {
            "sample_version": sample.get("sample_version"),
            "sample_type": sample.get("sample_type"),
            "ticker": ticker,
            "review_plan": sample.get("review_plan", {}),
            "outcome_placeholder": sample.get("outcome_placeholder", {}),
            "calibration_hooks": sample.get("calibration_hooks", {}),
        },
        "validation": {"sample_valid": not reject_reasons, "reject_reasons": reject_reasons,
                       "requires_future_outcome": True, "ready_for_real_ingestion": False},
        "write_policy": {"queue_write_allowed": False, "z9_write_allowed": False,
                         "write_status": "DEFERRED_NOT_CONNECTED", "reason": "D2_QUEUE_CONTRACT_ONLY_NO_REAL_WRITE"},
        "forbidden_real_trade_checked": True,
    }
