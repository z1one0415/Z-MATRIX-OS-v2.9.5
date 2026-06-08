#!/usr/bin/env python3
"""V13.F2.3 — Stage G: single factor evidence scorecard."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

def load_json(name):
    fpath = RUNTIME / name
    if not fpath.exists():
        return {}
    return json.loads(fpath.read_text())

ic = load_json("v13_f2_3_single_factor_ic_validation.json")
bucket = load_json("v13_f2_3_single_factor_bucket_validation.json")
diag = load_json("v13_f2_3_regime_horizon_diagnostics.json")
iso = load_json("v13_f2_3_outcome_label_isolation_validation.json")

def score_factor(factor_id: str) -> dict:
    """Score a factor based on available evidence."""
    # Gather evidence
    ic_info = None
    bucket_info = None
    diag_info = None

    for f in ic.get("per_factor_ic", []):
        if f.get("factor_id") == factor_id:
            ic_info = f
            break
    for f in bucket.get("per_factor_bucket_evidence", []):
        if f.get("factor_id") == factor_id:
            bucket_info = f
            break
    for f in diag.get("per_factor_diagnostics", []):
        if f.get("factor_id") == factor_id:
            diag_info = f
            break

    sample_count = 0
    if ic_info:
        sample_count = ic_info.get("sample_month_count", 0)
    elif bucket_info:
        sample_count = bucket_info.get("sample_month_count", 0)

    # Check blocked by insufficient sample
    if sample_count < 12:
        return {
            "factor_id": factor_id,
            "sample_month_count": sample_count,
            "evidence_score": "BLOCKED_BY_INSUFFICIENT_SAMPLE",
            "rationale": f"Only {sample_count} months of data; minimum 12 required"
        }

    # Check IC evidence
    ic_mean_20d = ic_info.get("ic_20d_mean", 0.0) if ic_info else 0.0
    ic_mean_60d = ic_info.get("ic_60d_mean", 0.0) if ic_info else 0.0
    ic_win_20d = ic_info.get("ic_20d_win_rate", 0.0) if ic_info else 0.0
    ic_win_60d = ic_info.get("ic_60d_win_rate", 0.0) if ic_info else 0.0

    # Check bucket evidence
    bucket_spread_20d = bucket_info.get("high_low_spread_20d", 0.0) if bucket_info else 0.0
    bucket_spread_60d = bucket_info.get("high_low_spread_60d", 0.0) if bucket_info else 0.0
    mono_20d = bucket_info.get("bucket_monotonicity_20d_rate", 0.0) if bucket_info else 0.0

    # Scoring logic
    has_positive_ic = ic_mean_20d > 0.01 or ic_mean_60d > 0.01
    has_winning_ic = ic_win_20d > 0.5 or ic_win_60d > 0.5
    has_bucket_spread = bucket_spread_20d > 0.005 or bucket_spread_60d > 0.01
    has_monotonicity = mono_20d > 0.5

    if has_positive_ic and has_bucket_spread and has_monotonicity:
        # Check if strong in both horizons
        if ic_mean_20d > 0.03 and ic_mean_60d > 0.03 and bucket_spread_20d > 0.01 and bucket_spread_60d > 0.02:
            return {
                "factor_id": factor_id,
                "sample_month_count": sample_count,
                "evidence_score": "PASS_RESEARCH_EVIDENCE",
                "rationale": f"Positive IC (20D={ic_mean_20d:.4f}, 60D={ic_mean_60d:.4f}), positive bucket spread, monotonic"
            }
        else:
            return {
                "factor_id": factor_id,
                "sample_month_count": sample_count,
                "evidence_score": "TACTICAL_ONLY",
                "rationale": f"Positive evidence but horizon-specific or regime-sensitive (IC={ic_mean_20d:.4f}/{ic_mean_60d:.4f})"
            }
    elif has_positive_ic or has_bucket_spread:
        return {
            "factor_id": factor_id,
            "sample_month_count": sample_count,
            "evidence_score": "WEAK_OR_UNSTABLE",
            "rationale": f"Mixed evidence (IC={ic_mean_20d:.4f}/{ic_mean_60d:.4f}, bucket={bucket_spread_20d:.4f}/{bucket_spread_60d:.4f})"
        }
    else:
        return {
            "factor_id": factor_id,
            "sample_month_count": sample_count,
            "evidence_score": "REJECTED",
            "rationale": f"No evidence of predictive power (IC={ic_mean_20d:.4f}/{ic_mean_60d:.4f}, spread={bucket_spread_20d:.4f}/{bucket_spread_60d:.4f})"
        }

per_factor = [score_factor("F03"), score_factor("F06")]
pass_count = sum(1 for f in per_factor if f["evidence_score"] == "PASS_RESEARCH_EVIDENCE")
tactical_count = sum(1 for f in per_factor if f["evidence_score"] == "TACTICAL_ONLY")
blocked_count = sum(1 for f in per_factor if "BLOCKED" in f["evidence_score"])
rejected_count = sum(1 for f in per_factor if f["evidence_score"] == "REJECTED")
weak_count = sum(1 for f in per_factor if f["evidence_score"] == "WEAK_OR_UNSTABLE")

scorecard = {
    "pipeline_signature": "Z2-V13-F2-3-EVIDENCE-SCORECARD",
    "status": "V13_F2_3_SINGLE_FACTOR_EVIDENCE_SCORECARD_BUILT",
    "validated_factors": ["F03", "F06"],
    "single_factor_validation_executed": True,
    "per_factor_evidence_scorecard": per_factor,
    "factor_pass_count": pass_count,
    "factor_tactical_count": tactical_count,
    "factor_weak_count": weak_count,
    "factor_blocked_count": blocked_count,
    "factor_rejected_count": rejected_count,
    "alpha_claim_allowed": False,
    "v13_6_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_3_single_factor_evidence_scorecard.json"
dst.write_text(json.dumps(scorecard, indent=2))
print(f"[F2.3-G] Evidence scorecard built -> {dst}")
sys.exit(0)
