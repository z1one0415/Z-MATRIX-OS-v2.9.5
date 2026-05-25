"""Data Fact Layer loaders v1.0 — 只读本地 CSV"""
import csv
from .schemas import validate_row, ALL_SCHEMAS

def _load_csv(path: str, schema_name: str) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            errors = validate_row(schema_name, row)
            if errors:
                raise ValueError(f"{path}: validation errors: {errors}")
            rows.append(row)
    return rows

def load_price_bars(path: str) -> list[dict]:
    return _load_csv(path, "price_bars")

def load_financial_snapshots(path: str) -> list[dict]:
    return _load_csv(path, "financial_snapshot")

def load_sector_chain_mapping(path: str) -> list[dict]:
    return _load_csv(path, "sector_chain")

def load_paper_ledger(path: str) -> list[dict]:
    return _load_csv(path, "paper_ledger")

def load_outcomes(path: str) -> list[dict]:
    return _load_csv(path, "outcome")
