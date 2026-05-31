#!/usr/bin/env python3
"""V5.1-D: Benchmark relative returns — date-aligned, formula-verified, non-predictive."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
CASES = W / "runtime_reports" / "cases"

def main():
    stock = json.loads((CASES / "core_12_real_returns.json").read_text())
    bench = json.loads((CASES / "csi300_benchmark_returns.json").read_text())

    # Verify shared entry_date
    assert stock["entry_date"] == bench["entry_date"], f"Entry date mismatch: {stock['entry_date']} vs {bench['entry_date']}"
    horizons = stock["horizons"]
    assert horizons == bench["horizons"], "Horizon mismatch"

    results = []
    for sc in stock["cases"]:
        rel = {}
        for hk in horizons:
            sr_data = sc["returns"][hk]
            br_data = bench["returns"][hk]
            sr = sr_data.get("return")
            br = br_data.get("return")
            sr_truth = sr_data.get("truth_status")
            br_truth = br_data.get("truth_status")
            se_date = sr_data.get("exit_date")
            be_date = br_data.get("exit_date")

            # Date alignment check
            date_match = (se_date == be_date)
            both_ready = (sr_truth == "REAL_READ_ONLY" and br_truth == "REAL_READ_ONLY")
            both_have = (sr is not None and br is not None)

            if not date_match:
                truth = "BLOCKED_DATE_MISMATCH"
                blocked = f"stock_exit={se_date} vs bench_exit={be_date}"
                rr = None
            elif not both_have:
                truth = "BLOCKED_MISSING_DATA"
                blocked = "stock or benchmark return is None"
                rr = None
            elif not both_ready:
                truth = f"BLOCKED_UPSTREAM_{sr_truth if sr_truth != 'REAL_READ_ONLY' else br_truth}"
                blocked = "upstream data not REAL_READ_ONLY"
                rr = None
            else:
                truth = "REAL_READ_ONLY"
                blocked = None
                rr = round(sr - br, 10)

            rel[hk] = {
                "stock_return": sr,
                "benchmark_return": br,
                "stock_exit_date": se_date,
                "benchmark_exit_date": be_date,
                "date_aligned": date_match,
                "benchmark_relative_return": rr,
                "calculation_formula": "stock_return - benchmark_return",
                "truth_status": truth,
                "blocked_reason": blocked,
                "can_interpret_as_predictive_alpha": False,
            }

        results.append({
            "case_id": sc["case_id"], "ticker": sc["ticker"], "name": sc["name"],
            "benchmark_id": "CSI300",
            "entry_date": stock["entry_date"],
            "relative_returns": rel,
            "ready_for_return_analysis": True,
            "ready_for_alpha_claim": False,
        })

    out = {"cases": results, "horizons": horizons, "entry_date": stock["entry_date"]}
    (CASES / "core_12_benchmark_relative_returns.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    blocked = sum(1 for r in results for hk in horizons if r["relative_returns"][hk]["truth_status"] != "REAL_READ_ONLY")
    print(f"Relative returns: {len(results)} cases x {len(horizons)} horizons | date_aligned={stock['entry_date']} | blocked_horizons={blocked}")

if __name__ == "__main__":
    main()
