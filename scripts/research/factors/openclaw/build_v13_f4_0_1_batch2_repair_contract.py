#!/usr/bin/env python3
"""V13.F4.0.1 — Stage A: repair contract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
(B2 / "v13_f4_0_1_batch2_repair_contract.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-1-BATCH2-REPAIR-CONTRACT",
    "status": "V13_F4_0_1_BATCH2_REPAIR_CONTRACT_BUILT",
    "base_commit": "0d660e10", "repair_only": True,
    "frozen_candidates_preserved": ["F04","F10","F11"],
    "frozen_candidate_mutation_allowed": False,
    "f3_5_1_monitoring_execution_allowed": False,
    "f3_6_true_oos_validation_allowed": False,
    "candidate_review_allowed": False, "promotion_allowed": False,
    "coverage_fail_blocks_pass": True, "sample_fail_blocks_pass": True,
    "source_blocked_blocks_pass": True,
    "source_audit_only_materialization_forbidden": True,
    "source_audit_only_validation_forbidden": True,
    "parent_merge_must_recompute_from_child_artifacts": True,
    "child_closeout_self_claim_not_sufficient": True,
    "multi_factor_composite_built": False, "weight_optimization_executed": False,
    "v13_6_allowed": False, "paper_trading_allowed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F4.0.1-A] Repair contract built")
sys.exit(0)
