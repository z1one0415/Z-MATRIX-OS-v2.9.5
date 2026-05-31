#!/usr/bin/env python3
"""V5-D: Calculate benchmark-relative returns. NOT predictive alpha."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
CASES = W / "runtime_reports" / "cases"

def main():
    stock = json.loads((CASES / "core_12_real_returns.json").read_text())
    bench = json.loads((CASES / "csi300_benchmark_returns.json").read_text())
    
    results = []
    for sc in stock["cases"]:
        rel = {}
        for hk in stock["horizons"]:
            sr = sc["returns"][hk].get("return")
            br = bench["returns"][hk].get("return")
            rr = (sr - br) if (sr is not None and br is not None) else None
            rel[hk] = {
                "stock_return": sr, "benchmark_return": br,
                "benchmark_relative_return": rr,
                "truth_status": "REAL_READ_ONLY" if rr is not None else "BLOCKED_MISSING_DATA",
                "can_interpret_as_predictive_alpha": False,
            }
        results.append({
            "case_id": sc["case_id"], "ticker": sc["ticker"], "name": sc["name"],
            "benchmark_id": "CSI300", "relative_returns": rel,
            "ready_for_return_analysis": True, "ready_for_alpha_claim": False,
        })
    
    out = {"cases": results, "horizons": stock["horizons"]}
    (CASES / "core_12_benchmark_relative_returns.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Relative returns: {len(results)} cases x {len(stock['horizons'])} horizons")

if __name__ == "__main__":
    main()
