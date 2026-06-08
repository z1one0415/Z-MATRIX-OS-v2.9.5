#!/usr/bin/env python3
"""V13.F3.4.1 — Stage C: canonical OOS boundary plan from resolved dates."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"

dates = json.loads((B / "v13_f3_4_1_last_in_sample_rebalance_dates.json").read_text())
per = dates.get("per_factor", [])
resolved = dates.get("all_last_in_sample_dates_resolved", False)
max_date = ""
if resolved:
    max_date = max(r["last_in_sample_rebalance_date"] for r in per)

(B / "v13_f3_4_1_canonical_oos_boundary_plan.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-1-CANONICAL-OOS-BOUNDARY-PLAN",
    "status": "V13_F3_4_1_CANONICAL_OOS_BOUNDARY_PLAN_PASS" if resolved else "V13_F3_4_1_CANONICAL_OOS_BOUNDARY_PLAN_BLOCKED",
    "selection_boundary_commit": "e6a3567", "freeze_source_commit": "c4d59ba",
    "current_requirement_commit": "27e16bb0",
    "candidate_scope": ["F04","F10","F11"],
    "per_factor_last_in_sample_rebalance_date": per,
    "max_last_in_sample_rebalance_date": max_date,
    "minimum_oos_start_exclusive": max_date,
    "true_oos_start_rule": "oos_rebalance_date > max_last_in_sample_rebalance_date",
    "same_sample_reuse_forbidden": True, "freeze_pre_sample_reuse_forbidden": True,
    "boundary_resolved": resolved,
    "true_oos_validation_executed": False, "oos_label_generation_executed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.4.1-C] Boundary plan: resolved={resolved} max_date={max_date}")
sys.exit(0)
