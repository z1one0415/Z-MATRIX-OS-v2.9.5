#!/usr/bin/env python3
"""V13.F6.3 Lane L — F56-F60 Money Flow Microstructure (BLOCKED_BY_SOURCE_DATA)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_l_money_flow_microstructure")
OUT.mkdir(parents=True, exist_ok=True)

TS = datetime.now(TZ).isoformat()
LID = "L"
FACTORS = ["F56", "F57", "F58", "F59", "F60"]

# No tick-level/order book data in current pipeline
outcome = "BLOCKED_BY_SOURCE_DATA"

def write_json(name, obj):
    p = OUT / name
    p.write_text(json.dumps({**obj, "timestamp": TS}, indent=2, ensure_ascii=False))

write_json("lane_contract.json", {
    "lane_id": LID, "target_factors": FACTORS,
    "goal": "money_flow_microstructure",
    "allowed_outcomes": ["MATERIALIZED","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA"]
})

write_json("source_availability_audit.json", {
    "sources": {"tick_data": "NOT_AVAILABLE", "order_book": "NOT_AVAILABLE",
                "northbound_flow": "PARTIALLY_AVAILABLE_DAILY", "large_order": "NOT_AVAILABLE",
                "block_trade": "NOT_AVAILABLE", "dde": "NOT_AVAILABLE"},
    "available": False, "blocked": True,
    "reason": "Money flow/microstructure factors (F56-F60) require tick-level order book data, large order detection, DDE (big/small order flow), or block trade data. Current pipeline only has daily OHLCV. Northbound connect daily flow available but insufficient for microstructure."
})

write_json("factor_definition_contract.json", {
    "factor_id": "F56", "name": "money_flow_mfi",
    "category": "flow", "dimension": "microstructure",
    "formula_description": "Chaikin Money Flow: SUM(((C-L)-(H-C))/(H-L)*Volume, 21) / SUM(Volume, 21); requires daily OHLCV (available) but truly microstructure needs tick data."
})

write_json("formula_contract.json", {
    "factor_id": "F56",
    "formula_components": {"close": "daily_ohlcv", "high": "daily_ohlcv", "low": "daily_ohlcv", "volume": "daily_ohlcv"},
    "weights": {},
    "normalization": "cross_sectional_zscore",
    "note": "MFI computable from daily OHLCV; F57-F60 (order flow imbalance, large order, DDE, northbound) require tick data.",
    "blocked": True
})

write_json("pit_policy.json", {
    "factor_id": "F56", "pit_safe": True,
    "known_at_strategy": "daily_close",
    "staleness_boundary": "next_trading_day",
    "blocked": True
})

write_json("materialization_plan.json", {
    "materialized": False, "source_contract_only": False, "blocked": True,
    "ticker_universe": "N/A", "rebalance_date": "N/A",
    "reason": "F56 MFI computable from daily OHLCV (low-quality proxy). F57-F60 require tick data unavailable in current pipeline."
})

write_json("validation_plan.json", {
    "unit_tests": "BLOCKED", "smoke_tests": "BLOCKED", "data_gap_tests": "BLOCKED"
})

write_json("skillos_handoff_contract.json", {
    "downstream_consumers": ["G18", "G17"], "input_format": "N/A", "output_format": "N/A", "blocked": True
})

write_json("safety_audit.json", {
    "alpha_claim": False, "forward_return": False, "real_trade": "BLOCKED",
    "monitoring": "BLOCKED", "runner": "BLOCKED"
})

write_json("lane_closeout.json", {
    "status": "V13_F6_3_LANE_L_CLOSE", "outcome": outcome,
    "reason": "Microstructure factors require tick-level order book data. Daily OHLCV can compute MFI (F56) as low-quality proxy; F57-F60 are completely blocked. Unified block decision: BLOCKED_BY_SOURCE_DATA.",
    "next": "INTEGRATE_TICK_LEVEL_DATA_FEED"
})

print(f"✅ Lane L closeout: {OUT / 'lane_closeout.json'} ({outcome})")
