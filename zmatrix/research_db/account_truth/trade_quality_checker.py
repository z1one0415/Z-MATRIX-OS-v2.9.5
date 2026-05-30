"""ResearchDB Account Truth — trade quality checker."""
from __future__ import annotations
from zmatrix.research_db.account_truth import TradeRecord, QualityStatus


def check_trade_quality(record: TradeRecord) -> dict:
    """Run quality checks on a single trade record."""
    issues = []
    if not record.trade_id:
        issues.append("missing_trade_id")
    if not record.ticker:
        issues.append("missing_ticker")
    if not record.trade_date:
        issues.append("missing_trade_date")
    if record.price <= 0:
        issues.append("zero_or_negative_price")
    if record.quantity <= 0:
        issues.append("zero_or_negative_quantity")
    if abs(record.amount - record.price * record.quantity) > 0.01:
        issues.append("amount_mismatch")
    return {
        "trade_id": record.trade_id,
        "quality": QualityStatus.ERROR.value if issues else QualityStatus.READY.value,
        "issues": issues,
    }


def filter_quality_trades(records: list[TradeRecord], min_quality: str = QualityStatus.READY.value) -> list[TradeRecord]:
    """Filter trades by minimum quality status."""
    quality_order = [QualityStatus.ERROR.value, QualityStatus.MISSING_REQUIRED_FIELD.value, 
                     QualityStatus.ESTIMATED_ONLY.value, QualityStatus.PARTIAL.value, QualityStatus.READY.value]
    if min_quality not in quality_order:
        return records
    min_idx = quality_order.index(min_quality)
    return [r for r in records if quality_order.index(r.quality_status) >= min_idx]
