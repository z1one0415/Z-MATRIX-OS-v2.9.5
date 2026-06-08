#!/usr/bin/env python3
"""V13.F3.5 — Stage I: monitoring plan closeout."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
safety = json.loads((B / "v13_f3_5_candidate_monitoring_plan_safety_audit.json").read_text())
ok = safety.get("violation_count", 999) == 0
(B / "v13_f3_5_candidate_monitoring_plan_closeout.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-5-CANDIDATE-MONITORING-PLAN-CLOSEOUT",
    "status": "V13_F3_5_CANDIDATE_MONITORING_PLAN_PASS" if ok else "V13_F3_5_CANDIDATE_MONITORING_PLAN_BLOCKED",
    "base_commit": "680f1542", "monitoring_plan_executed": True,
    "monitoring_execution_executed": False,
    "candidate_scope": ["F04","F10","F11"],
    "minimum_oos_start_exclusive": "20260501", "monitoring_frequency": "MONTHLY",
    "monitoring_metric_registry_built": True, "per_factor_monitoring_rules_built": True,
    "monitoring_state_machine_built": True, "monitoring_artifact_schema_built": True,
    "monitoring_trigger_calendar_plan_built": True, "f3_6_handoff_plan_built": True,
    "ready_for_f3_5_1_first_monitoring_execution": False,
    "ready_for_f3_6_true_oos_validation_execution": False,
    "ready_for_promotion_review": [], "promotion_review_allowed": False,
    "true_oos_validation_executed": False, "oos_label_generation_executed": False,
    "composite_execution_executed": False, "multi_factor_composite_built": False,
    "composite_panel_generated": False, "weight_optimization_executed": False,
    "skillos_protocol_modified": False, "frontend_modified": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": "WAIT_FOR_FIRST_ELIGIBLE_OOS_MONITORING_MONTH_OR_PREPARE_NEXT_FACTOR_BATCH"
}, indent=2))
print(f"[F3.5-I] Monitoring closeout: ok={ok}")
sys.exit(0)
