"""R-Matrix OscillationKingRanker v1.1 — Type A horizontal + Type B rising channel"""
from dataclasses import dataclass, field
from typing import List, Optional
from .oscillation_subtypes import OscillationType, assert_allowed_action
from .rising_channel_detector import detect_rising_channel
from .detrended_residual_reversion import residual_reversion_check
from .volatility_cone import residual_volatility_cone
from .rising_channel_entry_locator import locate_residual_position
from .bear_trap_detector import detect_bear_trap
from .weekly_cycle_detector import simple_weekly_cycles
from .horizontal_channel_detector import detect_horizontal_channel
from .support_resistance_detector import verify_support_resistance
from .horizontal_entry_locator import locate_horizontal_position

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

def rank_type_b_rising_channel(symbol, name, daily_prices, weekly_prices=None):
    forbidden=["不得直接BUY","不得在通道上沿追涨","跌破通道后未收回不得低吸","L2_LOST不得声称盘口承接有效"]
    trend=detect_rising_channel(daily_prices)
    if not trend.passed:
        return OscillationKingResult(symbol,name,"R_MATRIX_OSCILLATION_KING",OscillationType.RISING_CHANNEL.value,0.0,"WAIT",forbidden=forbidden,diagnostics={"reason":trend.reason})
    reversion=residual_reversion_check(trend.residuals)
    position=locate_residual_position(trend.residuals)
    cone=residual_volatility_cone(trend.residuals)
    cycle=simple_weekly_cycles(weekly_prices or daily_prices[::5])
    bear=detect_bear_trap([position.position])
    score=0.0
    if reversion.mean_reverting: score+=2.5
    if cycle.passed: score+=2.0
    if cone.state=="ACTIVE": score+=1.5
    if bear.state=="BEAR_TRAP_RECLAIMED": score+=1.5
    if position.zone=="HIGH_HARVEST_ZONE": score+=0.5
    elif position.zone in ("LOW_ZONE","LOW_REPAIR_ZONE"): score+=1.5
    score=min(score,10.0)
    # action mapping from zone+bear+cone
    if position.zone=="HIGH_HARVEST_ZONE": action="HARVEST"
    elif cone.state=="OSCILLATION_EXPIRED": action="WAIT"
    elif position.zone in ("LOW_ZONE","LOW_REPAIR_ZONE") and reversion.mean_reverting: action="WATCH"
    elif bear.state=="BEAR_TRAP_RECLAIMED": action="PAPER_PROBE"
    else: action="WAIT"
    triggers=["L3板块确认","L1.5确认承接","残差回归通道"]
    assert_allowed_action(action)
    return OscillationKingResult(symbol,name,"R_MATRIX_OSCILLATION_KING",OscillationType.RISING_CHANNEL.value,round(score,2),action,triggers,forbidden,{"trend_beta":trend.beta,"dfa_hurst":reversion.dfa_hurst,"half_life":reversion.half_life,"channel_position":position.position,"zone":position.zone,"cone":cone.state,"bear_trap":bear.state})

def rank_type_a_horizontal(symbol, name, daily_prices, weekly_prices=None):
    """Type A 水平震荡波动天王 — 6道硬门"""
    forbidden=["不得直接BUY","不得把水平箱体突破当成主升浪","跌破箱体未修复不得低吸","L2_LOST不得声称盘口承接有效"]
    # Gate A1+A2: 数据+水平趋势
    channel=detect_horizontal_channel(daily_prices)
    if not channel.passed:
        return OscillationKingResult(symbol,name,"R_MATRIX_OSCILLATION_KING",OscillationType.HORIZONTAL.value,0.0,"WAIT",forbidden=forbidden,diagnostics={"reason":channel.reason})
    # Gate A3: Hurst/DFA 均值回归
    reversion=residual_reversion_check(channel.residuals,hurst_threshold=0.46,max_half_life=60)
    if not reversion.mean_reverting:
        return OscillationKingResult(symbol,name,"R_MATRIX_OSCILLATION_KING",OscillationType.HORIZONTAL.value,0.0,"WAIT",forbidden=forbidden,diagnostics={"reason":"not mean reverting","dfa_hurst":reversion.dfa_hurst,"half_life":reversion.half_life})
    # Gate A5: 支撑阻力验证
    sr=verify_support_resistance(daily_prices[-250:],lower=channel.lower,upper=channel.upper)
    if not sr.passed:
        return OscillationKingResult(symbol,name,"R_MATRIX_OSCILLATION_KING",OscillationType.HORIZONTAL.value,0.0,"WAIT",forbidden=forbidden,diagnostics={"reason":sr.reason,"support_touches":sr.support_touches,"resistance_touches":sr.resistance_touches})
    # Gate A6: 当前位置
    entry=locate_horizontal_position(channel.channel_position)
    score=0.0
    score+=2.5  # mean reverting
    score+=2.0  # support/resistance passed
    score+=1.5 if channel.amplitude>=0.30 else 0.5
    if entry.zone=="LOW_SUPPORT_ZONE": score+=2.0
    elif entry.zone=="LOW_MID_ZONE": score+=1.0
    elif entry.zone in ("HIGH_WARNING_ZONE","RESISTANCE_HARVEST_ZONE"): score+=0.5
    score=min(score,10.0)
    action=entry.allowed_action
    assert_allowed_action(action)
    return OscillationKingResult(symbol,name,"R_MATRIX_OSCILLATION_KING",OscillationType.HORIZONTAL.value,round(score,2),action,entry.next_trigger,forbidden,{"beta":channel.beta,"dfa_hurst":reversion.dfa_hurst,"half_life":reversion.half_life,"amplitude":channel.amplitude,"channel_position":channel.channel_position,"zone":entry.zone,"support_touches":sr.support_touches,"resistance_touches":sr.resistance_touches,"support_bounce_success":sr.support_bounce_success,"resistance_reject_success":sr.resistance_reject_success})
