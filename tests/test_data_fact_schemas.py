"""Data Fact Layer schemas and validators tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.data_facts.schemas import validate_row, PRICE_BAR_FIELDS, PAPER_LEDGER_FIELDS

def test_price_bar_schema():
    r = {"date":"2026-01-01","ticker":"002472","open":10,"high":11,"low":9,"close":10.5,"volume":1000,"adj_close":10.5}
    assert validate_row("price_bars", r) == []
    print("✅ price_bar schema valid")

def test_missing_field():
    r = {"ticker":"002472","close":10.5}
    e = validate_row("price_bars", r)
    assert len(e) >= 1
    print(f"✅ missing field detected: {len(e)} errors")

def test_paper_ledger_fields():
    assert "paper_id" in PAPER_LEDGER_FIELDS
    assert "role" in PAPER_LEDGER_FIELDS
    print("✅ paper_ledger schema has required fields")

if __name__ == "__main__":
    test_price_bar_schema(); test_missing_field(); test_paper_ledger_fields()
    print("\n🏁 Data Fact Schemas — tests PASS")
