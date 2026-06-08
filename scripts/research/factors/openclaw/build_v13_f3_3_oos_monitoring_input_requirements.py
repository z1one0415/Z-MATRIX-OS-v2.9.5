#!/usr/bin/env python3
"""V13.F3.3 — Stage F: OOS + monitoring input requirements."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_3_oos_monitoring_input_requirements.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-3-OOS-MONITORING-INPUT-REQUIREMENTS",
    "status": "V13_F3_3_OOS_MONITORING_INPUT_REQUIREMENTS_BUILT",
    "required_for_f3_4_true_oos": ["post_freeze_rebalance_months","frozen_candidate_panels","outcome_label_isolation","regime_gate_labels","cost_turnover_gate_labels","holdout_start_date"],
    "minimum_true_oos_months_required": 6,
    "preferred_true_oos_months_required": 12,
    "required_for_f3_5_monitoring": ["monthly_factor_ic","bucket_spread","regime_state","cost_estimate","turnover_estimate","drift_alerts"],
    "forbidden": ["same_sample_promotion","lookahead_regime_label","future_cost_estimate","feature_label_leakage"],
    "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.3-F] OOS/monitoring requirements built")
sys.exit(0)
