#!/usr/bin/env python3
"""V13.F3.2 — Stage D: freeze risk guardrail registry."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(BATCH / "v13_f3_2_freeze_risk_guardrail_registry.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-2-FREEZE-RISK-GUARDRAIL-REGISTRY",
    "status": "V13_F3_2_FREEZE_RISK_GUARDRAIL_REGISTRY_BUILT",
    "guardrails": [
        {
            "factor_id": "F04",
            "guardrail_type": "FULL_HORIZON_RESEARCH_ONLY",
            "requires_oos_before_promotion": True,
            "requires_composite_interaction_review": True
        },
        {
            "factor_id": "F10",
            "guardrail_type": "REGIME_SPECIFIC",
            "requires_regime_gate": True,
            "blocked_if_regime_gate_missing": True,
            "requires_oos_before_promotion": True
        },
        {
            "factor_id": "F11",
            "guardrail_type": "TACTICAL_COST_FRAGILE",
            "requires_cost_gate": True,
            "blocked_if_cost_gate_missing": True,
            "requires_turnover_monitoring": True,
            "requires_oos_before_promotion": True
        }
    ],
    "multi_factor_composite_built": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.2-D] Guardrail registry built")
sys.exit(0)
