#!/usr/bin/env python3
"""ROC-F1: Architecture Freeze Acceptance Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_freeze_acceptance_doc_exists():
    assert (WORKSPACE / "docs" / "research_os" / "ARCHITECTURE_FREEZE_ACCEPTANCE.md").exists()

def test_freeze_manifest_exists():
    assert (WORKSPACE / "docs" / "research_os" / "RESEARCH_OS_V3_FREEZE_MANIFEST.md").exists()

def test_acceptance_contains_freeze_status():
    text = (WORKSPACE / "docs" / "research_os" / "ARCHITECTURE_FREEZE_ACCEPTANCE.md").read_text()
    assert "ARCHITECTURE_FREEZE" in text
    assert "160" in text
    assert "1190" in text or "1,190" in text
    assert "BLOCKED" in text

def test_freezed_module_count():
    """Confirm 160 modules (exact count from find command)"""
    modules = list((WORKSPACE / "zmatrix" / "research_db").rglob("*.py"))
    actual = [m for m in modules if m.name != "__init__.py" and "__pycache__" not in str(m)]
    count = len(actual)
    assert count == 160, f"Module count drift: {count} (expected 160)"
    # If this test fails, the freeze manifest needs updating.

def test_no_production_claims():
    files = [
        "docs/research_os/ARCHITECTURE_FREEZE_ACCEPTANCE.md",
        "docs/research_os/RESEARCH_OS_V3_FREEZE_MANIFEST.md",
    ]
    for fp in files:
        text = (WORKSPACE / fp).read_text()
        for forbidden in ["Production Ready", "Broker Ready", "Runtime Ready", "Real Trade Ready"]:
            assert forbidden not in text, f"{forbidden} in {fp}"

def test_forbidden_work_listed():
    text = (WORKSPACE / "docs" / "research_os" / "RESEARCH_OS_V3_FREEZE_MANIFEST.md").read_text()
    for fb in ["broker adapter", "runtime execution", "real trade"]:
        assert fb in text.lower(), f"Missing forbidden work: {fb}"

def test_verify_script_exists():
    assert (WORKSPACE / "scripts" / "verify_research_os_architecture_freeze.sh").exists()

if __name__ == "__main__":
    test_freeze_acceptance_doc_exists()
    test_freeze_manifest_exists()
    test_acceptance_contains_freeze_status()
    test_freezed_module_count()
    test_no_production_claims()
    test_forbidden_work_listed()
    test_verify_script_exists()
    print("✅ Architecture Freeze Acceptance tests PASS")
