#!/usr/bin/env python3
"""Test: Lane E F13 shareholder yield repair closeout."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
CLOSEOUT = ROOT / "research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_e_shareholder_yield_repair/lane_closeout.json"
VALID = ["MATERIALIZED","MATERIALIZED_NON_INFORMATIVE","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA","TAXONOMY_REVIEW_REQUIRED"]

def test_lane_e_closeout_exists():
    assert CLOSEOUT.exists()

def test_lane_e_status_valid():
    c = json.loads(CLOSEOUT.read_text())
    assert "status" in c
    assert c["outcome"] in VALID

def test_lane_e_json_count():
    d = CLOSEOUT.parent
    assert len(list(d.glob("*.json"))) == 10
