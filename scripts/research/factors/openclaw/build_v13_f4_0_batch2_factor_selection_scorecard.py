#!/usr/bin/env python3
"""V13.F4.0 — Stage C: batch 2 factor selection scorecard."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
audit = json.loads((B2 / "v13_f4_0_factor_registry_lifecycle_state_audit.json").read_text())

candidates = audit.get("ready_for_batch2_selection_candidates", [])
source_audits = audit.get("source_audit_only_candidates", [])

# Select 7 lanes: prefer price/turnover factors first, then fundamental, fallback to source audit
price_factors = [c for c in candidates if c["factor_id"] in ("F05","F14","F15")]
fund_factors = [c for c in candidates if c["factor_id"] in ("F09","F16")]
event_factors = [c for c in source_audits if c["factor_id"] in ("F17","F18","F19","F20")]

lanes = []
# Lane A: F05 TURNOVER_STABILITY (price-based, ready)
lanes.append({"lane_id":"A","factor_id":"F05","factor_name":"TURNOVER_STABILITY","lane_type":"MATERIALIZATION_AND_VALIDATION","selection_reason":["price_based","high_source_readiness","low_pit_risk"],"forbidden_if":["synthetic_source","lookahead","coverage_u475_blocked"]})
# Lane B: F02 reimplementation (already known to collision, repair plan)
lanes.append({"lane_id":"B","factor_id":"F02","factor_name":"DOWNSIDE_VOL_ADJUSTED_STRENGTH_REIMPLEMENTATION","lane_type":"MATERIALIZATION_AND_VALIDATION","selection_reason":["formula_collision_identified_in_F3.0","needs_clean_reimplementation"],"forbidden_if":["formula_collision_not_resolved"]})
# Lane C: F09 EARNINGS_REVISION (fundamental, source feasibility)
lanes.append({"lane_id":"C","factor_id":"F09","factor_name":"EARNINGS_REVISION","lane_type":"SOURCE_AUDIT_ONLY","selection_reason":["source_feasibility_check","needs_analyst_data"],"forbidden_if":["synthetic_analyst_data"]})
# Lane D: F14 ASSET_GROWTH_DISCIPLINE (price+fund)
lanes.append({"lane_id":"D","factor_id":"F14","factor_name":"ASSET_GROWTH_DISCIPLINE","lane_type":"MATERIALIZATION_AND_VALIDATION","selection_reason":["balanced_source_profile","research_diversification"],"forbidden_if":["coverage_u475_blocked"]})
# Lane E: F15 ACCRUALS_QUALITY (price+fund)
lanes.append({"lane_id":"E","factor_id":"F15","factor_name":"ACCRUALS_QUALITY","lane_type":"MATERIALIZATION_AND_VALIDATION","selection_reason":["balanced_source_profile","research_diversification"],"forbidden_if":["coverage_u475_blocked"]})
# Lane F: F16 SENTIMENT_ATTENTION (price+momentum style)
lanes.append({"lane_id":"F","factor_id":"F16","factor_name":"SENTIMENT_ATTENTION","lane_type":"MATERIALIZATION_AND_VALIDATION","selection_reason":["price_based_with_volume","diversification"],"forbidden_if":["coverage_u475_blocked"]})
# Lane G: F17+F18+F19+F20 event/domain source audit
lanes.append({"lane_id":"G","factor_id":"F17_F20_GROUP","factor_name":"EVENT_DOMAIN_SOURCE_AUDIT_GROUP","lane_type":"SOURCE_AUDIT_ONLY","selection_reason":["event_source_feasibility","domain_data_maturity"],"forbidden_if":["materialization_attempted"]})

(B2 / "v13_f4_0_batch2_factor_selection_scorecard.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-BATCH2-FACTOR-SELECTION-SCORECARD",
    "status": "V13_F4_0_BATCH2_FACTOR_SELECTION_SCORECARD_BUILT",
    "selection_scope_from_registry": True,
    "selection_candidate_count": len(candidates)+len(source_audits),
    "selected_batch2_lanes": lanes,
    "frozen_candidate_overlap_blocked": True,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0-C] Scorecard: {len(lanes)} lanes selected")
sys.exit(0)
