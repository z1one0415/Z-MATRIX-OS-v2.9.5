#!/usr/bin/env python3
"""V13.F4.0.2 — Stage E: parent safety audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
violations = []

merge = json.loads((B2 / "v13_f4_0_2_batch2_merge_report_canonical.json").read_text())
source_audit = json.loads((B2 / "v13_f4_0_2_batch2_source_audit_group_taxonomy_audit.json").read_text())

# Frozen candidates preserved
for fid in ["F04","F10","F11"]:
    co = json.loads((B / fid / f"{fid.lower()}_closeout_recomputed.json").read_text()) if (B / fid / f"{fid.lower()}_closeout_recomputed.json").exists() else {}
    if co.get("evidence_score") != "PASS_RESEARCH_EVIDENCE":
        violations.append(f"frozen_{fid}_mutated")

# No F17-F20 in materialized_but_coverage_blocked
if merge.get("materialized_but_coverage_blocked_factors"):
    for fid in ["F17","F18","F19","F20"]:
        if fid in merge["materialized_but_coverage_blocked_factors"]:
            violations.append(f"{fid}_misclassified_as_coverage_blocked")

# F09 not in pass
if "F09" in merge.get("pass_research_evidence_factors", []):
    violations.append("F09_in_pass_after_repair")

# Source audit clean
if not source_audit.get("all_members_source_audit_clean"):
    violations.append("source_audit_group_has_violations")

# Lane consistency
if not merge.get("lane_count_consistency_passed"):
    violations.append("lane_count_consistency_failed")

(B2 / "v13_f4_0_2_batch2_parent_safety_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-2-BATCH2-PARENT-SAFETY-AUDIT",
    "status": "V13_F4_0_2_BATCH2_PARENT_SAFETY_AUDIT_PASS" if len(violations)==0 else "V13_F4_0_2_BATCH2_PARENT_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations), "violations": violations,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0.2-E] Safety: {len(violations)} violations")
sys.exit(0)
