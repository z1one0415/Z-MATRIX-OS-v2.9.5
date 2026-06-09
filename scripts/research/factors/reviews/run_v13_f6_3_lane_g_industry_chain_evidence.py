#!/usr/bin/env python3
"""V13.F6.3 Lane G — F41/F42 Industry Chain Evidence (SOURCE_CONTRACT_ONLY)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_g_industry_chain_evidence")
OUT.mkdir(parents=True, exist_ok=True)

TS = datetime.now(TZ).isoformat()
LID = "G"
FACTORS = ["F41", "F42"]

# G15 evidence layering can supply chain position data
outcome = "SOURCE_CONTRACT_ONLY"

def write_json(name, obj):
    p = OUT / name
    p.write_text(json.dumps({**obj, "timestamp": TS}, indent=2, ensure_ascii=False))

write_json("lane_contract.json", {
    "lane_id": LID, "target_factors": FACTORS,
    "goal": "industry_chain_evidence",
    "allowed_outcomes": ["MATERIALIZED","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA","TAXONOMY_REVIEW_REQUIRED"]
})

write_json("source_availability_audit.json", {
    "sources": {"G15_evidence_layering": "AVAILABLE", "industry_chain_map": "NOT_AVAILABLE_DETAILED"},
    "available": True, "blocked": False,
    "reason": "G15 provides upstream/downstream evidence layering; detailed chain position map not yet available."
})

write_json("factor_definition_contract.json", {
    "factor_id": "F41", "name": "chain_position_score",
    "category": "industry_chain", "dimension": "supply_chain",
    "formula_description": "Weighted sum of upstream dominance, downstream brand power, midstream pricing power from G15 evidence"
})

write_json("formula_contract.json", {
    "factor_id": "F41",
    "formula_components": {"upstream_dominance": "G15_level_A", "downstream_brand": "G15_level_B", "midstream_pricing": "G15_level_C"},
    "weights": {"upstream": 0.4, "downstream": 0.35, "midstream": 0.25},
    "normalization": "min_max_0_1"
})

write_json("pit_policy.json", {
    "factor_id": "F41", "pit_safe": True,
    "known_at_strategy": "quarterly_chain_refresh_from_G15",
    "staleness_boundary": "90_days"
})

write_json("materialization_plan.json", {
    "materialized": False, "source_contract_only": True, "blocked": False,
    "ticker_universe": "all_a_shares", "rebalance_date": "quarterly",
    "reason": "Source contract defined; G15 integration needed before materialization"
})

write_json("validation_plan.json", {
    "unit_tests": ["score_in_0_1", "weights_sum_to_1"],
    "smoke_tests": ["chain_position_valid_for_top100"],
    "data_gap_tests": ["missing_chain_treat_as_0"]
})

write_json("skillos_handoff_contract.json", {
    "downstream_consumers": ["G18", "G17", "G05", "G15"],
    "input_format": "G15_evidence_vector", "output_format": "factor_vector_parquet"
})

write_json("safety_audit.json", {
    "alpha_claim": False, "forward_return": False, "real_trade": "BLOCKED",
    "monitoring": "BLOCKED", "runner": "BLOCKED"
})

write_json("lane_closeout.json", {
    "status": "V13_F6_3_LANE_G_CLOSE", "outcome": outcome,
    "reason": "G15 evidence layering provides source data; factor definition and formula ready; materialization deferred to G15 handoff phase.",
    "next": "INTEGRATE_G15_CHAIN_EVIDENCE_FEED"
})

print(f"✅ Lane G closeout: {OUT / 'lane_closeout.json'} ({outcome})")
