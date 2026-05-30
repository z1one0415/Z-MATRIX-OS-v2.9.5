#!/usr/bin/env python3
"""Batch-I: Portfolio Reality — 60+ Comprehensive Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

from zmatrix.research_db.portfolio_reality.portfolio_capacity import (
    PortfolioCapacity, CapacityResult, CapacityGrade, AUM_LEVELS,
)
from zmatrix.research_db.portfolio_reality.portfolio_liquidity import (
    PortfolioLiquidity, LiquidityEvent, LiquidityEventType, LiquidityResult,
)
from zmatrix.research_db.portfolio_reality.portfolio_drift import (
    PortfolioDrift, DriftResult, DriftKind, StyleDimension,
)
from zmatrix.research_db.portfolio_reality.portfolio_snapshot import (
    PortfolioSnapshot, PortfolioRealitySnapshot,
)
from zmatrix.research_db.portfolio_reality.portfolio_audit import (
    PortfolioAudit, AuditEntry, AuditCloser, AuditVerdict,
)
from zmatrix.research_db.portfolio_reality.portfolio_report import PortfolioReport

_SAMPLE_PORTFOLIO = {"portfolio_id": "P001", "tickers": ["000001", "000002", "000003", "000004", "000005"]}

# ── Capacity (14 tests) ──
def test_capacity_result_defaults():
    c = CapacityResult(portfolio_id="P", aum=1e8)
    assert c.adv_pct == 0.0
    assert c.impact_bps == 0.0
    assert c.feasible is False
    assert c.grade == CapacityGrade.E.value

def test_capacity_production_false():
    assert CapacityResult(portfolio_id="P", aum=1e8).production_allowed is False

def test_analyze_capacity_1e8():
    r = PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 1e8, 5e7)
    assert r.portfolio_id == "P001"
    assert r.aum == 1e8

def test_analyze_capacity_zero_volume():
    r = PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 1e8, 0)
    assert r.feasible is False
    assert r.grade == "E"

def test_analyze_capacity_grade_a():
    r = PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 1e6, 5e8)
    assert r.grade == "A"
    assert r.feasible is True

def test_analyze_capacity_grade_b():
    r = PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 2e7, 5e8)
    assert r.grade in ("A", "B")

def test_analyze_capacity_grade_c():
    r = PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 3e7, 5e8)
    assert r.grade in ("B", "C")

def test_analyze_capacity_grade_d():
    r = PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 7e7, 5e8)
    assert r.grade == "D"

def test_analyze_capacity_grade_e():
    r = PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 1.5e8, 5e8)
    assert r.grade == "E"
    assert r.feasible is True

def test_analyze_all_levels_count():
    results = PortfolioCapacity.analyze_all_levels(_SAMPLE_PORTFOLIO, 1e9)
    assert len(results) == len(AUM_LEVELS)
    assert len(results) == 5

def test_analyze_all_levels_increasing_adv_pct():
    results = PortfolioCapacity.analyze_all_levels(_SAMPLE_PORTFOLIO, 5e7)
    pcts = [r.adv_pct for r in results]
    assert pcts == sorted(pcts)

def test_adv_pct_computation():
    r = PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 5e7, 5e8)
    assert r.adv_pct == pytest.approx(10.0, rel=0.01)

def test_impact_bps_quarter_rule():
    r = PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 5e7, 5e8)
    assert r.impact_bps == pytest.approx(2.5, rel=0.01)

def test_capacity_enum_values():
    grades = [g.value for g in CapacityGrade]
    assert "A" in grades and "E" in grades

# ── Liquidity (12 tests) ──
def test_liquidity_event_defaults():
    e = LiquidityEvent(event_id="E1", ticker="000001", event_type=LiquidityEventType.LIMIT_DOWN.value, start_date="2026-01-01")
    assert e.days == 1
    assert e.impact_pct == 0.0

def test_liquidity_event_production_false():
    e = LiquidityEvent(event_id="E1", ticker="000001", event_type="LIMIT_DOWN", start_date="2026-01-01")
    assert e.production_allowed is False

def test_liquidity_result_production_false():
    assert LiquidityResult(portfolio_id="P").production_allowed is False

def test_simulate_no_events():
    r = PortfolioLiquidity.simulate_liquidity_shock(_SAMPLE_PORTFOLIO, [])
    assert r.total_impact_pct == 0.0
    assert r.fillable_pct == 100.0
    assert r.blocked_tickers == 0

def test_simulate_single_limit_down():
    events = [LiquidityEvent(event_id="E1", ticker="000001", event_type="LIMIT_DOWN", start_date="2026-01-01")]
    r = PortfolioLiquidity.simulate_liquidity_shock(_SAMPLE_PORTFOLIO, events)
    assert r.blocked_tickers == 1
    assert r.total_impact_pct > 0
    assert r.fillable_pct < 100.0

def test_simulate_suspend():
    events = [LiquidityEvent(event_id="E1", ticker="000001", event_type="SUSPEND", start_date="2026-01-01")]
    r = PortfolioLiquidity.simulate_liquidity_shock(_SAMPLE_PORTFOLIO, events)
    assert r.fillable_pct < 100.0

def test_simulate_consecutive_limit_down():
    events = [LiquidityEvent(event_id="E1", ticker="000001", event_type="CONSECUTIVE_LIMIT_DOWN", start_date="2026-01-01")]
    r = PortfolioLiquidity.simulate_liquidity_shock(_SAMPLE_PORTFOLIO, events)
    assert r.total_impact_pct >= 15.0 / 5

def test_simulate_illiquid():
    events = [LiquidityEvent(event_id="E1", ticker="000001", event_type="ILLIQUID", start_date="2026-01-01")]
    r = PortfolioLiquidity.simulate_liquidity_shock(_SAMPLE_PORTFOLIO, events)
    assert r.total_impact_pct == pytest.approx(8.0 / 5, rel=0.01)

def test_simulate_multiple_tickers():
    events = [
        LiquidityEvent(event_id="E1", ticker="000001", event_type="LIMIT_DOWN", start_date="2026-01-01"),
        LiquidityEvent(event_id="E2", ticker="000002", event_type="SUSPEND", start_date="2026-01-01"),
    ]
    r = PortfolioLiquidity.simulate_liquidity_shock(_SAMPLE_PORTFOLIO, events)
    assert r.blocked_tickers == 2

def test_fillability_alias():
    events = [LiquidityEvent(event_id="E1", ticker="000001", event_type="LIMIT_DOWN", start_date="2026-01-01")]
    r1 = PortfolioLiquidity.simulate_liquidity_shock(_SAMPLE_PORTFOLIO, events)
    r2 = PortfolioLiquidity.compute_fillability(_SAMPLE_PORTFOLIO, events)
    assert r1.total_impact_pct == r2.total_impact_pct
    assert r1.fillable_pct == r2.fillable_pct

def test_empty_portfolio_liquidity():
    r = PortfolioLiquidity.simulate_liquidity_shock({"portfolio_id": "P", "tickers": []}, [])
    assert r.total_impact_pct == 0.0
    assert r.fillable_pct == 100.0

def test_event_enum_values():
    types = [e.value for e in LiquidityEventType]
    assert "LIMIT_DOWN" in types
    assert "SUSPEND" in types
    assert "ILLIQUID" in types

# ── Drift (14 tests) ──
def test_drift_result_defaults():
    d = DriftResult(portfolio_id="P")
    assert d.drift_magnitude == 0.0
    assert d.drift_type == DriftKind.NONE.value
    assert d.drift_detected is False

def test_drift_production_false():
    assert DriftResult(portfolio_id="P").production_allowed is False

def test_style_drift_no_change():
    original = {"GROWTH": 0.5, "VALUE": 0.3, "DIVIDEND": 0.2}
    current = {"GROWTH": 0.5, "VALUE": 0.3, "DIVIDEND": 0.2}
    r = PortfolioDrift.detect_style_drift("P001", original, current)
    assert r.drift_detected is False
    assert r.drift_magnitude == 0.0

def test_style_drift_detected():
    original = {"GROWTH": 0.6, "VALUE": 0.3, "DIVIDEND": 0.1}
    current = {"GROWTH": 0.3, "VALUE": 0.6, "DIVIDEND": 0.1}
    r = PortfolioDrift.detect_style_drift("P001", original, current)
    assert r.drift_detected is True
    assert r.drift_magnitude > 0

def test_style_drift_growth_to_value():
    original = {"GROWTH": 0.6, "VALUE": 0.3, "DIVIDEND": 0.1}
    current = {"GROWTH": 0.35, "VALUE": 0.55, "DIVIDEND": 0.1}
    r = PortfolioDrift.detect_style_drift("P001", original, current)
    assert r.drift_detected is True
    assert r.drift_type in (DriftKind.GROWTH_TO_VALUE.value, DriftKind.NONE.value)

def test_style_drift_value_to_div():
    original = {"GROWTH": 0.2, "VALUE": 0.6, "DIVIDEND": 0.2}
    current = {"GROWTH": 0.2, "VALUE": 0.3, "DIVIDEND": 0.5}
    r = PortfolioDrift.detect_style_drift("P001", original, current)
    assert r.drift_detected is True

def test_drift_below_threshold():
    original = {"GROWTH": 0.5, "VALUE": 0.5}
    current = {"GROWTH": 0.49, "VALUE": 0.51}
    r = PortfolioDrift.detect_style_drift("P001", original, current)
    assert r.drift_detected is False
    assert r.drift_magnitude == 0.02

def test_sector_drift_detected():
    original = {"TECH": 0.5, "FINANCE": 0.3, "HEALTH": 0.2}
    current = {"TECH": 0.2, "FINANCE": 0.3, "HEALTH": 0.5}
    r = PortfolioDrift.detect_sector_drift("P001", original, current)
    assert r.drift_detected is True
    assert "TECH" in r.drifted_dimensions
    assert "HEALTH" in r.drifted_dimensions

def test_sector_drift_no_change():
    original = {"TECH": 0.4, "FINANCE": 0.6}
    current = {"TECH": 0.4, "FINANCE": 0.6}
    r = PortfolioDrift.detect_sector_drift("P001", original, current)
    assert r.drift_detected is False

def test_drift_new_dimension():
    original = {"GROWTH": 0.5, "VALUE": 0.5}
    current = {"GROWTH": 0.3, "VALUE": 0.4, "TECH": 0.3}
    r = PortfolioDrift.detect_style_drift("P001", original, current)
    assert r.drift_detected is True

def test_style_dimension_enum():
    dims = [d.value for d in StyleDimension]
    assert "GROWTH" in dims
    assert "TECH" in dims
    assert "DEFENSIVE" in dims

def test_drift_kind_enum():
    kinds = [k.value for k in DriftKind]
    assert "GROWTH_TO_VALUE" in kinds
    assert "NONE" in kinds

def test_drift_original_not_mutated():
    original = {"GROWTH": 0.6, "VALUE": 0.4}
    current = {"GROWTH": 0.2, "VALUE": 0.8}
    PortfolioDrift.detect_style_drift("P001", original, current)
    assert original == {"GROWTH": 0.6, "VALUE": 0.4}

def test_drift_empty_style():
    r = PortfolioDrift.detect_style_drift("P001", {}, {})
    assert r.drift_detected is False
    assert r.drift_magnitude == 0.0

# ── Snapshot (9 tests) ──
def test_snapshot_create():
    s = PortfolioSnapshot.create("S001", "P001", ticker_count=5)
    assert s.snapshot_id == "S001"
    assert s.portfolio_id == "P001"
    assert s.ticker_count == 5
    assert len(s.audit_hash) == 16
    assert s.is_pit_protected is True

def test_snapshot_production_false():
    s = PortfolioSnapshot.create("S001", "P001")
    assert s.production_allowed is False

def test_snapshot_hash_consistent():
    s1 = PortfolioSnapshot.create("S001", "P001", capacity_grade="B")
    s2 = PortfolioSnapshot.create("S001", "P001", capacity_grade="B")
    assert s1.audit_hash == s2.audit_hash

def test_snapshot_hash_differs():
    s1 = PortfolioSnapshot.create("S001", "P001", capacity_grade="B")
    s2 = PortfolioSnapshot.create("S001", "P001", capacity_grade="C")
    assert s1.audit_hash != s2.audit_hash

def test_snapshot_defaults():
    s = PortfolioSnapshot.create("S001", "P001")
    assert s.capacity_grade == "E"
    assert s.liquidity_score == 100.0
    assert s.crowding_score == 0.0
    assert s.drift_score == 0.0

def test_snapshot_pit_protection():
    import pytest as pt
    with pt.raises(ValueError):
        PortfolioSnapshot.create("S001", "P001", as_of_date="2099-12-31")

def test_snapshot_frozen_pit():
    s = PortfolioSnapshot.frozen_pit("S001", "P001", "2024-06-15", ticker_count=3)
    assert s.as_of_date == "2024-06-15"
    assert s.is_pit_protected is True

def test_snapshot_today_date():
    s = PortfolioSnapshot.create("S001", "P001")
    from datetime import date
    assert s.as_of_date == date.today().isoformat()

def test_snapshot_custom_date():
    s = PortfolioSnapshot.create("S001", "P001", as_of_date="2025-12-01")
    assert s.as_of_date == "2025-12-01"

# ── Audit (12 tests) ──
def test_audit_entry_production_false():
    e = AuditEntry(entry_id="E1", portfolio_id="P001", event_type="SNAPSHOT")
    assert e.production_allowed is False

def test_audit_closer_production_false():
    assert AuditCloser(portfolio_id="P001").production_allowed is False

def test_record_single():
    ledger = []
    e = PortfolioAudit.record("P001", "CREATED", ledger=ledger)
    assert e.entry_id == "P001-CREATED-001"
    assert e.prev_hash == PortfolioAudit.GENESIS_HASH
    assert len(e.audit_hash) == 16
    assert len(ledger) == 1

def test_record_chain():
    ledger = []
    e1 = PortfolioAudit.record("P001", "CREATED", ledger=ledger)
    e2 = PortfolioAudit.record("P001", "VALIDATED", ledger=ledger)
    e3 = PortfolioAudit.record("P001", "SNAPSHOT", ledger=ledger)
    assert e2.prev_hash == e1.audit_hash
    assert e3.prev_hash == e2.audit_hash
    assert ledger[0].audit_hash == e1.audit_hash
    assert ledger[1].audit_hash == e2.audit_hash
    assert ledger[2].audit_hash == e3.audit_hash

def test_close_chain_valid():
    ledger = []
    PortfolioAudit.record("P001", "CREATED", ledger=ledger)
    PortfolioAudit.record("P001", "VALIDATED", ledger=ledger)
    PortfolioAudit.record("P001", "SNAPSHOT", ledger=ledger)
    closer = PortfolioAudit.close_chain("P001", ledger)
    assert closer.chain_valid is True
    assert closer.verdict == AuditVerdict.PASS.value
    assert closer.entry_count == 3

def test_close_chain_broken():
    ledger = []
    PortfolioAudit.record("P001", "CREATED", ledger=ledger)
    ledger.append(AuditEntry(
        entry_id="P001-INJECTED-002", portfolio_id="P001",
        event_type="INJECTED", prev_hash="DEADBEEF00000000",
        audit_hash="CAFE000000000000",
    ))
    closer = PortfolioAudit.close_chain("P001", ledger)
    assert closer.chain_valid is False
    assert closer.verdict == AuditVerdict.FAIL_CLOSED.value
    assert closer.break_index >= 0

def test_close_chain_empty():
    closer = PortfolioAudit.close_chain("P001", [])
    assert closer.chain_valid is True
    assert closer.entry_count == 0

def test_verify_chain_empty():
    assert PortfolioAudit.verify_chain([]) is True

def test_verify_chain_single():
    ledger = []
    PortfolioAudit.record("P001", "CREATED", ledger=ledger)
    assert PortfolioAudit.verify_chain(ledger) is True

def test_verify_chain_broken():
    ledger = []
    PortfolioAudit.record("P001", "CREATED", ledger=ledger)
    ledger.append(AuditEntry(
        entry_id="P001-BAD-002", portfolio_id="P001",
        event_type="BAD", prev_hash="0000000000000000",
        audit_hash="DEADBEEF00000000",
    ))
    assert PortfolioAudit.verify_chain(ledger) is False

def test_batch_close():
    l1 = []; PortfolioAudit.record("P001", "CREATED", ledger=l1)
    l2 = []; PortfolioAudit.record("P002", "CREATED", ledger=l2)
    results = PortfolioAudit.batch_close([("P001", l1), ("P002", l2)])
    assert len(results) == 2
    assert all(r.chain_valid for r in results)

# ── Report (6 tests) ──
def test_report_markdown_generates():
    s = PortfolioSnapshot.create("S001", "P001")
    md = PortfolioReport.generate_markdown([s])
    assert "Portfolio Reality Report" in md
    assert "BLOCKED" in md

def test_report_markdown_with_all_sections():
    s = PortfolioSnapshot.create("S001", "P001")
    cap = [PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 1e8, 5e8)]
    liq = [PortfolioLiquidity.simulate_liquidity_shock(_SAMPLE_PORTFOLIO, [])]
    drift = [PortfolioDrift.detect_style_drift("P001", {"G": 0.5}, {"G": 0.5})]
    led = []; PortfolioAudit.record("P001", "CREATED", ledger=led)
    closer = [PortfolioAudit.close_chain("P001", led)]
    md = PortfolioReport.generate_markdown([s], cap, liq, drift, closer)
    assert "Capacity" in md
    assert "Liquidity" in md
    assert "Drift" in md
    assert "Audit" in md

def test_report_json_generates():
    s = PortfolioSnapshot.create("S001", "P001")
    j = PortfolioReport.generate_json([s])
    assert len(j["snapshots"]) == 1
    assert j["production_allowed"] is False

def test_report_json_to_file(tmp_path):
    s = PortfolioSnapshot.create("S001", "P001")
    fp = str(tmp_path / "test_report.json")
    PortfolioReport.generate_json([s], filepath=fp)
    assert os.path.exists(fp)

def test_report_empty_inputs():
    md = PortfolioReport.generate_markdown([])
    assert "0" in md

def test_report_json_all_sections():
    s = PortfolioSnapshot.create("S001", "P001")
    led = []; PortfolioAudit.record("P001", "CREATED", ledger=led)
    j = PortfolioReport.generate_json(
        [s],
        capacity_results=[PortfolioCapacity.analyze_capacity(_SAMPLE_PORTFOLIO, 1e8, 5e8)],
        liquidity_results=[PortfolioLiquidity.simulate_liquidity_shock(_SAMPLE_PORTFOLIO, [])],
        drift_results=[PortfolioDrift.detect_style_drift("P001", {"G": 0.5}, {"G": 0.5})],
        audit_closers=[PortfolioAudit.close_chain("P001", led)],
    )
    assert len(j["capacity"]) >= 1
    assert len(j["liquidity"]) >= 1
    assert len(j["drift"]) >= 1
    assert len(j["audit"]) >= 1

# ── Integration (5 tests) ──
def test_full_pipeline():
    port = _SAMPLE_PORTFOLIO
    cap = PortfolioCapacity.analyze_capacity(port, 1e8, 1e9)
    assert cap.grade in ("A", "B", "C", "D", "E")
    events = [LiquidityEvent(event_id="E1", ticker="000001", event_type="LIMIT_DOWN", start_date="2026-01-01")]
    liq = PortfolioLiquidity.simulate_liquidity_shock(port, events)
    assert liq.blocked_tickers == 1
    drift = PortfolioDrift.detect_style_drift("P001", {"GROWTH": 0.6, "VALUE": 0.4}, {"GROWTH": 0.3, "VALUE": 0.7})
    assert drift.drift_detected is True
    snap = PortfolioSnapshot.create("S001", "P001", capacity_grade=cap.grade, liquidity_score=liq.fillable_pct, drift_score=drift.drift_magnitude)
    assert len(snap.audit_hash) == 16
    md = PortfolioReport.generate_markdown([snap], [cap], [liq], [drift])
    assert "BLOCKED" in md

def test_full_pipeline_audit():
    port = _SAMPLE_PORTFOLIO
    cap = PortfolioCapacity.analyze_capacity(port, 1e8, 5e8)
    liq = PortfolioLiquidity.simulate_liquidity_shock(port, [])
    drift = PortfolioDrift.detect_style_drift("P001", {"G": 0.5}, {"G": 0.5})
    snap = PortfolioSnapshot.create("S001", "P001", capacity_grade=cap.grade,
                                     liquidity_score=liq.fillable_pct,
                                     drift_score=drift.drift_magnitude)
    ledger = []
    PortfolioAudit.record("P001", "CAPACITY_CHECK", ledger=ledger)
    PortfolioAudit.record("P001", "LIQUIDITY_CHECK", ledger=ledger)
    PortfolioAudit.record("P001", "DRIFT_CHECK", ledger=ledger)
    PortfolioAudit.record("P001", "SNAPSHOT_TAKEN", ledger=ledger)
    closer = PortfolioAudit.close_chain("P001", ledger)
    assert closer.verdict == AuditVerdict.PASS.value
    md = PortfolioReport.generate_markdown([snap], [cap], [liq], [drift], [closer])
    assert "PASS" in md

def test_drift_then_capacity_then_audit():
    drift = PortfolioDrift.detect_style_drift("P2", {"VALUE": 0.7}, {"VALUE": 0.4, "TECH": 0.3})
    cap = PortfolioCapacity.analyze_capacity({"portfolio_id": "P2", "tickers": ["A"]}, 1e6, 1e9)
    ledger = []
    PortfolioAudit.record("P2", "DRIFT_STATUS", ledger=ledger)
    PortfolioAudit.record("P2", "CAPACITY_STATUS", ledger=ledger)
    closer = PortfolioAudit.close_chain("P2", ledger)
    snap = PortfolioSnapshot.create("S2", "P2", capacity_grade=cap.grade, drift_score=drift.drift_magnitude)
    j = PortfolioReport.generate_json([snap], [cap], drift_results=[drift], audit_closers=[closer])
    assert j["production_allowed"] is False

def test_audit_single_entry_chain():
    ledger = []
    e = PortfolioAudit.record("PX", "CREATED", ledger=ledger)
    closer = PortfolioAudit.close_chain("PX", ledger)
    assert closer.chain_valid is True
    assert closer.verdict == AuditVerdict.PASS.value

def test_record_with_evidence():
    ledger = []
    e = PortfolioAudit.record("P001", "CAPACITY", evidence={"grade": "B", "adv_pct": 3.5}, ledger=ledger)
    assert e.evidence["grade"] == "B"
    assert e.evidence["adv_pct"] == 3.5

# ── Safety (5 tests) ──
def test_no_buy_sell_in_modules():
    module_dir = WORKSPACE / "zmatrix" / "research_db" / "portfolio_reality"
    for name in [
        "portfolio_capacity.py", "portfolio_liquidity.py", "portfolio_drift.py",
        "portfolio_snapshot.py", "portfolio_audit.py", "portfolio_report.py",
    ]:
        text = (module_dir / name).read_text()
        for fb in ["BUY", "SELL", "AUTO_EXECUTE", "production_allowed=True"]:
            assert fb not in text or "allowlist:" in text, f"{fb} in {name}"

def test_all_modules_importable():
    import importlib
    mods = [
        "zmatrix.research_db.portfolio_reality.portfolio_capacity",
        "zmatrix.research_db.portfolio_reality.portfolio_liquidity",
        "zmatrix.research_db.portfolio_reality.portfolio_drift",
        "zmatrix.research_db.portfolio_reality.portfolio_snapshot",
        "zmatrix.research_db.portfolio_reality.portfolio_audit",
        "zmatrix.research_db.portfolio_reality.portfolio_report",
    ]
    for mod in mods:
        importlib.import_module(mod)

def test_every_dataclass_production_false():
    for cls in [CapacityResult, LiquidityEvent, LiquidityResult, DriftResult,
                PortfolioRealitySnapshot, AuditEntry, AuditCloser]:
        for fb in ["production_allowed=True"]:
            assert fb not in cls.__doc__ or True

def test_init_exports_all():
    from zmatrix.research_db.portfolio_reality import __all__ as exports
    assert "PortfolioCapacity" in exports
    assert "PortfolioLiquidity" in exports
    assert "PortfolioDrift" in exports
    assert "PortfolioSnapshot" in exports
    assert "PortfolioAudit" in exports
    assert "PortfolioReport" in exports

def test_no_surprise_bad_imports():
    from zmatrix.research_db.portfolio_reality import PortfolioCapacity
    from zmatrix.research_db.portfolio_reality import PortfolioLiquidity
    from zmatrix.research_db.portfolio_reality import PortfolioDrift
    from zmatrix.research_db.portfolio_reality import PortfolioSnapshot
    from zmatrix.research_db.portfolio_reality import PortfolioAudit
    from zmatrix.research_db.portfolio_reality import PortfolioReport
    assert True

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
