#!/usr/bin/env python3
"""Load Core 12 market data from processed/ directory (read-only)."""
import json, csv
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
PROCESSED = WORKSPACE / "data" / "research_db" / "market_data" / "processed"
FIXTURES = WORKSPACE / "tests" / "fixtures" / "market_data"
REGISTRY = json.loads((WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())

def check_real_data(ticker):
    """Check if real market data exists for a ticker — in single-file or per-ticker format."""
    import csv, io
    # Check combined file first
    combined = PROCESSED / "core12_daily_price_bar.csv"
    if combined.exists():
        reader = csv.DictReader(io.StringIO(combined.read_text()))
        for row in reader:
            if row.get("ticker") == ticker:
                return {"status": "LOCAL_USER_PROVIDED", "file": str(combined.relative_to(WORKSPACE))}
    # Check per-ticker files
    for f in PROCESSED.glob(f"*{ticker}*"):
        if f.suffix == ".csv":
            return {"status": "LOCAL_USER_PROVIDED", "file": str(f.relative_to(WORKSPACE))}
    return {"status": "MISSING", "file": None}

def check_fixture_data(ticker):
    """Check if fixture data exists."""
    fp = FIXTURES / "sample_daily_price_bar.csv"
    if fp.exists():
        for row in csv.DictReader(fp.read_text().splitlines()):
            if row.get("ticker") == ticker:
                return {"status": "FIXTURE", "file": str(fp.relative_to(WORKSPACE))}
    return {"status": "MISSING", "file": None}

def main():
    results = []
    for c in REGISTRY:
        if c.get("case_layer") != "CORE": continue
        ticker = c["ticker"]
        real = check_real_data(ticker)
        fixture = check_fixture_data(ticker)
        has_any = real["status"] != "MISSING" or fixture["status"] != "MISSING"
        status = real["status"] if real["status"] != "MISSING" else fixture["status"]

        # Check processed for benchmark and calendar
        has_benchmark = (PROCESSED / "benchmark_csi300_price.csv").exists() or any("CSI300" in f.name for f in PROCESSED.glob("*CSI300*"))
        has_calendar = any("calendar" in f.name.lower() for f in PROCESSED.glob("*calendar*"))
        has_calendar = has_calendar or (FIXTURES / "sample_trading_calendar.csv").exists()

        rd = {
            "case_id": c["case_id"], "ticker": ticker, "name": c["name"],
            "daily_price_status": status,
            "daily_price_start": None, "daily_price_end": None, "trading_days": None,
            "t20_ready": False, "t60_ready": False,
            "adjustment_factor_status": "MISSING",
            "benchmark_status": "LOCAL_USER_PROVIDED" if has_benchmark else ("FIXTURE" if (FIXTURES / "sample_benchmark_registry.csv").exists() else "MISSING"),
            "calendar_status": "LOCAL_USER_PROVIDED" if (PROCESSED / "trading_calendar.csv").exists() else ("FIXTURE" if has_calendar else "MISSING"),
            "fixture_return_ready": status == "FIXTURE" and has_calendar,
            "ready_for_real_return": (status.startswith("REAL") or status.startswith("LOCAL")) and has_calendar,
            "ready_for_alpha_claim": False,
            "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
        }
        results.append(rd)

    out = {"schema_version": "v4.0", "cases": results,
           "summary": {
               "total": len(results),
               "daily_price_real": sum(1 for r in results if r["daily_price_status"] == "LOCAL_USER_PROVIDED"),
               "daily_price_fixture": sum(1 for r in results if r["daily_price_status"] == "FIXTURE"),
               "daily_price_missing": sum(1 for r in results if r["daily_price_status"] == "MISSING"),
               "benchmark_fixture": sum(1 for r in results if r["benchmark_status"] == "FIXTURE"),
               "calendar_fixture": sum(1 for r in results if r["calendar_status"] == "FIXTURE"),
               "fixture_return_ready": sum(1 for r in results if r.get("fixture_return_ready", False)),
               "ready_for_real_return": sum(1 for r in results if r["ready_for_real_return"]),
               "ready_for_alpha_claim": 0,
           }}
    (WORKSPACE / "runtime_reports" / "cases" / "core_12_real_market_data_readiness.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Market Data Readiness: {len(results)} cases | REAL:{out['summary']['daily_price_real']} FIXTURE:{out['summary']['daily_price_fixture']} MISSING:{out['summary']['daily_price_missing']} | Return Ready:{out['summary']['ready_for_real_return']}")

if __name__ == "__main__":
    main()
