"""ResearchDB Account Truth — raw import schema and data status enums."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class DataStatus(str, Enum):
    BROKER_EXPORT = "BROKER_EXPORT"
    BROKER_RECONSTRUCTED = "BROKER_RECONSTRUCTED"
    MANUAL_IMPORT = "MANUAL_IMPORT"
    PARTIAL_RECONSTRUCTED = "PARTIAL_RECONSTRUCTED"
    ESTIMATED = "ESTIMATED"
    UNKNOWN_SOURCE = "UNKNOWN_SOURCE"


class QualityStatus(str, Enum):
    READY = "READY"
    PARTIAL = "PARTIAL"
    ERROR = "ERROR"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    RECONCILIATION_FAILED = "RECONCILIATION_FAILED"
    ESTIMATED_ONLY = "ESTIMATED_ONLY"


class TradeSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"
    CORRECTION = "CORRECTION"


class CashflowType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    DIVIDEND = "DIVIDEND"
    INTEREST = "INTEREST"
    FEE = "FEE"
    TAX = "TAX"
    CORRECTION = "CORRECTION"
    UNKNOWN = "UNKNOWN"


class DecisionType(str, Enum):
    BUY_DECISION = "BUY_DECISION"
    SELL_DECISION = "SELL_DECISION"
    WATCH_DECISION = "WATCH_DECISION"
    PASS_DECISION = "PASS_DECISION"
    REDUCE_DECISION = "REDUCE_DECISION"
    ADD_DECISION = "ADD_DECISION"
    REVIEW_DECISION = "REVIEW_DECISION"


class WatchStatus(str, Enum):
    ACTIVE = "ACTIVE"
    REMOVED = "REMOVED"
    PROMOTED_TO_CANDIDATE = "PROMOTED_TO_CANDIDATE"
    PROMOTED_TO_POSITION = "PROMOTED_TO_POSITION"
    MISSED_OPPORTUNITY_REVIEW = "MISSED_OPPORTUNITY_REVIEW"


class ExitReason(str, Enum):
    TAKE_PROFIT = "TAKE_PROFIT"
    STOP_LOSS = "STOP_LOSS"
    THESIS_INVALIDATED = "THESIS_INVALIDATED"
    CATALYST_EXPIRED = "CATALYST_EXPIRED"
    RISK_REDUCTION = "RISK_REDUCTION"
    PORTFOLIO_REBALANCE = "PORTFOLIO_REBALANCE"
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"
    UNKNOWN = "UNKNOWN"


@dataclass
class TradeRecord:
    trade_id: str = ""
    account_id: str = ""
    ticker: str = ""
    name: str = ""
    trade_date: str = ""
    side: str = ""
    price: float = 0.0
    quantity: int = 0
    amount: float = 0.0
    fee: float = 0.0
    stamp_duty: float = 0.0
    transfer_fee: float = 0.0
    slippage: float = 0.0
    total_cost: float = 0.0
    net_amount: float = 0.0
    source: str = ""
    data_status: str = DataStatus.UNKNOWN_SOURCE.value
    source_file: str = ""
    signal_id: str = ""
    thesis_id: str = ""
    human_action_id: str = ""
    quality_status: str = QualityStatus.READY.value


@dataclass
class PositionRecord:
    date: str = ""
    account_id: str = ""
    ticker: str = ""
    name: str = ""
    quantity: int = 0
    market_price: float = 0.0
    market_value: float = 0.0
    cost_basis: float = 0.0
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    total_pnl: float = 0.0
    position_pct: float = 0.0
    holding_days: int = 0
    thesis_id: str = ""
    data_status: str = DataStatus.UNKNOWN_SOURCE.value
    source_file: str = ""
    quality_status: str = QualityStatus.READY.value


@dataclass
class AccountSnapshot:
    date: str = ""
    account_id: str = ""
    total_equity: float = 0.0
    cash: float = 0.0
    market_value: float = 0.0
    daily_pnl: float = 0.0
    daily_return: float = 0.0
    cumulative_return: float = 0.0
    max_drawdown: float = 0.0
    exposure: float = 0.0
    turnover: float = 0.0
    data_status: str = DataStatus.UNKNOWN_SOURCE.value
    source_file: str = ""
    quality_status: str = QualityStatus.READY.value


@dataclass
class CashflowRecord:
    cashflow_id: str = ""
    account_id: str = ""
    date: str = ""
    cashflow_type: str = ""
    amount: float = 0.0
    source: str = ""
    data_status: str = DataStatus.UNKNOWN_SOURCE.value
    source_file: str = ""
    notes: str = ""
    quality_status: str = QualityStatus.READY.value
