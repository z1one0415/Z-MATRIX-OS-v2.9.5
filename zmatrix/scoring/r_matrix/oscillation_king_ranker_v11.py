from dataclasses import dataclass, field
from typing import List, Optional
from .oscillation_subtypes import OscillationType, assert_allowed_action
from .rising_channel_detector import detect_rising_channel
from .detrended_residual_reversion import residual_reversion_check
from .volatility_cone import residual_volatility_cone
from .rising_channel_entry_locator import locate_residual_position
from .bear_trap_detector import detect_bear_trap
from .weekly_cycle_detector import simple_weekly_cycles

@dataclass
class OscillationKingResult:
    symbol: str
    name: str
    role: str
    oscillation_type: str
    score: float
    allowed_action: str
    next_trigger: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=list)
    diagnostics: dict = field(default_factory=dict)


def rank_type_b_rising_channel(symbol: str, name: str, daily_prices: List[float], weekly_prices: Optional[List[float]] = None) -> OscillationKingResult:
    """Rank Type B Rising Channel Oscillation candidate.

    This function returns only non-execution actions.
    """
    forbidden = [
        "不得直接BUY",
        "不得在通道上沿追涨",
        "跌破通道后未收回不得低吸",
        "L2_LOST不得声称盘口承接有效",
    ]
    trend = detect_rising_channel(daily_prices)
    if not trend.passed:
        return OscillationKingResult(symbol, name, "R_MATRIX_OSCILLATION_KING", OscillationType.RISING_CHANNEL.value, 0.0, "WAIT", forbidden=forbidden, diagnostics={"reason": trend.reason})
    reversion = residual_reversion_check(trend.residuals)
    position = locate_residual_position(trend.residuals)
    cone = residual_volatility_cone(trend.residuals)
    cycle = simple_weekly_cycles(weekly_prices or daily_prices[::5])
    bear = detect_bear_trap([position.position])

    score = 0.0
    if reversion.mean_reverting:
        score += 2.5
    if cycle.passed:
        score += 2.0
    if cone.state == "ACTIVE":
        score += 1.5
    elif cone.state == "OSCILLATION_DECAY":
        score += 0.5
    if position.zone in {"LOW_ZONE", "LOW_REPAIR_ZONE"}:
        score += 2.0
    elif position.zone == "HIGH_HARVEST_ZONE":
        score += 0.5
    score += 1.0  # passed rising trend
    score = min(score, 10.0)

    if position.zone == "HIGH_HARVEST_ZONE":
        action = "HARVEST"
    elif cone.state == "OSCILLATION_EXPIRED":
        action = "WAIT"
    elif position.zone in {"LOW_ZONE", "LOW_REPAIR_ZONE"} and reversion.mean_reverting:
        action = "WATCH"
    elif bear.state == "BEAR_TRAP_RECLAIMED":
        action = "PAPER_PROBE"
    else:
        action = "WAIT"
    assert_allowed_action(action)
    return OscillationKingResult(
        symbol=symbol,
        name=name,
        role="R_MATRIX_OSCILLATION_KING",
        oscillation_type=OscillationType.RISING_CHANNEL.value,
        score=score,
        allowed_action=action,
        next_trigger=["L3板块确认", "L1.5确认承接", "残差回归通道"],
        forbidden=forbidden,
        diagnostics={
            "trend_beta": trend.beta,
            "dfa_hurst": reversion.dfa_hurst,
            "half_life": reversion.half_life,
            "channel_position": position.position,
            "zone": position.zone,
            "volatility_cone": cone.state,
            "decay_ratio": cone.decay_ratio,
            "cycle_count": cycle.cycle_count,
            "avg_elasticity": cycle.avg_elasticity,
        },
    )
