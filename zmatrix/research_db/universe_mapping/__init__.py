"""Universe Mapping — security master data, chain layer, and value capture classification."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ChainLayer(Enum):
    HARDWARE_BOTTLENECK = "HARDWARE_BOTTLENECK"
    DELIVERY_PLATFORM = "DELIVERY_PLATFORM"
    APPLICATION_ADAPTER = "APPLICATION_ADAPTER"
    RESOURCE_UPSTREAM = "RESOURCE_UPSTREAM"
    CHANNEL_DISTRIBUTION = "CHANNEL_DISTRIBUTION"
    FINANCIAL_BETA = "FINANCIAL_BETA"
    DEFENSIVE_ANCHOR = "DEFENSIVE_ANCHOR"


class ValueCaptureGrade(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


@dataclass
class SecurityMaster:
    ticker: str
    name: str
    exchange: str
    listing_date: Optional[str] = None
    listing_status: Optional[str] = None
    market_cap_float: Optional[float] = None
    market_cap_total: Optional[float] = None
    sw_l1: Optional[str] = None
    sw_l2: Optional[str] = None
    sw_l3: Optional[str] = None

    def __post_init__(self) -> None:
        self.production_allowed = False
