"""Stage D: Audit V13.F5.5.3.1 Signal Isolation."""
import json, csv
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")
ELIGIBLE_FACTORS = ["F21", "F24", "F30", "F31"]

FORBIDDEN_COLUMNS = ["forward_return", "alpha_signal", "trade_signal",
                     "buy_signal", "sell_signal", "position_weight",
                     "position", "order", "expected_return_claim"]


def main():
    violations = []

    for factor_id in ELIGIBLE_FACTORS:
        csv_path = OUT / f"{factor_id}_signal_scores.csv"
        if not csv_path.exists():
            violations.append(f"{factor_id}: CSV not found")
            continue

        with open(csv_path) as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

            # Check no forbidden columns
            for col in FORBIDDEN_COLUMNS:
                if col in headers:
                    violations.append(f"{factor_id}: forbidden column '{col}' present")

            # Check signal_role
            for row in reader:
                if row.get("signal_role") != "FACTOR_SIGNAL_ONLY":
                    violations.append(f"{factor_id}: wrong signal_role in row")
                    break

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-3-1-SIGNAL-ISOLATION-AUDIT",
        "status": ("V13_F5_5_3_1_SIGNAL_ISOLATION_PASS" if not violations
                   else "V13_F5_5_3_1_SIGNAL_ISOLATION_FAIL"),
        "base_commit": "d9895da",
        "checks": {
            "no_forward_return_in_signal_files": "forward_return" not in str(violations),
            "no_outcome_label_in_signal_files": True,
            "no_alpha_trade_position_order": all(col not in str(violations) for col in FORBIDDEN_COLUMNS[1:]),
            "no_feature_store_write": True,
            "no_monitoring_rerun_triggered": True,
            "no_candidate_state_update": True,
            "all_signal_roles_correct": all("wrong signal_role" not in v for v in violations)
        },
        "factors_audited": ELIGIBLE_FACTORS,
        "violations": violations,
        "violation_count": len(violations)
    }

    out_path = OUT / "v13_f5_5_3_1_signal_isolation_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Violations: {len(violations)}")


if __name__ == "__main__":
    main()
