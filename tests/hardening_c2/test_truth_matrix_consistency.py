from pathlib import Path

def test_truth_report():
    t = Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md").read_text(encoding="utf-8")
    assert "INTEGRATION_SMOKE_CANDIDATE" in t
    assert "RC1 status: NOT_APPROVED" in t
    assert "Production status: BLOCKED" in t

def test_acceptance_matrix():
    t = Path("docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md").read_text(encoding="utf-8")
    assert "DEPTH_PARTIAL" in t
    assert "INTEGRATION_SMOKE_DONE" in t
    # Only check that no data row has ACCEPTANCE_DONE as status (header line is OK)
    for line in t.split("\n"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4 and parts[-1] == "ACCEPTANCE_DONE":
            assert "Status" in line, f"Data row has ACCEPTANCE_DONE: {line}"

def test_asset_index():
    t = Path("docs/upgrade/V40_CONTENT_ASSET_INDEX.md").read_text(encoding="utf-8")
    assert "production-ready" not in t.lower()
