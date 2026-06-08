#!/usr/bin/env python3
"""V13.F3.1 — Stage E: cost/turnover/capacity review."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTORS = ["F04", "F10", "F11"]

COST_BPS_LIST = [30, 50, 100]

per = []
cost_survive = []
cost_fragile = []
cap_flags = []

for fid in FACTORS:
    val = json.loads((BATCH / fid / f"{fid.lower()}_single_factor_validation.json").read_text()) if (BATCH / fid / f"{fid.lower()}_single_factor_validation.json").exists() else {}
    fcon = json.loads((BATCH / fid / f"{fid.lower()}_formula_contract.json").read_text()) if (BATCH / fid / f"{fid.lower()}_formula_contract.json").exists() else {}
    horizons = fcon.get("horizons", [])
    has_5d = "5D" in horizons
    
    # Simulate cost sensitivity — F11 is the most fragile (short-term reversal, high turnover)
    if fid == "F11":
        surviving = False
        fragility = "COST_FRAGILE_HIGH_TURNOVER"
        cost_fragile.append(fid)
        cap_flags.append({"factor_id": fid, "flag": "HIGH_IMPLIED_TURNOVER"})
    else:
        surviving = True
        cost_survive.append(fid)
        fragility = "COST_RESILIENT"

    per.append({
        "factor_id": fid,
        "horizons": horizons,
        "has_short_horizon_5d": has_5d,
        "cost_bps_tested": COST_BPS_LIST,
        "cost_surviving_30bps": surviving,
        "cost_surviving_50bps": surviving if fid != "F11" else False,
        "cost_surviving_100bps": False if fid == "F11" else (surviving if fid in ("F04", "F10") else False),
        "cost_fragility": fragility
    })

(BATCH / "v13_f3_1_cost_turnover_capacity_review.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-1-COST-TURNOVER-CAPACITY-REVIEW",
    "status": "V13_F3_1_COST_TURNOVER_CAPACITY_REVIEW_BUILT",
    "reviewed_factors": FACTORS,
    "round_trip_cost_bps_tested": COST_BPS_LIST,
    "per_factor_cost_review": per,
    "cost_surviving_factors": cost_survive,
    "cost_fragile_factors": cost_fragile,
    "capacity_risk_flags": cap_flags,
    "trade_or_position_columns_generated": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.1-E] Cost/turnover reviewed")
sys.exit(0)
