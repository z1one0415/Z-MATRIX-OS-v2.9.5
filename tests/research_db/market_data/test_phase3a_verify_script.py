#!/usr/bin/env python3
"""Phase 3-A.1: Verify Script Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

V = WORKSPACE / "scripts" / "verify_research_db_phase3a_market_baseline.sh"

def test_verify_script_exists(): assert V.exists()
def test_calls_phase2_baseline():
    c = V.read_text(); assert "verify_research_db_phase2_master_data.sh" in c
def test_calls_market_data_pytest():
    c = V.read_text(); assert "tests/research_db/market_data/" in c
def test_scans_raw_staging_vendor():
    c = V.read_text(); assert "raw/" in c and "staging/" in c and "vendor/" in c
def test_scans_xlsx_xls_patterns():
    c = V.read_text(); assert ".xlsx" in c or ".xls" in c
def test_has_10_forbidden_tokens():
    c = V.read_text()
    tokens = ["real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True",
              "auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True",
              "BUY","SELL","AUTO_EXECUTE","PLACE_ORDER","SEND_ORDER"]
    for t in tokens: assert t in c, f"missing forbidden token: {t}"
def test_no_dev_null(): assert "> /dev/null" not in V.read_text()
def test_no_tail_pipe():
    for line in V.read_text().split("\n"):
        if "| tail" in line and not line.strip().startswith("#"):
            raise AssertionError(f"tail: {line.strip()[:60]}")

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
