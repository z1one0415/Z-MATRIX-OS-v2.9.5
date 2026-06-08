#!/usr/bin/env python3
"""V13.F3.4 — Stage B: freeze boundary + OOS eligibility."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTORS = ["F04","F10","F11"]

last_in_sample = []
for fid in FACTORS:
    val = json.loads((B / fid / f"{fid.lower()}_single_factor_validation.json").read_text()) if (B / fid / f"{fid.lower()}_single_factor_validation.json").exists() else {}
    last_date = val.get("last_sample_rebalance_date", "N/A")
    last_in_sample.append({"factor_id": fid, "last_in_sample_rebalance_date": last_date})

(B / "v13_f3_4_freeze_boundary_oos_eligibility_plan.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-FREEZE-BOUNDARY-OOS-ELIGIBILITY",
    "status": "V13_F3_4_FREEZE_BOUNDARY_OOS_ELIGIBILITY_PLAN_BUILT",
    "selection_boundary_commit": "e6a3567", "freeze_source_commit": "c4d59ba",
    "candidate_factors": FACTORS,
    "per_factor_last_in_sample_rebalance_date": last_in_sample,
    "minimum_oos_start_exclusive_rule": "after max(last_in_sample_rebalance_date, candidate_freeze_boundary)",
    "same_sample_reuse_forbidden": True, "oos_eligibility_check_executed": False,
    "true_oos_validation_executed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.4-B] Freeze boundary plan built")
sys.exit(0)
