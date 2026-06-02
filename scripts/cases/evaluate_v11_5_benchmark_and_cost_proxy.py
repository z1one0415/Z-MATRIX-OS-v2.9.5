#!/usr/bin/env python3
"""V11.5-D: Evaluate benchmark and cost proxy — allows partial results."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def main():
    sim = json.loads(
        (C / "v11_5_paper_portfolio_simulation.json").read_text()
    )
    calc = sim.get("calculated_result_count", 0)
    blocked = sim.get("blocked_result_count", 0)

    if calc == 0:
        c = {
            "status": "V11_5_BENCHMARK_COST_PROXY_EVALUATION_BLOCKED",
            "blocking_reasons": ["NO_CALCULATED_PORTFOLIO_RESULTS"],
            "gross_positive_count": None,
            "net_positive_count": None,
        }
    else:
        gp = sum(
            1
            for r in sim["results"]
            if r.get("calculation_status") == "CALCULATED"
            and r.get("bucket_spread") is not None
            and r["bucket_spread"] > 0
        )
        np2 = sum(
            1
            for r in sim["results"]
            if r.get("calculation_status") == "CALCULATED"
            and r.get("bucket_spread") is not None
            and r["bucket_spread"] > 0.003
        )
        c = {
            "status": (
                "V11_5_BENCHMARK_COST_PROXY_EVALUATION_BUILT"
                if blocked == 0
                else "V11_5_BENCHMARK_COST_PROXY_EVALUATION_PARTIAL"
            ),
            "gross_positive_count": gp,
            "net_positive_count": np2,
            "calculated_results_used": calc,
            "blocked_results_skipped": blocked,
        }

    c.update(
        {
            "cost_model_status": "PROXY_ONLY",
            "one_way_cost_bps": 15,
            "round_trip_cost_bps": 30,
            "ready_for_alpha_claim": False,
            "alpha_validated": False,
            "production": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
        }
    )
    json.dump(
        c,
        open(C / "v11_5_benchmark_cost_proxy_evaluation.json", "w"),
        indent=2,
    )
    print(
        f"Cost: {c['status']} | gp={c.get('gross_positive_count')} calc={c.get('calculated_results_used', calc)}"
    )


if __name__ == "__main__":
    main()
