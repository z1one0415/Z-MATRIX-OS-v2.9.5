#!/usr/bin/env python3
"""Phase 1: Account Truth Framework — Comprehensive Tests"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from pathlib import Path
from io import StringIO

WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

# ── helpers ──

def _read_csv(filename):
    p = WORKSPACE / "tests" / "fixtures" / "account_truth" / filename
    with open(p) as f:
        return list(csv.DictReader(f))

# ── raw_import_schema ──

def test_raw_import_schema_trade_fields():
    from zmatrix.research_db.account_truth.raw_import_schema import TRADE_CSV_FIELDS
    assert "trade_id" in TRADE_CSV_FIELDS
    assert "ticker" in TRADE_CSV_FIELDS
    assert "price" in TRADE_CSV_FIELDS
    assert "quantity" in TRADE_CSV_FIELDS

def test_csv_field_validation():
    from zmatrix.research_db.account_truth.raw_import_schema import validate_csv_fields, TRADE_CSV_FIELDS
    r = validate_csv_fields(["trade_id","ticker","price","quantity","amount"], TRADE_CSV_FIELDS)
    assert r["valid"] is False
    assert len(r["missing_fields"]) > 0

def test_all_schema_files_exist():
    from zmatrix.research_db.account_truth.raw_import_schema import (
        POSITION_CSV_FIELDS, ACCOUNT_SNAPSHOT_CSV_FIELDS, CASHFLOW_CSV_FIELDS,
        CAPITAL_CURVE_FIELDS, HOLDING_PNL_FIELDS, DRAWDOWN_FIELDS,
    )
    assert len(POSITION_CSV_FIELDS) > 5
    assert len(CAPITAL_CURVE_FIELDS) > 5

# ── trade_normalizer ──

def test_trade_normalizer_single():
    from zmatrix.research_db.account_truth.trade_normalizer import normalize_trade
    raw = {"trade_id": "T001", "ticker": "000001", "name": "平安银行",
           "trade_date": "2024-01-15", "side": "BUY", "price": "11.50", "quantity": "1000", "amount": "11500"}
    r = normalize_trade(raw, source_file="test.csv")
    assert r.ticker == "000001"
    assert r.total_cost == r.fee + r.stamp_duty + r.transfer_fee + r.slippage
    assert r.net_amount == r.amount - r.total_cost

def test_trade_normalizer_batch():
    from zmatrix.research_db.account_truth.trade_normalizer import normalize_trades
    rows = _read_csv("sample_trades.csv")
    results = normalize_trades(rows)
    assert len(results) == 3
    assert results[0].side == "BUY"

def test_trade_normalizer_missing_fields():
    from zmatrix.research_db.account_truth.trade_normalizer import normalize_trade
    r = normalize_trade({})
    assert r.quality_status == "MISSING_REQUIRED_FIELD"

# ── position_normalizer ──

def test_position_normalizer():
    from zmatrix.research_db.account_truth.position_normalizer import normalize_position, normalize_positions
    rows = _read_csv("sample_positions.csv")
    results = normalize_positions(rows)
    assert len(results) == 2
    assert results[0].market_value == results[0].quantity * results[0].market_price

# ── cashflow_normalizer ──

def test_cashflow_normalizer():
    from zmatrix.research_db.account_truth.cashflow_normalizer import normalize_cashflow, normalize_cashflows
    rows = _read_csv("sample_cashflows.csv")
    results = normalize_cashflows(rows)
    assert len(results) == 2
    assert results[0].cashflow_type == "DEPOSIT"

# ── account_snapshot_normalizer ──

def test_snapshot_normalizer():
    from zmatrix.research_db.account_truth.account_snapshot_normalizer import normalize_snapshot, normalize_snapshots
    rows = _read_csv("sample_account_snapshots.csv")
    results = normalize_snapshots(rows)
    assert len(results) == 2
    assert results[1].exposure > 0  # second row has market_value>0

# ── account_reconciler ──

def test_reconcile_trade_amount():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_trade_amount
    from zmatrix.research_db.account_truth.trade_normalizer import normalize_trade
    t = normalize_trade({"trade_id":"T1","ticker":"000001","trade_date":"2024-01-15","side":"BUY","price":"10","quantity":"100","amount":"1000"})
    r = reconcile_trade_amount(t)
    assert r["status"] == "PASS"

def test_reconcile_trade_mismatch():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_trade_amount
    from zmatrix.research_db.account_truth.trade_normalizer import normalize_trade
    t = normalize_trade({"trade_id":"T2","ticker":"000001","trade_date":"2024-01-15","side":"BUY","price":"10","quantity":"100","amount":"1001"})
    r = reconcile_trade_amount(t)
    assert r["status"] in ("FAILED","ERROR")  # strict_mode → ERROR on mismatch

def test_reconcile_equity():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_equity
    from zmatrix.research_db.account_truth.account_snapshot_normalizer import normalize_snapshot
    s = normalize_snapshot({"date":"2024-01-15","total_equity":"111000","cash":"88645","market_value":"22355"})
    r = reconcile_equity(s)
    assert r["status"] == "PASS"

def test_reconcile_capital_curve_empty():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_capital_curve
    r = reconcile_capital_curve([], [])
    assert r["status"] == "FAILED"
    assert r["blocking"] is True

# ── capital_curve_builder ──

def test_capital_curve_builder():
    from zmatrix.research_db.account_truth.capital_curve_builder import build_capital_curve
    curve = build_capital_curve([
        {"date": "2024-01-01", "total_equity": 100000},
        {"date": "2024-01-15", "total_equity": 101150},
    ])
    assert len(curve) == 2
    assert curve[0]["total_equity"] == 100000

def test_capital_curve_empty():
    from zmatrix.research_db.account_truth.capital_curve_builder import build_capital_curve
    assert build_capital_curve([]) == []

# ── holding_pnl_builder ──

def test_holding_pnl_builder():
    from zmatrix.research_db.account_truth.holding_pnl_builder import build_holding_pnl, COST_METHOD
    assert COST_METHOD == "FIFO"
    trades = [
        {"trade_id":"T1","ticker":"000001","name":"PB","trade_date":"2024-01-15","side":"BUY","price":"10","quantity":"100","amount":"1000"},
        {"trade_id":"T2","ticker":"000001","name":"PB","trade_date":"2024-03-20","side":"SELL","price":"12","quantity":"100","amount":"1200"},
    ]
    h = build_holding_pnl(trades, [])
    assert len(h) == 1
    assert h[0]["realized_pnl"] == 200

# ── drawdown_calculator ──

def test_drawdown_calculator():
    from zmatrix.research_db.account_truth.drawdown_calculator import calculate_drawdowns
    curve = [
        {"date":"2024-01-01","total_equity":100000},
        {"date":"2024-01-15","total_equity":95000},
        {"date":"2024-02-01","total_equity":98000},
        {"date":"2024-03-01","total_equity":105000},
    ]
    dd = calculate_drawdowns(curve)
    assert len(dd) >= 1

def test_drawdown_empty():
    from zmatrix.research_db.account_truth.drawdown_calculator import calculate_drawdowns
    assert calculate_drawdowns([]) == []

# ── trade_quality_checker ──

def test_trade_quality_ok():
    from zmatrix.research_db.account_truth.trade_quality_checker import check_trade_quality
    from zmatrix.research_db.account_truth.trade_normalizer import normalize_trade
    t = normalize_trade({"trade_id":"T1","ticker":"000001","trade_date":"2024-01-15","side":"BUY","price":"10","quantity":"100","amount":"1000"})
    r = check_trade_quality(t)
    assert r["quality"] == "READY"

def test_trade_quality_missing_ticker():
    from zmatrix.research_db.account_truth.trade_quality_checker import check_trade_quality
    from zmatrix.research_db.account_truth.trade_normalizer import normalize_trade
    t = normalize_trade({"trade_id":"T1","trade_date":"2024-01-15","side":"BUY","price":"0","quantity":"0","amount":"0"})
    r = check_trade_quality(t)
    assert r["quality"] == "ERROR"

def test_filter_quality_trades():
    from zmatrix.research_db.account_truth.trade_quality_checker import filter_quality_trades, check_trade_quality
    from zmatrix.research_db.account_truth.trade_normalizer import normalize_trade
    t1 = normalize_trade({"trade_id":"T1","ticker":"000001","trade_date":"2024-01-15","side":"BUY","price":"10","quantity":"100","amount":"1000"})
    t2 = normalize_trade({"trade_id":"T2"})
    filtered = filter_quality_trades([t1, t2])
    assert len(filtered) >= 1

# ── missing_data_detector ──

def test_detect_missing_dates():
    from zmatrix.research_db.account_truth.missing_data_detector import detect_missing_dates
    r = detect_missing_dates([{"date":"2024-01-01"},{"date":"2024-01-03"}], "2024-01-01", "2024-01-03")
    assert r["missing_dates"] >= 1  # 2024-01-02 missing

def test_detect_missing_fields():
    from zmatrix.research_db.account_truth.missing_data_detector import detect_missing_fields
    r = detect_missing_fields([{"a":1}, {"a":2,"b":3}], ["a","b"])
    assert r["issue_count"] >= 1

# ── account_truth_report ──

def test_account_truth_report_generates():
    from zmatrix.research_db.account_truth.account_truth_report import generate_account_truth_report
    report = generate_account_truth_report(trades_count=100, positions_count=50, snapshots_count=200, holdings=[{"ticker":"000001","realized_pnl":1500,"total_return":0.15}])
    assert "100" in report
    assert "BLOCKED" in report

# ── import_audit ──

def test_import_audit():
    from zmatrix.research_db.account_truth.import_audit import audit_import
    r = audit_import("test.csv", 100, 0)
    assert r["status"] == "PASS"
    assert r["production_allowed"] is False

def test_import_audit_with_errors():
    from zmatrix.research_db.account_truth.import_audit import audit_import
    r = audit_import("test.csv", 95, 5)
    assert r["status"] == "PARTIAL"

# ── no production boundary ──

def test_no_production_flags_in_module():
    from zmatrix.research_db.no_production_boundary import SAFETY_FLAGS, is_production_allowed
    assert is_production_allowed() is False
    assert SAFETY_FLAGS["production_allowed"] is False

def test_import_audit_production_false():
    from zmatrix.research_db.account_truth.import_audit import audit_import
    r = audit_import("test.csv", 10, 0)
    assert r["production_allowed"] is False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
