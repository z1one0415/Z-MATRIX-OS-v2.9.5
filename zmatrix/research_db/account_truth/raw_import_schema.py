"""ResearchDB Account Truth — raw import schemas and CSV field definitions."""
from __future__ import annotations

TRADE_CSV_FIELDS = [
    "trade_id", "account_id", "ticker", "name", "trade_date", "side",
    "price", "quantity", "amount", "fee", "stamp_duty", "transfer_fee",
    "slippage", "total_cost", "net_amount", "source", "data_status",
    "source_file", "signal_id", "thesis_id", "human_action_id", "quality_status",
]

POSITION_CSV_FIELDS = [
    "date", "account_id", "ticker", "name", "quantity", "market_price",
    "market_value", "cost_basis", "unrealized_pnl", "realized_pnl", "total_pnl",
    "position_pct", "holding_days", "thesis_id", "data_status", "source_file", "quality_status",
]

ACCOUNT_SNAPSHOT_CSV_FIELDS = [
    "date", "account_id", "total_equity", "cash", "market_value", "daily_pnl",
    "daily_return", "cumulative_return", "max_drawdown", "exposure", "turnover",
    "data_status", "source_file", "quality_status",
]

CASHFLOW_CSV_FIELDS = [
    "cashflow_id", "account_id", "date", "cashflow_type", "amount",
    "source", "data_status", "source_file", "notes", "quality_status",
]

CAPITAL_CURVE_FIELDS = [
    "date", "account_id", "total_equity", "net_deposit_adjusted_equity",
    "daily_return", "cumulative_return", "max_drawdown",
    "rolling_20d_return", "rolling_60d_return", "quality_status",
]

HOLDING_PNL_FIELDS = [
    "holding_id", "account_id", "ticker", "name", "open_date", "close_date",
    "holding_days", "buy_amount", "sell_amount", "realized_pnl", "unrealized_pnl",
    "total_return", "max_favorable_excursion", "max_adverse_excursion",
    "exit_reason", "quality_status",
]

DRAWDOWN_FIELDS = [
    "drawdown_id", "account_id", "start_date", "trough_date", "end_date",
    "drawdown_pct", "duration_days", "recovery_days",
    "related_positions", "related_trades", "quality_status",
]


def validate_csv_fields(header: list[str], required: list[str]) -> dict:
    missing = [f for f in required if f not in header]
    unknown = [f for f in header if f not in required]
    return {
        "valid": len(missing) == 0,
        "missing_fields": missing,
        "unknown_fields": unknown,
        "expected_count": len(required),
        "actual_count": len(header),
    }
