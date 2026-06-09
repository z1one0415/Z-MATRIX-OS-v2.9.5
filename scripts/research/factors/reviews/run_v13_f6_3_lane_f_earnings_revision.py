#!/usr/bin/env python3
"""V13.F6.3 Lane F — F09 Earnings Revision (BLOCKED: no analyst expectations data)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_f_earnings_revision")
OUT.mkdir(parents=True, exist_ok=True)

TS = datetime.now(TZ).isoformat()
LID = "F"
FACTORS = ["F09"]

# No sell-side analyst revision data in current system
outcome = "BLOCKED_BY_SOURCE_DATA"

def write_json(name, obj):
    p = OUT / name
    p.write_text(json.dumps({**obj, "timestamp": TS}, indent=2, ensure_ascii=False))

write_json("lane_contract.json", {
    "lane_id": LID, "target_factors": FACTORS,
    "goal": "earnings_revision_or_proxy",
    "allowed_outcomes": ["MATERIALIZED","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA"]
})

write_json("source_availability_audit.json", {
    "sources": {"analyst_earnings_forecast": "NOT_AVAILABLE", "analyst_revision": "NOT_AVAILABLE"},
    "available": False, "blocked": True,
    "reason": "No sell-side analyst consensus/revision data feed in current pipeline. Would need external API (Wind, Bloomberg, Refinitiv)."
})

write_json("factor_definition_contract.json", {
    "factor_id": "F09", "name": "earnings_revision_diffusion",
    "category": "sentiment", "dimension": "analyst_expectations",
    "formula_description": "SUM(analyst_revision[up/down]) / NUM_COVERING; 4-week window; requires external data feed"
})

write_json("formula_contract.json", {
    "factor_id": "F09",
    "formula_components": {"num_upgrades": "external", "num_downgrades": "external", "num_covering": "external"},
    "weights": {},
    "normalization": "cross_sectional_zscore",
    "blocked": True
})

write_json("pit_policy.json", {
    "factor_id": "F09", "pit_safe": True,
    "known_at_strategy": "T+1 from analyst report publish",
    "staleness_boundary": "30_days",
    "blocked": True
})

write_json("materialization_plan.json", {
    "materialized": False, "source_contract_only": False, "blocked": True,
    "ticker_universe": "N/A", "rebalance_date": "N/A",
    "reason": "No analyst data source"
})

write_json("validation_plan.json", {
    "unit_tests": "BLOCKED", "smoke_tests": "BLOCKED", "data_gap_tests": "BLOCKED"
})

write_json("skillos_handoff_contract.json", {
    "downstream_consumers": ["G18", "G17"],
    "input_format": "N/A", "output_format": "N/A",
    "blocked": True
})

write_json("safety_audit.json", {
    "alpha_claim": False, "forward_return": False, "real_trade": "BLOCKED",
    "monitoring": "BLOCKED", "runner": "BLOCKED"
})

write_json("lane_closeout.json", {
    "status": "V13_F6_3_LANE_F_CLOSE", "outcome": outcome,
    "reason": "No analyst EPS/revision data feed; factor cannot be computed. Unblock requires Wind/Bloomberg integration.",
    "next": "INTEGRATE_ANALYST_DATA_FEED_THEN_RERUN"
})

print(f"✅ Lane F closeout: {OUT / 'lane_closeout.json'} ({outcome})")
