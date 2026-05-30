"""ResearchDB Account Truth — cashflow record normalizer."""
from __future__ import annotations
from zmatrix.research_db.account_truth import CashflowRecord, CashflowType, DataStatus, QualityStatus


def normalize_cashflow(raw: dict, source_file: str = "", data_status: str = DataStatus.BROKER_EXPORT.value) -> CashflowRecord:
    record = CashflowRecord(
        cashflow_id=str(raw.get("cashflow_id", f"CF-{raw.get('date','')}-{raw.get('amount',0)}")),
        account_id=str(raw.get("account_id", "")),
        date=str(raw.get("date", "")),
        cashflow_type=str(raw.get("cashflow_type", CashflowType.UNKNOWN.value)),
        amount=float(raw.get("amount", 0)),
        source=str(raw.get("source", "")),
        source_file=source_file,
        data_status=data_status,
        notes=str(raw.get("notes", "")),
    )
    if not record.date:
        record.quality_status = QualityStatus.MISSING_REQUIRED_FIELD.value
    return record


def normalize_cashflows(raw_rows: list[dict], source_file: str = "") -> list[CashflowRecord]:
    return [normalize_cashflow(r, source_file) for r in raw_rows]
