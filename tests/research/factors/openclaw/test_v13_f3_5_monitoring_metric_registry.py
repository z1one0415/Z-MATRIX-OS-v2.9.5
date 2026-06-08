"""V13.F3.5 — Metric registry tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((B / "v13_f3_5_monitoring_metric_registry.json").read_text())
def test_4_categories(): assert len(r.get("monitoring_metrics", {})) == 4
def test_factor_quality(): assert "monthly_rank_ic" in r["monitoring_metrics"].get("factor_quality_metrics", [])
def test_gate_metrics(): assert "regime_gate_pass" in r["monitoring_metrics"].get("gate_metrics", [])
def test_risk_metrics(): assert "signal_decay" in r["monitoring_metrics"].get("risk_metrics", [])
def test_not_executed(): assert r.get("monitoring_execution_executed") is False
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
