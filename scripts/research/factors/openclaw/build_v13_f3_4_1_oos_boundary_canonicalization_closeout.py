#!/usr/bin/env python3
"""V13.F3.4.1 — Stage F: boundary canonicalization closeout."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
dates = json.loads((B / "v13_f3_4_1_last_in_sample_rebalance_dates.json").read_text())
plan = json.loads((B / "v13_f3_4_1_canonical_oos_boundary_plan.json").read_text())
safety = json.loads((B / "v13_f3_4_1_oos_boundary_safety_audit.json").read_text())
resolved = dates.get("all_last_in_sample_dates_resolved", False)
ok = resolved and safety.get("violation_count", 999) == 0
max_date = plan.get("minimum_oos_start_exclusive", "")
(B / "v13_f3_4_1_oos_boundary_canonicalization_closeout.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-1-OOS-BOUNDARY-CANONICALIZATION-CLOSEOUT",
    "status": "V13_F3_4_1_OOS_BOUNDARY_CANONICALIZATION_PASS" if ok else "V13_F3_4_1_OOS_BOUNDARY_CANONICALIZATION_BLOCKED",
    "base_commit": "27e16bb0", "boundary_canonicalization_executed": True,
    "all_last_in_sample_dates_resolved": resolved,
    "any_na_last_in_sample_date": not resolved,
    "candidate_scope": ["F04","F10","F11"],
    "max_last_in_sample_rebalance_date": max_date,
    "minimum_oos_start_exclusive": max_date,
    "true_oos_validation_executed": False, "oos_label_generation_executed": False,
    "ready_for_f3_5_candidate_monitoring_plan": ok,
    "ready_for_f3_6_true_oos_validation_execution": False,
    "ready_for_promotion_review": [], "promotion_review_allowed": False,
    "composite_execution_executed": False, "multi_factor_composite_built": False,
    "composite_panel_generated": False, "weight_optimization_executed": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": "PREPARE_V13_F3_5_CANDIDATE_MONITORING_PLAN" if ok else "FIX_TRUE_OOS_BOUNDARY_DATE_RESOLUTION"
}, indent=2))
print(f"[F3.4.1-F] Closeout: resolved={resolved} max={max_date} ok={ok}")
sys.exit(0)
