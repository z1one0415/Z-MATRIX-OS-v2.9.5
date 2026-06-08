"""V13.F3.0.1 — Repair closeout tests."""
import json
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

co = load("v13_f3_0_1_parallel_batch_repair_closeout.json")

def test_closeout_present():
    assert "REPAIR" in co.get("status", "")

def test_repair_executed():
    assert co.get("repair_executed") is True

def test_inconsistent_before_3():
    assert co.get("inconsistent_factor_count_before_repair") == 3

def test_coverage_expansion_attempted():
    assert "F04" in co.get("coverage_expansion_attempted_factors", [])

def test_ready_next_is_list():
    assert isinstance(co.get("ready_for_next_validation"), list)

def test_promotion_empty():
    assert co.get("ready_for_promotion_review") == []

def test_multi_composite_false():
    assert co.get("multi_factor_composite_built") is False

def test_oos_not_executed():
    assert co.get("oos_alpha_validation_executed") is False

def test_skillos_unchanged():
    assert co.get("skillos_protocol_modified") is False

def test_v13_6_false():
    assert co.get("v13_6_allowed") is False

def test_paper_false():
    assert co.get("paper_trading_allowed") is False

def test_alpha_false():
    assert co.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert co.get("production") == "BLOCKED"

def test_next_action():
    assert len(co.get("recommended_next_action", "")) > 0
