#!/usr/bin/env python3
"""V13.F4.0 — Stage F: batch 2 merge."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
FACTOR_IDS = ["F05","F02","F09","F14","F15","F16","F17","F18","F19","F20"]

def load_closeout(fid):
    p = B2 / fid / f"{fid.lower()}_closeout.json"
    return json.loads(p.read_text()) if p.exists() else {}

pass_f = []
blocked_f = []
source_audit = []
for fid in FACTOR_IDS:
    co = load_closeout(fid)
    ev = co.get("subsession_status", "")
    mat = co.get("materialization_executed", True)
    if ev == "SOURCE_AUDIT_COMPLETE":
        source_audit.append(fid)
    elif co.get("evidence_score") == "PASS_RESEARCH_EVIDENCE":
        pass_f.append(fid)
    else:
        blocked_f.append(fid)

(B2 / "v13_f4_0_batch2_merge_report.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-BATCH2-MERGE",
    "status": "V13_F4_0_BATCH2_MERGE_BUILT",
    "expected_subsessions": 10, "completed_subsessions": len(pass_f)+len(blocked_f)+len(source_audit),
    "materialized_factors": pass_f + [f for f in blocked_f if f not in source_audit],
    "pass_research_evidence_factors": pass_f,
    "tactical_candidate_factors": [],
    "blocked_by_sample_factors": [],
    "source_audit_only_completed": source_audit,
    "ready_for_candidate_review": pass_f,
    "ready_for_promotion_review": [],
    "frozen_candidates_mutated": False,
    "multi_factor_composite_built": False, "weight_optimization_executed": False,
    "v13_6_allowed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0-F] Merge: pass={pass_f} source={source_audit}")
sys.exit(0)
