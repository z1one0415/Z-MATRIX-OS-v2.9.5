#!/usr/bin/env python3
"""Test: V13.F6.3 remaining dimension closeout aggregate."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
CLOSEOUT = ROOT / "research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/v13_f6_3_remaining_dimension_closeout.json"

def test_closeout_exists():
    assert CLOSEOUT.exists()

def test_closeout_valid():
    c = json.loads(CLOSEOUT.read_text())
    assert c["pipeline_signature"].startswith("Z2-V13-F6-3")
    assert c["lanes_executed"] == 8
    assert c["production"] == "BLOCKED"
    assert len(c["materialized_lanes"]) + len(c["source_contract_only"]) + len(c["blocked_lanes"]) + len(c["taxonomy_review_required"]) == 8

def test_closeout_no_alpha():
    c = json.loads(CLOSEOUT.read_text())
    assert c["alpha_claim_allowed"] == False
    assert c["real_trade"] == "BLOCKED"
