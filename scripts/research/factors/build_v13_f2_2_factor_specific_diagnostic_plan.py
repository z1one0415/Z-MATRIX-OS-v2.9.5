#!/usr/bin/env python3
"""V13.F2.2 — Stage E: factor-specific diagnostic plan."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"
RUNTIME.mkdir(parents=True, exist_ok=True)

plan = {
    "pipeline_signature": "Z2-V13-F2-2-FACTOR-DIAGNOSTIC",
    "status": "V13_F2_2_FACTOR_SPECIFIC_DIAGNOSTIC_PLAN_BUILT",
    "diagnostic_scope": ["F03", "F06"],
    "f03_diagnostics": [
        "sector_concentration",
        "industry_neutrality",
        "sector_wind_overlap",
        "regime_split",
        "20d_vs_60d_decay"
    ],
    "f06_diagnostics": [
        "quality_score_dispersion",
        "reporting_period_distribution",
        "disclosure_freshness",
        "fundamental_staleness",
        "20d_vs_60d_decay"
    ],
    "diagnostics_executed_this_round": [],
    "diagnostics_allowed_next_step": True,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_2_factor_specific_diagnostic_plan.json"
dst.write_text(json.dumps(plan, indent=2))
print(f"[F2.2-E] Factor-specific diagnostic plan built -> {dst}")
sys.exit(0)
