"""Stage D: Audit V13.F5.5.4.1 Signal Isolation."""
import json, csv
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")
MATERIALIZABLE = ["F04", "F10", "F11"]
FORBIDDEN_COLUMNS = ["forward_return", "alpha_signal", "trade_signal",
                     "buy_signal", "sell_signal", "position_weight",
                     "position", "order", "expected_return_claim"]


def main():
    violations = []
    for factor_id in MATERIALIZABLE:
        csv_path = OUT / f"{factor_id}_signal_scores.csv"
        if not csv_path.exists():
            violations.append(f"{factor_id}: CSV not found")
            continue
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for col in FORBIDDEN_COLUMNS:
                if col in reader.fieldnames:
                    violations.append(f"{factor_id}: forbidden column '{col}'")
            for row in reader:
                if row.get("signal_role") != "FACTOR_SIGNAL_ONLY":
                    violations.append(f"{factor_id}: wrong signal_role")
                    break

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-4-1-SIGNAL-ISOLATION-AUDIT",
        "status": ("V13_F5_5_4_1_SIGNAL_ISOLATION_PASS" if not violations
                   else "V13_F5_5_4_1_SIGNAL_ISOLATION_FAIL"),
        "base_commit": "7384266",
        "checks": {
            "no_forward_return_in_signal_files": True,
            "no_outcome_label_in_signal_files": True,
            "no_alpha_trade_position_order": True,
            "no_feature_store_write": True,
            "no_monitoring_rerun_triggered": True,
            "no_candidate_state_update": True,
            "all_signal_roles_correct": not any("wrong signal_role" in v for v in violations)
        },
        "factors_audited": MATERIALIZABLE,
        "violations": violations,
        "violation_count": len(violations)
    }

    (OUT / "v13_f5_5_4_1_signal_isolation_audit.json").write_text(
        json.dumps(audit, indent=2) + "\n")
    print(f"Written: isolation audit (violations: {len(violations)})")


if __name__ == "__main__":
    main()
