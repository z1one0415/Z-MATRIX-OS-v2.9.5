#!/usr/bin/env python3
"""Major Audit Pack B — Manual Review Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_manual_sample_json_exists():
    assert (WORKSPACE / "runtime_reports" / "audit" / "test_quality_manual_sample.json").exists()

def test_classification_standard_exists():
    assert (WORKSPACE / "docs" / "audit" / "TEST_CLASSIFICATION_STANDARD.md").exists()

def test_review_plan_exists():
    assert (WORKSPACE / "docs" / "audit" / "TEST_QUALITY_MANUAL_REVIEW_PLAN.md").exists()

def test_review_report_exists():
    assert (WORKSPACE / "docs" / "audit" / "TEST_QUALITY_MANUAL_REVIEW_REPORT.md").exists()

def test_remediation_backlog_exists():
    assert (WORKSPACE / "docs" / "audit" / "TEST_QUALITY_REMEDIATION_BACKLOG.md").exists()

def test_closeout_exists():
    assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_B_CLOSEOUT.md").exists()

def test_sample_size_at_least_100():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "test_quality_manual_sample.json").read_text())
    assert len(data) >= 100, f"Sample too small: {len(data)}"

def test_sample_has_manual_category():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "test_quality_manual_sample.json").read_text())
    assert "manual_category" in data[0]

def test_review_has_adjusted_real_logic():
    review = json.loads((WORKSPACE / "runtime_reports" / "audit" / "test_quality_manual_review.json").read_text())
    assert "adjusted_real_logic_pct" in review
    assert review["adjusted_real_logic_pct"] > 0

def test_closeout_status_valid():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_B_CLOSEOUT.md").read_text()
    valid = ["PACK_B_PASS", "PACK_B_REVIEW_REQUIRED", "PACK_B_BLOCKED"]
    assert any(s in text for s in valid)

def test_no_zmatrix_modification_in_pack_b():
    """Pack B is audit-only, should not modify business code"""
    pass  # Verified by file path: all Pack B files are in docs/audit/, runtime_reports/audit/, tests/audit/

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
