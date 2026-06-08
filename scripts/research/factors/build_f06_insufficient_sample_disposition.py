#!/usr/bin/env python3
"""V13.F2.3.1 — Stage D: F06 insufficient sample disposition."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

disposition = {
    "pipeline_signature": "Z2-V13-F2-3-1-F06-SAMPLE-BLOCKED",
    "status": "F06_INSUFFICIENT_SAMPLE_DISPOSITION_BUILT",
    "factor_id": "F06",
    "factor_name": "FUNDAMENTAL_QUALITY",
    "previous_evidence_score": "BLOCKED_BY_INSUFFICIENT_SAMPLE",
    "sample_month_count": 1,
    "minimum_month_count_required": 12,
    "preferred_month_count_required": 24,
    "factor_rejected": False,
    "factor_promoted": False,
    "validation_blocked": True,
    "blocked_reason": "INSUFFICIENT_REBALANCE_MONTH_SAMPLE",
    "recommended_next_action": "EXTEND_F06_FUNDAMENTAL_HISTORY_AND_REVALIDATE",
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "f06_fundamental_quality_insufficient_sample_disposition.json"
dst.write_text(json.dumps(disposition, indent=2))
print(f"[F2.3.1-D] F06 sample-blocked disposition built -> {dst}")
sys.exit(0)
