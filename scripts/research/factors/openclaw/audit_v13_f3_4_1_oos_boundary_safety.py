#!/usr/bin/env python3
"""V13.F3.4.1 — Stage E: boundary safety audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
violations = []
dates = json.loads((B / "v13_f3_4_1_last_in_sample_rebalance_dates.json").read_text())
plan = json.loads((B / "v13_f3_4_1_canonical_oos_boundary_plan.json").read_text())
for r in dates.get("per_factor", []):
    if r.get("last_in_sample_rebalance_date") in (None, "", "N/A"):
        violations.append(f"{r['factor_id']}:date_NA")
if not plan.get("minimum_oos_start_exclusive"):
    violations.append("minimum_oos_start_exclusive_empty")
for name in ["v13_f3_4_true_oos_requirement_closeout.json","v13_f3_3_research_composite_design_closeout.json"]:
    d = json.loads((B / name).read_text()) if (B / name).exists() else {}
    if d.get("ready_for_promotion_review"): violations.append(f"{name}:promotion")
    if d.get("alpha_claim_allowed"): violations.append(f"{name}:alpha")
    if d.get("v13_6_allowed"): violations.append(f"{name}:v13.6")
    if d.get("production") != "BLOCKED": violations.append(f"{name}:prod")
(B / "v13_f3_4_1_oos_boundary_safety_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-1-OOS-BOUNDARY-SAFETY-AUDIT",
    "status": "V13_F3_4_1_OOS_BOUNDARY_SAFETY_AUDIT_PASS" if len(violations)==0 else "V13_F3_4_1_OOS_BOUNDARY_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations), "violations": violations,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.4.1-E] Safety: {len(violations)} violations")
sys.exit(0)
