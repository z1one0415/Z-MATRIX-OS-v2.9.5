"""Master Data Schema — Phase 2 standard fields with governance metadata."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Exchange(Enum):
    SSE = "SSE"
    SZSE = "SZSE"
    BSE = "BSE"


class ListingStatus(Enum):
    LISTED = "LISTED"
    DELISTED = "DELISTED"
    SUSPENDED = "SUSPENDED"
    UNKNOWN = "UNKNOWN"


class AliasType(Enum):
    FORMER_NAME = "FORMER_NAME"
    SHORT_NAME = "SHORT_NAME"
    ENGLISH_NAME = "ENGLISH_NAME"
    CODE_CHANGE = "CODE_CHANGE"


class Confidence(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNVERIFIED = "UNVERIFIED"


class DataStatus(Enum):
    SYNTHETIC_FIXTURE = "SYNTHETIC_FIXTURE"
    PUBLIC_REFERENCE = "PUBLIC_REFERENCE"
    VENDOR_EXPORT = "VENDOR_EXPORT"
    BROKER_EXPORT = "BROKER_EXPORT"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class QualityStatus(Enum):
    VALIDATED = "VALIDATED"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class AssetType(Enum):
    STOCK = "STOCK"
    ETF = "ETF"
    INDEX = "INDEX"
    BOND = "BOND"
    CASH = "CASH"
    UNKNOWN = "UNKNOWN"


@dataclass
class SecurityMaster:
    ticker: str
    name: str
    exchange: Exchange
    board: Optional[str] = None
    asset_type: AssetType = AssetType.STOCK
    list_status: ListingStatus = ListingStatus.UNKNOWN
    list_date: Optional[str] = None
    delist_date: Optional[str] = None
    currency: str = "CNY"
    country: str = "CN"
    data_status: DataStatus = DataStatus.SYNTHETIC_FIXTURE
    quality_status: QualityStatus = QualityStatus.UNKNOWN
    source_file: str = ""
    version: int = 1
    effective_from: Optional[str] = None
    effective_to: Optional[str] = None
    market_cap_float: Optional[float] = None
    market_cap_total: Optional[float] = None
    sw_l1: Optional[str] = None
    sw_l2: Optional[str] = None
    sw_l3: Optional[str] = None
    # Backward-compatible aliases — synced from list_date/list_status in __post_init__
    listing_date: Optional[str] = field(default=None, repr=False)
    listing_status: Optional[ListingStatus] = field(default=None, repr=False)
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        self.production_allowed = False
        # Sync backward-compatible aliases
        if self.listing_date is None and self.list_date is not None:
            object.__setattr__(self, 'listing_date', self.list_date)
        if self.listing_status is None and self.list_status is not None:
            object.__setattr__(self, 'listing_status', self.list_status)
        # Reverse sync: if old alias was set, copy to new field
        if self.listing_date is not None and self.list_date is None:
            object.__setattr__(self, 'list_date', self.listing_date)
        if self.listing_status is not None and self.list_status == ListingStatus.UNKNOWN:
            object.__setattr__(self, 'list_status', self.listing_status)


@dataclass
class TickerAlias:
    ticker: str
    alias: str
    alias_type: AliasType
    effective_date: Optional[str] = None
    expiry_date: Optional[str] = None
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        self.production_allowed = False


@dataclass
class IndustryMapping:
    ticker: str
    sw_l1: Optional[str] = None
    sw_l2: Optional[str] = None
    sw_l3: Optional[str] = None
    confidence: Confidence = Confidence.UNVERIFIED
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        self.production_allowed = False


@dataclass
class SectorMapping:
    ticker: str
    sector_id: str
    sector_name: str
    weight: float
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        self.production_allowed = False


@dataclass
class ChainTaxonomy:
    chain_id: str
    chain_name: str
    chain_type: str
    parent_chain_id: Optional[str] = None
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        self.production_allowed = False


@dataclass
class ChainNodeMapping:
    ticker: str
    chain_id: str
    chain_layer: str
    chain_position: str
    value_capture_grade: str
    evidence_grade: str
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        self.production_allowed = False
