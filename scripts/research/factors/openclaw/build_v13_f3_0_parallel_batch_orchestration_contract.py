#!/usr/bin/env python3
"""V13.F3.0 — Parent orchestration contract."""
import json, sys
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
BATCH.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F3-0-OPENCLAW-PARALLEL-FACTOR-BATCH",
    "status": "V13_F3_0_PARALLEL_BATCH_ORCHESTRATION_CONTRACT_BUILT",
    "base_commit": "e05a8ff",
    "parallel_mode": True,
    "openclaw_subsessions_allowed": True,
    "parent_session_role": "ORCHESTRATION_ONLY",
    "subsession_count": 8,
    "factor_batch_scope": ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"],
    "factor_batch_priority": {
        "P0_FAST_PRICE_FACTORS": ["F04", "F10", "F11"],
        "P1_LIGHT_FUNDAMENTAL_FACTORS": ["F12", "F13", "F07", "F08"],
        "P2_HYPOTHESIS_ONLY": ["F03R"]
    },
    "subsession_output_isolation_required": True,
    "multi_factor_composite_allowed": False,
    "promotion_review_allowed": False,
    "v13_6_allowed": False,
    "paper_trading_allowed": False,
    "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = BATCH / "v13_f3_0_parallel_batch_orchestration_contract.json"
dst.write_text(json.dumps(contract, indent=2))
print(f"[F3.0-P] Orchestration contract built -> {dst}")
sys.exit(0)
