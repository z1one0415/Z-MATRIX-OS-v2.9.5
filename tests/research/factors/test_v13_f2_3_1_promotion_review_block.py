"""V13.F2.3.1 — Stage F: promotion review block tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

b = L("v13_f2_3_1_promotion_review_block.json")

def test_block_built():
    assert b.get("status") == "V13_F2_3_1_PROMOTION_REVIEW_BLOCK_BUILT"

def test_promotion_not_allowed():
    assert b.get("promotion_review_allowed") is False

def test_ready_list_empty():
    assert b.get("ready_for_f2_4_promotion_review") == []

def test_two_blocked_factors():
    assert len(b.get("blocked_factors", [])) == 2

def test_f03_blocked_reason():
    f03 = next((f for f in b.get("blocked_factors", []) if f["factor_id"] == "F03"), None)
    assert f03 is not None
    assert "REJECTED" in f03.get("reason", "")

def test_f06_blocked_reason():
    f06 = next((f for f in b.get("blocked_factors", []) if f["factor_id"] == "F06"), None)
    assert f06 is not None
    assert "INSUFFICIENT" in f06.get("reason", "")

def test_multi_composite_false():
    assert b.get("multi_factor_composite_allowed") is False

def test_v13_6_false():
    assert b.get("v13_6_allowed") is False

def test_paper_false():
    assert b.get("paper_trading_allowed") is False

def test_alpha_false():
    assert b.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert b.get("production") == "BLOCKED"
