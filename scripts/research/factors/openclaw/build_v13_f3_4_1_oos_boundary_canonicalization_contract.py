#!/usr/bin/env python3
"""V13.F3.4.1 — Stage A: boundary canonicalization contract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_4_1_oos_boundary_canonicalization_contract.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-1-OOS-BOUNDARY-CANONICALIZATION-CONTRACT",
    "status": "V13_F3_4_1_OOS_BOUNDARY_CANONICALIZATION_CONTRACT_BUILT",
    "base_commit": "27e16bb0", "canonicalization_only": True,
    "candidate_scope": ["F04","F10","F11"],
    "must_resolve_last_in_sample_rebalance_date": True,
    "na_last_in_sample_date_allowed": False,
    "true_oos_validation_executed": False, "oos_label_generation_executed": False,
    "composite_execution_executed": False, "composite_panel_generated": False,
    "weight_optimization_executed": False, "promotion_allowed": False,
    "v13_6_allowed": False, "paper_trading_allowed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.4.1-A] Boundary contract built")
sys.exit(0)
