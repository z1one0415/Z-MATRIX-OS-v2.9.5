#!/usr/bin/env python3
"""Test: V13.F6.3 remaining dimension contract exists and valid."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
CONTRACT = ROOT / "research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion/v13_f6_3_remaining_dimension_contract.json"

def test_contract_exists():
    assert CONTRACT.exists(), f"Contract missing: {CONTRACT}"

def test_contract_valid():
    c = json.loads(CONTRACT.read_text())
    assert c["pipeline_signature"].startswith("Z2-V13-F6-3")
    assert c["production"] == "BLOCKED"
    assert len(c["target_lanes"]) == 8
