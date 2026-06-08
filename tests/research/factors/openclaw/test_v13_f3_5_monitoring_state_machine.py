"""V13.F3.5 — State machine tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
m = json.loads((B / "v13_f3_5_monitoring_state_machine.json").read_text())
def test_8_states(): assert len(m.get("states", [])) == 8
def test_watch_orange(): assert "WATCH" in m["states"] and "ORANGE" in m["states"]
def test_suspension(): assert "SUSPENSION_REVIEW" in m["states"]
def test_promotion_absent(): assert m.get("promotion_state_absent") is True
def test_no_alpha(): assert m.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert m.get("production") == "BLOCKED"
