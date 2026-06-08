#!/usr/bin/env python3
"""V13.F2.3 — Stage A: execution contract."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"
RUNTIME.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F2-3-EXECUTION-CONTRACT",
    "status": "V13_F2_3_SINGLE_FACTOR_VALIDATION_EXECUTION_CONTRACT_BUILT",
    "v13_f2_3_executed": True,
    "execution_scope": ["F03", "F06"],
    "validation_execution_allowed": True,
    "outcome_label_generation_allowed": True,
    "outcome_label_write_to_factor_panel_allowed": False,
    "ic_validation_allowed": True,
    "rank_ic_validation_allowed": True,
    "bucket_return_validation_allowed": True,
    "horizon_split_allowed": True,
    "regime_split_allowed": True,
    "cost_adjusted_allowed": True,
    "multi_factor_composite_allowed": False,
    "v13_6_allowed": False,
    "paper_trading_allowed": False,
    "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_3_single_factor_validation_execution_contract.json"
dst.write_text(json.dumps(contract, indent=2))
print(f"[F2.3-A] Contract built -> {dst}")
sys.exit(0)
