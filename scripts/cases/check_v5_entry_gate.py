#!/usr/bin/env python3
"""V5 Entry Gate — ALL conditions must be met. No single-gate bypass."""
import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
READINESS = WORKSPACE / "runtime_reports" / "cases" / "core_12_real_market_data_readiness.json"
RETURN = WORKSPACE / "runtime_reports" / "cases" / "core_12_real_return_readiness.json"

def safe_get(json_path, key, default):
    if json_path.exists():
        d = json.loads(json_path.read_text())
        return d.get("summary", {}).get(key, d.get(key, default))
    return default

def main():
    daily_price = safe_get(READINESS, "daily_price_real", 0)
    adj_ready = safe_get(RETURN, "adjustment_factor_ready", 0)
    bench_real = safe_get(READINESS, "benchmark_real_read_only", False)
    cal_real = safe_get(READINESS, "calendar_real_read_only", False)
    ret_ready = safe_get(RETURN, "ready_for_real_return", 0)
    alpha_ready = safe_get(RETURN, "ready_for_alpha_claim", 0)

    blocking = []
    if daily_price < 12: blocking.append("DAILY_PRICE_NOT_12")
    if adj_ready < 12: blocking.append("ADJUSTMENT_FACTOR_NOT_READY")
    if not bench_real: blocking.append("BENCHMARK_NOT_REAL")
    if not cal_real: blocking.append("CALENDAR_NOT_REAL")
    if ret_ready < 12: blocking.append("REAL_RETURN_NOT_READY")
    if alpha_ready > 0: blocking.append("ALPHA_CLAIM_NOT_ZERO")  # safety

    ready = len(blocking) == 0

    gate = {
        "status": "V5_ENTRY_ALLOWED" if ready else "V5_ENTRY_BLOCKED_WAITING_USER_MARKET_DATA",
        "daily_price_real_read_only": daily_price,
        "adjustment_factor_ready": adj_ready,
        "benchmark_real_read_only": bench_real,
        "calendar_real_read_only": cal_real,
        "ready_for_real_return": ret_ready,
        "ready_for_alpha_claim": alpha_ready,
        "v5_entry_allowed": ready,
        "blocking_reasons": blocking,
        "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    }
    (WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").write_text(json.dumps(gate, indent=2, ensure_ascii=False))
    print("V5 Entry Gate:", "ALLOWED" if ready else "BLOCKED", "| Price:", daily_price, "/12 | Reasons:", blocking)

if __name__ == "__main__":
    main()
