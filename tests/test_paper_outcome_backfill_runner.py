"""Backfill Runner tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.outcome_backfill_runner import run_outcome_backfill

def test_backfill_no_price_path_degrades():
    r = run_outcome_backfill(paper_entry={"paper_id":"p1","ticker":"002472","entry_price":45.0})
    assert r["outcome_status"] == "INSUFFICIENT_DATA"
    print("✅ insufficient data handled")

def test_backfill_with_price_path():
    path = [45.0,46,47,48,49] + [50.0]*80
    r = run_outcome_backfill(paper_entry={"paper_id":"p1","ticker":"002472","entry_price":45.0,"entry_date":"2024-01-01"}, price_path=path)
    assert r["outcome_status"] == "READY"
    assert r["actual_return_t5"] is not None
    assert r["safety"]["hermes_memory_write_allowed"] is False
    print("✅ backfill with price path works")

if __name__ == "__main__":
    test_backfill_no_price_path_degrades()
    test_backfill_with_price_path()
    print("\n🏁 Backfill Runner PASS")
