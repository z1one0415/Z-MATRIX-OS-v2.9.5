"""Stage H: Build V13.F5.5.1.2 OOS Label Materialization Closeout."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")
INTEGRITY = OUT / "v13_f5_5_1_2_actual_label_data_integrity_audit.json"
MANIFEST = OUT / "v13_f5_5_1_2_actual_oos_label_panel_manifest.json"
ISOLATION = OUT / "v13_f5_5_1_2_actual_label_isolation_audit.json"
SAFETY = OUT / "v13_f5_5_1_2_label_materialization_safety_audit.json"


def main():
    integrity = json.loads(INTEGRITY.read_text())
    manifest = json.loads(MANIFEST.read_text())
    isolation = json.loads(ISOLATION.read_text())
    safety = json.loads(SAFETY.read_text())

    row_count = integrity["label_data_row_count"]
    has_data = row_count > 0
    isolation_pass = isolation["violation_count"] == 0
    safety_pass = safety["violation_count"] == 0

    all_pass = has_data and isolation_pass and safety_pass
    status = ("V13_F5_5_1_2_OOS_LABEL_MATERIALIZATION_PASS" if all_pass
              else "V13_F5_5_1_2_OOS_LABEL_MATERIALIZATION_BLOCKED")

    closeout = {
        "pipeline_signature": "Z2-V13-F5-5-1-2-OOS-LABEL-MATERIALIZATION-CLOSEOUT",
        "status": status,
        "base_commit": "db190ff",
        "read_only_price_data_access_used": True,
        "label_month": manifest["label_month"],
        "rebalance_date": manifest["rebalance_date"],
        "generated_horizons": manifest["generated_horizons"],
        "blocked_horizons": manifest["blocked_horizons"],
        "actual_forward_returns_generated": has_data,
        "label_data_row_count": row_count,
        "label_role": "OUTCOME_LABEL_ONLY",
        "written_to_feature_store": False,
        "used_for_factor_calculation": False,
        "used_for_candidate_decision": False,
        "used_for_monitoring_execution": False,
        "monitoring_execution_executed": False,
        "true_oos_validation_executed": False,
        "candidate_decision_update_executed": False,
        "ready_for_first_monitoring_execution": all_pass,
        "ready_for_promotion_review": [],
        "promotion_allowed": False,
        "runner_enabled": False,
        "execution_allowed": False,
        "v13_6_allowed": False,
        "paper_trading_allowed": False,
        "alpha_claim_allowed": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
        "recommended_next_action": ("EXECUTE_V13_F5_5_2_FIRST_PARTIAL_MONITORING_EXECUTION"
                                     if all_pass else
                                     "FIX_LABEL_MATERIALIZATION_FAILURES")
    }

    out_path = OUT / "v13_f5_5_1_2_oos_label_materialization_closeout.json"
    out_path.write_text(json.dumps(closeout, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Status: {status}")
    print(f"Row count: {row_count}")
    print(f"Ready for monitoring: {all_pass}")


if __name__ == "__main__":
    main()
