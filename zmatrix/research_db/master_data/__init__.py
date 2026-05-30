"""Master Data Schema — security identity, industry/chain mapping, and privacy guardrails."""
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


@dataclass
class SecurityMaster:
    ticker: str
    name: str
    exchange: Exchange
    listing_date: Optional[str] = None
    listing_status: ListingStatus = ListingStatus.UNKNOWN
    market_cap_float: Optional[float] = None
    market_cap_total: Optional[float] = None
    sw_l1: Optional[str] = None
    sw_l2: Optional[str] = None
    sw_l3: Optional[str] = None
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        self.production_allowed = False


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
