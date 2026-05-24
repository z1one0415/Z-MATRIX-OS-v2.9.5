"""G18 Paper Execution Record v1.0 — build auditable, reviewable, Z9-ready paper records.

No real trade actions allowed. Z9 hooks present but never real write.
"""
from __future__ import annotations
from datetime import datetime
from zmatrix.action.action_contracts import assert_no_real_trade


def _get(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def build_paper_execution_record(prediction, *, run_id: str | None = None) -> dict:
    """Build a paper execution record from a G18 prediction object."""

    fd = _get(prediction, "final_decision", {}) or {}
    conflicts = fd.get("conflicts", [])
    conflict_codes = [c["code"] for c in conflicts]
    paper_action = fd.get("paper_action")
    entry = fd.get("entry_intent", "WAIT")

    record = {
        "record_version": "v1.0",
        "record_type": "PAPER_EXECUTION_RECORD",
        "run_id": run_id or datetime.now().strftime("%Y%m%d_%H%M%S"),
        "ticker": _get(prediction, "ticker"),
        "name": _get(prediction, "name", ""),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prediction": {
            "probability": _get(prediction, "probability"),
            "horizon": _get(prediction, "horizon", {}),
            "action_proposal": _get(prediction, "action_proposal", "WAIT"),
            "confidence": _get(prediction, "confidence", "LOW"),
        },
        "final_decision": fd,
        "upstream_evidence_available": _get(prediction, "upstream_evidence", {}).get("evidence_available", {}),
        "missing_sources": _get(prediction, "upstream_evidence", {}).get("missing_sources", []),
        "conflict_summary": {
            "has_conflict": fd.get("conflict_resolution", {}).get("has_conflict", False),
            "conflict_level": fd.get("conflict_resolution", {}).get("conflict_level", "NONE"),
            "conflict_codes": conflict_codes,
        },
        "paper_execution": {
            "allowed": paper_action is not None,
            "paper_action": paper_action,
            "entry_intent": entry,
            "exit_intent": fd.get("exit_intent"),
            "action_cap": fd.get("action_cap", "WAIT"),
            "required_confirmations": fd.get("required_confirmations", []),
        },
        "z9_calibration_hooks": {
            "needs_future_review": True,
            "review_horizons": ["T1", "T5", "T20"],
            "expected_fields": ["actual_return_T1", "actual_return_T5", "actual_return_T20", "decision_outcome"],
        },
        "forbidden_real_trade_checked": True,
    }

    # Forbidden real trade actions
    assert_no_real_trade(record["paper_execution"]["entry_intent"])
    if record["paper_execution"]["exit_intent"]:
        assert_no_real_trade(record["paper_execution"]["exit_intent"])
    for bad in ["BUY", "SELL", "AUTO_TRADE", "MARKET_ORDER"]:
        assert bad not in str(record), f"record leaked {bad}"

    return record
