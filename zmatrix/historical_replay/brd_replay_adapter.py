# allowlist: forbidden-token-definition
"""Historical Replay v1.0 — B/R/D Replay Adapter (v3.1-data-spine)"""
from __future__ import annotations

_HISTORICAL_REPLAY_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "real_z9_write_allowed": False, "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False,
    "runtime_enabled": False, "future_data_allowed": False,
}


def build_brd_replay_payload(*, replay_date: str, ticker: str,
                              price_snapshot: dict, financial_snapshot: dict | None = None,
                              sector_snapshot: dict | None = None,
                              market_snapshot: dict | None = None) -> dict:
    """Build point-in-time B/R/D replay payload for one ticker."""
    return {
        "payload_version": "BRD_REPLAY_PAYLOAD_V10",
        "mode": "HISTORICAL_REPLAY_ONLY",
        "replay_date": replay_date, "ticker": ticker,
        "price_snapshot": price_snapshot,
        "financial_snapshot": financial_snapshot or {},
        "sector_snapshot": sector_snapshot or {},
        "market_snapshot": market_snapshot or {},
        "point_in_time_only": True,
        "real_trade_allowed": False, "broker_order_allowed": False,
        "future_data_allowed": False,
        "safety": dict(_HISTORICAL_REPLAY_SAFETY),
    }


def normalize_brd_replay_result(*, replay_date: str, ticker: str,
                                 brd_result: dict) -> dict:
    """Normalize B/R/D output into replay result schema."""
    return {
        "result_version": "BRD_REPLAY_RESULT_V10",
        "replay_date": replay_date, "ticker": ticker,
        "role": brd_result.get("role", "UNKNOWN"),
        "role_confidence": brd_result.get("role_confidence"),
        "brd_score": brd_result.get("brd_score"),
        "hard_gate_passed": brd_result.get("hard_gate_passed", False),
        "decision": brd_result.get("decision", "WATCH_ONLY"),
        "invalidation_condition": brd_result.get("invalidation_condition"),
        "max_loss_plan": brd_result.get("max_loss_plan"),
        "replay_only": True,
        "real_trade_allowed": False, "broker_order_allowed": False,
        "safety": dict(_HISTORICAL_REPLAY_SAFETY),
    }
