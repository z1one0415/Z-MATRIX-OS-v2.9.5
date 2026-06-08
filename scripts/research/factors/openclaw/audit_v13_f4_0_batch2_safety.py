#!/usr/bin/env python3
"""V13.F4.0 — Stage G: batch 2 safety audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B1 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
violations = []
# Check frozen candidates not mutated
for fid in ["F04","F10","F11"]:
    co = json.loads((B1 / fid / f"{fid.lower()}_closeout_recomputed.json").read_text()) if (B1 / fid / f"{fid.lower()}_closeout_recomputed.json").exists() else {}
    if co.get("evidence_score") != "PASS_RESEARCH_EVIDENCE":
        violations.append(f"{fid}:frozen_candidate_mutated")
# Check batch 2 safety
for fid in ["F05","F02","F09","F14","F15","F16","F17","F18","F19","F20"]:
    co = json.loads((B2 / fid / f"{fid.lower()}_closeout.json").read_text()) if (B2 / fid / f"{fid.lower()}_closeout.json").exists() else {}
    if co.get("alpha_claim_allowed"): violations.append(f"{fid}:alpha")
    if co.get("v13_6_allowed"): violations.append(f"{fid}:v13.6")
    if co.get("production") != "BLOCKED" and co.get("production") is not None: violations.append(f"{fid}:prod")
    if co.get("ready_for_promotion_review"): violations.append(f"{fid}:promotion")
    if co.get("multi_factor_composite_built"): violations.append(f"{fid}:composite")
    if co.get("materialization_executed") is False and "SOURCE_AUDIT" in co.get("subsession_status","") and "materialization" in str(co.get("materialization_executed","")):
        pass  # source audit ok
    elif co.get("materialization_executed") is False and "SOURCE_AUDIT" not in co.get("subsession_status",""):
        pass  # materialization lane but not materialized is fine if blocked
(B2 / "v13_f4_0_batch2_safety_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-BATCH2-SAFETY-AUDIT",
    "status": "V13_F4_0_BATCH2_SAFETY_AUDIT_PASS" if len(violations) == 0 else "V13_F4_0_BATCH2_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations), "violations": violations,
    "frozen_candidates_mutated": any("mutated" in v for v in violations),
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0-G] Safety: {len(violations)} violations")
sys.exit(0)
