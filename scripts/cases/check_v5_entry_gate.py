#!/usr/bin/env python3
"""V5 Entry Gate — ALL conditions must be met. No single-gate bypass."""
import json, csv, io
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
CORE12_SET = {"600519","300750","688981","601899","300124","002594","300274","002371","600030","600276","002050","300763"}
READINESS = WORKSPACE / "runtime_reports" / "cases" / "core_12_real_market_data_readiness.json"
RETURN = WORKSPACE / "runtime_reports" / "cases" / "core_12_real_return_readiness.json"

def safe_get(json_path, key, default):
    if json_path.exists():
        d = json.loads(json_path.read_text())
        return d.get("summary", {}).get(key, d.get(key, default))
    return default

def main():
    PROCESSED = WORKSPACE / "data" / "research_db" / "market_data" / "processed"
    
    daily_price = safe_get(READINESS, "daily_price_real", 0)
    
    # Check adjustment factor CSV directly
    adj_csv = PROCESSED / "core12_adjustment_factor.csv"
    if adj_csv.exists():
        reader = csv.DictReader(io.StringIO(adj_csv.read_text()))
        tickers_in_adj = set(row.get("ticker","") for row in reader)
        adj_ready = len(tickers_in_adj & CORE12_SET)
    else:
        adj_ready = 0
    
    # Check benchmark CSV
    bench_csv = PROCESSED / "benchmark_csi300_price.csv"
    bench_real = bench_csv.exists()
    
    # Check calendar CSV
    cal_csv = PROCESSED / "trading_calendar.csv"
    cal_real = cal_csv.exists()
    
    ret_ready = safe_get(RETURN, "ready_for_real_return", 0)
    alpha_ready = safe_get(RETURN, "ready_for_alpha_claim", 0)

    blocking = []
    if daily_price < 12: blocking.append("DAILY_PRICE_NOT_12")
    if adj_ready < 12: blocking.append("ADJUSTMENT_FACTOR_NOT_READY")
    if not bench_real: blocking.append("BENCHMARK_NOT_REAL")
    if not cal_real: blocking.append("CALENDAR_NOT_REAL")
    if ret_ready < 12: blocking.append("REAL_RETURN_NOT_READY")
    if alpha_ready > 0: blocking.append("ALPHA_CLAIM_NOT_ZERO")

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
    print("V5 Entry Gate: " + ("ALLOWED" if ready else "BLOCKED") + " | Price:" + str(daily_price) + "/12 Adj:" + str(adj_ready) + "/12 Bench:" + str(bench_real) + " Cal:" + str(cal_real) + " Return:" + str(ret_ready) + "/12")

if __name__ == "__main__":
    main()
