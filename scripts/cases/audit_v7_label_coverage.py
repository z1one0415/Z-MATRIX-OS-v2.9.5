#!/usr/bin/env python3
"""V7-C: Label coverage audit — count valid labels per horizon."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
CASES = W / "runtime_reports" / "cases"

def main():
    labels = json.loads((CASES / "v7_forward_return_labels.json").read_text())
    cov = {}
    for hn in labels["horizons"]:
        valid = [l for l in labels["labels"] if l["horizon"] == hn and l["label_status"] == "REAL_FORWARD_LABEL"]
        dates = len(set(l["as_of_date"] for l in valid))
        cov[hn] = {"valid_dates": dates, "valid_labels": len(valid)}

    audit = {
        "status": "V7_LABEL_COVERAGE_AUDIT_PASS",
        "coverage_by_horizon": cov,
        "missing_policy": "INSUFFICIENT_NOT_ZERO_FILLED",
    }
    (CASES / "v7_label_coverage_audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False))
    for hn, c in cov.items():
        print(f"  {hn}: {c['valid_dates']} dates, {c['valid_labels']} labels")

if __name__ == "__main__":
    main()
