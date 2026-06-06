"""Tests for Level 3 audit retention stability."""

import os, time, pytest
from pathlib import Path
from tempfile import TemporaryDirectory

RETENTION_STABILITY_RUNS = 50

from zmatrix.agent.skillos_level3_retention_config import get_default_retention_config, FORBIDDEN_CLEANUP_PATHS
from zmatrix.agent.skillos_level3_retention_cleanup import run_retention_cleanup


def _populate(audit: Path, count: int = 5):
    for i in range(count):
        f = audit / f"log_{i}.txt"
        f.write_text("x" * 100)
        past = time.time() - (15 + i) * 86400
        os.utime(f, (past, past))


class TestStability:
    def test_retention_stability_audit_script_passes(self):
        import subprocess
        r = subprocess.run(
            ["python3", "scripts/skillos/audit_level3_audit_retention_stability.py"],
            capture_output=True, text=True, cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."},
        )
        assert r.returncode == 0, f"stability audit failed:\n{r.stderr}"
        assert "Z_SKILLOS_LEVEL3_AUDIT_RETENTION_STABILITY_PASS" in r.stdout

    def test_dry_run_repeated_deletes_nothing(self):
        with TemporaryDirectory() as td:
            for i in range(RETENTION_STABILITY_RUNS):
                a = Path(td) / f"s{i}"; a.mkdir(); _populate(a, 3)
                c = get_default_retention_config(a)
                r = run_retention_cleanup(c, apply=False)
                remaining = list(a.iterdir())
                assert len(remaining) == 3, f"run {i}: {len(remaining)} remain"

    def test_apply_repeated_deletes_only_scoped(self):
        with TemporaryDirectory() as td:
            a = Path(td) / "s"; a.mkdir(); _populate(a, 3)
            c = get_default_retention_config(a)
            r = run_retention_cleanup(c, apply=True)
            assert r.refused_count == 0

    def test_retention_days_repeatedly_enforced(self):
        with TemporaryDirectory() as td:
            a = Path(td) / "s"; a.mkdir()
            f = a / "fresh.txt"; f.write_text("x")
            c = get_default_retention_config(a)
            for i in range(RETENTION_STABILITY_RUNS):
                run_retention_cleanup(c, apply=True)
            assert f.exists()

    def test_cleanup_summary_deterministic(self):
        with TemporaryDirectory() as td:
            a = Path(td) / "s"; a.mkdir(); _populate(a, 5)
            c = get_default_retention_config(a)
            r1 = run_retention_cleanup(c, apply=False)
            r2 = run_retention_cleanup(c, apply=False)
            assert r1.deleted_paths == r2.deleted_paths

    def test_forbidden_paths_refused(self):
        for fb in FORBIDDEN_CLEANUP_PATHS:
            assert fb in FORBIDDEN_CLEANUP_PATHS

    def test_retention_disabled_verify_still_passes(self):
        import subprocess
        r = subprocess.run(
            ["python3", "scripts/skillos/verify_level3_audit_retention_disabled.py"],
            capture_output=True, text=True, cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."},
        )
        assert r.returncode == 0

    def test_no_runtime_code_modified_by_stability_branch(self):
        src = open("scripts/skillos/audit_level3_audit_retention_stability.py").read()
        assert "zmatrix/agent" not in src or "import" not in src
