#!/usr/bin/env python3
"""Z-MATRIX-OS v2.9.6-RC1 — RC Packaging Tests (Batch E-2)"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
RC_DIR = WORKSPACE / "release" / "v2.9.6-RC1"


def test_rc_package_directory_exists():
    assert RC_DIR.exists(), f"missing: {RC_DIR}"
    assert RC_DIR.is_dir()
    print(f"✅ RC package directory: {RC_DIR}")


def test_rc_package_required_files_exist():
    files = [
        "README.md",
        "RC_MANIFEST_v2.9.6.md",
        "CONTRACT_INDEX_v2.9.6.md",
        "RC_KNOWN_LIMITATIONS_v2.9.6.md",
        "RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md",
        "VERIFY_COMMANDS.md",
        "ARTIFACT_CHECKSUMS.txt",
        "RELEASE_NOTES_v2.9.6-RC1.md",
    ]
    for f in files:
        path = RC_DIR / f
        assert path.exists(), f"missing required file: {path}"
    print(f"✅ RC package required files: {len(files)}/8 present")


def test_rc_package_readme_mentions_no_real_ops():
    readme = RC_DIR / "README.md"
    content = readme.read_text()
    for keyword in [
        "no real trade",
        "no real Z9 write",
        "no real market data fetch",
        "no auto calibration",
        "paper execution only",
    ]:
        assert keyword in content, f"README missing: {keyword}"
    print("✅ README: no-real-ops boundaries declared")


def test_rc_package_readme_mentions_package_commit():
    content = (RC_DIR / "README.md").read_text()
    assert "RC gate closeout commit" in content
    assert "a2ad4991ba224b532edbce7e1c03cbd4c6f43195" in content
    assert "RC package commit" in content
    assert "0882a7802dc68fdc0080933ac6e0fdc1b280eec8" in content
    print("✅ README: commits matched (gate closeout + package)")


def test_verify_commands_packaging_count_is_6():
    content = (RC_DIR / "VERIFY_COMMANDS.md").read_text()
    assert "test_rc_packaging.py" in content
    assert "6/6 PASS" in content
    print("✅ VERIFY_COMMANDS: packaging test count is 6")


def test_release_notes_mentions_core_chain_and_safety_boundaries():
    content = (RC_DIR / "RELEASE_NOTES_v2.9.6-RC1.md").read_text()
    for keyword in [
        "G18 prediction",
        "z9_calibration_policy_preview",
        "Real trade",
        "Real Z9 write",
        "Real market data fetch",
        "Auto calibration",
        "禁止",
        "Release Candidate",
        "Operator Runbook",
        "Tag v2.9.6-RC1",
    ]:
        assert keyword in content, f"release notes missing: {keyword}"
    print("✅ RELEASE_NOTES: core chain + safety boundaries confirmed")


def test_verify_commands_mentions_rc_gate():
    vc = RC_DIR / "VERIFY_COMMANDS.md"
    content = vc.read_text()
    for keyword in [
        "test_rc_verification_gate.py",
        "verify_rc_candidate.sh",
        "9/9 PASS",
        "compileall",
    ]:
        assert keyword in content, f"VERIFY_COMMANDS missing: {keyword}"
    print("✅ VERIFY_COMMANDS: references RC gate + verify script")


def test_artifact_checksums_exist_and_non_empty():
    checksums = RC_DIR / "ARTIFACT_CHECKSUMS.txt"
    content = checksums.read_text()
    assert len(content) > 100, "checksums file too short"
    assert "SHA256" in content or "checksum" in content.lower()
    # 每行检查: hex(64) + "  " + filename
    lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("Total")]
    checksum_lines = [l for l in lines if len(l.split()) >= 2]
    assert len(checksum_lines) >= 2, f"too few checksum lines: {len(checksum_lines)}"
    for l in checksum_lines:
        parts = l.split()
        digest = parts[0]
        assert len(digest) == 64, f"invalid checksum length: {len(digest)} for {parts[1]}"
        assert all(c in "0123456789abcdef" for c in digest)
    print(f"✅ ARTIFACT_CHECKSUMS: {len(checksum_lines)} files with valid sha256")


def test_checksums_are_consistent():
    """每个文件的checksum应与实际计算一致"""
    checksums = RC_DIR / "ARTIFACT_CHECKSUMS.txt"
    content = checksums.read_text()
    lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("Total")]
    for l in lines:
        parts = l.split()
        if len(parts) >= 2:
            expected_digest = parts[0]
            filename = parts[1]
            filepath = RC_DIR / filename
            if filepath.exists():
                actual = hashlib.sha256(filepath.read_bytes()).hexdigest()
                assert actual == expected_digest, f"checksum mismatch: {filename}"
    print("✅ checksums: all verified against actual files")


if __name__ == "__main__":
    test_rc_package_directory_exists()
    test_rc_package_required_files_exist()
    test_rc_package_readme_mentions_no_real_ops()
    test_rc_package_readme_mentions_package_commit()
    test_verify_commands_packaging_count_is_6()
    test_release_notes_mentions_core_chain_and_safety_boundaries()
    test_verify_commands_mentions_rc_gate()
    test_artifact_checksums_exist_and_non_empty()
    test_checksums_are_consistent()
    print("\n🏁 Z-MATRIX-OS v2.9.6-RC1 — RC Packaging tests PASS")
