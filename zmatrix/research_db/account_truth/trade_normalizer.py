"""ResearchDB Account Truth — trade record normalizer."""
from __future__ import annotations
from zmatrix.research_db.account_truth import TradeRecord, TradeSide, DataStatus, QualityStatus


def normalize_trade(raw: dict, source_file: str = "", data_status: str = DataStatus.BROKER_EXPORT.value) -> TradeRecord:
    """Normalize raw trade dict into a TradeRecord."""
    record = TradeRecord(
        trade_id=str(raw.get("trade_id", "")),
        account_id=str(raw.get("account_id", "")),
        ticker=str(raw.get("ticker", "")),
        name=str(raw.get("name", raw.get("ticker", ""))),
        trade_date=str(raw.get("trade_date", "")),
        side=str(raw.get("side", "")),
        price=float(raw.get("price", 0)),
        quantity=int(raw.get("quantity", 0)),
        amount=float(raw.get("amount", 0)),
        fee=float(raw.get("fee", 0)),
        stamp_duty=float(raw.get("stamp_duty", 0)),
        transfer_fee=float(raw.get("transfer_fee", 0)),
        slippage=float(raw.get("slippage", 0)),
        source=str(raw.get("source", "")),
        source_file=source_file,
        data_status=data_status,
        signal_id=str(raw.get("signal_id", "")),
        thesis_id=str(raw.get("thesis_id", "")),
        human_action_id=str(raw.get("human_action_id", "")),
    )
    # Calculate derived fields
    record.total_cost = record.fee + record.stamp_duty + record.transfer_fee + record.slippage
    record.net_amount = record.amount - record.total_cost
    # Quality check
    if not record.trade_id or not record.ticker or not record.trade_date:
        record.quality_status = QualityStatus.MISSING_REQUIRED_FIELD.value
    return record


def normalize_trades(raw_rows: list[dict], source_file: str = "", data_status: str = DataStatus.BROKER_EXPORT.value) -> list[TradeRecord]:
    """Normalize a list of raw trade dicts."""
    return [normalize_trade(r, source_file, data_status) for r in raw_rows]
