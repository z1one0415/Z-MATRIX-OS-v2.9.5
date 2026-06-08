#!/usr/bin/env python3
"""V13.F3.5 — Stage B: monitoring metric registry."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_5_monitoring_metric_registry.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-5-MONITORING-METRIC-REGISTRY",
    "status": "V13_F3_5_MONITORING_METRIC_REGISTRY_BUILT",
    "candidate_scope": ["F04","F10","F11"],
    "monitoring_metrics": {
        "factor_quality_metrics": ["monthly_rank_ic","monthly_bucket_spread","cost_adjusted_spread","bucket_monotonicity","win_rate","month_concentration"],
        "coverage_and_data_metrics": ["covered_ticker_count","coverage_tier","missing_factor_value_rate","pit_passed","label_isolation_passed"],
        "gate_metrics": ["regime_state","regime_gate_pass","cost_turnover_gate_pass","horizon_gate_pass"],
        "risk_metrics": ["signal_decay","factor_drift","turnover_estimate","cost_bps_estimate","capacity_warning","correlation_shift"]
    },
    "monitoring_execution_executed": False, "oos_label_generation_executed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.5-B] Metric registry built")
sys.exit(0)
