#!/usr/bin/env python3
"""V13.F3.3 — Stage G: safety audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
artifacts = ["v13_f3_3_composite_role_architecture.json","v13_f3_3_composite_conflict_matrix.json","v13_f3_3_composite_gate_design.json","v13_f3_3_research_composite_blueprint.json","v13_f3_3_oos_monitoring_input_requirements.json"]
violations = []
for name in artifacts:
    d = json.loads((B / name).read_text()) if (B / name).exists() else {}
    for key in ["composite_panel_generated","numeric_weights_assigned","multi_factor_composite_built"]:
        if d.get(key) is True:
            violations.append(f"{name}:{key}=true")
    for key in ["composite_execution_allowed","gate_execution_allowed","weight_optimization_allowed"]:
        if d.get(key) is True:
            violations.append(f"{name}:{key}=true")
    for key in ["alpha_claim_allowed","v13_6_allowed","paper_trading_allowed"]:
        if d.get(key) is True:
            violations.append(f"{name}:{key}=true")
    for key in ["production","broker_runtime","real_trade"]:
        if d.get(key) != "BLOCKED" and d.get(key) is not None:
            violations.append(f"{name}:{key}_not_blocked")
(B / "v13_f3_3_research_composite_design_safety_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-3-RESEARCH-COMPOSITE-DESIGN-SAFETY-AUDIT",
    "status": "V13_F3_3_RESEARCH_COMPOSITE_DESIGN_SAFETY_AUDIT_PASS" if len(violations) == 0 else "V13_F3_3_RESEARCH_COMPOSITE_DESIGN_SAFETY_AUDIT_VIOLATIONS",
    "violation_count": len(violations), "violations": violations,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.3-G] Safety: {len(violations)} violations")
sys.exit(0)
