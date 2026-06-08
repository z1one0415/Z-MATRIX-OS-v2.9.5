#!/usr/bin/env python3
"""V13.F2.3.2 — Stage A: rework execution contract."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"
RUNTIME.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F2-3-2-REWORK-CONTRACT",
    "status": "V13_F2_3_2_REWORK_EXECUTION_CONTRACT_BUILT",
    "v13_f2_3_2_executed": True,
    "primary_task": "F06_SAMPLE_EXTENSION",
    "secondary_task": "F03R_MATERIALIZATION_PLANNING_ONLY",
    "f06_sample_extension_allowed": True,
    "f03r_materialization_planning_allowed": True,
    "f03r_materialization_executed": False,
    "f03r_validation_executed": False,
    "ic_validation_executed": False,
    "rank_ic_validation_executed": False,
    "bucket_return_validation_executed": False,
    "multi_factor_composite_built": False,
    "oos_alpha_validation_executed": False,
    "v13_6_allowed": False,
    "paper_trading_allowed": False,
    "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_3_2_rework_execution_contract.json"
dst.write_text(json.dumps(contract, indent=2))
print(f"[F2.3.2-A] Contract built -> {dst}")
sys.exit(0)
