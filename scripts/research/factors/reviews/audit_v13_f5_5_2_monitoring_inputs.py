"""Stage B: Audit V13.F5.5.2 Monitoring Inputs."""
import json, csv
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

LABEL_DIR = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")
CLOSEOUT = LABEL_DIR / "v13_f5_5_1_2_oos_label_materialization_closeout.json"
PANEL = LABEL_DIR / "v13_f5_5_1_2_actual_oos_label_panel.csv"
REGISTRY = Path("research/factor_library/unified_candidate_registry.json")


def main():
    closeout = json.loads(CLOSEOUT.read_text())
    registry = json.loads(REGISTRY.read_text())

    # Read label panel
    rows = []
    with open(PANEL) as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            rows.append(row)

    horizons = set(r["horizon"] for r in rows)
    frozen_ids = [c["factor_id"] for c in registry.get("frozen_candidates", [])]

    # Forbidden columns check
    forbidden = ["factor_score", "rank", "bucket", "alpha_signal",
                 "trade_signal", "position", "order"]
    has_forbidden = any(col in headers for col in forbidden)

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-2-MONITORING-INPUT-AUDIT",
        "status": "V13_F5_5_2_MONITORING_INPUT_AUDIT_PASS",
        "base_commit": "e7d7b1f",
        "checks": {
            "f5_5_1_2_closeout_pass": "PASS" in closeout["status"],
            "label_data_row_count": len(rows),
            "label_data_row_count_gte_1": len(rows) >= 1,
            "horizon_only_5d_20d": horizons <= {"5D", "20D"},
            "60D_not_present": "60D" not in horizons,
            "label_role_outcome_only": all(r["label_role"] == "OUTCOME_LABEL_ONLY" for r in rows),
            "no_forbidden_columns": not has_forbidden,
            "monitoring_scope_count": len(frozen_ids),
            "monitoring_scope_matches_10_frozen": len(frozen_ids) == 10,
            "registry_promotion_allowed_false": registry.get("promotion_allowed") is False or registry.get("promotion_allowed", False) is False,
            "runner_enabled_false": closeout.get("runner_enabled") is False,
            "execution_allowed_false": closeout.get("execution_allowed") is False
        },
        "monitoring_scope": frozen_ids,
        "violation_count": 0
    }

    # Check all checks pass
    violations = sum(1 for k, v in audit["checks"].items()
                     if v is False or v == 0)
    audit["violation_count"] = violations
    if violations > 0:
        audit["status"] = "V13_F5_5_2_MONITORING_INPUT_AUDIT_FAIL"

    out_path = OUT / "v13_f5_5_2_monitoring_input_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Violations: {violations}")


if __name__ == "__main__":
    main()
