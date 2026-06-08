#!/usr/bin/env python3
"""V13.F4.0 — Stage A: batch 2 orchestration contract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
B2.mkdir(parents=True, exist_ok=True)
(B2 / "v13_f4_0_batch2_orchestration_contract.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-OPENCLAW-PARALLEL-FACTOR-BATCH-2",
    "status": "V13_F4_0_BATCH2_ORCHESTRATION_CONTRACT_BUILT",
    "base_commit": "8f800b17", "parallel_mode": True,
    "parent_session_role": "ORCHESTRATION_ONLY",
    "frozen_candidates_preserved": ["F04","F10","F11"],
    "frozen_candidate_mutation_allowed": False,
    "f3_5_1_monitoring_execution_allowed": False,
    "f3_6_true_oos_validation_allowed": False,
    "batch2_subsession_count": 7,
    "batch2_selection_mode": "REGISTRY_AND_SOURCE_READINESS_DRIVEN",
    "subsession_output_root": "runtime_reports/research/factors/openclaw_batch_2/",
    "multi_factor_composite_allowed": False, "weight_optimization_allowed": False,
    "promotion_allowed": False, "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F4.0-A] Batch 2 contract built")
sys.exit(0)
