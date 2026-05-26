"""Backfill Runner tests — with benchmark + invalidation"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.outcome_backfill_runner import run_outcome_backfill

def test_backfill_with_price_path():
    path = [45.0,46,47,48,49] + [50.0]*80
    r = run_outcome_backfill(paper_entry={"paper_id":"p1","ticker":"002472","entry_price":45.0,"entry_date":"2024-01-01","max_loss_plan":15}, price_path=path)
    assert r["outcome_status"] == "READY"
    assert r["actual_return_t5"] is not None
    assert r["max_adverse_excursion_pct"] is not None
    print(f"✅ backfill: T5={r['actual_return_t5']}% MAE={r['max_adverse_excursion_pct']}%")

def test_invalidation_on_max_loss():
    path = [45.0,44,43,42,41,40,39] + [39.0]*80
    r = run_outcome_backfill(paper_entry={"paper_id":"p2","ticker":"002472","entry_price":45.0,"entry_date":"2024-01-01","max_loss_plan":10}, price_path=path)
    assert r["invalidation_triggered"] is True
    print("✅ invalidation triggered on max_loss breach")

if __name__ == "__main__":
    test_backfill_with_price_path()
    test_invalidation_on_max_loss()
    print("\n🏁 Backfill Runner PASS")
