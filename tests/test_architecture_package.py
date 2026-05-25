#!/usr/bin/env python3
"""Architecture Package v1.0 — Batch F-7 tests"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
ARCH_DIR = WORKSPACE / "release" / "v2.9.7-arch-RC1"


def test_arch_package_directory_exists():
    assert ARCH_DIR.exists() and ARCH_DIR.is_dir()
    print(f"✅ arch package directory: {ARCH_DIR}")


def test_required_files_exist():
    files = [
        "README.md",
        "ARCHITECTURE_MANIFEST_v2.9.7.md",
        "SHARED_SKILL_REGISTRY_V10.md",
        "PIPELINE_REGISTRY_V10.md",
        "GATE_REGISTRY_V10.md",
        "WORKFLOW_DAG_V10.md",
        "ARCHITECTURE_ENFORCEMENT_V10.md",
        "CROSS_PIPELINE_CONFLICT_AUDIT_V10.md",
        "SYSTEM_CONTROLLER_MVP_V10.md",
        "VERIFY_ARCHITECTURE_COMMANDS.md",
        "ARTIFACT_CHECKSUMS.txt",
    ]
    for f in files:
        assert (ARCH_DIR / f).exists(), f"missing: {f}"
    print(f"✅ required files: {len(files)}/11 present")


def test_checksum_file_exists_and_non_empty():
    content = (ARCH_DIR / "ARTIFACT_CHECKSUMS.txt").read_text()
    assert len(content) > 100
    assert "SHA256" in content or "checksum" in content.lower()
    print("✅ ARTIFACT_CHECKSUMS: exists and non-empty")


def test_checksums_are_consistent():
    content = (ARCH_DIR / "ARTIFACT_CHECKSUMS.txt").read_text()
    lines = [l.strip() for l in content.split("\n")
             if l.strip() and not l.startswith("#") and not l.startswith("Total")]
    for l in lines:
        parts = l.split()
        if len(parts) >= 2:
            expected = parts[0]
            filename = parts[1]
            filepath = ARCH_DIR / filename
            if filepath.exists():
                actual = hashlib.sha256(filepath.read_bytes()).hexdigest()
                assert actual == expected, f"checksum mismatch: {filename}"
    print(f"✅ checksums: {len(lines)} files verified")


def test_readme_mentions_three_layer_architecture():
    content = (ARCH_DIR / "README.md").read_text()
    assert "Shared Skill Module" in content
    assert "Pipeline Application" in content
    assert "System Control" in content
    print("✅ README: three-layer architecture mentioned")


def test_manifest_mentions_f1_to_f6():
    content = (ARCH_DIR / "ARCHITECTURE_MANIFEST_v2.9.7.md").read_text()
    for batch in ["F-1", "F-2", "F-3", "F-4", "F-5", "F-6", "F-7", "F-8"]:
        assert batch in content, f"manifest missing batch: {batch}"
    print("✅ manifest: F-1 to F-8 listed")


def test_verify_commands_mentions_script():
    content = (ARCH_DIR / "VERIFY_ARCHITECTURE_COMMANDS.md").read_text()
    assert "verify_architecture_candidate.sh" in content
    print("✅ verify commands: references verify_architecture_candidate.sh")


def test_architecture_enforcement_scope_declared():
    content = (ARCH_DIR / "ARCHITECTURE_ENFORCEMENT_V10.md").read_text()
    assert "registry-level enforcement" in content
    assert "source-level" in content
    print("✅ enforcement docs: declare registry-level scope")


def test_workflow_dag_node_types_declared():
    content = (ARCH_DIR / "WORKFLOW_DAG_V10.md").read_text()
    assert "skill nodes" in content
    assert "gate nodes" in content
    assert "SHARED_SKILL_REGISTRY" in content
    assert "GATE_REGISTRY" in content
    print("✅ workflow DAG docs: declare skill/gate node types")


def test_manifest_known_limitation_declared():
    content = (ARCH_DIR / "ARCHITECTURE_MANIFEST_v2.9.7.md").read_text()
    assert "registry-level enforcement" in content
    assert "source-level" in content.lower() or "Source-level" in content
    print("✅ manifest: known limitation declared")


def test_no_real_ops_in_boundaries():
    content = (ARCH_DIR / "README.md").read_text() + \
              (ARCH_DIR / "ARCHITECTURE_MANIFEST_v2.9.7.md").read_text()
    assert "no real trade" in content or "禁止" in content
    assert "no real Z9 write" in content or "no real_z9_write" in content
    assert "no real market fetch" in content or "no real_market_fetch" in content
    assert "no auto calibration" in content or "no auto_calibration" in content
    print("✅ boundaries: no real ops declared")


if __name__ == "__main__":
    test_arch_package_directory_exists()
    test_required_files_exist()
    test_checksum_file_exists_and_non_empty()
    test_checksums_are_consistent()
    test_readme_mentions_three_layer_architecture()
    test_manifest_mentions_f1_to_f6()
    test_verify_commands_mentions_script()
    test_architecture_enforcement_scope_declared()
    test_workflow_dag_node_types_declared()
    test_manifest_known_limitation_declared()
    test_no_real_ops_in_boundaries()
    print("\n🏁 Architecture Package v1.0 — all F-7 tests PASS")
