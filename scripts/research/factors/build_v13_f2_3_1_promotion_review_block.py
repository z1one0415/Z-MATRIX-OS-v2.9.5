#!/usr/bin/env python3
"""V13.F2.3.1 — Stage F: promotion review block."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

block = {
    "pipeline_signature": "Z2-V13-F2-3-1-PROMOTION-BLOCK",
    "status": "V13_F2_3_1_PROMOTION_REVIEW_BLOCK_BUILT",
    "promotion_review_allowed": False,
    "ready_for_f2_4_promotion_review": [],
    "blocked_factors": [
        {
            "factor_id": "F03",
            "reason": "REJECTED_CURRENT_DIRECTION"
        },
        {
            "factor_id": "F06",
            "reason": "INSUFFICIENT_SAMPLE"
        }
    ],
    "multi_factor_composite_allowed": False,
    "v13_6_allowed": False,
    "paper_trading_allowed": False,
    "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_3_1_promotion_review_block.json"
dst.write_text(json.dumps(block, indent=2))
print(f"[F2.3.1-F] Promotion review block built -> {dst}")
sys.exit(0)
