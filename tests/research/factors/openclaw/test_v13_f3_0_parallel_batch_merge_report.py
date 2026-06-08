"""V13.F3.0 — Merge report tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

BATCH = RUNTIME_FACTORS / "openclaw_batch"

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

m = load("v13_f3_0_parallel_batch_merge_report.json")

def test_merge_built():
    assert "MERGE" in m.get("status", "")

def test_expected_8():
    assert m.get("expected_subsessions") == 8

def test_merged_factors_8():
    assert len(m.get("merged_factors", [])) == 8

def test_multi_composite_false():
    assert m.get("multi_factor_composite_built") is False

def test_v13_6_false():
    assert m.get("v13_6_allowed") is False

def test_alpha_false():
    assert m.get("alpha_claim_allowed") is False

def test_promotion_empty():
    assert m.get("ready_for_promotion_review") == []

def test_prod_blocked():
    assert m.get("production") == "BLOCKED"

def test_broker_blocked():
    assert m.get("broker_runtime") == "BLOCKED"

def test_real_trade_blocked():
    assert m.get("real_trade") == "BLOCKED"
