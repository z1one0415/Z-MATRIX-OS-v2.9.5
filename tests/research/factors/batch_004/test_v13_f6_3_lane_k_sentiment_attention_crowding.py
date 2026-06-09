#!/usr/bin/env python3
"""Test: Lane K Sentiment Attention Crowding closeout."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
CLOSEOUT = ROOT / "research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/lane_k_sentiment_attention_crowding/lane_closeout.json"
VALID = ["MATERIALIZED","MATERIALIZED_NON_INFORMATIVE","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA","TAXONOMY_REVIEW_REQUIRED"]

def test_lane_k_closeout_exists():
    assert CLOSEOUT.exists()

def test_lane_k_status_valid():
    c = json.loads(CLOSEOUT.read_text())
    assert "status" in c
    assert c["outcome"] in VALID

def test_lane_k_json_count():
    d = CLOSEOUT.parent
    assert len(list(d.glob("*.json"))) == 10
