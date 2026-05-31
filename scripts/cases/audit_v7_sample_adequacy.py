#!/usr/bin/env python3
"""V7-C: Sample adequacy audit — grade horizons by data sufficiency."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
CASES = W / "runtime_reports" / "cases"

def grade(n):
    if n >= 40: return "EXPLORATORY_USABLE"
    if n >= 20: return "LOW_CONFIDENCE"
    return "INSUFFICIENT"

def main():
    cov = json.loads((CASES / "v7_label_coverage_audit.json").read_text())
    horizon_status = {hn: grade(c["valid_dates"]) for hn, c in cov["coverage_by_horizon"].items()}

    audit = {
        "status": "V7_SAMPLE_ADEQUACY_AUDIT_PASS",
        "horizon_status": horizon_status,
        "label_records_per_horizon": {hn: c["valid_labels"] for hn, c in cov["coverage_by_horizon"].items()},
        "total_label_records": sum(c["valid_labels"] for c in cov["coverage_by_horizon"].values()),
        "formal_validation_allowed": False,
        "alpha_claim_allowed": False,
    }
    (CASES / "v7_sample_adequacy_audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False))
    for hn, s in horizon_status.items():
        print(f"  {hn}: {s}")

if __name__ == "__main__":
    main()
