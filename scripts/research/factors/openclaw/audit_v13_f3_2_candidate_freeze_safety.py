#!/usr/bin/env python3
"""V13.F3.2 — Stage G: freeze safety audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTORS = ["F04", "F10", "F11"]
violations = []
for fid in FACTORS:
    co = json.loads((BATCH / fid / f"{fid.lower()}_closeout_recomputed.json").read_text()) if (BATCH / fid / f"{fid.lower()}_closeout_recomputed.json").exists() else {}
    if co.get("alpha_claim_allowed"): violations.append(f"{fid}:alpha")
    if co.get("v13_6_allowed"): violations.append(f"{fid}:v13.6")
    if co.get("production") != "BLOCKED": violations.append(f"{fid}:prod")
    if co.get("ready_for_promotion_review"): violations.append(f"{fid}:promotion")
    if co.get("multi_factor_composite_built"): violations.append(f"{fid}:composite")
frozen_reg = json.loads((BATCH / "v13_f3_2_candidate_freeze_registry.json").read_text()) if (BATCH / "v13_f3_2_candidate_freeze_registry.json").exists() else {}
if len(frozen_reg.get("frozen_candidates", [])) != 3:
    violations.append("not_3_frozen_candidates")
(BATCH / "v13_f3_2_candidate_freeze_safety_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-2-CANDIDATE-FREEZE-SAFETY-AUDIT",
    "status": "V13_F3_2_CANDIDATE_FREEZE_SAFETY_AUDIT_PASS" if len(violations) == 0 else "V13_F3_2_CANDIDATE_FREEZE_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations), "violations": violations,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.2-G] Safety: {len(violations)} violations")
sys.exit(0)
