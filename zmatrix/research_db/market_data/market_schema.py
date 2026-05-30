"""Phase 3-A: Market Data Schema — price bars, calendar, benchmarks, adjustment factors."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class DataStatus(str, Enum):
    SYNTHETIC_FIXTURE="SYNTHETIC_FIXTURE"; PUBLIC_REFERENCE="PUBLIC_REFERENCE"
    VENDOR_EXPORT="VENDOR_EXPORT"; BROKER_EXPORT="BROKER_EXPORT"; MANUAL_REVIEW="MANUAL_REVIEW"

class QualityStatus(str, Enum):
    VALIDATED="VALIDATED"; WARNING="WARNING"; BLOCKED="BLOCKED"; UNKNOWN="UNKNOWN"

class BenchmarkType(str, Enum):
    LARGE_CAP="LARGE_CAP"; MID_CAP="MID_CAP"; SMALL_CAP="SMALL_CAP"
    GROWTH="GROWTH"; CHINEXT="CHINEXT"; STAR="STAR"; CASH="CASH"

class AdjType(str, Enum):
    FORWARD="FORWARD"; BACKWARD="BACKWARD"; NONE="NONE"

@dataclass
class DailyPriceBar:
    ticker: str; trade_date: str; open: float; high: float; low: float; close: float
    pre_close: float = 0.0; volume: int = 0; amount: float = 0.0; turnover_rate: float = 0.0
    limit_up_price: float = 0.0; limit_down_price: float = 0.0
    is_suspended: bool = False; is_limit_up: bool = False; is_limit_down: bool = False
    is_one_price_limit: bool = False
    data_status: str = DataStatus.SYNTHETIC_FIXTURE.value; quality_status: str = QualityStatus.VALIDATED.value
    source_file: str = ""; version: int = 1
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False

@dataclass
class TradingCalendarRecord:
    trade_date: str; exchange: str = "SSE"; is_open: bool = True
    prev_trade_date: Optional[str] = None; next_trade_date: Optional[str] = None
    week_index: int = 0; month_index: int = 0
    data_status: str = DataStatus.SYNTHETIC_FIXTURE.value; quality_status: str = QualityStatus.VALIDATED.value
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False

@dataclass
class BenchmarkRecord:
    benchmark_id: str; benchmark_name: str; benchmark_type: str; ticker: str
    exchange: str = "SSE"; currency: str = "CNY"; country: str = "CN"
    data_status: str = DataStatus.SYNTHETIC_FIXTURE.value; quality_status: str = QualityStatus.VALIDATED.value
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False

@dataclass
class AdjustmentFactorRecord:
    ticker: str; trade_date: str; adj_factor: float; adj_type: str = "FORWARD"
    source_file: str = ""
    data_status: str = DataStatus.SYNTHETIC_FIXTURE.value; quality_status: str = QualityStatus.VALIDATED.value
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False
