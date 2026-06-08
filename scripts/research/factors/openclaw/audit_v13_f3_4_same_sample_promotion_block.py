#!/usr/bin/env python3
"""V13.F3.4 — Stage G: same-sample promotion block audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
violations = []
for name in ["v13_f3_3_research_composite_design_closeout.json","v13_f3_2_candidate_freeze_closeout.json"]:
    d = json.loads((B / name).read_text()) if (B / name).exists() else {}
    if d.get("ready_for_promotion_review"):
        violations.append(f"{name}:ready_for_promotion_review_not_empty")
    if d.get("promotion_review_allowed") is True:
        violations.append(f"{name}:promotion_not_blocked")
    if d.get("multi_factor_composite_built") is True:
        violations.append(f"{name}:composite_built")
    if d.get("composite_execution_executed") is True:
        violations.append(f"{name}:composite_executed")
    if d.get("alpha_claim_allowed") is True:
        violations.append(f"{name}:alpha_unblocked")
(B / "v13_f3_4_same_sample_promotion_block_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-SAME-SAMPLE-PROMOTION-BLOCK-AUDIT",
    "status": "V13_F3_4_SAME_SAMPLE_PROMOTION_BLOCK_AUDIT_PASS" if len(violations) == 0 else "V13_F3_4_SAME_SAMPLE_PROMOTION_BLOCK_AUDIT_VIOLATIONS",
    "same_sample_promotion_blocked": len(violations) == 0,
    "ready_for_promotion_review": [], "true_oos_validation_executed": False,
    "composite_execution_executed": False, "alpha_claim_allowed": False,
    "violation_count": len(violations), "violations": violations,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.4-G] Same-sample block audit: {len(violations)} violations")
sys.exit(0)
