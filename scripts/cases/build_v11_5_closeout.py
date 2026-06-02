#!/usr/bin/env python3
"""V11.5-F: Closeout — only CONFIRMED when all upstream gates pass."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def main():
    sim = json.loads((C / "v11_5_paper_portfolio_simulation.json").read_text())
    align = json.loads((C / "v11_5_forward_label_alignment_audit.json").read_text())
    risk = json.loads((C / "v11_5_paper_portfolio_risk_audit.json").read_text())
    cost = json.loads((C / "v11_5_benchmark_cost_proxy_evaluation.json").read_text())

    label_ok = align.get("ready_for_portfolio_simulation", False)
    calc_ok = sim.get("calculated_result_count", 0) > 0
    blocked_ok = sim.get("blocked_result_count", 999) == 0
    null_ok = sim.get("null_return_count", 999) == 0
    risk_ok = risk.get("status") == "V11_5_PAPER_PORTFOLIO_RISK_AUDIT_PASS"
    cost_ok = "BLOCKED" not in cost.get("status", "")

    confirmed = label_ok and calc_ok and blocked_ok and null_ok and risk_ok and cost_ok

    co = {
        "status": (
            "CASE_EXPANSION_V11_5_PAPER_PORTFOLIO_SIMULATION_CONFIRMED"
            if confirmed
            else "CASE_EXPANSION_V11_5_BLOCKED"
        ),
        "portfolio_count": sim.get("portfolio_count", 0),
        "calculated_result_count": sim.get("calculated_result_count", 0),
        "blocked_result_count": sim.get("blocked_result_count", 0),
        "null_return_count": sim.get("null_return_count", 0),
        "label_alignment_pass": label_ok,
        "missing_label_count": sim.get("missing_label_count", 0),
        "cost_model_status": "PROXY_ONLY",
        "risk_audit_pass": risk_ok,
        "ready_for_v12": False,
        "v12_blocking_reasons": risk.get("v12_blocking_reasons", []),
        "blocking_reasons": (
            []
            if confirmed
            else [
                "MISSING_FORWARD_LABELS" if not label_ok else None,
                "NO_CALCULATED_RESULTS" if not calc_ok else None,
                "BLOCKED_RESULTS_PRESENT" if not blocked_ok else None,
                "NULL_RETURNS" if not null_ok else None,
                "RISK_AUDIT_FAIL" if not risk_ok else None,
            ]
        ),
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    # Filter None from blocking
    co["blocking_reasons"] = [b for b in co["blocking_reasons"] if b is not None]
    json.dump(
        co,
        open(C / "case_expansion_v11_5_closeout.json", "w"),
        indent=2,
        ensure_ascii=False,
    )
    print(
        f"Closeout: {co['status']} | label_ok={label_ok} calc={sim.get('calculated_result_count')} blocked={sim.get('blocked_result_count')}"
    )


if __name__ == "__main__":
    main()
