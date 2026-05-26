"""Replay Engine — single-day full replay with fallback stub"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.historical_replay.replay_universe import build_replay_universe
from zmatrix.historical_replay.brd_replay_adapter import build_brd_replay_payload, normalize_brd_replay_result

_HISTORICAL_REPLAY_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "real_z9_write_allowed": False, "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False,
    "runtime_enabled": False, "future_data_allowed": False,
}

FALLBACK_STUB_RESULT = {
    "role": "UNKNOWN", "role_confidence": 0.0, "brd_score": 0.0,
    "hard_gate_passed": False, "decision": "WATCH_ONLY",
    "fallback": True, "fallback_reason": "brd_classifier_unavailable",
}


def run_single_day_replay(*, replay_date: str, local_data_root: str,
                           max_tickers: int | None = None) -> dict:
    """Run full-market replay for one historical date."""
    universe = build_replay_universe(
        replay_date=replay_date, local_data_root=local_data_root,
        max_tickers=max_tickers,
    )
    tickers = universe.get("tickers", [])
    results = []
    for ticker in tickers:
        snap = {"date": replay_date, "close": None}
        payload = build_brd_replay_payload(
            replay_date=replay_date, ticker=ticker, price_snapshot=snap,
        )
        normalized = normalize_brd_replay_result(
            replay_date=replay_date, ticker=ticker,
            brd_result=FALLBACK_STUB_RESULT,
        )
        results.append({"ticker": ticker, "payload": payload,
                         "result": normalized, "fallback": True})
    seed = f"{replay_date}|{len(results)}"
    engine_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "engine_version": "REPLAY_ENGINE_V10", "mode": "HISTORICAL_REPLAY_ONLY",
        "engine_id": engine_id, "replay_date": replay_date,
        "created_at": created_at,
        "tickers_scanned": len(tickers), "results": results,
        "fallback_count": sum(1 for r in results if r.get("fallback")),
        "universe": universe,
        "real_trade_allowed": False, "broker_order_allowed": False,
        "safety": dict(_HISTORICAL_REPLAY_SAFETY),
    }
