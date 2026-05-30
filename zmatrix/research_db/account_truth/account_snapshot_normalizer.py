"""ResearchDB Account Truth — account snapshot normalizer."""
from __future__ import annotations
from zmatrix.research_db.account_truth import AccountSnapshot, DataStatus, QualityStatus


def normalize_snapshot(raw: dict, source_file: str = "", data_status: str = DataStatus.BROKER_EXPORT.value) -> AccountSnapshot:
    record = AccountSnapshot(
        date=str(raw.get("date", "")),
        account_id=str(raw.get("account_id", "")),
        total_equity=float(raw.get("total_equity", 0)),
        cash=float(raw.get("cash", 0)),
        market_value=float(raw.get("market_value", 0)),
        daily_pnl=float(raw.get("daily_pnl", 0)),
        daily_return=float(raw.get("daily_return", 0)),
        cumulative_return=float(raw.get("cumulative_return", 0)),
        max_drawdown=float(raw.get("max_drawdown", 0)),
        exposure=float(raw.get("exposure", 0)),
        turnover=float(raw.get("turnover", 0)),
        source_file=source_file,
        data_status=data_status,
    )
    if record.exposure == 0 and record.total_equity > 0:
        record.exposure = record.market_value / record.total_equity
    if not record.date or not record.total_equity:
        record.quality_status = QualityStatus.MISSING_REQUIRED_FIELD.value
    return record


def normalize_snapshots(raw_rows: list[dict], source_file: str = "") -> list[AccountSnapshot]:
    return [normalize_snapshot(r, source_file) for r in raw_rows]
