#!/usr/bin/env python3
"""V13.F3.1 — Stage A: candidate review contract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(BATCH / "v13_f3_1_candidate_review_contract.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-1-CANDIDATE-REVIEW-CONTRACT",
    "status": "V13_F3_1_CANDIDATE_REVIEW_CONTRACT_BUILT",
    "base_commit": "337dbb5",
    "candidate_review_scope": ["F04", "F10", "F11"],
    "review_only": True, "promotion_allowed": False,
    "candidate_freeze_allowed_next_gate": True,
    "multi_factor_composite_allowed": False, "weight_optimization_allowed": False,
    "oos_alpha_validation_allowed": False, "v13_6_allowed": False,
    "paper_trading_allowed": False, "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.1-A] Review contract built")
sys.exit(0)
