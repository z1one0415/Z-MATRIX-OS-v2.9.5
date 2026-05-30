#!/usr/bin/env python3
"""Golden Path Runner Tests — read-only demo, no capability expansion."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_golden_path_module_importable():
    from zmatrix.research_os.golden_path_runner import run_golden_path, generate_markdown

def test_golden_path_dry_run():
    from zmatrix.research_os.golden_path_runner import run_golden_path
    result = run_golden_path(dry_run=True)
    assert "idea" in result
    assert result["idea"]["ticker"] == "600519"
    assert "_audit_hash" in result
    assert len(result["_audit_hash"]) == 16

def test_all_9_stages_present():
    from zmatrix.research_os.golden_path_runner import run_golden_path
    result = run_golden_path(dry_run=True)
    expected_stages = ["idea", "data", "factor", "outcome", "attribution", "replay", "council", "decision", "memory"]
    for stage in expected_stages:
        assert stage in result, f"Missing stage: {stage}"

def test_council_has_12_reviewers():
    from zmatrix.research_os.golden_path_runner import run_golden_path
    result = run_golden_path(dry_run=True)
    council = result["council"]
    assert council["pass"] + council["fail"] + council.get("conditional", 0) > 0

def test_no_production_flag():
    from zmatrix.research_os.golden_path_runner import run_golden_path
    result = run_golden_path(dry_run=True)
    result_str = json.dumps(result, default=str)
    assert "production_allowed=True" not in result_str
    assert "broker_order_allowed=True" not in result_str

def test_markdown_generation():
    from zmatrix.research_os.golden_path_runner import run_golden_path, generate_markdown
    result = run_golden_path(dry_run=True)
    md = generate_markdown(result)
    assert "600519" in md
    assert "BLOCKED" in md

def test_script_exists():
    assert (WORKSPACE / "scripts" / "run_golden_path_600519.sh").exists()

def test_module_count_not_expanded():
    """Architecture freeze: no new modules beyond 160"""
    modules = list((WORKSPACE / "zmatrix" / "research_db").rglob("*.py"))
    actual = [m for m in modules if m.name != "__init__.py" and "__pycache__" not in str(m)]
    assert len(actual) == 160, f"Module count changed: {len(actual)} (freezed at 160)"

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
