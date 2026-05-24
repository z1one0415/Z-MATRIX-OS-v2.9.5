"""Z9 Calibration Sample v1.0 — contract freeze only, no real Z9 write."""
from __future__ import annotations
from datetime import datetime
from typing import Any

_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}


def build_z9_calibration_sample(paper_record: dict, *, run_id: str | None = None, sample_id: str | None = None) -> dict:
    sample_id = sample_id or f"Z9S_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_id = run_id or datetime.now().strftime('%Y%m%d_%H%M%S')
    pe = paper_record.get("paper_execution", {}) or {}
    fd = paper_record.get("final_decision", {}) or {}
    cs = paper_record.get("conflict_summary", {}) or {}
    uea = paper_record.get("upstream_evidence_available", {}) or {}
    ms = paper_record.get("missing_sources", []) or []

    # Forbidden real trade check on execution fields only (no str(record) scan)
    for fld in [pe.get("entry_intent"), pe.get("exit_intent"), pe.get("paper_action"),
                pe.get("action_cap"), fd.get("entry_intent"), fd.get("exit_intent"),
                fd.get("paper_action"), fd.get("action_cap")]:
        if fld and fld in _FORBIDDEN:
            raise ValueError(f"forbidden real trade in z9 sample: {fld}")

    return {
        "sample_version": "v1.0",
        "sample_type": "Z9_CALIBRATION_SAMPLE",
        "sample_id": sample_id,
        "run_id": run_id,
        "ticker": paper_record.get("ticker", ""),
        "name": paper_record.get("name", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_record": {"record_version": paper_record.get("record_version"), "record_type": paper_record.get("record_type"), "record_ref": sample_id},
        "prediction_snapshot": paper_record.get("prediction", {}),
        "decision_snapshot": {"entry_intent": pe.get("entry_intent"), "exit_intent": pe.get("exit_intent"),
                              "paper_action": pe.get("paper_action"), "action_cap": pe.get("action_cap"),
                              "required_confirmations": pe.get("required_confirmations", []),
                              "blocking_reasons": fd.get("blocking_reasons", []),
                              "risk_warnings": fd.get("risk_warnings", [])},
        "evidence_snapshot": {"upstream_evidence_available": uea, "missing_sources": ms,
                              "conflict_summary": {"has_conflict": cs.get("has_conflict"), "conflict_level": cs.get("conflict_level"),
                                                   "conflict_codes": cs.get("conflict_codes", [])}},
        "review_plan": {"needs_future_review": True, "review_horizons": ["T1", "T5", "T20"],
                        "expected_fields": ["actual_return_T1","actual_return_T5","actual_return_T20",
                                            "max_drawdown_T5","max_drawdown_T20","decision_outcome",
                                            "rule_hit_accuracy","false_positive_flags","false_negative_flags"]},
        "outcome_placeholder": {"actual_return_T1": None, "actual_return_T5": None, "actual_return_T20": None,
                                "max_drawdown_T5": None, "max_drawdown_T20": None, "decision_outcome": "PENDING_REVIEW",
                                "review_status": "WAITING_FOR_FUTURE_MARKET_DATA"},
        "calibration_hooks": {"ev_calibration_ready": False, "r_matrix_calibration_ready": False,
                              "g18_rule_calibration_ready": False, "requires_future_outcome": True},
        "z9_write_policy": {"write_allowed": False, "write_status": "DEFERRED_NOT_CONNECTED",
                            "reason": "CONTRACT_FREEZE_ONLY_NO_REAL_Z9_WRITE"},
        "forbidden_real_trade_checked": True,
    }
