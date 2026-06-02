#!/usr/bin/env python3
"""V11.5-B: Build paper portfolio rules."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
r={"status":"V11_5_PORTFOLIO_RULES_BUILT","rebalance_frequency":"MONTHLY","holding_horizons":["T20","T60"],"weighting_method":"EQUAL_WEIGHT","selection_policy":"ACTIVE_PAPER_WATCH_ONLY","mixed_direction_policy":"EXCLUDE_FROM_PORTFOLIO_SIMULATION","watch_with_limitation_policy":"EXCLUDE_FROM_PORTFOLIO_SIMULATION","max_single_name_weight":0.10,"cost_proxy_bps":15,"round_trip_cost_bps":30,"portfolio_action":"PAPER_ONLY","investment_action":"NONE","ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(r,open(C/"v11_5_portfolio_rules.json","w"),indent=2)
print("Rules built")
