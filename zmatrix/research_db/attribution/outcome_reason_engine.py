"""Batch-A: Outcome Reason Engine — classify outcome reasons."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class OutcomeReasonType(str, Enum):
    OUTPERFORM_MARKET = "OUTPERFORM_MARKET"
    OUTPERFORM_INDUSTRY = "OUTPERFORM_INDUSTRY"
    SELECTION_ALPHA = "SELECTION_ALPHA"
    MARKET_BETA_ONLY = "MARKET_BETA_ONLY"
    COST_EROSION = "COST_EROSION"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNKNOWN = "UNKNOWN"

@dataclass
class OutcomeReason:
    ticker: str; signal_date: str
    primary_reason: str = "UNKNOWN"
    secondary_reasons: list = field(default_factory=list)
    confidence: str = "LOW"
    net_return: float = 0.0
    alpha_vs_market: float = 0.0
    alpha_vs_industry: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False

class OutcomeReasonEngine:
    REASON_THRESHOLDS = {"alpha_small": 0.005, "cost_significant": 0.003, "alpha_significant": 0.03}

    @staticmethod
    def classify(ticker: str, signal_date: str, net_return: float,
                 market_return: float, industry_return: float,
                 cost_erosion_pct: float = 0.0, sample_size: int = 1) -> OutcomeReason:
        r = OutcomeReason(ticker=ticker, signal_date=signal_date, net_return=net_return)
        r.alpha_vs_market = net_return - market_return
        r.alpha_vs_industry = net_return - industry_return
        reasons = []
        th = OutcomeReasonEngine.REASON_THRESHOLDS

        if sample_size < 3: r.confidence = "LOW"
        elif sample_size >= 10: r.confidence = "HIGH"
        else: r.confidence = "MEDIUM"

        if cost_erosion_pct > 20: reasons.append(OutcomeReasonType.COST_EROSION.value)

        if r.alpha_vs_market > th["alpha_significant"]: reasons.append(OutcomeReasonType.OUTPERFORM_MARKET.value)
        if r.alpha_vs_industry > th["alpha_significant"]: reasons.append(OutcomeReasonType.OUTPERFORM_INDUSTRY.value)
        if r.alpha_vs_industry > th["alpha_small"] and r.alpha_vs_market > th["alpha_small"]:
            reasons.append(OutcomeReasonType.SELECTION_ALPHA.value)
        elif abs(r.alpha_vs_market) <= th["alpha_small"] and abs(r.alpha_vs_industry) <= th["alpha_small"]:
            reasons.append(OutcomeReasonType.MARKET_BETA_ONLY.value)

        if not reasons: reasons.append(OutcomeReasonType.INSUFFICIENT_DATA.value)
        r.primary_reason = reasons[0]
        r.secondary_reasons = reasons[1:] if len(reasons) > 1 else []
        return r

    @staticmethod
    def batch_classify(records: list[dict]) -> list[OutcomeReason]:
        return [OutcomeReasonEngine.classify(**r) for r in records]
