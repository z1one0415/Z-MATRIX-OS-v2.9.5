#!/usr/bin/env python3
"""Architecture Enforcement v1.0 — Batch F-5 tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.architecture.enforcement import (
    check_pipeline_allowed_skills_only,
    check_no_unregistered_pipeline_required_gates,
    check_no_duplicate_skill_modules,
    check_no_pipeline_declares_forbidden_capability,
    check_no_real_ops_enabled_anywhere,
    run_architecture_enforcement,
)


def test_run_architecture_enforcement_clean():
    v = run_architecture_enforcement()
    assert len(v) == 0, f"enforcement violations: {v}"
    print("✅ architecture enforcement: clean")


def test_pipeline_allowed_skills_registered():
    v = check_pipeline_allowed_skills_only()
    assert len(v) == 0, f"unregistered skills: {v}"
    print("✅ enforcement: all pipeline allowed_skills registered")


def test_pipeline_required_gates_registered():
    v = check_no_unregistered_pipeline_required_gates()
    assert len(v) == 0, f"unregistered gates: {v}"
    print("✅ enforcement: all pipeline required_gates registered")


def test_no_duplicate_skill_modules():
    v = check_no_duplicate_skill_modules()
    assert len(v) == 0, f"duplicate modules: {v}"
    print("✅ enforcement: no duplicate skill modules")


def test_pipeline_forbidden_capabilities_complete():
    v = check_no_pipeline_declares_forbidden_capability()
    assert len(v) == 0, f"missing forbidden capabilities: {v}"
    print("✅ enforcement: all pipelines have complete forbidden_capabilities")


def test_no_real_ops_enabled():
    v = check_no_real_ops_enabled_anywhere()
    assert len(v) == 0, f"real ops found: {v}"
    print("✅ enforcement: no real ops enabled anywhere")


def test_enforcement_is_registry_level_scope():
    from pathlib import Path
    content = Path("docs/architecture/ARCHITECTURE_ENFORCEMENT_V10.md").read_text()
    assert "registry-level enforcement" in content
    assert "source-level" in content
    print("✅ enforcement docs: registry-level scope declared")


if __name__ == "__main__":
    test_run_architecture_enforcement_clean()
    test_pipeline_allowed_skills_registered()
    test_pipeline_required_gates_registered()
    test_no_duplicate_skill_modules()
    test_pipeline_forbidden_capabilities_complete()
    test_no_real_ops_enabled()
    test_enforcement_is_registry_level_scope()
    print("\n🏁 Architecture Enforcement v1.0 — all F-5 tests PASS")
