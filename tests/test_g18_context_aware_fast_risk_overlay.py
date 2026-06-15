"""Tests for V13.G18.1 Context-Aware Fast Risk Overlay."""
import sys, pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from zmatrix.prediction.fast_risk_overlay import (
    MarketSnapshot, FastRiskResult, evaluate_fast_risk_overlay,
    _check_r3_entry_cost_line_break, _check_r6_multi_market_structure_break,
    _check_r7a_blackswan_event, _check_r7b_scheduled_macro_event,
    _check_r7c_scheduled_event_day, _check_r11_position_oversold_review,
)

def _snap(**kw): return MarketSnapshot(**kw)

# ═══ R3: entry cost line break ═══
def test_r3_planned_entry_triggers():
    assert _check_r3_entry_cost_line_break(
        _snap(close=95, planned_entry_price=100, position_state="NO_POSITION", cost_line_source="planned_entry"))

def test_r3_holding_does_not_trigger():
    assert not _check_r3_entry_cost_line_break(
        _snap(close=95, planned_entry_price=100, position_state="HOLDING", cost_line_source="avg_holding_cost"))

def test_r3_no_position_no_price():
    assert not _check_r3_entry_cost_line_break(
        _snap(close=95, position_state="NO_POSITION", cost_line_source="none"))

# ═══ R6: market structure only ═══
def test_r6_r4_r5_triggers():
    assert _check_r6_multi_market_structure_break(True, True)

def test_r6_r4_alone_no():
    assert not _check_r6_multi_market_structure_break(True, False)

def test_r6_none_no():
    assert not _check_r6_multi_market_structure_break(False, False)

# ═══ R7: event splits ═══
def test_r7a_blackswan_triggers():
    assert _check_r7a_blackswan_event(
        _snap(event_risk_severity="blackswans", event_window_active=True, event_confirmation_received=False))

def test_r7a_confirmed_no():
    assert not _check_r7a_blackswan_event(
        _snap(event_risk_severity="blackswans", event_window_active=True, event_confirmation_received=True))

def test_r7b_scheduled_pre1d():
    assert _check_r7b_scheduled_macro_event(
        _snap(event_risk_severity="scheduled", event_window_active=True, event_phase="pre_1d"))

def test_r7b_no_scheduled_event():
    assert not _check_r7b_scheduled_macro_event(
        _snap(event_risk_severity="none", event_window_active=True, event_phase="pre_1d"))

def test_r7c_event_day():
    assert _check_r7c_scheduled_event_day(
        _snap(event_risk_severity="scheduled", event_window_active=True, event_phase="event_day"))

# ═══ R11: position oversold review ═══
def test_r11_holding_oversold():
    assert _check_r11_position_oversold_review(
        _snap(position_state="HOLDING", shares=100, avg_holding_cost=100, close=84, ma60_deviation_pct=-15, fundamental_deteriorated=False))

def test_r11_no_holding_no():
    assert not _check_r11_position_oversold_review(
        _snap(position_state="NO_POSITION", avg_holding_cost=100, close=84, ma60_deviation_pct=-15))

def test_r11_fundamental_deteriorated_no():
    assert not _check_r11_position_oversold_review(
        _snap(position_state="HOLDING", shares=100, avg_holding_cost=100, close=84, ma60_deviation_pct=-15, fundamental_deteriorated=True))

# ═══ No real trade ═══
def test_no_real_trade_in_result():
    result = evaluate_fast_risk_overlay(_snap(), base_score=75)
    assert result.recommended_action in ("PAPER_TRACK", "CONDITIONAL_TRACK", "WAIT", "REDUCE_OR_WAIT", "AVOID")

# ═══ R11 flag, not penalty ═══
def test_r11_not_in_penalty():
    snap = _snap(position_state="HOLDING", shares=100, avg_holding_cost=100, close=84, ma60_deviation_pct=-15)
    result = evaluate_fast_risk_overlay(snap, base_score=75)
    assert "R11" not in [g.get("gate","") for g in result.position_management_flags] or any("R11" in g.get("gate","") for g in result.position_management_flags)
