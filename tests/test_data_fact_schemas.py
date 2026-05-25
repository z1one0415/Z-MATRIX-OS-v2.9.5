"""Data Fact Layer tests — validators"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.data_facts.schemas import validate_row
from zmatrix.data_facts.validators import validate_price_bars, validate_paper_ledger, validate_outcomes

def test_price_bar_rejects_negative_price():
    rows=[{"date":"2026-01-01","ticker":"002472","open":"-1","high":"11","low":"9","close":"10","volume":"1000","adj_close":"10"}]
    e=validate_price_bars(rows); assert e, "should reject negative"; print(f"✅ negative price rejected: {e[0][:40]}...")

def test_price_bar_rejects_empty_ticker():
    rows=[{"date":"2026-01-01","ticker":"","open":"10","high":"11","low":"9","close":"10","volume":"1000","adj_close":"10"}]
    e=validate_price_bars(rows); assert e; print(f"✅ empty ticker rejected: {e[0][:40]}...")

def test_paper_ledger_rejects_invalid_horizon():
    rows=[{"paper_id":"x","ticker":"002472","role":"A_LONG_CORE","entry_date":"2026-01-01","entry_price":"10","paper_action":"PAPER_TRACK","reason":"test","target_horizon":"T99","max_loss_plan":"0.01","invalidation_condition":"x","created_at":"2026-01-01"}]
    e=validate_paper_ledger(rows); assert e; print(f"✅ invalid horizon rejected: {e[0][:40]}...")

def test_outcome_rejects_invalid_status():
    rows=[{"paper_id":"x","ticker":"002472","entry_date":"2026-01-01","actual_return_t5":"","actual_return_t20":"","actual_return_t60":"","max_drawdown_t20":"","max_drawdown_t60":"","outcome_status":"FAKE_READY","error_type":"","review_note":""}]
    e=validate_outcomes(rows); assert e; print(f"✅ invalid outcome_status rejected: {e[0][:40]}...")

if __name__ == "__main__":
    test_price_bar_rejects_negative_price(); test_price_bar_rejects_empty_ticker()
    test_paper_ledger_rejects_invalid_horizon(); test_outcome_rejects_invalid_status()
    print("\n🏁 Data Fact Validators — tests PASS")
