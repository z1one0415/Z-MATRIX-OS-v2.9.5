"""Data Fact Layer validators v1.0"""
from .schemas import ALL_SCHEMAS

def validate_rows(schema_name: str, rows: list[dict]) -> list[str]:
    errors = []
    for i, row in enumerate(rows):
        for f in ALL_SCHEMAS.get(schema_name, []):
            if f not in row or row[f] is None:
                errors.append(f"row {i}: MISSING_FIELD:{f}")
    return errors

validate_price_bars = lambda rows: validate_rows("price_bars", rows)
validate_financial_snapshots = lambda rows: validate_rows("financial_snapshot", rows)
validate_paper_ledger = lambda rows: validate_rows("paper_ledger", rows)
validate_outcomes = lambda rows: validate_rows("outcome", rows)
