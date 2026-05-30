#!/usr/bin/env python3
"""Phase 3-B: Outcome Schema Tests (5+)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from zmatrix.research_db.outcome_engine.outcome_schema import SignalOutcome, QualityStatus


def test_signal_outcome_creation():
    so = SignalOutcome(
        signal_id="SIG-001", ticker="000001", name="PINGAN",
        signal_date="2024-01-02", horizon="T20",
    )
    assert so.signal_id == "SIG-001"
    assert so.ticker == "000001"
    assert so.name == "PINGAN"
    assert so.signal_date == "2024-01-02"
    assert so.horizon == "T20"


def test_signal_outcome_defaults():
    so = SignalOutcome(
        signal_id="SIG-X", ticker="XXXXXX", name="TEST",
        signal_date="2024-01-01", horizon="T1",
    )
    assert so.ready is False
    assert so.blocked_reason is None
    assert so.entry_price is None
    assert so.exit_price is None
    assert so.gross_return is None
    assert so.execution_blocked is False
    assert so.execution_blocked_reason is None
    assert so.required_forward_days == 0
    assert so.available_forward_days == 0


def test_signal_outcome_quality_status():
    so = SignalOutcome(
        signal_id="SIG-002", ticker="600519", name="MAOTAI",
        signal_date="2024-01-02", horizon="T60",
        quality_status=QualityStatus.BLOCKED.value,
    )
    assert so.quality_status == "BLOCKED"


def test_signal_outcome_production_not_allowed():
    so = SignalOutcome(
        signal_id="SIG-003", ticker="000002", name="WANKE",
        signal_date="2024-01-15", horizon="T20",
    )
    assert so.production_allowed is False

    so2 = SignalOutcome(
        signal_id="SIG-004", ticker="600036", name="MERCHANTS",
        signal_date="2024-01-02", horizon="T5",
        production_allowed=True,
    )
    assert so2.production_allowed is False


def test_signal_outcome_with_alpha_fields():
    so = SignalOutcome(
        signal_id="SIG-005", ticker="000858", name="WULIANGYE",
        signal_date="2024-01-02", horizon="T1",
        ready=True, entry_price=150.0, exit_date="2024-01-03", exit_price=152.0,
        gross_return=0.0133, market_return=0.0020, alpha_vs_market=0.0113,
        max_favorable_excursion=0.02, max_adverse_excursion=0.0067,
    )
    assert so.ready is True
    assert so.gross_return == 0.0133
    assert so.alpha_vs_market == 0.0113
    assert so.max_favorable_excursion == 0.02
    assert so.max_adverse_excursion == 0.0067


def test_quality_status_enum():
    assert QualityStatus.VALIDATED.value == "VALIDATED"
    assert QualityStatus.WARNING.value == "WARNING"
    assert QualityStatus.BLOCKED.value == "BLOCKED"
    assert QualityStatus.UNKNOWN.value == "UNKNOWN"


if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
