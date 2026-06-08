#!/usr/bin/env python3
"""V13.F2.3.2 — Stage F: F03R materialization planning only."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

contract = {
    "pipeline_signature": "Z2-V13-F2-3-2-F03R-MATERIALIZATION-PLANNING",
    "status": "F03R_MATERIALIZATION_PLANNING_CONTRACT_BUILT",
    "hypothesis_id": "F03R",
    "hypothesis_name": "INDUSTRY_RELATIVE_REVERSAL",
    "parent_factor_id": "F03",
    "parent_factor_status": "REJECTED_CURRENT_DIRECTION",
    "proposed_formula": "industry_relative_reversal_score = -1 * industry_relative_strength_score",
    "planning_only": True,
    "materialization_executed": False,
    "validation_executed": False,
    "data_snooping_risk_acknowledged": True,
    "same_sample_validation_for_promotion_forbidden": True,
    "requires_separate_holdout_or_future_oos_validation": True,
    "promotion_review_allowed": False,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "f03r_materialization_planning_contract.json"
dst.write_text(json.dumps(contract, indent=2))
print(f"[F2.3.2-F] F03R planning contract built -> {dst}")
sys.exit(0)
