#!/usr/bin/env python3
"""RA-1: Full Verify Reproduction Script Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_full_verify_script_exists():
    p = WORKSPACE / "scripts" / "rc1_audit_run_full_verify.sh"
    assert p.exists(), "missing rc1_audit_run_full_verify.sh"

def test_script_calls_required_verifiers():
    content = (WORKSPACE / "scripts" / "rc1_audit_run_full_verify.sh").read_text()
    assert "verify_v40_hardening_b.sh" in content
    assert "verify_v40_hardening_c2_all.sh" in content
    assert "verify_v40_hardening_c3_all.sh" in content
    assert "pytest" in content and "tests/" in content

def test_script_uses_tee_for_logging():
    content = (WORKSPACE / "scripts" / "rc1_audit_run_full_verify.sh").read_text()
    assert "tee" in content, "must use tee to preserve output"
    assert "runtime_reports/rc1_audit" in content
    assert ".log" in content

def test_script_generates_log():
    """Run the script and verify log is generated."""
    import subprocess
    # Just check the log file is created, not running full verify here
    script = str(WORKSPACE / "scripts" / "rc1_audit_run_full_verify.sh")
    result = subprocess.run(["bash", script], capture_output=True, text=True, timeout=120, cwd=str(WORKSPACE))
    # Find log path in output
    for line in result.stdout.split("\n"):
        if line.startswith("log_path="):
            log_path = line.split("=", 1)[1].strip()
            assert Path(log_path).exists(), f"log not found: {log_path}"
            log_content = Path(log_path).read_text()
            assert "RC1 Audit Full Verify" in log_content
            assert "commit=" in log_content
            return
    assert False, "no log_path in output"

if __name__ == "__main__":
    test_full_verify_script_exists()
    test_script_calls_required_verifiers()
    test_script_uses_tee_for_logging()
    test_script_generates_log()
    print("✅ RA-1 Full Verify Reproduction tests PASS")
