#!/usr/bin/env python3
"""ResearchDB Phase 0: Directory Standard Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent


def test_directory_registry_exists():
    from zmatrix.research_db.directory_registry import get_directory_registry
    reg = get_directory_registry()
    assert len(reg) == 10


def test_validate_directory_structure_pass():
    from zmatrix.research_db.directory_registry import validate_directory_structure
    result = validate_directory_structure(WORKSPACE / "data" / "research_db")
    assert result["status"] == "PASS"
    assert len(result["missing"]) == 0


def test_validate_directory_structure_partial():
    from zmatrix.research_db.directory_registry import validate_directory_structure
    result = validate_directory_structure(Path("/nonexistent"))
    assert result["status"] == "PARTIAL"


def test_research_db_root_data_dir_exists():
    assert (WORKSPACE / "data" / "research_db" / "README.md").exists()


def test_all_subdir_readmes_exist():
    for d in ["account", "universe", "market", "finance", "signal", "outcome", "factor", "event", "caseforge", "knowledge"]:
        assert (WORKSPACE / "data" / "research_db" / d / "README.md").exists(), f"missing {d}/README.md"


if __name__ == "__main__":
    test_directory_registry_exists()
    test_validate_directory_structure_pass()
    test_validate_directory_structure_partial()
    test_research_db_root_data_dir_exists()
    test_all_subdir_readmes_exist()
    print("✅ ResearchDB Phase 0 Directory Standard tests PASS")
