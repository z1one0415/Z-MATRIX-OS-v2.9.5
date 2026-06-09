#!/usr/bin/env python3
"""V13.F6.3 Lane K — F16/F53-F55 Sentiment Attention Crowding (TAXONOMY_REVIEW_REQUIRED)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_k_sentiment_attention_crowding")
OUT.mkdir(parents=True, exist_ok=True)

TS = datetime.now(TZ).isoformat()
LID = "K"
FACTORS = ["F16", "F53", "F54", "F55"]

# F16 needs redefinition as PRICE_VOLUME_ATTENTION before proceeding
outcome = "TAXONOMY_REVIEW_REQUIRED"

def write_json(name, obj):
    p = OUT / name
    p.write_text(json.dumps({**obj, "timestamp": TS}, indent=2, ensure_ascii=False))

write_json("lane_contract.json", {
    "lane_id": LID, "target_factors": FACTORS,
    "goal": "sentiment_attention_crowding",
    "allowed_outcomes": ["MATERIALIZED","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA","TAXONOMY_REVIEW_REQUIRED"]
})

write_json("source_availability_audit.json", {
    "sources": {"market_volume": "AVAILABLE", "price_data": "AVAILABLE",
                "social_sentiment": "NOT_AVAILABLE", "news_sentiment": "PARTIALLY_AVAILABLE_AS_TEXT",
                "crowding_metrics": "NOT_AVAILABLE"},
    "available": True, "blocked": False,
    "reason": "Price and volume data available. F16 currently defined as sentiment factor; redefinition to PRICE_VOLUME_ATTENTION required before proceeding. Social sentiment NLP pipeline not available."
})

write_json("factor_definition_contract.json", {
    "factor_id": "F16", "name": "price_volume_attention",
    "category": "attention", "dimension": "crowding",
    "formula_description": "TBD: F16 needs redefinition from sentiment to PRICE_VOLUME_ATTENTION. Proposed: abnormal_volume / average_volume + relative_strength_zscore composite.",
    "taxonomy_review": True,
    "review_reason": "F16 label 'sentiment' conflicts with actual computable data (price/volume). Must be reclassified as PRICE_VOLUME_ATTENTION in factor taxonomy before formula can be finalized."
})

write_json("formula_contract.json", {
    "factor_id": "F16",
    "formula_components": {"TBD": "pending_taxonomy_review"},
    "weights": {},
    "normalization": "TBD",
    "taxonomy_review": True
})

write_json("pit_policy.json", {
    "factor_id": "F16", "pit_safe": True,
    "known_at_strategy": "daily_close",
    "staleness_boundary": "next_trading_day",
    "taxonomy_review": True
})

write_json("materialization_plan.json", {
    "materialized": False, "source_contract_only": False, "blocked": False,
    "ticker_universe": "all_a_shares", "rebalance_date": "TBD",
    "reason": "Blocked pending F16 taxonomy reclassification"
})

write_json("validation_plan.json", {
    "unit_tests": "BLOCKED_TAXONOMY", "smoke_tests": "BLOCKED_TAXONOMY",
    "data_gap_tests": "BLOCKED_TAXONOMY"
})

write_json("skillos_handoff_contract.json", {
    "downstream_consumers": ["G18", "G17"],
    "input_format": "TBD", "output_format": "TBD",
    "taxonomy_review": True
})

write_json("safety_audit.json", {
    "alpha_claim": False, "forward_return": False, "real_trade": "BLOCKED",
    "monitoring": "BLOCKED", "runner": "BLOCKED"
})

write_json("lane_closeout.json", {
    "status": "V13_F6_3_LANE_K_CLOSE", "outcome": outcome,
    "reason": "F16 is labeled as 'sentiment' in taxonomy but system only has price/volume data (no NLP sentiment pipeline). Must be reclassified as PRICE_VOLUME_ATTENTION before factor can be finalized. F53-F55 (crowding) also depend on this reclassification.",
    "next": "EXECUTE_F16_TAXONOMY_REDEFINITION_TO_PRICE_VOLUME_ATTENTION"
})

print(f"✅ Lane K closeout: {OUT / 'lane_closeout.json'} ({outcome})")
