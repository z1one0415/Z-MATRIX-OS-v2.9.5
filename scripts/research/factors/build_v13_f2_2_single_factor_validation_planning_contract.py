#!/usr/bin/env python3
"""V13.F2.2 — Stage A: single factor validation planning contract."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"
RUNTIME.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F2-2-PLANNING-CONTRACT",
    "status": "V13_F2_2_SINGLE_FACTOR_VALIDATION_PLANNING_CONTRACT_BUILT",
    "v13_f2_2_executed": True,
    "planning_only": True,
    "validation_executed": False,
    "validated_factor_scope": ["F03", "F06"],
    "allowed_validation_methods": [
        "IC",
        "RANK_IC",
        "BUCKET_SPREAD",
        "HORIZON_SPLIT",
        "REGIME_SPLIT",
        "COST_ADJUSTED_SPREAD"
    ],
    "validation_methods_executed_this_round": [],
    "outcome_label_generation_allowed_next_step": True,
    "outcome_label_written_to_feature_panel": False,
    "multi_factor_composite_allowed": False,
    "multi_factor_composite_built": False,
    "v13_6_allowed": False,
    "paper_trading_allowed": False,
    "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
    "recommended_next_action": "BUILD_SINGLE_FACTOR_VALIDATION_METHOD_CONTRACTS"
}

dst = RUNTIME / "v13_f2_2_single_factor_validation_planning_contract.json"
dst.write_text(json.dumps(contract, indent=2))
print(f"[F2.2-A] Contract built -> {dst}")
sys.exit(0)
