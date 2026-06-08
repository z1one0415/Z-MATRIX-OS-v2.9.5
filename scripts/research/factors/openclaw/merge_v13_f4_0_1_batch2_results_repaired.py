#!/usr/bin/env python3
"""V13.F4.0.1 — Stage F: repaired merge."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
FACTORS = ["F02","F05","F09","F14","F15","F16","F17","F18","F19","F20"]
CONTRACT_COUNT = 7

def load_preferred(fid):
    p = B2 / fid / f"{fid.lower()}_closeout_recomputed.json"
    if p.exists():
        return json.loads(p.read_text())
    p = B2 / fid / f"{fid.lower()}_closeout.json"
    return json.loads(p.read_text()) if p.exists() else {}

pass_f = []
cov_blocked = []
source_violated = []
source_clean = []

for fid in FACTORS:
    co = load_preferred(fid)
    ev = co.get("evidence_score", "")
    if ev == "PASS_RESEARCH_EVIDENCE":
        pass_f.append(fid)
    elif "COVERAGE_BLOCKED" in ev:
        cov_blocked.append(fid)
    elif "CONTRACT_VIOLATED" in ev:
        source_violated.append(fid)
    elif ev == "SOURCE_AUDIT_COMPLETE":
        source_clean.append(fid)
    else:
        cov_blocked.append(fid)

(B2 / "v13_f4_0_1_batch2_merge_report_repaired.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-1-BATCH2-MERGE-REPAIRED",
    "status": "V13_F4_0_1_BATCH2_MERGE_REPAIRED_BUILT",
    "expected_subsessions_from_contract": CONTRACT_COUNT,
    "completed_subsessions_detected": len(FACTORS),
    "subsession_count_consistency_passed": False,
    "pass_research_evidence_factors": pass_f,
    "materialized_but_coverage_blocked_factors": cov_blocked,
    "source_audit_contract_violated_factors": source_violated,
    "source_audit_only_completed": source_clean,
    "ready_for_candidate_review": pass_f,
    "ready_for_promotion_review": [],
    "frozen_candidates_mutated": False,
    "multi_factor_composite_built": False, "weight_optimization_executed": False,
    "v13_6_allowed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0.1-F] Repaired merge: pass={pass_f} cov_blocked={cov_blocked} violated={source_violated} clean={source_clean}")
sys.exit(0)
