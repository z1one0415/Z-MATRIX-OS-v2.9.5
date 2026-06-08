#!/usr/bin/env python3
"""V13.F3.1 — Stage G: candidate review scorecard."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTORS = ["F04", "F10", "F11"]

def load(name):
    return json.loads((BATCH / name).read_text()) if (BATCH / name).exists() else {}

packages = load("v13_f3_1_candidate_evidence_packages.json")
stability = load("v13_f3_1_signal_stability_review.json")
horizons = load("v13_f3_1_horizon_regime_review.json")
cost = load("v13_f3_1_cost_turnover_capacity_review.json")
overlap = load("v13_f3_1_factor_overlap_correlation_review.json")

per_decision = []
freeze_ready = []
tactical_ready = []
needs_oos = []
rework = []
rejected = []

for fid in FACTORS:
    ev_pkg = next((p for p in packages.get("evidence_packages", []) if p["factor_id"] == fid), {})
    sig = next((s for s in stability.get("per_factor_signal_stability", []) if s["factor_id"] == fid), {})
    hor = next((h for h in horizons.get("per_factor_horizon_regime", []) if h["factor_id"] == fid), {})
    co = next((c for c in cost.get("per_factor_cost_review", []) if c["factor_id"] == fid), {})

    sig_status = sig.get("signal_stability_status", "NEEDS_OOS")
    hor_verdict = hor.get("horizon_regime_verdict", "NEEDS_OOS")
    cost_fragile = co.get("cost_fragility", "COST_RESILIENT")
    ev = ev_pkg.get("evidence_score", "UNKNOWN")

    # Decision logic
    if ev == "PASS_RESEARCH_EVIDENCE" and sig_status == "PASS" and cost_fragile == "COST_RESILIENT":
        if hor_verdict == "FULL_HORIZON_CANDIDATE":
            decision = "FREEZE_CANDIDATE"
        elif hor_verdict == "REGIME_SPECIFIC_CANDIDATE":
            decision = "REGIME_SPECIFIC_CANDIDATE"
        else:
            decision = "TACTICAL_CANDIDATE"
        freeze_ready.append(fid)
    elif ev == "PASS_RESEARCH_EVIDENCE" and sig_status == "PASS" and cost_fragile != "COST_RESILIENT":
        decision = "TACTICAL_CANDIDATE"
        tactical_ready.append(fid)
    elif sig_status == "NEEDS_OOS":
        decision = "NEEDS_OOS"
        needs_oos.append(fid)
    elif sig_status == "REWORK":
        decision = "REWORK_REQUIRED"
        rework.append(fid)
    else:
        decision = "REJECTED"
        rejected.append(fid)

    per_decision.append({
        "factor_id": fid,
        "decision": decision,
        "decision_reasons": [
            f"evidence={ev}",
            f"signal_stability={sig_status}",
            f"horizon_regime={hor_verdict}",
            f"cost_fragility={cost_fragile}"
        ],
        "candidate_scope": {
            "allowed_horizons": hor.get("available_horizons", []),
            "blocked_horizons": [],
            "allowed_regimes": [],
            "blocked_regimes": []
        },
        "requires_oos": decision in ("NEEDS_OOS", "REWORK_REQUIRED"),
        "promotion_allowed": False,
        "alpha_claim_allowed": False
    })

scorecard = {
    "pipeline_signature": "Z2-V13-F3-1-CANDIDATE-REVIEW-SCORECARD",
    "status": "V13_F3_1_CANDIDATE_REVIEW_SCORECARD_BUILT",
    "reviewed_factors": FACTORS,
    "per_factor_candidate_decision": per_decision,
    "candidate_freeze_ready": freeze_ready,
    "tactical_candidate_ready": tactical_ready,
    "needs_oos_factors": needs_oos,
    "rework_required_factors": rework,
    "rejected_factors": rejected,
    "ready_for_f3_2_candidate_freeze_review": freeze_ready + tactical_ready,
    "ready_for_promotion_review": [],
    "multi_factor_composite_built": False, "v13_6_allowed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}
(BATCH / "v13_f3_1_candidate_review_scorecard.json").write_text(json.dumps(scorecard, indent=2))
print(f"[F3.1-G] Scorecard: freeze={freeze_ready} tactical={tactical_ready} oos={needs_oos} rework={rework} reject={rejected}")
sys.exit(0)
