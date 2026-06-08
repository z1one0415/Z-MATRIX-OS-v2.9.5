#!/usr/bin/env python3
"""V13.F3.0 — Subsession F03R INDUSTRY_RELATIVE_REVERSAL (planning only)."""
import json, sys
from pathlib import Path

FID = "F03R"
FNAME = "INDUSTRY_RELATIVE_REVERSAL"
FFAMILY = "REVERSAL"
FORMULA = "industry_relative_reversal_score = -1 * industry_relative_strength_score"
HYPOTHESIS = "in current regime, top industry-relative stocks underperform (reversal)"
PRIORITY = "P2"

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch" / FID
BATCH.mkdir(parents=True, exist_ok=True)

def wj(name, data):
    (BATCH / name).write_text(json.dumps(data, indent=2))
    print(f"  [{FID}] wrote {name}")

# Planning only — no materialization, no validation
wj("f03r_formula_contract.json", {
    "pipeline_signature": "Z2-V13-F3-0-SUBSESSION-FORMULA",
    "factor_id": FID, "factor_name": FNAME, "factor_family": FFAMILY,
    "priority": PRIORITY, "formula": FORMULA, "economic_hypothesis": HYPOTHESIS,
    "data_sources": ["price_bars", "sector_mapping"],
    "horizons": ["PLANNING_ONLY"], "required_diagnostics": [],
    "is_planning_only": True, "requires_fundamentals": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
})
wj("f03r_source_readiness.json", {
    "factor_id": FID, "price_bars_available": True, "data_sources_satisfied": True,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
})
wj("f03r_materialization.json", {
    "factor_id": FID, "materialization_executed": False, "extended_panel_built": False,
    "planning_only": True, "note": "data_snooping_risk; requires separate holdout or future OOS validation",
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
})
wj("f03r_pit_leakage_validation.json", {
    "factor_id": FID, "pit_validation_executed": False, "planning_only": True,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
})
wj("f03r_coverage_validation.json", {
    "factor_id": FID, "coverage_validation_executed": False, "planning_only": True,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
})
wj("f03r_single_factor_validation.json", {
    "factor_id": FID, "single_factor_validation_executed": False, "planning_only": True,
    "same_sample_validation_for_promotion_forbidden": True,
    "data_snooping_risk_acknowledged": True,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
})
wj("f03r_evidence_scorecard.json", {
    "factor_id": FID, "factor_name": FNAME,
    "evidence_score": "HYPOTHESIS_ONLY",
    "single_factor_validation_executed": False, "planning_only": True,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
})
wj("f03r_closeout.json", {
    "factor_id": FID, "factor_name": FNAME,
    "subsession_status": "PASS_PLANNING_ONLY",
    "materialized": False, "pit_passed": False, "coverage_passed": False,
    "single_factor_validation_executed": False,
    "evidence_score": "HYPOTHESIS_ONLY",
    "ready_for_parent_merge": True, "ready_for_promotion_review": False,
    "data_snooping_risk_acknowledged": True,
    "same_sample_validation_for_promotion_forbidden": True,
    "multi_factor_composite_built": False, "v13_6_allowed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
})
print(f"[F03R] Planning-only complete. Ready for parent merge.")
sys.exit(0)
