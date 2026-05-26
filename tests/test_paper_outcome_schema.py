"""Paper Outcome Schema tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.schema import OUTCOME_RECORD_FIELDS, DEFAULT_OUTCOME_SAFETY

def test_schema_has_required_fields():
    for f in ["paper_id","ticker","entry_price","actual_return_t5","actual_return_t20","actual_return_t60","max_drawdown_t20","max_drawdown_t60","outcome_status"]:
        assert f in OUTCOME_RECORD_FIELDS
    print("✅ schema has required fields")

def test_default_safety_all_false():
    assert DEFAULT_OUTCOME_SAFETY["real_trade_allowed"] is False
    assert DEFAULT_OUTCOME_SAFETY["broker_order_allowed"] is False
    assert DEFAULT_OUTCOME_SAFETY["hermes_memory_write_allowed"] is False
    print("✅ default safety all False")

if __name__ == "__main__":
    test_schema_has_required_fields()
    test_default_safety_all_false()
    print("\n🏁 Schema PASS")
