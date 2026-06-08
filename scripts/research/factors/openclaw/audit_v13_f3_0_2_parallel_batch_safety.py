#!/usr/bin/env python3
"""V13.F3.0.2 — Stage D: canonical safety audit."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"]

def load_closeout(fid):
    p = BATCH / fid / f"{fid.lower()}_closeout_recomputed.json"
    if p.exists():
        return json.loads(p.read_text())
    p = BATCH / fid / f"{fid.lower()}_closeout.json"
    return json.loads(p.read_text()) if p.exists() else {}

violations = []

for fid in FACTOR_IDS:
    co = load_closeout(fid)
    if not co:
        violations.append({"factor_id": fid, "violation": "closeout_not_found"})
        continue
    if co.get("alpha_claim_allowed") is True:
        violations.append({"factor_id": fid, "violation": "alpha_claim"})
    if co.get("v13_6_allowed") is True:
        violations.append({"factor_id": fid, "violation": "v13_6"})
    if co.get("production") != "BLOCKED":
        violations.append({"factor_id": fid, "violation": "production"})
    if co.get("broker_runtime") != "BLOCKED":
        violations.append({"factor_id": fid, "violation": "broker"})
    if co.get("multi_factor_composite_built") is True:
        violations.append({"factor_id": fid, "violation": "composite"})
    if co.get("ready_for_promotion_review") is True:
        violations.append({"factor_id": fid, "violation": "promotion"})
    if co.get("coverage_passed") is False and co.get("evidence_score") == "PASS_RESEARCH_EVIDENCE":
        violations.append({"factor_id": fid, "violation": "coverage_fail_but_pass"})
    if fid == "F03R":
        if co.get("materialized") is True:
            violations.append({"factor_id": "F03R", "violation": "materialized"})
        if co.get("single_factor_validation_executed") is True:
            violations.append({"factor_id": "F03R", "violation": "validated"})
        if co.get("ready_for_promotion_review") is True:
            violations.append({"factor_id": "F03R", "violation": "promotion"})

audit = {
    "pipeline_signature": "Z2-V13-F3-0-2-PARALLEL-BATCH-SAFETY",
    "status": "V13_F3_0_2_PARALLEL_BATCH_SAFETY_AUDIT_PASS" if len(violations) == 0 else "V13_F3_0_2_PARALLEL_BATCH_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations), "violations": violations,
    "all_blocked": all(load_closeout(fid).get("production") == "BLOCKED" for fid in FACTOR_IDS if load_closeout(fid)),
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}
(BATCH / "v13_f3_0_2_parallel_batch_safety_audit.json").write_text(json.dumps(audit, indent=2))
print(f"[F3.0.2-D] Canonical safety: {len(violations)} violations")
for v in violations:
    print(f"  ❌ {v['factor_id']}: {v['violation']}")
sys.exit(0)
