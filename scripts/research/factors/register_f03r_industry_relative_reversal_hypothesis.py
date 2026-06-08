#!/usr/bin/env python3
"""V13.F2.3.1 — Stage C: register F03R reversal hypothesis (registration only)."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

registry = {
    "pipeline_signature": "Z2-V13-F2-3-1-F03R-REGISTRY",
    "status": "F03R_INDUSTRY_RELATIVE_REVERSAL_HYPOTHESIS_REGISTERED",
    "hypothesis_id": "F03R",
    "hypothesis_name": "INDUSTRY_RELATIVE_REVERSAL",
    "parent_factor_id": "F03",
    "parent_factor_status": "REJECTED_CURRENT_DIRECTION",
    "hypothesis_type": "DIRECTIONAL_REVERSAL_CANDIDATE",
    "proposed_formula": "industry_relative_reversal_score = -1 * industry_relative_strength_score",
    "economic_hypothesis": "industry-relative winners may underperform and industry-relative laggards may mean-revert in this sample regime",
    "registration_only": True,
    "materialization_executed": False,
    "validation_executed": False,
    "promotion_review_allowed": False,
    "requires_separate_materialization_gate": True,
    "requires_separate_validation_gate": True,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "f03r_industry_relative_reversal_hypothesis_registry.json"
dst.write_text(json.dumps(registry, indent=2))
print(f"[F2.3.1-C] F03R hypothesis registered -> {dst}")
print("  NOTE: Registration only. Materialization and validation require separate gates.")
sys.exit(0)
