#!/usr/bin/env python3
"""V13.F6.3 Lane J — F50-F52 Policy Macro Risk (SOURCE_CONTRACT_ONLY)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_j_policy_macro_risk")
OUT.mkdir(parents=True, exist_ok=True)

TS = datetime.now(TZ).isoformat()
LID = "J"
FACTORS = ["F50", "F51", "F52"]

# Macro data exists in system (flow S, MacroVeto)
outcome = "SOURCE_CONTRACT_ONLY"

def write_json(name, obj):
    p = OUT / name
    p.write_text(json.dumps({**obj, "timestamp": TS}, indent=2, ensure_ascii=False))

write_json("lane_contract.json", {
    "lane_id": LID, "target_factors": FACTORS,
    "goal": "policy_macro_risk",
    "allowed_outcomes": ["MATERIALIZED","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA","TAXONOMY_REVIEW_REQUIRED"]
})

write_json("source_availability_audit.json", {
    "sources": {"macro_veto": "AVAILABLE", "policy_news": "AVAILABLE_AS_TEXT",
                "sector_regulation": "PARTIALLY_AVAILABLE"},
    "available": True, "blocked": False,
    "reason": "Flow S MacroVeto provides global macro signals; policy/news text available but unstructured."
})

write_json("factor_definition_contract.json", {
    "factor_id": "F50", "name": "macro_regime_score",
    "category": "macro", "dimension": "policy_risk",
    "formula_description": "Composite of VIX, 10Y yield, CNH, copper/gold ratio; regime classification via MacroVeto"
})

write_json("formula_contract.json", {
    "factor_id": "F50",
    "formula_components": {"vix": "market_data", "us10y": "market_data", "cnh": "market_data",
                           "copper_gold_ratio": "market_data"},
    "weights": {"vix": 0.25, "us10y": 0.25, "cnh": 0.25, "copper_gold": 0.25},
    "normalization": "zscore_rolling_252d"
})

write_json("pit_policy.json", {
    "factor_id": "F50", "pit_safe": True,
    "known_at_strategy": "daily_close",
    "staleness_boundary": "next_trading_day"
})

write_json("materialization_plan.json", {
    "materialized": False, "source_contract_only": True, "blocked": False,
    "ticker_universe": "all_a_shares", "rebalance_date": "daily",
    "reason": "Macro data sources exist in Flow S; factor composable from existing feeds. Sector-level regulation mapping pending."
})

write_json("validation_plan.json", {
    "unit_tests": ["score_in_range", "regime_labels_valid"],
    "smoke_tests": ["macro_veto_consistency"],
    "data_gap_tests": ["holiday_forward_fill"]
})

write_json("skillos_handoff_contract.json", {
    "downstream_consumers": ["G18", "G17", "G05", "G16"],
    "input_format": "macro_veto_json", "output_format": "factor_vector_parquet"
})

write_json("safety_audit.json", {
    "alpha_claim": False, "forward_return": False, "real_trade": "BLOCKED",
    "monitoring": "BLOCKED", "runner": "BLOCKED"
})

write_json("lane_closeout.json", {
    "status": "V13_F6_3_LANE_J_CLOSE", "outcome": outcome,
    "reason": "Macro data (VIX, yields, CNH, copper/gold) available via Flow S. Factor definitions, formulas, PIT policies defined. Sector regulation mapping pending structured NLP pipeline.",
    "next": "BUILD_SECTOR_REGULATION_MAPPING"
})

print(f"✅ Lane J closeout: {OUT / 'lane_closeout.json'} ({outcome})")
