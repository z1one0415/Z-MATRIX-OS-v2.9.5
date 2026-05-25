#!/usr/bin/env python3
"""Pipeline Registry v1.0 — Batch F-2 contract tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path

from zmatrix.architecture.pipeline_registry import (
    PIPELINE_REGISTRY,
    get_pipeline,
    get_allowed_skills,
    check_pipeline_registry_integrity,
    check_pipeline_skills_registered,
)
from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY


def test_pipeline_registry_exists_and_non_empty():
    assert isinstance(PIPELINE_REGISTRY, dict)
    assert len(PIPELINE_REGISTRY) >= 2, f"expected >=2 pipelines, got {len(PIPELINE_REGISTRY)}"
    print(f"✅ pipeline registry exists: {len(PIPELINE_REGISTRY)} pipelines registered")


def test_every_pipeline_has_required_fields():
    for pid, p in PIPELINE_REGISTRY.items():
        assert p.get("layer") == "pipeline_application", f"{pid}: layer"
        assert p.get("pipeline_path"), f"{pid}: missing pipeline_path"
        assert p.get("owner"), f"{pid}: missing owner"
        assert p.get("contract"), f"{pid}: missing contract"
        assert p.get("test"), f"{pid}: missing test"
        assert p.get("allowed_skills") is not None, f"{pid}: missing allowed_skills"
        assert p.get("forbidden_capabilities") is not None, f"{pid}: missing forbidden_capabilities"
    print(f"✅ every pipeline has required fields ({len(PIPELINE_REGISTRY)} pipelines)")


def test_every_allowed_skill_is_registered():
    """allowed_skills 必须存在于 SHARED_SKILL_REGISTRY"""
    for pid, p in PIPELINE_REGISTRY.items():
        for skill_id in p.get("allowed_skills", []):
            assert skill_id in SHARED_SKILL_REGISTRY, \
                f"{pid}: allowed_skill '{skill_id}' not registered in SHARED_SKILL_REGISTRY"
    print("✅ all pipeline allowed_skills exist in SHARED_SKILL_REGISTRY")


def test_g18_pipeline_uses_required_z9_chain_skills():
    """Z-G18 必须包含 paper.record + z9 sample/queue/backfill/policy"""
    g18 = get_pipeline("Z-G18")
    assert g18 is not None, "Z-G18 not registered"
    skills = set(g18["allowed_skills"])
    required = {
        "paper.record",
        "z9.sample.build",
        "z9.queue.build",
        "z9.backfill_task.build",
        "z9.calibration_policy.preview",
    }
    missing = required - skills
    assert not missing, f"Z-G18 missing required skills: {missing}"
    print(f"✅ Z-G18 has all {len(required)} required Z9 chain skills")


def test_pipeline_forbidden_capabilities_include_no_real_ops():
    """每条 pipeline 的 forbidden_capabilities 必须包含 no-real-ops 四项"""
    for pid, p in PIPELINE_REGISTRY.items():
        fc = p.get("forbidden_capabilities", [])
        for required in ["real_trade", "real_z9_write", "real_market_fetch", "auto_calibration"]:
            assert required in fc, f"{pid}: forbidden_capabilities missing {required}"
    print("✅ all pipelines forbid real_trade / real_z9_write / real_market_fetch / auto_calibration")


def test_pipeline_registry_integrity_clean():
    violations = check_pipeline_registry_integrity()
    assert len(violations) == 0, f"integrity violations: {violations}"
    print("✅ pipeline registry integrity: clean")


def test_rc_release_pipeline_registered():
    rc = get_pipeline("RC-release")
    assert rc is not None, "RC-release not registered"
    assert rc["owner"] == "RC"
    assert "rc.checksum.build" in rc["allowed_skills"]
    print("✅ RC-release pipeline registered")


def test_g09_g14_pipelines_registered():
    for pid in ["Z-G09", "Z-G14"]:
        p = get_pipeline(pid)
        assert p is not None, f"{pid} not registered"
        assert "r_matrix.evaluate_cycle" in p["allowed_skills"], f"{pid} missing r_matrix.evaluate_cycle"
    print("✅ Z-G09 / Z-G14 pipelines registered with R-Matrix skill")


def test_pipeline_skills_registered_check_clean():
    unreg = check_pipeline_skills_registered()
    assert len(unreg) == 0, f"unregistered skills found: {unreg}"
    print("✅ all pipeline skills pass registration cross-check")


def test_get_pipeline_api():
    assert get_pipeline("Z-G18") is not None
    assert get_pipeline("nonexistent") is None
    print("✅ get_pipeline API works")


def test_get_allowed_skills_api():
    skills = get_allowed_skills("Z-G18")
    assert "paper.record" in skills
    assert "decision.finalize" in skills
    assert get_allowed_skills("nonexistent") == []
    print("✅ get_allowed_skills API works")


if __name__ == "__main__":
    test_pipeline_registry_exists_and_non_empty()
    test_every_pipeline_has_required_fields()
    test_every_allowed_skill_is_registered()
    test_g18_pipeline_uses_required_z9_chain_skills()
    test_pipeline_forbidden_capabilities_include_no_real_ops()
    test_pipeline_registry_integrity_clean()
    test_rc_release_pipeline_registered()
    test_g09_g14_pipelines_registered()
    test_pipeline_skills_registered_check_clean()
    test_get_pipeline_api()
    test_get_allowed_skills_api()
    print("\n🏁 Pipeline Registry v1.0 — all F-2 tests PASS")
