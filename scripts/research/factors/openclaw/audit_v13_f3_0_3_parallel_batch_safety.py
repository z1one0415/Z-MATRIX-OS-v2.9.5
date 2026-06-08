#!/usr/bin/env python3
"""V13.F3.0.3 — Stage D: safety audit v2."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"]
def load_closeout(fid):
    for suffix in ["_closeout_recomputed.json", "_closeout.json"]:
        p = BATCH / fid / f"{fid.lower()}{suffix}"
        if p.exists():
            return json.loads(p.read_text())
    return {}
violations = []
for fid in FACTOR_IDS:
    co = load_closeout(fid)
    if not co: continue
    if co.get("alpha_claim_allowed"): violations.append({"factor_id": fid, "v": "alpha"})
    if co.get("v13_6_allowed"): violations.append({"factor_id": fid, "v": "v13.6"})
    if co.get("production") != "BLOCKED": violations.append({"factor_id": fid, "v": "prod"})
    if co.get("multi_factor_composite_built"): violations.append({"factor_id": fid, "v": "composite"})
    if co.get("ready_for_promotion_review"): violations.append({"factor_id": fid, "v": "promotion"})
    if co.get("coverage_passed") is False and co.get("evidence_score") == "PASS_RESEARCH_EVIDENCE":
        violations.append({"factor_id": fid, "v": "cov_fail_but_pass"})
    if fid == "F03R":
        if co.get("materialized"): violations.append({"factor_id": "F03R", "v": "materialized"})
        if co.get("single_factor_validation_executed"): violations.append({"factor_id": "F03R", "v": "validated"})
(BATCH / "v13_f3_0_3_parallel_batch_safety_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-0-3-PARALLEL-BATCH-SAFETY",
    "status": "V13_F3_0_3_PARALLEL_BATCH_SAFETY_AUDIT_PASS" if len(violations) == 0 else "V13_F3_0_3_PARALLEL_BATCH_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations), "violations": violations,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.0.3-D] Safety: {len(violations)} violations")
sys.exit(0)
