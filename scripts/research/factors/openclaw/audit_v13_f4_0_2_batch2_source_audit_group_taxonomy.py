#!/usr/bin/env python3
"""V13.F4.0.2 — Stage C: source audit group taxonomy audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
SOURCE_GROUP_MEMBERS = ["F17","F18","F19","F20"]
RESULTS = {}
ALL_CLEAN = True

for fid in SOURCE_GROUP_MEMBERS:
    co = json.loads((B2 / fid / f"{fid.lower()}_closeout.json").read_text()) if (B2 / fid / f"{fid.lower()}_closeout.json").exists() else {}
    mat = co.get("materialization_executed", None)
    val = co.get("single_factor_validation_executed", None)
    ev = co.get("evidence_score", "UNKNOWN")
    clean = mat is not True and val is not True
    if not clean:
        ALL_CLEAN = False
    RESULTS[fid] = {"materialization_executed": mat, "validation_executed": val, "evidence_score": ev, "source_audit_clean": clean}

(B2 / "v13_f4_0_2_batch2_source_audit_group_taxonomy_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-2-BATCH2-SOURCE-AUDIT-GROUP-TAXONOMY-AUDIT",
    "status": "V13_F4_0_2_BATCH2_SOURCE_AUDIT_GROUP_TAXONOMY_AUDIT_BUILT",
    "source_audit_group_id": "F17_F20_GROUP",
    "source_audit_group_members": SOURCE_GROUP_MEMBERS,
    "group_status": "SOURCE_AUDIT_GROUP_COMPLETED" if ALL_CLEAN else "SOURCE_AUDIT_GROUP_VIOLATED",
    "all_members_source_audit_clean": ALL_CLEAN,
    "per_member": RESULTS,
    "group_must_not_be_coverage_blocked": True,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0.2-C] Source audit group: {'ALL CLEAN' if ALL_CLEAN else 'VIOLATIONS'}")
sys.exit(0)
