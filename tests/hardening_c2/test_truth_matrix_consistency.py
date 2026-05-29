"""C2-0 Truth Matrix Consistency Test"""
from pathlib import Path

def test_truth_report():
    t = Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md").read_text(encoding="utf-8")
    assert "INTEGRATION_SMOKE_CANDIDATE" in t
    assert "RC1 status: NOT_APPROVED" in t
    assert "Production status: BLOCKED" in t
    assert "This release is not RC1" in t

def test_acceptance_matrix():
    t = Path("docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md").read_text(encoding="utf-8")
    assert "MINIMAL_CORE_DONE" in t or "IN_PROGRESS" in t
    item_lines = [l for l in t.split("\n") if "| ACCEPTANCE_DONE" in l]
    assert len(item_lines) == 0, f"Items with ACCEPTANCE_DONE: {item_lines}"

def test_asset_index():
    t = Path("docs/upgrade/V40_CONTENT_ASSET_INDEX.md").read_text(encoding="utf-8")
    assert "production-ready" not in t.lower()
