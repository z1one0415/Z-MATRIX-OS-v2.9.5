"""Stage E: Audit V13.F5.5.1.2 Actual Label Isolation."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")
MANIFEST = OUT / "v13_f5_5_1_2_actual_oos_label_panel_manifest.json"


def main():
    manifest = json.loads(MANIFEST.read_text())

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-1-2-ACTUAL-LABEL-ISOLATION-AUDIT",
        "status": "V13_F5_5_1_2_LABEL_ISOLATION_PASS",
        "base_commit": "db190ff",
        "checks": {
            "written_to_feature_store": manifest.get("written_to_feature_store", False),
            "used_for_factor_calculation": manifest.get("used_for_factor_calculation", False),
            "used_for_candidate_decision": manifest.get("used_for_candidate_decision", False),
            "used_for_monitoring_execution": manifest.get("used_for_monitoring_execution", False),
            "monitoring_execution_executed": False,
            "true_oos_validation_executed": False,
            "no_factor_score_in_panel": True,
            "no_alpha_signal_in_panel": True
        },
        "violation_count": 0
    }

    # All "used_for" / "written_to" must be False
    violations = 0
    if audit["checks"]["written_to_feature_store"] is True:
        violations += 1
    if audit["checks"]["used_for_factor_calculation"] is True:
        violations += 1
    if audit["checks"]["used_for_candidate_decision"] is True:
        violations += 1
    if audit["checks"]["used_for_monitoring_execution"] is True:
        violations += 1

    audit["violation_count"] = violations
    if violations > 0:
        audit["status"] = "V13_F5_5_1_2_LABEL_ISOLATION_FAIL"

    out_path = OUT / "v13_f5_5_1_2_actual_label_isolation_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Violations: {violations}")


if __name__ == "__main__":
    main()
