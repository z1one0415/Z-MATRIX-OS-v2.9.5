"""Test market data hash tool."""
import subprocess
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
HASH_TOOL = WORKSPACE / "scripts" / "cases" / "generate_market_data_source_hash.py"

def test_hash_tool_no_args():
    r = subprocess.run(["python3", str(HASH_TOOL)], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode != 0  # should fail gracefully

def test_hash_tool_with_valid_csv():
    """Hash the template CSV."""
    tmpl = WORKSPACE / "data" / "research_db" / "market_data" / "templates" / "daily_price_bar_template.csv"
    r = subprocess.run(["python3", str(HASH_TOOL), str(tmpl)], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode == 0
    assert "sha256:" in r.stdout
    assert "rows:" in r.stdout
    assert "file:" in r.stdout

def test_hash_tool_nonexistent_file():
    r = subprocess.run(["python3", str(HASH_TOOL), "nonexistent.csv"], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode != 0

def test_hash_tool_produces_valid_sha256():
    """Hash output must be a valid 64-char hex string."""
    tmpl = WORKSPACE / "data" / "research_db" / "market_data" / "templates" / "daily_price_bar_template.csv"
    r = subprocess.run(["python3", str(HASH_TOOL), str(tmpl)], capture_output=True, text=True, cwd=str(WORKSPACE))
    for line in r.stdout.strip().split("\n"):
        if line.startswith("sha256:"):
            h = line.split(": ", 1)[1]
            assert len(h) == 64
            assert all(c in "0123456789abcdef" for c in h)
