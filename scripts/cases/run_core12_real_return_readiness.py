#!/usr/bin/env python3
"""Real Return Readiness Gate — FIXTURE ≠ REAL. Only REAL_READ_ONLY enables real return."""
import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
READINESS = WORKSPACE / "runtime_reports" / "cases" / "core_12_real_market_data_readiness.json"

def main():
    if not READINESS.exists():
        print("No readiness data. Run check_core12_real_market_data_readiness.py first.")
        return
    data = json.loads(READINESS.read_text())
    results = []
    for c in data["cases"]:
        price_real = c["daily_price_status"] in ("REAL_READ_ONLY", "PUBLIC_READ_ONLY", "LOCAL_USER_PROVIDED")
        price_ok = c["daily_price_status"] not in ("MISSING", "SYNTHETIC")
        price_fixture = c["daily_price_status"] == "FIXTURE"
        cal_ok = c["calendar_status"] not in ("MISSING",)
        bench_real = c["benchmark_status"] in ("REAL_READ_ONLY", "PUBLIC_READ_ONLY", "LOCAL_USER_PROVIDED")
        real_return_ready = price_real and cal_ok
        fixture_ready = price_fixture and cal_ok

        rd = {
            "case_id": c["case_id"], "ticker": c["ticker"], "name": c["name"],
            "real_return_status": "READY" if real_return_ready else (
                "BLOCKED_FIXTURE_ONLY" if fixture_ready else (
                "BLOCKED_MISSING_PRICE" if not price_ok else "BLOCKED_MISSING_CALENDAR")),
            "fixture_return_ready": fixture_ready,
            "t20_return_ready": real_return_ready,
            "t60_return_ready": real_return_ready,
            "real_alpha_status": "BLOCKED_NO_REAL_BENCHMARK" if not bench_real else "NOT_STARTED",
            "adjustment_factor_status": c.get("adjustment_factor_status", "MISSING"),
            "ready_for_real_return": real_return_ready,
            "ready_for_alpha_claim": False,
            "council_status": "BLOCKED_UNTIL_FACTOR_REAL",
            "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
        }
        results.append(rd)

    out = {"schema_version": "v4.1", "cases": results,
           "summary": {
               "total": len(results),
               "fixture_return_ready": sum(1 for r in results if r.get("fixture_return_ready", False)),
               "ready_for_real_return": sum(1 for r in results if r["ready_for_real_return"]),
               "ready_for_alpha_claim": 0,
               "blocked_missing_price": sum(1 for r in results if "PRICE" in r.get("real_return_status", "")),
               "blocked_missing_calendar": sum(1 for r in results if "CALENDAR" in r.get("real_return_status", "")),
               "blocked_fixture_only": sum(1 for r in results if "FIXTURE" in r.get("real_return_status", "")),
           }}
    (WORKSPACE / "runtime_reports" / "cases" / "core_12_real_return_readiness.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Return Readiness: {len(results)} cases | Fixture Ready:{out['summary']['fixture_return_ready']} | Real Return:{out['summary']['ready_for_real_return']} | Alpha: 0")

if __name__ == "__main__":
    main()
