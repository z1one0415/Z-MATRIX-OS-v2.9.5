#!/usr/bin/env python3
"""V13.F3.2 — Stage E: candidate freeze registry."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(BATCH / "v13_f3_2_candidate_freeze_registry.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-2-CANDIDATE-FREEZE-REGISTRY",
    "status": "V13_F3_2_CANDIDATE_FREEZE_REGISTRY_BUILT",
    "frozen_candidate_count": 3,
    "frozen_candidates": [
        {"factor_id": "F04", "candidate_type": "FULL_HORIZON_RESEARCH_CANDIDATE", "freeze_status": "FROZEN_CANDIDATE"},
        {"factor_id": "F10", "candidate_type": "REGIME_SPECIFIC_RESEARCH_CANDIDATE", "freeze_status": "FROZEN_CANDIDATE"},
        {"factor_id": "F11", "candidate_type": "TACTICAL_RESEARCH_CANDIDATE", "freeze_status": "FROZEN_TACTICAL_CANDIDATE"}
    ],
    "ready_for_f3_3_research_composite_design": ["F04", "F10", "F11"],
    "ready_for_promotion_review": [],
    "promotion_allowed": False, "multi_factor_composite_built": False,
    "weight_optimization_executed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.2-E] Freeze registry built")
sys.exit(0)
