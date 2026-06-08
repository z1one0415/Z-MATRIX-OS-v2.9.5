"""V13.F3.5 — Artifact schema tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
s = json.loads((B / "v13_f3_5_monitoring_artifact_schema.json").read_text())
def test_schema_built(): assert "BUILT" in s.get("status", "")
def test_trade_signal_forbidden(): assert "trade_signal" in s.get("forbidden_fields", [])
def test_position_forbidden(): assert "position" in s.get("forbidden_fields", [])
def test_order_forbidden(): assert "order" in s.get("forbidden_fields", [])
def test_broker_forbidden(): assert "broker_instruction" in s.get("forbidden_fields", [])
def test_not_executed(): assert s.get("monitoring_execution_executed") is False
def test_no_alpha(): assert s.get("alpha_claim_allowed") is False
