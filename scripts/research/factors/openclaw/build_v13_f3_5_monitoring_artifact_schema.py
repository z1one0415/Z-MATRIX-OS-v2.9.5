#!/usr/bin/env python3
"""V13.F3.5 — Stage E: monitoring artifact schema."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_5_monitoring_artifact_schema.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-5-MONITORING-ARTIFACT-SCHEMA",
    "status": "V13_F3_5_MONITORING_ARTIFACT_SCHEMA_BUILT",
    "future_monitoring_report_path": "runtime_reports/research/factors/openclaw_batch/monitoring/monthly_candidate_monitoring_report_<YYYY_MM>.json",
    "required_report_fields": ["monitoring_month","candidate_scope","oos_boundary","per_factor_monitoring","gate_results","state_transitions","warnings","suspension_reviews","promotion_allowed","alpha_claim_allowed","production","broker_runtime","real_trade"],
    "forbidden_fields": ["trade_signal","position","order","broker_instruction","portfolio_weight","live_signal"],
    "monitoring_execution_executed": False, "alpha_claim_allowed": False
}, indent=2))
print("[F3.5-E] Artifact schema built")
sys.exit(0)
