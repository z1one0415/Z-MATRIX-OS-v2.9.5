#!/usr/bin/env python3
"""V13.F3.4.1 — Stage D: rebuild freeze boundary OOS eligibility plan."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"

dates = json.loads((B / "v13_f3_4_1_last_in_sample_rebalance_dates.json").read_text())
per = dates.get("per_factor", [])
resolved = dates.get("all_last_in_sample_dates_resolved", False)
max_date = max(r["last_in_sample_rebalance_date"] for r in per) if resolved else ""

(B / "v13_f3_4_freeze_boundary_oos_eligibility_plan.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-FREEZE-BOUNDARY-OOS-ELIGIBILITY",
    "status": "V13_F3_4_FREEZE_BOUNDARY_OOS_ELIGIBILITY_PLAN_BUILT" if resolved else "V13_F3_4_FREEZE_BOUNDARY_OOS_ELIGIBILITY_BLOCKED",
    "selection_boundary_commit": "e6a3567", "freeze_source_commit": "c4d59ba",
    "candidate_factors": ["F04","F10","F11"],
    "per_factor_last_in_sample_rebalance_date": per,
    "any_na_last_in_sample_date": not resolved,
    "all_last_in_sample_dates_resolved": resolved,
    "minimum_oos_start_exclusive": max_date,
    "same_sample_reuse_forbidden": True, "oos_eligibility_check_executed": False,
    "true_oos_validation_executed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.4.1-D] Freeze boundary rebuilt: resolved={resolved} max={max_date}")
sys.exit(0)
