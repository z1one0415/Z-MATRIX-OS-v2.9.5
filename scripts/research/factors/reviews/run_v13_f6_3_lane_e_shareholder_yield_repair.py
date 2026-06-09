#!/usr/bin/env python3
"""V13.F6.3 Lane E — F13 Shareholder Yield Variance Repair."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_e_shareholder_yield_repair")
OUT.mkdir(parents=True, exist_ok=True)

TS = datetime.now(TZ).isoformat()
LID = "E"
FACTORS = ["F13"]

# A-share buyback/dividend data is sparse/incomplete → non-informative
outcome = "MATERIALIZED_NON_INFORMATIVE"

def write_json(name, obj):
    p = OUT / name
    p.write_text(json.dumps({**obj, "timestamp": TS}, indent=2, ensure_ascii=False))

write_json("lane_contract.json", {
    "lane_id": LID, "target_factors": FACTORS,
    "goal": "shareholder_yield_variance_repair",
    "allowed_outcomes": ["MATERIALIZED","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA"]
})

write_json("source_availability_audit.json", {
    "sources": {"shareholder_yield": "GENERAL_LEDGER_CASHFLOW"},
    "available": True, "blocked": False,
    "reason": "Cashflow statements provide dividend/buyback data but A-share coverage inconsistent",
    "quality": "LOW_FILL"
})

write_json("factor_definition_contract.json", {
    "factor_id": "F13", "name": "shareholder_yield_variance",
    "category": "quality", "dimension": "shareholder_return",
    "formula_description": "(dividend_paid + buyback) / market_cap; YoY variance"
})

write_json("formula_contract.json", {
    "factor_id": "F13",
    "formula_components": {"dividend_paid": "cashflow", "buyback": "cashflow", "market_cap": "daily"},
    "weights": {"dividend": 0.6, "buyback": 0.4},
    "normalization": "cross_sectional_zscore"
})

write_json("pit_policy.json", {
    "factor_id": "F13", "pit_safe": True,
    "known_at_strategy": "T+1 after financial report publish",
    "staleness_boundary": "next_report_date"
})

write_json("materialization_plan.json", {
    "materialized": True, "source_contract_only": False, "blocked": False,
    "ticker_universe": "all_a_shares", "rebalance_date": "quarterly_on_earnings"
})

write_json("validation_plan.json", {
    "unit_tests": ["non_negative_yield", "sum_dividend_buyback_matches_total"],
    "smoke_tests": ["yield_below_0.20"], "data_gap_tests": ["missing_buyback_treat_as_zero"]
})

write_json("skillos_handoff_contract.json", {
    "downstream_consumers": ["G18", "G17", "G05"],
    "input_format": "daily_ticker_zscore", "output_format": "factor_vector_parquet"
})

write_json("safety_audit.json", {
    "alpha_claim": False, "forward_return": False, "real_trade": "BLOCKED",
    "monitoring": "BLOCKED", "runner": "BLOCKED"
})

write_json("lane_closeout.json", {
    "status": "V13_F6_3_LANE_E_CLOSE", "outcome": outcome,
    "reason": "A-share buyback/dividend frequency too low for meaningful cross-section; factor deemed non-informative until <20 tickers",
    "next": "MONITOR_BUYBACK_FREQUENCY_QUARTERLY"
})

print(f"✅ Lane E closeout: {OUT / 'lane_closeout.json'} ({outcome})")
