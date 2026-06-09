#!/usr/bin/env python3
"""Test: Lane L Money Flow Microstructure closeout."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
CLOSEOUT = ROOT / "research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_l_money_flow_microstructure/lane_closeout.json"
VALID = ["MATERIALIZED","MATERIALIZED_NON_INFORMATIVE","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA","TAXONOMY_REVIEW_REQUIRED"]

def test_lane_l_closeout_exists():
    assert CLOSEOUT.exists()

def test_lane_l_status_valid():
    c = json.loads(CLOSEOUT.read_text())
    assert "status" in c
    assert c["outcome"] in VALID

def test_lane_l_json_count():
    d = CLOSEOUT.parent
    assert len(list(d.glob("*.json"))) == 10
