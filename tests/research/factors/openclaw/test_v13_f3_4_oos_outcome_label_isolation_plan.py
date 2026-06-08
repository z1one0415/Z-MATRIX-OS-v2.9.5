"""V13.F3.4 — OOS label isolation tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
p = json.loads((B / "v13_f3_4_oos_outcome_label_isolation_plan.json").read_text())
def test_not_generated(): assert p.get("label_generation_executed") is False
def test_label_role(): assert "TRUE_OOS" in p.get("label_role", "")
def test_horizons(): assert "5D" in p.get("label_horizons", [])
def test_factor_panel_forbidden(): assert p.get("label_panel_write_to_factor_panel_allowed") is False
def test_forbidden(): fb = p.get("forbidden_in_factor_panels", []); assert "forward_return_20d" in fb
def test_no_alpha(): assert p.get("alpha_claim_allowed") is False
