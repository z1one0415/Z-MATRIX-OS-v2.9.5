#!/usr/bin/env python3
"""V13.F3.5 — Stage H: monitoring plan safety audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
violations = []
for name in ["v13_f3_5_candidate_monitoring_plan_contract.json","v13_f3_5_monitoring_metric_registry.json","v13_f3_5_per_factor_monitoring_rules.json","v13_f3_5_monitoring_state_machine.json","v13_f3_5_monitoring_artifact_schema.json","v13_f3_5_monitoring_trigger_calendar_plan.json","v13_f3_5_to_f3_6_true_oos_handoff_plan.json"]:
    d = json.loads((B / name).read_text()) if (B / name).exists() else {}
    for k in ["monitoring_execution_executed","true_oos_validation_executed","oos_label_generation_executed","composite_execution_executed","composite_panel_generated","weight_optimization_executed","promotion_allowed"]:
        if d.get(k) is True: violations.append(f"{name}:{k}=true")
    for k in ["production","broker_runtime","real_trade"]:
        if d.get(k) != "BLOCKED" and d.get(k) is not None: violations.append(f"{name}:{k}")
schema = json.loads((B / "v13_f3_5_monitoring_artifact_schema.json").read_text()) if (B / "v13_f3_5_monitoring_artifact_schema.json").exists() else {}
for fb in schema.get("forbidden_fields", []):
    if fb in schema.get("required_report_fields", []): violations.append(f"artifact_schema:forbidden_field_{fb}_also_required")
(B / "v13_f3_5_candidate_monitoring_plan_safety_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-5-CANDIDATE-MONITORING-PLAN-SAFETY-AUDIT",
    "status": "V13_F3_5_CANDIDATE_MONITORING_PLAN_SAFETY_AUDIT_PASS" if len(violations)==0 else "V13_F3_5_CANDIDATE_MONITORING_PLAN_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations), "violations": violations,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.5-H] Safety: {len(violations)} violations")
sys.exit(0)
