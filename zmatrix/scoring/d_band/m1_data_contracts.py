from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class M1Freshness(str, Enum):
    FRESH = "fresh"
    STALE = "stale"
    HISTORICAL = "historical"
    UNAVAILABLE = "unavailable"


class M1Usability(str, Enum):
    USABLE = "USABLE"
    DEGRADED = "DEGRADED"
    UNUSABLE = "UNUSABLE"


class LateDayAnomalyType(str, Enum):
    NONE = "NONE"
    FALSE_PREHEAT = "FALSE_PREHEAT"
    SMART_MONEY_TAIL_GRAB = "SMART_MONEY_TAIL_GRAB"
    UNCERTAIN_LATE_DAY_ANOMALY = "UNCERTAIN_LATE_DAY_ANOMALY"


@dataclass(slots=True)
class M1DataQuality:
    usability: M1Usability
    expected_bars: int
    actual_bars: int
    missing_minutes: int
    synthetic_bars: int
    missing_tail_minutes: int = 0
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["usability"] = self.usability.value
        return d


@dataclass(slots=True)
class M1FeaturePack:
    total_gain_pct: float
    late_day_gain_pct: float
    late_day_gain_contribution: float
    total_turnover: float
    late_day_turnover: float
    late_day_turnover_share: float
    close_position_pct: float
    data_quality: M1DataQuality
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["data_quality"] = self.data_quality.to_dict()
        return d


@dataclass(slots=True)
class LateDayAnomalyResult:
    anomaly_type: LateDayAnomalyType
    false_preheat: bool
    smart_money_tail_grab: bool
    volume_price_preload_penalty: float
    cooldown_days: int
    requires_next_day_validation: bool
    allowed_action: str
    reason: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["anomaly_type"] = self.anomaly_type.value
        return d
