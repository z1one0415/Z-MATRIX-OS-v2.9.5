#!/usr/bin/env python3
"""V13.F3.0.1 — Stage A: evidence consistency contract."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
BATCH.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F3-0-1-EVIDENCE-CONSISTENCY-CONTRACT",
    "status": "V13_F3_0_1_EVIDENCE_CONSISTENCY_CONTRACT_BUILT",
    "base_commit": "673ec6c",
    "repair_only": True,
    "target_factors": ["F04", "F10", "F11"],
    "all_subsessions_audited": True,
    "pass_research_evidence_requires": {
        "materialized": True, "pit_passed": True, "coverage_passed": True,
        "single_factor_validation_executed": True, "sample_month_count_min": 12,
        "forbidden_label_columns_present": False, "alpha_claim_allowed": False
    },
    "coverage_fail_blocks_pass": True,
    "sample_fail_blocks_pass": True,
    "pit_fail_blocks_pass": True,
    "schema_fail_blocks_pass": True,
    "parent_merge_must_recompute_evidence_from_child_artifacts": True,
    "child_closeout_self_claim_not_sufficient": True,
    "multi_factor_composite_built": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}
(BATCH / "v13_f3_0_1_evidence_consistency_contract.json").write_text(json.dumps(contract, indent=2))
print("[F3.0.1-A] Consistency contract built")
sys.exit(0)
