"""Replay Engine — single-day full replay with real price data from CSV"""
from __future__ import annotations
import csv
import hashlib
from pathlib import Path
from datetime import datetime, timezone

from zmatrix.historical_replay.replay_universe import build_replay_universe
from zmatrix.historical_replay.brd_replay_adapter import build_brd_replay_payload, normalize_brd_replay_result

_HISTORICAL_REPLAY_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "real_z9_write_allowed": False, "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False,
    "runtime_enabled": False, "future_data_allowed": False,
}


def _load_price_snapshot(ticker: str, replay_date: str, data_root: str) -> dict | None:
    """Read a single ticker's CSV and extract the close price on or before replay_date."""
    bar_dir = Path(data_root) / "data" / "price_bars"
    path = bar_dir / f"{ticker}.csv"
    if not path.exists():
        return None
    try:
        rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
        clean = replay_date.replace("-", "")
        best = None
        for r in rows:
            d = (r.get("trade_date") or r.get("date", "")).replace("-", "")
            if not d:
                continue
            if d <= clean:
                best = r
            else:
                break
        if best is None:
            return None
        return {
            "date": best.get("trade_date") or best.get("date", ""),
            "close": float(best.get("close", 0) or 0),
            "open": float(best.get("open", 0) or 0),
            "high": float(best.get("high", 0) or 0),
            "low": float(best.get("low", 0) or 0),
            "volume": float(best.get("vol", 0) or best.get("volume", 0) or 0),
        }
    except Exception:
        return None


def run_single_day_replay(*, replay_date: str, local_data_root: str,
                           max_tickers: int | None = None) -> dict:
    """Run full-market replay for one historical date with real CSV data."""
    universe = build_replay_universe(
        replay_date=replay_date, local_data_root=local_data_root,
        max_tickers=max_tickers,
    )
    tickers = universe.get("tickers", [])
    results = []
    fallback_count = 0

    for ticker in tickers:
        snap = _load_price_snapshot(ticker, replay_date, local_data_root)
        if snap is None:
            results.append({
                "ticker": ticker, "payload": {},
                "result": normalize_brd_replay_result(
                    replay_date=replay_date, ticker=ticker,
                    brd_result={"role": "UNKNOWN", "decision": "DATA_GAP"},
                ),
                "data_available": False,
            })
            fallback_count += 1
            continue

        payload = build_brd_replay_payload(
            replay_date=replay_date, ticker=ticker, price_snapshot=snap,
        )
        # Real B/R/D evaluation could go here; for now classify by price availability
        # Real B/R/D evaluation could go here
        # For now, explicitly mark as BRD_NOT_CONNECTED
        result = normalize_brd_replay_result(
            replay_date=replay_date, ticker=ticker,
            brd_result={
                "role": "UNKNOWN",
                "role_confidence": 0.0,
                "brd_score": 0.0,
                "hard_gate_passed": False,
                "decision": "WATCH_ONLY",
                "fallback": True,
                "fallback_reason": "BRD_NOT_CONNECTED",
            },
        )
        results.append({
            "ticker": ticker, "payload": payload, "result": result,
            "data_available": True, "price": snap.get("close"),
            "fallback": True,
        })

    seed = f"{replay_date}|{len(results)}"
    engine_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total = len(results)
    data_ok = total - fallback_count

    return {
        "engine_version": "REPLAY_ENGINE_V10",
        "mode": "HISTORICAL_REPLAY_ONLY",
        "engine_id": engine_id,
        "replay_date": replay_date,
        "created_at": created_at,
        "tickers_scanned": len(tickers),
        "tickers_with_data": data_ok,
        "tickers_without_data": fallback_count,
        "data_coverage_pct": round(data_ok / total * 100, 1) if total > 0 else 0.0,
        "brd_connected": False,
        "fallback_count": sum(1 for r in results if r.get("fallback")),
        "results": results,
        "universe": universe,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "safety": dict(_HISTORICAL_REPLAY_SAFETY),
    }
