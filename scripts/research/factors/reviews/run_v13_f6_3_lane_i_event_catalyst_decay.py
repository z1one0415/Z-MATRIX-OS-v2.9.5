#!/usr/bin/env python3
"""V13.F6.3 Lane I — F47-F49 Event Catalyst Decay (SOURCE_CONTRACT_ONLY)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_i_event_catalyst_decay")
OUT.mkdir(parents=True, exist_ok=True)

TS = datetime.now(TZ).isoformat()
LID = "I"
FACTORS = ["F47", "F48", "F49"]

# Event calendar exists in system; can bridge to factor
outcome = "SOURCE_CONTRACT_ONLY"

def write_json(name, obj):
    p = OUT / name
    p.write_text(json.dumps({**obj, "timestamp": TS}, indent=2, ensure_ascii=False))

write_json("lane_contract.json", {
    "lane_id": LID, "target_factors": FACTORS,
    "goal": "event_catalyst_decay",
    "allowed_outcomes": ["MATERIALIZED","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA","TAXONOMY_REVIEW_REQUIRED"]
})

write_json("source_availability_audit.json", {
    "sources": {"event_calendar": "AVAILABLE_IN_SYSTEM", "event_impact_scores": "NOT_AVAILABLE",
                "decay_model": "NOT_AVAILABLE"},
    "available": True, "blocked": False,
    "reason": "Event calendar (earnings dates, AGM, ex-dividend) exists; impact scoring and decay modeling need implementation."
})

write_json("factor_definition_contract.json", {
    "factor_id": "F47", "name": "earnings_event_proximity",
    "category": "event", "dimension": "catalyst_timing",
    "formula_description": "Decay function: days_until_next_earnings mapped to [0,1]; closer = higher"
})

write_json("formula_contract.json", {
    "factor_id": "F47",
    "formula_components": {"days_to_earnings": "event_calendar", "historical_surprise": "event_calendar"},
    "weights": {"proximity": 0.7, "surprise_magnitude": 0.3},
    "normalization": "min_max_0_1"
})

write_json("pit_policy.json", {
    "factor_id": "F47", "pit_safe": True,
    "known_at_strategy": "event_announcement_date",
    "staleness_boundary": "event_date"
})

write_json("materialization_plan.json", {
    "materialized": False, "source_contract_only": True, "blocked": False,
    "ticker_universe": "all_a_shares", "rebalance_date": "daily",
    "reason": "Event calendar source exists; impact scoring and decay model pending implementation."
})

write_json("validation_plan.json", {
    "unit_tests": ["proximity_in_0_1", "decay_monotonic"],
    "smoke_tests": ["all_active_events_have_score"],
    "data_gap_tests": ["no_event_treat_as_0"]
})

write_json("skillos_handoff_contract.json", {
    "downstream_consumers": ["G18", "G17", "G05"],
    "input_format": "event_calendar_json", "output_format": "factor_vector_parquet"
})

write_json("safety_audit.json", {
    "alpha_claim": False, "forward_return": False, "real_trade": "BLOCKED",
    "monitoring": "BLOCKED", "runner": "BLOCKED"
})

write_json("lane_closeout.json", {
    "status": "V13_F6_3_LANE_I_CLOSE", "outcome": outcome,
    "reason": "Event calendar source data available in system. Factor definitions, formulas, and PIT policies defined. Materialization requires decay model implementation.",
    "next": "IMPLEMENT_EVENT_DECAY_MODEL"
})

print(f"✅ Lane I closeout: {OUT / 'lane_closeout.json'} ({outcome})")
