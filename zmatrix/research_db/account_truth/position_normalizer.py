"""ResearchDB Account Truth — position record normalizer."""
from __future__ import annotations
from zmatrix.research_db.account_truth import PositionRecord, DataStatus, QualityStatus


def normalize_position(raw: dict, source_file: str = "", data_status: str = DataStatus.BROKER_EXPORT.value) -> PositionRecord:
    record = PositionRecord(
        date=str(raw.get("date", "")),
        account_id=str(raw.get("account_id", "")),
        ticker=str(raw.get("ticker", "")),
        name=str(raw.get("name", raw.get("ticker", ""))),
        quantity=int(raw.get("quantity", 0)),
        market_price=float(raw.get("market_price", 0)),
        cost_basis=float(raw.get("cost_basis", 0)),
        unrealized_pnl=float(raw.get("unrealized_pnl", 0)),
        realized_pnl=float(raw.get("realized_pnl", 0)),
        thesis_id=str(raw.get("thesis_id", "")),
        source_file=source_file,
        data_status=data_status,
    )
    record.market_value = record.quantity * record.market_price
    record.total_pnl = record.unrealized_pnl + record.realized_pnl
    if not record.date or not record.ticker:
        record.quality_status = QualityStatus.MISSING_REQUIRED_FIELD.value
    return record


def normalize_positions(raw_rows: list[dict], source_file: str = "") -> list[PositionRecord]:
    return [normalize_position(r, source_file) for r in raw_rows]
