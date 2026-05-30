"""Batch-A: Attribution Engine — decompose returns into market/industry/sector/selection/residual."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class AttributionType(str, Enum):
    MARKET = "market"; INDUSTRY = "industry"; SECTOR = "sector"
    SELECTION = "selection"; RESIDUAL = "residual"; UNKNOWN = "unknown"

@dataclass
class AttributionResult:
    ticker: str; signal_date: str; exit_date: str
    gross_return: float = 0.0
    market_contribution: float = 0.0
    industry_contribution: float = 0.0
    sector_contribution: float = 0.0
    selection_alpha: float = 0.0
    residual: float = 0.0
    total_attributed: float = 0.0
    attribution_status: str = "READY"
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False

class AttributionEngine:
    @staticmethod
    def compute_market_attribution(signal_return: float, market_return: float, beta: float = 1.0) -> float:
        return market_return * beta

    @staticmethod
    def compute_industry_attribution(industry_return: float, market_return: float, industry_beta: float = 1.0) -> float:
        return (industry_return - market_return) * industry_beta

    @staticmethod
    def compute_sector_attribution(sector_return: float, industry_return: float) -> float:
        return sector_return - industry_return

    @staticmethod
    def compute_selection_alpha(signal_return: float, industry_return: float) -> float:
        return signal_return - industry_return

    @staticmethod
    def compute_residual(gross_return: float, *attributions: float) -> float:
        total_attr = sum(attributions)
        return gross_return - total_attr

    @staticmethod
    def decompose(ticker: str, signal_date: str, exit_date: str,
                  gross_return: float, market_return: float, industry_return: float,
                  sector_return: float = 0.0, beta: float = 1.0) -> AttributionResult:
        market_attr = AttributionEngine.compute_market_attribution(gross_return, market_return, beta)
        industry_attr = AttributionEngine.compute_industry_attribution(industry_return, market_return)
        sector_attr = AttributionEngine.compute_sector_attribution(sector_return, industry_return)
        selection = AttributionEngine.compute_selection_alpha(gross_return, industry_return)
        residual = AttributionEngine.compute_residual(gross_return, market_attr, industry_attr, sector_attr, selection)
        total = market_attr + industry_attr + sector_attr + selection + residual
        return AttributionResult(ticker=ticker, signal_date=signal_date, exit_date=exit_date,
                                  gross_return=gross_return, market_contribution=market_attr,
                                  industry_contribution=industry_attr, sector_contribution=sector_attr,
                                  selection_alpha=selection, residual=residual, total_attributed=total)

    @staticmethod
    def batch_decompose(records: list[dict]) -> list[AttributionResult]:
        return [AttributionEngine.decompose(**r) for r in records]
