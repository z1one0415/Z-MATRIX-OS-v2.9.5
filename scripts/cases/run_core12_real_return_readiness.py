#!/usr/bin/env python3
"""Real Return Readiness Gate — gate return calc on real data presence."""
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
        price_ok = c["daily_price_status"] not in ("MISSING", "SYNTHETIC")
        bench_ok = c["benchmark_status"] not in ("MISSING",)
        cal_ok = c["calendar_status"] not in ("MISSING",)
        rd = {
            "case_id": c["case_id"], "ticker": c["ticker"], "name": c["name"],
            "real_return_status": "READY" if (price_ok and cal_ok) else (
                "BLOCKED_MISSING_PRICE" if not price_ok else "BLOCKED_MISSING_CALENDAR"),
            "t20_return_ready": price_ok and cal_ok,
            "t60_return_ready": price_ok and cal_ok,
            "real_alpha_status": "NOT_STARTED" if not bench_ok else "BLOCKED_NO_BENCHMARK",
            "adjustment_factor_status": c["adjustment_factor_status"],
            "ready_for_real_return": price_ok and cal_ok,
            "ready_for_alpha_claim": False,
            "council_status": "BLOCKED_UNTIL_FACTOR_REAL",
            "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
        }
        results.append(rd)
    out = {"schema_version": "v4.0", "cases": results,
           "summary": {
               "total": len(results),
               "ready_for_real_return": sum(1 for r in results if r["ready_for_real_return"]),
               "ready_for_alpha_claim": 0,
               "blocked_missing_price": sum(1 for r in results if "PRICE" in r.get("real_return_status","")),
               "blocked_missing_calendar": sum(1 for r in results if "CALENDAR" in r.get("real_return_status","")),
           }}
    (WORKSPACE / "runtime_reports" / "cases" / "core_12_real_return_readiness.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Return Readiness: {len(results)} cases | Ready:{out['summary']['ready_for_real_return']} | Blocked Price:{out['summary']['blocked_missing_price']} | Alpha Ready: 0")

if __name__ == "__main__":
    main()
