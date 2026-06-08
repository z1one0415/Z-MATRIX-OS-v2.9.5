#!/usr/bin/env python3
"""V13.F3.4 — Stage F: per-factor OOS acceptance criteria."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_4_per_factor_oos_acceptance_criteria.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-PER-FACTOR-OOS-ACCEPTANCE-CRITERIA",
    "status": "V13_F3_4_PER_FACTOR_OOS_ACCEPTANCE_CRITERIA_BUILT",
    "criteria": [
        {"factor_id": "F04", "candidate_type": "FULL_HORIZON_RESEARCH_CANDIDATE",
         "required_horizons": ["20D","60D"], "minimum_oos_months": 6, "preferred_oos_months": 12,
         "required_checks": ["rank_ic_positive","bucket_spread_positive","cost_adjusted_spread_positive","month_concentration_not_detected","coverage_u475"],
         "pass_scope": "FULL_HORIZON_OR_NEEDS_REVIEW"},
        {"factor_id": "F10", "candidate_type": "REGIME_SPECIFIC_RESEARCH_CANDIDATE",
         "required_horizons": ["20D","60D"], "required_gate": "REGIME_GATE_FOR_F10",
         "minimum_oos_months": 6, "preferred_oos_months": 12,
         "required_checks": ["regime_gate_label_available","regime_conditioned_spread_positive","down_market_or_high_volatility_effect_confirmed","coverage_u475"],
         "pass_scope": "REGIME_SPECIFIC_OR_NEEDS_REVIEW"},
        {"factor_id": "F11", "candidate_type": "TACTICAL_RESEARCH_CANDIDATE",
         "required_horizons": ["5D","20D"], "blocked_horizons": ["60D_FOR_STANDALONE_USE"],
         "required_gate": "COST_TURNOVER_GATE_FOR_F11",
         "minimum_oos_months": 6, "preferred_oos_months": 12,
         "required_checks": ["cost_gate_label_available","cost_adjusted_spread_positive_30bps","cost_adjusted_spread_positive_50bps","turnover_risk_not_excessive","coverage_u475"],
         "pass_scope": "TACTICAL_OR_NEEDS_REVIEW"}
    ],
    "oos_validation_executed": False, "promotion_allowed": False, "alpha_claim_allowed": False
}, indent=2))
print("[F3.4-F] Per-factor criteria built")
sys.exit(0)
