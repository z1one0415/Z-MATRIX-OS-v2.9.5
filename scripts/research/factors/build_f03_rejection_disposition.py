#!/usr/bin/env python3
"""V13.F2.3.1 — Stage B: F03 rejection disposition."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

disposition = {
    "pipeline_signature": "Z2-V13-F2-3-1-F03-REJECTION",
    "status": "F03_REJECTION_DISPOSITION_BUILT",
    "factor_id": "F03",
    "factor_name": "INDUSTRY_RELATIVE_STRENGTH",
    "previous_evidence_score": "REJECTED",
    "sample_month_count": 20,
    "ic_20d_mean": -0.0588,
    "ic_60d_mean": -0.0577,
    "high_low_spread_20d": -0.0099,
    "dominant_failure_mode": "DIRECTIONAL_HYPOTHESIS_REVERSAL",
    "current_direction_rejected": True,
    "promotion_review_allowed": False,
    "multi_factor_composite_allowed": False,
    "recommended_next_action": "REGISTER_F03R_INDUSTRY_RELATIVE_REVERSAL_HYPOTHESIS",
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "f03_industry_relative_strength_rejection_disposition.json"
dst.write_text(json.dumps(disposition, indent=2))
print(f"[F2.3.1-B] F03 rejection disposition built -> {dst}")
sys.exit(0)
