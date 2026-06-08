"""V13.F3.0 — Batch closeout tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

BATCH = RUNTIME_FACTORS / "openclaw_batch"

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

co = load("v13_f3_0_parallel_batch_closeout.json")

def test_closeout_present():
    assert "BATCH" in co.get("status", "")

def test_executed():
    assert co.get("v13_f3_0_executed") is True

def test_subsessions_8():
    assert co.get("parallel_subsessions_launched") == 8

def test_multi_composite_false():
    assert co.get("multi_factor_composite_built") is False

def test_oos_not_executed():
    assert co.get("oos_alpha_validation_executed") is False

def test_skillos_unchanged():
    assert co.get("skillos_protocol_modified") is False

def test_frontend_unchanged():
    assert co.get("frontend_modified") is False

def test_v13_6_false():
    assert co.get("v13_6_allowed") is False

def test_paper_false():
    assert co.get("paper_trading_allowed") is False

def test_alpha_false():
    assert co.get("alpha_claim_allowed") is False

def test_ready_for_alpha_false():
    assert co.get("ready_for_alpha_claim") is False

def test_alpha_validated_false():
    assert co.get("alpha_validated") is False

def test_prod_blocked():
    assert co.get("production") == "BLOCKED"

def test_broker_blocked():
    assert co.get("broker_runtime") == "BLOCKED"

def test_real_trade_blocked():
    assert co.get("real_trade") == "BLOCKED"

def test_next_action():
    assert len(co.get("recommended_next_action", "")) > 0
