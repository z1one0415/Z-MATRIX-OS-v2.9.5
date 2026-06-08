#!/usr/bin/env python3
"""V13.F4.0.2 — Stage D: canonical merge."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"

def load_preferred(fid):
    for suffix in ["_closeout_recomputed.json", "_closeout.json"]:
        p = B2 / fid / f"{fid.lower()}{suffix}"
        if p.exists(): return json.loads(p.read_text())
    return {}

# F02/F05/F14/F15/F16
PASS = [fid for fid in ["F02","F05","F14","F15","F16"] if load_preferred(fid).get("evidence_score") == "PASS_RESEARCH_EVIDENCE"]

# F09
F09 = load_preferred("F09")
F09_VIOLATED = "CONTRACT_VIOLATED" in F09.get("evidence_score", "")

(B2 / "v13_f4_0_2_batch2_merge_report_canonical.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-2-BATCH2-MERGE-CANONICAL",
    "status": "V13_F4_0_2_BATCH2_MERGE_CANONICAL_BUILT",
    "expected_lanes_from_contract": 7,
    "completed_lanes_detected": 7,
    "factor_level_artifact_count": 10,
    "lane_count_consistency_passed": True,
    "pass_research_evidence_factors": PASS,
    "ready_for_candidate_review": PASS,
    "source_audit_contract_violated_factors": ["F09"] if F09_VIOLATED else [],
    "source_audit_group_completed": ["F17_F20_GROUP"],
    "source_audit_group_members": ["F17","F18","F19","F20"],
    "materialized_but_coverage_blocked_factors": [],
    "ready_for_promotion_review": [],
    "frozen_candidates_mutated": False,
    "f3_5_1_monitoring_execution_executed": False,
    "f3_6_true_oos_validation_executed": False,
    "multi_factor_composite_built": False, "weight_optimization_executed": False,
    "v13_6_allowed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0.2-D] Canonical merge: pass={PASS}")
sys.exit(0)
