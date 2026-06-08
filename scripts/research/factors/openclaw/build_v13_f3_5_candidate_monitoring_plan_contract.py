#!/usr/bin/env python3
"""V13.F3.5 — Stage A: monitoring plan contract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_5_candidate_monitoring_plan_contract.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-5-CANDIDATE-MONITORING-PLAN-CONTRACT",
    "status": "V13_F3_5_CANDIDATE_MONITORING_PLAN_CONTRACT_BUILT",
    "base_commit": "680f1542", "monitoring_plan_only": True,
    "monitoring_execution_allowed": False,
    "candidate_scope": ["F04","F10","F11"],
    "minimum_oos_start_exclusive": "20260501", "monitoring_frequency": "MONTHLY",
    "true_oos_validation_executed": False, "oos_label_generation_executed": False,
    "composite_execution_allowed": False, "composite_panel_generation_allowed": False,
    "weight_optimization_allowed": False, "promotion_allowed": False,
    "v13_6_allowed": False, "paper_trading_allowed": False, "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.5-A] Monitoring contract built")
sys.exit(0)
