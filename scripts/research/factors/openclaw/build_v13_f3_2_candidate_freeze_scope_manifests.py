#!/usr/bin/env python3
"""V13.F3.2 — Stage B: candidate freeze scope manifests."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
sc = json.loads((BATCH / "v13_f3_1_candidate_review_scorecard.json").read_text()) if (BATCH / "v13_f3_1_candidate_review_scorecard.json").exists() else {"per_factor_candidate_decision": []}
decisions = {d["factor_id"]: d for d in sc.get("per_factor_candidate_decision", [])}

f04 = decisions.get("F04", {})
f10 = decisions.get("F10", {})
f11 = decisions.get("F11", {})

manifests = [
    {
        "factor_id": "F04", "factor_name": "RESIDUAL_MOMENTUM",
        "freeze_status": "FROZEN_CANDIDATE",
        "candidate_type": "FULL_HORIZON_RESEARCH_CANDIDATE",
        "source_decision": "V13.F3.1",
        "allowed_horizons": ["20D", "60D"], "blocked_horizons": [],
        "allowed_regimes": ["ALL_RESEARCH_REGIMES"], "blocked_regimes": [],
        "known_risks": f04.get("decision_reasons", []),
        "requires_true_oos_before_promotion": True,
        "promotion_allowed": False, "alpha_claim_allowed": False
    },
    {
        "factor_id": "F10", "factor_name": "LOW_VOLATILITY",
        "freeze_status": "FROZEN_CANDIDATE",
        "candidate_type": "REGIME_SPECIFIC_RESEARCH_CANDIDATE",
        "source_decision": "V13.F3.1",
        "allowed_horizons": ["20D", "60D"],
        "preferred_regimes": ["DOWN_MARKET", "HIGH_VOLATILITY"],
        "risk_flags": ["MAY_UNDERPERFORM_IN_STRONG_UP_MARKET"],
        "requires_regime_gate_before_use": True,
        "requires_true_oos_before_promotion": True,
        "promotion_allowed": False, "alpha_claim_allowed": False
    },
    {
        "factor_id": "F11", "factor_name": "SHORT_TERM_REVERSAL",
        "freeze_status": "FROZEN_TACTICAL_CANDIDATE",
        "candidate_type": "TACTICAL_RESEARCH_CANDIDATE",
        "source_decision": "V13.F3.1",
        "allowed_horizons": ["5D", "20D"],
        "blocked_horizons": ["60D_FOR_STANDALONE_USE"],
        "risk_flags": ["COST_FRAGILE_HIGH_TURNOVER", "TACTICAL_ONLY"],
        "requires_cost_gate_before_use": True,
        "requires_true_oos_before_promotion": True,
        "promotion_allowed": False, "alpha_claim_allowed": False
    }
]
(BATCH / "v13_f3_2_candidate_freeze_scope_manifests.json").write_text(json.dumps(manifests, indent=2))
print(f"[F3.2-B] Scope manifests built: {[m['factor_id'] for m in manifests]}")
sys.exit(0)
