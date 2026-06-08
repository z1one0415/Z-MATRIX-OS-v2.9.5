#!/usr/bin/env python3
"""V13.F3.0 — Parent safety audit."""
import json, sys
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"]

def load_json(fid: str, fname: str) -> dict:
    p = BATCH / fid / fname
    return json.loads(p.read_text()) if p.exists() else {}

violations = []

for fid in FACTOR_IDS:
    closeout = load_json(fid, f"{fid.lower()}_closeout.json")
    if not closeout:
        violations.append({"factor_id": fid, "violation": "closeout_not_found"})
        continue

    if closeout.get("alpha_claim_allowed") is True:
        violations.append({"factor_id": fid, "violation": "alpha_claim_allowed_true"})
    if closeout.get("v13_6_allowed") is True:
        violations.append({"factor_id": fid, "violation": "v13_6_allowed_true"})
    if closeout.get("production") != "BLOCKED":
        violations.append({"factor_id": fid, "violation": f"production_not_blocked: {closeout.get('production')}"})
    if closeout.get("broker_runtime") != "BLOCKED":
        violations.append({"factor_id": fid, "violation": "broker_not_blocked"})
    if closeout.get("real_trade") != "BLOCKED":
        violations.append({"factor_id": fid, "violation": "real_trade_not_blocked"})
    if closeout.get("multi_factor_composite_built") is True:
        violations.append({"factor_id": fid, "violation": "multi_factor_composite_built_true"})
    if closeout.get("ready_for_promotion_review") is True:
        violations.append({"factor_id": fid, "violation": "ready_for_promotion_review_true"})

    # F03R specific: must not be materialized or validated
    if fid == "F03R":
        if closeout.get("materialized") is True:
            violations.append({"factor_id": "F03R", "violation": "materialized_despite_planning_only"})
        if closeout.get("single_factor_validation_executed") is True:
            violations.append({"factor_id": "F03R", "violation": "validated_despite_planning_only"})

audit = {
    "pipeline_signature": "Z2-V13-F3-0-PARALLEL-BATCH-SAFETY",
    "status": "V13_F3_0_PARALLEL_BATCH_SAFETY_AUDIT_PASS" if len(violations) == 0 else "V13_F3_0_PARALLEL_BATCH_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations),
    "violations": violations,
    "all_factors_blocked": all(
        load_json(fid, f"{fid.lower()}_closeout.json").get("production") == "BLOCKED" for fid in FACTOR_IDS
    ),
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = BATCH / "v13_f3_0_parallel_batch_safety_audit.json"
dst.write_text(json.dumps(audit, indent=2))
print(f"[F3.0-A] Safety audit -> {dst}")
print(f"  Violations: {len(violations)}")
for v in violations:
    print(f"    ❌ {v['factor_id']}: {v['violation']}")
sys.exit(0)
