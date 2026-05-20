from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class BaseType(str, Enum):
    """B-Matrix bottom-holding asset types.

    v2.1.1 keeps all v2.1 types and adds BRAND_SCARCITY_MONOPOLY.
    COMPOUNDING_QUALITY remains the stable enum value for backwards compatibility,
    but it should be read as COMPOUNDING_REINVESTMENT in v2.1.1 documents.
    """
    HIGH_DIVIDEND_ANCHOR = "HIGH_DIVIDEND_ANCHOR"
    COMPOUNDING_QUALITY = "COMPOUNDING_QUALITY"
    RESOURCE_CASH_COW = "RESOURCE_CASH_COW"
    STATE_INFRA_MONOPOLY = "STATE_INFRA_MONOPOLY"
    BRAND_SCARCITY_MONOPOLY = "BRAND_SCARCITY_MONOPOLY"
    NOT_B_MATRIX = "NOT_B_MATRIX"


class BRating(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class BEligibility(str, Enum):
    B_ELIGIBLE = "B_ELIGIBLE"
    B_WATCH = "B_WATCH"
    B_ACCUMULATION_CANDIDATE = "B_ACCUMULATION_CANDIDATE"
    B_HOLD = "B_HOLD"
    B_REVIEW = "B_REVIEW"
    B_DISQUALIFIED = "B_DISQUALIFIED"


class TrapSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CAP_B = "CAP_B"
    CAP_C = "CAP_C"
    REJECT = "REJECT"


@dataclass(frozen=True)
class TrapFlag:
    code: str
    message: str
    severity: TrapSeverity = TrapSeverity.WARNING


@dataclass
class BMatrixInput:
    symbol: str
    name: str = ""
    industry: str = ""
    is_state_owned: bool = False
    is_market_leader: bool = False
    is_st: bool = False
    suspended: bool = False
    delisting_risk: bool = False

    # profitability and return metrics
    roe_5y: Optional[float] = None
    roe_trend: Optional[str] = None
    roic_5y: Optional[float] = None
    roic_trend: Optional[str] = None
    gross_margin: Optional[float] = None
    gross_margin_stability: Optional[float] = None
    net_margin_stability: Optional[float] = None

    # valuation
    pe_ttm: Optional[float] = None
    pb: Optional[float] = None
    ev_ebitda: Optional[float] = None
    profit_percentile_5y: Optional[float] = None
    commodity_price_percentile: Optional[float] = None

    # balance sheet
    debt_ratio: Optional[float] = None
    interest_bearing_debt_growth_2y: Optional[float] = None
    goodwill_to_net_assets: Optional[float] = None

    # dividend and shareholder return
    dividend_yield: Optional[float] = None
    dividend_years_stable: Optional[int] = None
    dividends_paid_1y: Optional[float] = None
    dividends_paid_2y: Optional[List[float]] = None
    capex_2y: Optional[List[float]] = None
    ocf_2y: Optional[List[float]] = None
    buyback_quality_score: Optional[float] = None

    # time-series financials
    ocf_3y: Optional[List[float]] = None
    net_profit_3y: Optional[List[float]] = None
    ar_growth_4q: Optional[List[float]] = None
    revenue_growth_4q: Optional[List[float]] = None
    inventory_growth_4q: Optional[List[float]] = None
    cogs_growth_4q: Optional[List[float]] = None

    # v2.1 qualitative / context
    policy_stability_score: Optional[float] = None
    demand_durability_score: Optional[float] = None
    asset_monopoly_score: Optional[float] = None
    cost_curve_score: Optional[float] = None
    resource_quality_score: Optional[float] = None
    moat_score_hint: Optional[float] = None
    substitution_risk_score: Optional[float] = None

    # v2.1.1 brand scarcity features
    brand_premium_score: Optional[float] = None
    pricing_power_score: Optional[float] = None
    supply_constraint_score: Optional[float] = None
    scarcity_durability_score: Optional[float] = None
    brand_mindshare_score: Optional[float] = None
    channel_health_score: Optional[float] = None
    batch_price_trend_score: Optional[float] = None
    channel_inventory_risk_score: Optional[float] = None
    terminal_price_stability_score: Optional[float] = None
    capex_reinvestment_need: Optional[float] = None
    reinvestment_runway_score: Optional[float] = None
    young_consumer_relevance_score: Optional[float] = None
    policy_consumption_risk_score: Optional[float] = None
    demand_generation_risk_score: Optional[float] = None

    data_completeness: float = 1.0
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BMatrixResult:
    symbol: str
    name: str
    matrix: str
    base_type: BaseType
    score_raw: float
    score_final: float
    rating: BRating
    rating_cap: BRating
    eligibility: BEligibility
    quality_flags: List[str] = field(default_factory=list)
    valuation_flags: List[str] = field(default_factory=list)
    trap_flags: List[str] = field(default_factory=list)
    secondary_traits: List[str] = field(default_factory=list)
    thesis_snapshot_required: bool = True
    thesis_stop: List[str] = field(default_factory=list)
    next_trigger: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=lambda: [
        "B-Matrix only evaluates bottom-holding eligibility",
        "B-Matrix only outputs eligibility, never trade execution",
        "10% price drop is review trigger, not automatic exit",
    ])

    def validate_no_trade_action(self) -> None:
        forbidden_actions = {"BUY", "ADD", "CLEAR", "HEAVY_POSITION"}
        # Only inspect fields that may contain action-like outputs. Avoid substring false positives
        # such as buyback_quality_score or documentation text.
        action_like = [self.eligibility.value, *self.next_trigger, *self.forbidden]
        for item in action_like:
            tokenized = str(item).upper().replace("/", " ").replace(",", " ").split()
            leaked = forbidden_actions.intersection(tokenized)
            if leaked:
                raise ValueError(f"B-Matrix result leaked forbidden trade action: {sorted(leaked)[0]}")
