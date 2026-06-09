#!/usr/bin/env python3
"""V13.F6.3 Lane H — F43-F46 Operating Cycle (BLOCKED_BY_SOURCE_DATA)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_h_operating_cycle")
OUT.mkdir(parents=True, exist_ok=True)

TS = datetime.now(TZ).isoformat()
LID = "H"
FACTORS = ["F43", "F44", "F45", "F46"]

# Order/inventory/capacity data not available at ticker level in current pipeline
outcome = "BLOCKED_BY_SOURCE_DATA"

def write_json(name, obj):
    p = OUT / name
    p.write_text(json.dumps({**obj, "timestamp": TS}, indent=2, ensure_ascii=False))

write_json("lane_contract.json", {
    "lane_id": LID, "target_factors": FACTORS,
    "goal": "operating_cycle",
    "allowed_outcomes": ["MATERIALIZED","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA","TAXONOMY_REVIEW_REQUIRED"]
})

write_json("source_availability_audit.json", {
    "sources": {"order_backlog": "NOT_AVAILABLE", "inventory_turnover": "NOT_AVAILABLE",
                "capacity_utilization": "NOT_AVAILABLE", "cash_conversion_cycle": "PARTIAL_VIA_STATEMENTS"},
    "available": False, "blocked": True,
    "reason": "Operating cycle data (order backlog, real-time inventory, capacity utilization) require order-level or industrial data feeds not in current pipeline."
})

write_json("factor_definition_contract.json", {
    "factor_id": "F43", "name": "cash_conversion_cycle",
    "category": "efficiency", "dimension": "operating_cycle",
    "formula_description": "DIO + DSO - DPO; days inventory outstanding + days sales outstanding - days payable outstanding"
})

write_json("formula_contract.json", {
    "factor_id": "F43",
    "formula_components": {"avr_inventory": "balance_sheet", "cogs": "income", "avr_receivables": "balance_sheet",
                           "revenue": "income", "avr_payables": "balance_sheet"},
    "weights": {},
    "normalization": "cross_sectional_zscore",
    "blocked": True
})

write_json("pit_policy.json", {
    "factor_id": "F43", "pit_safe": True,
    "known_at_strategy": "T+1 after quarterly statement",
    "staleness_boundary": "next_report_date",
    "blocked": True
})

write_json("materialization_plan.json", {
    "materialized": False, "source_contract_only": False, "blocked": True,
    "ticker_universe": "N/A", "rebalance_date": "N/A"
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
    "status": "V13_F6_3_LANE_H_CLOSE", "outcome": outcome,
    "reason": "Order-level inventory/capacity data unavailable. Cash conversion cycle composable from statements but requires daily balance sheet which current pipeline does not supply.",
    "next": "SOURCE_ORDER_CAPACITY_DATA_FEED"
})

print(f"✅ Lane H closeout: {OUT / 'lane_closeout.json'} ({outcome})")
