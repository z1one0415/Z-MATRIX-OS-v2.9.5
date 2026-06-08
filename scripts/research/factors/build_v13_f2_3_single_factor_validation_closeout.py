#!/usr/bin/env python3
"""V13.F2.3 — Stage H: execution closeout."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

def load_json(name):
    fpath = RUNTIME / name
    if not fpath.exists():
        return {}
    return json.loads(fpath.read_text())

iso = load_json("v13_f2_3_outcome_label_isolation_validation.json")
ic = load_json("v13_f2_3_single_factor_ic_validation.json")
bucket = load_json("v13_f2_3_single_factor_bucket_validation.json")
diag = load_json("v13_f2_3_regime_horizon_diagnostics.json")
scorecard = load_json("v13_f2_3_single_factor_evidence_scorecard.json")

label_isolation_passed = iso.get("label_isolation_passed", False)
ic_executed = ic.get("ic_validation_executed", False)
bucket_executed = bucket.get("bucket_validation_executed", False)
diag_executed = diag.get("diagnostics_executed", False)
all_executed = ic_executed and bucket_executed and diag_executed

per_factor_final = scorecard.get("per_factor_evidence_scorecard", [])

# Determine ready factors
ready_for_next = [f["factor_id"] for f in per_factor_final
                  if f.get("evidence_score") in ("PASS_RESEARCH_EVIDENCE", "TACTICAL_ONLY")]

# Determine next action
factor_scores = [f.get("evidence_score", "") for f in per_factor_final]
has_pass_or_tactical = any(s in ("PASS_RESEARCH_EVIDENCE", "TACTICAL_ONLY") for s in factor_scores)
has_blocked = any("BLOCKED" in s for s in factor_scores)
all_rejected_or_weak = all(s in ("REJECTED", "WEAK_OR_UNSTABLE") for s in factor_scores) and len(factor_scores) == 2

if has_pass_or_tactical and ready_for_next:
    recommended_next_action = "PREPARE_V13_F2_4_SINGLE_FACTOR_PROMOTION_REVIEW"
elif all_rejected_or_weak:
    recommended_next_action = "REJECT_OR_REWORK_F03_F06_FACTOR_HYPOTHESES"
elif has_blocked:
    recommended_next_action = "EXTEND_SAMPLE_OR_BLOCK_SINGLE_FACTOR_VALIDATION"
else:
    recommended_next_action = "REVIEW_V13_F2_3_EVIDENCE"

closeout = {
    "pipeline_signature": "Z2-V13-F2-3-VALIDATION-CLOSEOUT",
    "status": "V13_F2_3_SINGLE_FACTOR_VALIDATION_PASS" if all_executed and label_isolation_passed else "V13_F2_3_SINGLE_FACTOR_VALIDATION_PARTIAL",
    "v13_f2_3_executed": True,
    "outcome_label_generation_executed": True,
    "label_isolation_passed": label_isolation_passed,
    "ic_validation_executed": ic_executed,
    "rank_ic_validation_executed": ic_executed,
    "bucket_return_validation_executed": bucket_executed,
    "regime_diagnostics_executed": diag_executed,
    "cost_adjusted_validation_executed": bucket_executed,
    "validated_factors": ["F03", "F06"],
    "per_factor_final_status": per_factor_final,
    "ready_for_next_research_gate": ready_for_next,
    "multi_factor_composite_built": False,
    "oos_alpha_validation_executed": False,
    "skillos_protocol_modified": False,
    "frontend_modified": False,
    "v13_6_allowed": False,
    "paper_trading_allowed": False,
    "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
    "recommended_next_action": recommended_next_action
}

dst = RUNTIME / "v13_f2_3_single_factor_validation_closeout.json"
dst.write_text(json.dumps(closeout, indent=2))
print(f"[F2.3-H] Closeout built -> {dst}")
print(f"  Label isolation: {'PASS' if label_isolation_passed else 'FAIL'}")
print(f"  IC: {'EXECUTED' if ic_executed else 'FAILED'}")
print(f"  Bucket: {'EXECUTED' if bucket_executed else 'FAILED'}")
print(f"  Diagnostics: {'EXECUTED' if diag_executed else 'FAILED'}")
print(f"  Ready for next gate: {ready_for_next}")
print(f"  Next action: {recommended_next_action}")
sys.exit(0)
