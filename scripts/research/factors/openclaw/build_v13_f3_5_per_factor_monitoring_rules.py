#!/usr/bin/env python3
"""V13.F3.5 — Stage C: per-factor monitoring rules."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_5_per_factor_monitoring_rules.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-5-PER-FACTOR-MONITORING-RULES",
    "status": "V13_F3_5_PER_FACTOR_MONITORING_RULES_BUILT",
    "rules": [
        {"factor_id": "F04", "candidate_type": "FULL_HORIZON_RESEARCH_CANDIDATE",
         "monitoring_horizons": ["20D","60D"],
         "required_monthly_checks": ["rank_ic_20d","rank_ic_60d","bucket_spread_20d","bucket_spread_60d","cost_adjusted_spread","month_concentration","coverage_u475"],
         "retain_condition": "rank_ic_positive_or_bucket_spread_positive_without_month_concentration",
         "warning_condition": "two_consecutive_months_negative_or_spread_decay",
         "suspension_condition": "three_consecutive_months_negative_and_cost_adjusted_spread_negative",
         "promotion_allowed": False},
        {"factor_id": "F10", "candidate_type": "REGIME_SPECIFIC_RESEARCH_CANDIDATE",
         "monitoring_horizons": ["20D","60D"], "required_gate": "REGIME_GATE_FOR_F10",
         "required_monthly_checks": ["regime_state","regime_gate_pass","regime_conditioned_spread","down_market_effect","high_volatility_effect","coverage_u475"],
         "retain_condition": "positive_effect_when_regime_gate_passes",
         "warning_condition": "regime_gate_passes_but_spread_negative",
         "suspension_condition": "two_regime_gate_months_negative_or_regime_definition_unstable",
         "promotion_allowed": False},
        {"factor_id": "F11", "candidate_type": "TACTICAL_RESEARCH_CANDIDATE",
         "monitoring_horizons": ["5D","20D"], "blocked_horizons": ["60D_FOR_STANDALONE_USE"],
         "required_gate": "COST_TURNOVER_GATE_FOR_F11",
         "required_monthly_checks": ["cost_turnover_gate_pass","cost_adjusted_spread_30bps","cost_adjusted_spread_50bps","turnover_estimate","spread_proxy","coverage_u475"],
         "retain_condition": "cost_adjusted_spread_positive_when_cost_gate_passes",
         "warning_condition": "raw_spread_positive_but_cost_adjusted_spread_negative",
         "suspension_condition": "two_consecutive_cost_adjusted_negative_months_or_turnover_excessive",
         "promotion_allowed": False}
    ],
    "monitoring_execution_executed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.5-C] Per-factor rules built")
sys.exit(0)
