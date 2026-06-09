"""Stage F: V13.F5.5.6 G18 Handoff Gate Plan."""
import json
from pathlib import Path
OUT = Path("research/factor_library/reviews/batch_003/f5_5_6_expansion_gate_plan")
OUT.mkdir(parents=True, exist_ok=True)
g = {
    "pipeline_signature": "Z2-V13-F5-5-6-G18-HANDOFF-GATE-PLAN",
    "status": "V13_F5_5_6_G18_HANDOFF_GATE_PLAN_BUILT",
    "base_commit": "7cc8a76",
    "g18_fast_risk_overlay_merged": True,
    "current_factor_monitoring_use_for_g18": "OBSERVATION_ONLY",
    "auto_weight_update_allowed": False,
    "action_gate_parameter_update_allowed": False,
    "minimum_requirement_for_g18_reweighting": {
        "ticker_count": 475,
        "oos_months": 6,
        "preferred_oos_months": 12,
        "formal_oos_validation_passed": True
    },
    "micro_sample_result_not_allowed_for_g18_reweighting": True,
    "current_g18_status": "OBSERVATION_MODE_ONLY"
}
(OUT / "v13_f5_5_6_g18_handoff_gate_plan.json").write_text(json.dumps(g, indent=2) + "\n")
print("Written: G18 handoff gate plan")
