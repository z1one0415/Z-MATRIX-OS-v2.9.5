#!/usr/bin/env python3
"""V13.F4.0.1 — Stage G: safety audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
violations = []
merge = json.loads((B2 / "v13_f4_0_1_batch2_merge_report_repaired.json").read_text())

# Frozen candidates preserved
for fid in ["F04","F10","F11"]:
    co = json.loads((B / fid / f"{fid.lower()}_closeout_recomputed.json").read_text()) if (B / fid / f"{fid.lower()}_closeout_recomputed.json").exists() else {}
    if co.get("evidence_score") != "PASS_RESEARCH_EVIDENCE":
        violations.append(f"frozen_{fid}_mutated")

# Coverage fail not in pass
for fid in merge.get("pass_research_evidence_factors", []):
    rc = json.loads((B2 / fid / f"{fid.lower()}_closeout_recomputed.json").read_text()) if (B2 / fid / f"{fid.lower()}_closeout_recomputed.json").exists() else {}
    if rc.get("coverage_passed") is False:
        violations.append(f"{fid}:coverage_fail_in_pass_after_repair")

# Source audit not in pass
if "F09" in merge.get("pass_research_evidence_factors", []):
    violations.append("F09:source_audit_violated_in_pass")

# Ready for review not include violated
for fid in merge.get("ready_for_candidate_review", []):
    rc = json.loads((B2 / fid / f"{fid.lower()}_closeout_recomputed.json").read_text()) if (B2 / fid / f"{fid.lower()}_closeout_recomputed.json").exists() else {}
    if rc.get("ready_for_candidate_review") is False:
        violations.append(f"{fid}:in_review_but_not_ready")

(B2 / "v13_f4_0_1_batch2_safety_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-1-BATCH2-SAFETY-AUDIT",
    "status": "V13_F4_0_1_BATCH2_SAFETY_AUDIT_PASS" if len(violations)==0 else "V13_F4_0_1_BATCH2_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations), "violations": violations,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0.1-G] Safety: {len(violations)} violations")
for v in violations: print(f"  ❌ {v}")
sys.exit(0)
