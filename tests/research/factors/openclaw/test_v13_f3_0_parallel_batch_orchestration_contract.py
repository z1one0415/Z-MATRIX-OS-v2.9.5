"""V13.F3.0 — Parent orchestration contract tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

BATCH = RUNTIME_FACTORS / "openclaw_batch"

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

c = load("v13_f3_0_parallel_batch_orchestration_contract.json")

def test_contract_built():
    assert c.get("status") == "V13_F3_0_PARALLEL_BATCH_ORCHESTRATION_CONTRACT_BUILT"

def test_parallel_mode():
    assert c.get("parallel_mode") is True

def test_subsession_count():
    assert c.get("subsession_count") == 8

def test_batch_scope():
    scope = c.get("factor_batch_scope", [])
    assert len(scope) == 8
    assert "F04" in scope
    assert "F10" in scope
    assert "F11" in scope
    assert "F12" in scope
    assert "F13" in scope
    assert "F07" in scope
    assert "F08" in scope
    assert "F03R" in scope

def test_p0_price():
    p0 = c.get("factor_batch_priority", {}).get("P0_FAST_PRICE_FACTORS", [])
    assert "F04" in p0
    assert "F10" in p0
    assert "F11" in p0

def test_p1_fundamental():
    p1 = c.get("factor_batch_priority", {}).get("P1_LIGHT_FUNDAMENTAL_FACTORS", [])
    assert "F12" in p1
    assert "F13" in p1
    assert "F07" in p1
    assert "F08" in p1

def test_p2_hypothesis():
    p2 = c.get("factor_batch_priority", {}).get("P2_HYPOTHESIS_ONLY", [])
    assert "F03R" in p2

def test_multi_composite_false():
    assert c.get("multi_factor_composite_allowed") is False

def test_v13_6_false():
    assert c.get("v13_6_allowed") is False

def test_alpha_false():
    assert c.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert c.get("production") == "BLOCKED"
