"""Data Fact Layer validators v1.0"""
from .schemas import ALL_SCHEMAS

def validate_rows(schema_name: str, rows: list[dict]) -> list[str]:
    errors = []
    for i, row in enumerate(rows):
        for f in ALL_SCHEMAS.get(schema_name, []):
            if f not in row or row[f] is None:
                errors.append(f"row {i}: MISSING_FIELD:{f}")
    return errors


import datetime
def _type_error(v, type_name):
    try: return None if type(v) == type_name else f"type_error: expected {type_name}"
    except: return f"type_error: cannot check"

def deep_validate_price_bars(rows):
    errors = []
    for i, r in enumerate(rows):
        if not r.get("date","").strip(): errors.append(f"row {i}: empty date")
        if not r.get("ticker","").strip(): errors.append(f"row {i}: empty ticker")
        for fld in ["open","high","low","close","volume"]:
            v = r.get(fld)
            if v is None: errors.append(f"row {i}: missing {fld}")
            else:
                try:
                    fv = float(v)
                    if fv < 0: errors.append(f"row {i}: negative {fld}={v}")
                except: errors.append(f"row {i}: non-numeric {fld}={v}")
    return errors

def deep_validate_paper_ledger(rows):
    errors = []
    for i, r in enumerate(rows):
        if not r.get("ticker","").strip(): errors.append(f"row {i}: empty ticker")
        ep = r.get("entry_price")
        try:
            if float(ep) <= 0: errors.append(f"row {i}: entry_price <= 0")
        except: errors.append(f"row {i}: non-numeric entry_price")
        h = r.get("target_horizon","")
        if h not in ("T5","T20","T60"): errors.append(f"row {i}: invalid target_horizon={h}")
    return errors

validate_price_bars = lambda rows: validate_rows("price_bars", rows)
validate_financial_snapshots = lambda rows: validate_rows("financial_snapshot", rows)
validate_paper_ledger = lambda rows: deep_validate_paper_ledger(rows)
validate_outcomes = lambda rows: validate_rows("outcome", rows)

validate_financial_snapshots = lambda rows: validate_rows("financial_snapshot", rows)
validate_paper_ledger = lambda rows: validate_rows("paper_ledger", rows)
validate_outcomes = lambda rows: validate_rows("outcome", rows)
