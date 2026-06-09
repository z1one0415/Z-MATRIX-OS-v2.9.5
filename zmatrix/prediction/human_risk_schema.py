"""☯️ G17 Human Risk Schema v1.0

Data classes for the Human Risk Rule Engine.
Separates input/output contracts from evaluation logic.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════
# Input: Position-level market data for risk evaluation
# ═══════════════════════════════════════════════════════

@dataclass
class HumanRiskInput:
    """All data needed to evaluate position-level risk for a single holding.

    Safe default policy: None/missing fields → corresponding rule does NOT fire.
    We never penalize without evidence.
    """
    ticker: str = "UNKNOWN"

    # ── Price & volume (current bar) ──
    close: Optional[float] = None
    high: Optional[float] = None
    volume: Optional[float] = None
    avg_volume_20d: Optional[float] = None

    # ── Return data ──
    daily_return: Optional[float] = None          # today's return (decimal, e.g. -0.05 = -5%)
    prior_day_return: Optional[float] = None      # yesterday's return (decimal)

    # ── Cost & support levels ──
    user_cost_line: Optional[float] = None        # user's average cost
    d1_support: Optional[float] = None            # D1 key support level
    cycle_origin: Optional[float] = None          # cycle start price (for cycle_break)

    # ── Multi-break composite (pre-computed or from MarketSnapshot) ──
    cost_break: Optional[bool] = None             # close < user_cost_line
    support_break: Optional[bool] = None          # close < d1_support
    cycle_break: Optional[bool] = None            # close < cycle_origin

    # ── Sector & market context ──
    sector_5d_return: Optional[float] = None      # sector 5-day cumulative return
    index_5d_return: Optional[float] = None       # broad market index 5-day return
    vix_equiv: Optional[float] = None             # volatility index equivalent
    vix_threshold: float = 25.0                   # threshold for market risk trigger

    # ── Event risk ──
    event_window_active: bool = False
    days_to_event: Optional[int] = None

    # ── Position P&L ──
    unrealized_loss_pct: Optional[float] = None   # negative = loss (e.g. -0.174 = -17.4%)

    # ── Thin rebound detection ──
    prior_breakdown: bool = False                 # was there a prior breakdown?


# ═══════════════════════════════════════════════════════
# Output: Triggered rule detail
# ═══════════════════════════════════════════════════════

@dataclass
class TriggeredRule:
    """A single triggered risk rule."""
    rule_id: str                  # R01..R12
    name: str                     # human-readable
    severity: str                 # LOW / MEDIUM / HIGH / CRITICAL
    description: str              # why it fired
    values: dict = field(default_factory=dict)  # diagnostic values


# ═══════════════════════════════════════════════════════
# Output: Full risk assessment
# ═══════════════════════════════════════════════════════

@dataclass
class HumanRiskAssessment:
    """G17 output: position-level risk assessment for human consumption.

    This is NOT a trading signal. It tells the human:
    - How dangerous is this position right now?
    - What actions are gated?
    - Must I review before any operation?
    """
    ticker: str
    risk_level: str = "GREEN"                     # GREEN/YELLOW/ORANGE/RED/BLACK
    risk_score: int = 0                           # 0-100 (100 = most dangerous)
    triggered_rules: list = field(default_factory=list)  # list[TriggeredRule]
    action_gate: str = "OBSERVE"                  # OBSERVE/CONDITIONAL_TRACK/WAIT/REDUCE_OR_WAIT/EXIT_REVIEW
    add_position_allowed: bool = True
    paper_track_allowed: bool = True
    must_review: bool = False
    explain: dict = field(default_factory=dict)   # structured explanation

    def to_dict(self) -> dict:
        """Serialize for G18 pipeline consumption."""
        return {
            "ticker": self.ticker,
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "triggered_rules": [
                {"rule_id": r.rule_id, "name": r.name, "severity": r.severity,
                 "description": r.description, "values": r.values}
                for r in self.triggered_rules
            ],
            "action_gate": self.action_gate,
            "add_position_allowed": self.add_position_allowed,
            "paper_track_allowed": self.paper_track_allowed,
            "must_review": self.must_review,
            "explain": self.explain,
        }
