"""Batch-I: Portfolio Drift — style/sector drift detection."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class DriftKind(str, Enum):
    GROWTH_TO_VALUE = "GROWTH_TO_VALUE"
    VALUE_TO_DIV = "VALUE_TO_DIV"
    DIV_TO_TECH = "DIV_TO_TECH"
    NONE = "NONE"


class StyleDimension(str, Enum):
    GROWTH = "GROWTH"
    VALUE = "VALUE"
    DIVIDEND = "DIVIDEND"
    TECH = "TECH"
    CYCLICAL = "CYCLICAL"
    DEFENSIVE = "DEFENSIVE"


@dataclass
class DriftResult:
    portfolio_id: str
    original_style: dict = field(default_factory=dict)
    current_style: dict = field(default_factory=dict)
    drift_magnitude: float = 0.0
    drift_type: str = DriftKind.NONE.value
    drift_detected: bool = False
    drifted_dimensions: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False


class PortfolioDrift:
    DRIFT_THRESHOLD = 0.15
    STYLE_TRAJECTORIES = {
        (StyleDimension.GROWTH.value, StyleDimension.VALUE.value): DriftKind.GROWTH_TO_VALUE.value,
        (StyleDimension.VALUE.value, StyleDimension.DIVIDEND.value): DriftKind.VALUE_TO_DIV.value,
        (StyleDimension.DIVIDEND.value, StyleDimension.TECH.value): DriftKind.DIV_TO_TECH.value,
    }

    @staticmethod
    def _classify_style_drift(
        dim1: str, dim2: str, direction: int
    ) -> str:
        if direction > 0:
            pair = (dim1, dim2)
        else:
            pair = (dim2, dim1)
        return PortfolioDrift.STYLE_TRAJECTORIES.get(pair, DriftKind.NONE.value)

    @staticmethod
    def detect_style_drift(
        portfolio_id: str,
        original: dict,
        current: dict,
    ) -> DriftResult:
        r = DriftResult(
            portfolio_id=portfolio_id,
            original_style=dict(original),
            current_style=dict(current),
        )
        all_keys = set(list(original.keys()) + list(current.keys()))
        magnitudes = []
        for key in all_keys:
            diff = abs(current.get(key, 0.0) - original.get(key, 0.0))
            if diff > PortfolioDrift.DRIFT_THRESHOLD:
                r.drift_detected = True
                r.drifted_dimensions.append(key)
            magnitudes.append(diff)
        r.drift_magnitude = round(sum(magnitudes), 4)
        if r.drift_detected and r.drifted_dimensions:
            sorted_dims = sorted(
                r.drifted_dimensions,
                key=lambda k: current.get(k, 0.0) - original.get(k, 0.0),
                reverse=True,
            )
            if len(sorted_dims) >= 2:
                direction = 1 if current.get(sorted_dims[0], 0.0) > original.get(sorted_dims[0], 0.0) else -1
                r.drift_type = PortfolioDrift._classify_style_drift(
                    sorted_dims[0], sorted_dims[1], direction
                ) or DriftKind.NONE.value
            else:
                biggest = sorted_dims[0]
                for (a, b), kind in PortfolioDrift.STYLE_TRAJECTORIES.items():
                    if biggest in (a, b):
                        r.drift_type = kind
                        break
        return r

    @staticmethod
    def detect_sector_drift(
        portfolio_id: str,
        original: dict,
        current: dict,
    ) -> DriftResult:
        r = DriftResult(
            portfolio_id=portfolio_id,
            original_style=dict(original),
            current_style=dict(current),
        )
        all_keys = set(list(original.keys()) + list(current.keys()))
        magnitudes = []
        for key in all_keys:
            diff = abs(current.get(key, 0.0) - original.get(key, 0.0))
            if diff > PortfolioDrift.DRIFT_THRESHOLD:
                r.drift_detected = True
                r.drifted_dimensions.append(key)
            magnitudes.append(diff)
        r.drift_magnitude = round(sum(magnitudes), 4)
        return r
