"""V13.F3.4.1 — Boundary plan tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
p = json.loads((B / "v13_f3_4_1_canonical_oos_boundary_plan.json").read_text())
def test_resolved(): assert p.get("boundary_resolved") is True
def test_max_date(): assert len(p.get("max_last_in_sample_rebalance_date", "")) > 0
def test_oos_start(): assert len(p.get("minimum_oos_start_exclusive", "")) > 0
def test_no_oos(): assert p.get("true_oos_validation_executed") is False
def test_no_alpha(): assert p.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert p.get("production") == "BLOCKED"
