"""G17 Account Confirmation Adapter — wired to Human Risk Engine v1.0.

Replaces the placeholder with real position-level risk assessment.
G18's build_final_decision reads the g17 upstream evidence slot from this output.
"""
from __future__ import annotations

from typing import Optional

from zmatrix.prediction.human_risk_schema import HumanRiskInput, HumanRiskAssessment
from zmatrix.prediction.human_risk_engine import evaluate_human_risk


def load_g17_signal(
    ticker: Optional[str] = None,
    close: Optional[float] = None,
    high: Optional[float] = None,
    volume: Optional[float] = None,
    avg_volume_20d: Optional[float] = None,
    daily_return: Optional[float] = None,
    prior_day_return: Optional[float] = None,
    user_cost_line: Optional[float] = None,
    d1_support: Optional[float] = None,
    cycle_origin: Optional[float] = None,
    sector_5d_return: Optional[float] = None,
    index_5d_return: Optional[float] = None,
    vix_equiv: Optional[float] = None,
    event_window_active: bool = False,
    days_to_event: Optional[int] = None,
    unrealized_loss_pct: Optional[float] = None,
    prior_breakdown: bool = False,
    **kwargs,
) -> dict:
    """Evaluate G17 human risk and return structured signal for G18.

    Args:
        ticker: Stock ticker
        All other args: forwarded to HumanRiskInput

    Returns:
        dict compatible with G18 upstream evidence slot format:
        {
            "source": "G17_HUMAN_RISK_ENGINE",
            "available": True,
            "risk_level": ...,
            "risk_score": ...,
            "action_gate": ...,
            "add_position_allowed": ...,
            "paper_track_allowed": ...,
            "must_review": ...,
            "triggered_rules": [...],
            "explain": {...},
        }
    """
    if ticker is None:
        # Fallback: no ticker provided, return unavailable signal
        return {
            "source": "G17_HUMAN_RISK_ENGINE",
            "available": False,
            "required": True,
            "status": "NO_TICKER_PROVIDED",
            "warnings": ["G17_NO_TICKER"],
        }

    # ── Build input ──
    inp = HumanRiskInput(
        ticker=ticker,
        close=close,
        high=high,
        volume=volume,
        avg_volume_20d=avg_volume_20d,
        daily_return=daily_return,
        prior_day_return=prior_day_return,
        user_cost_line=user_cost_line,
        d1_support=d1_support,
        cycle_origin=cycle_origin,
        sector_5d_return=sector_5d_return,
        index_5d_return=index_5d_return,
        vix_equiv=vix_equiv,
        event_window_active=event_window_active,
        days_to_event=days_to_event,
        unrealized_loss_pct=unrealized_loss_pct,
        prior_breakdown=prior_breakdown,
    )

    # ── Evaluate ──
    assessment: HumanRiskAssessment = evaluate_human_risk(inp)

    # ── Return G18-compatible signal ──
    return {
        "source": "G17_HUMAN_RISK_ENGINE",
        "available": True,
        "required": True,
        "status": "EVALUATED",
        "ticker": assessment.ticker,
        "risk_level": assessment.risk_level,
        "risk_score": assessment.risk_score,
        "action_gate": assessment.action_gate,
        "add_position_allowed": assessment.add_position_allowed,
        "paper_track_allowed": assessment.paper_track_allowed,
        "must_review": assessment.must_review,
        "triggered_rules": [
            {"rule_id": r.rule_id, "name": r.name, "severity": r.severity, "description": r.description}
            for r in assessment.triggered_rules
        ],
        "explain": assessment.explain,
        "human_final_override_required": True,
        "real_trade_allowed": False,
    }
