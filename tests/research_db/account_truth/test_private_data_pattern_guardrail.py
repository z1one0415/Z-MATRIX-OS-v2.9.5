#!/usr/bin/env python3
"""Phase 1.1: Private Data Pattern Guardrail Tests"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent


def test_guardrail_script_exists():
    assert (WORKSPACE / "scripts" / "verify_research_db_private_data_guardrail.sh").exists()


def test_raw_path_blocked():
    r = subprocess.run(["git", "ls-files", "data/research_db/account/raw/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    real_files = [l for l in r.stdout.split("\n") if l.strip() and not l.endswith(".gitkeep")]
    assert len(real_files) == 0, f"real files in raw/: {real_files}"


def test_staging_path_blocked():
    r = subprocess.run(["git", "ls-files", "data/research_db/account/staging/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    real_files = [l for l in r.stdout.split("\n") if l.strip() and not l.endswith(".gitkeep")]
    assert len(real_files) == 0, f"real files in staging/: {real_files}"


def test_fixtures_allowed():
    assert (WORKSPACE / "tests" / "fixtures" / "account_truth" / "sample_trades.csv").exists()
    assert (WORKSPACE / "tests" / "fixtures" / "account_truth" / "sample_positions.csv").exists()


def test_ledger_templates_allowed():
    r = subprocess.run(["git", "ls-files", "data/research_db/signal/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert "manual_decision_ledger.csv" in r.stdout


def test_guardrail_script_runs():
    r = subprocess.run(["bash", "scripts/verify_research_db_private_data_guardrail.sh"], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode == 0, f"guardrail failed: {r.stderr}"


if __name__ == "__main__":
    test_guardrail_script_exists()
    test_raw_path_blocked()
    test_staging_path_blocked()
    test_fixtures_allowed()
    test_ledger_templates_allowed()
    test_guardrail_script_runs()
    print("✅ Phase 1.1 Private Data Pattern Guardrail tests PASS")
