"""V13.F3.1 — Cost/turnover tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((BATCH / "v13_f3_1_cost_turnover_capacity_review.json").read_text())
def test_reviewed_3(): assert r.get("reviewed_factors") == ["F04", "F10", "F11"]
def test_cost_bps(): assert 30 in r.get("round_trip_cost_bps_tested", [])
def test_f11_fragile(): assert "F11" in r.get("cost_fragile_factors", [])
def test_no_trade_columns(): assert r.get("trade_or_position_columns_generated") is False
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert r.get("production") == "BLOCKED"
