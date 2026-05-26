"""Batch Runner tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.batch_runner import run_outcome_batch

def test_batch_runner():
    entries = [{"paper_id":"p1","ticker":"002472","entry_price":45.0,"entry_date":"2024-01-01"}]
    paths = {"002472": [45,46,47,48,49]+[50.0]*80}
    r = run_outcome_batch(entries, paths)
    assert r["ok"] == 1
    print("✅ batch runner works")

if __name__ == "__main__":
    test_batch_runner()
    print("\n🏁 Batch Runner PASS")
