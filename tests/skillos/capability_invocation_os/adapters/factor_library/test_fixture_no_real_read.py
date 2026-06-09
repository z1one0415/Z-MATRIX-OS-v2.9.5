"""Tests for no-real-read enforcement via AST/source scanning — 8 tests."""

import os

# Source files to scan
_BASE_DIR = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "..", "..",
    "skillos", "capability_invocation_os", "adapters", "factor_library",
)

_SOURCE_FILES = [
    os.path.join(_BASE_DIR, "fixtures.py"),
    os.path.join(_BASE_DIR, "fixture_provider.py"),
]


def _read_all_sources() -> str:
    """Read and concatenate all source files for scanning."""
    contents = []
    for path in _SOURCE_FILES:
        resolved = os.path.normpath(path)
        with open(resolved, "r") as f:
            contents.append(f.read())
    return "\n".join(contents)


def test_no_open_call():
    """Source files must not contain open( for file reading."""
    source = _read_all_sources()
    # Allow 'open(' only if it doesn't exist
    assert "open(" not in source, "Found 'open(' in fixture source files"


def test_no_pathlib_read():
    """Source files must not contain read_text or read_bytes."""
    source = _read_all_sources()
    assert "read_text" not in source, "Found 'read_text' in fixture source files"
    assert "read_bytes" not in source, "Found 'read_bytes' in fixture source files"


def test_no_import_research():
    """Source files must not import research."""
    source = _read_all_sources()
    assert "import research" not in source, "Found 'import research' in fixture source files"


def test_no_research_factor_library():
    """Source files must not reference research.factor_library."""
    source = _read_all_sources()
    assert "research.factor_library" not in source, (
        "Found 'research.factor_library' in fixture source files"
    )


def test_no_runtime_reports():
    """Source files must not reference runtime_reports."""
    source = _read_all_sources()
    assert "runtime_reports" not in source, "Found 'runtime_reports' in fixture source files"


def test_no_runtime_audit():
    """Source files must not reference runtime_audit."""
    source = _read_all_sources()
    assert "runtime_audit" not in source, "Found 'runtime_audit' in fixture source files"


def test_no_network_imports():
    """Source files must not import network libraries."""
    source = _read_all_sources()
    for lib in ["import requests", "import httpx", "import urllib", "import socket"]:
        assert lib not in source, f"Found '{lib}' in fixture source files"
    for lib in ["from requests", "from httpx", "from urllib", "from socket"]:
        assert lib not in source, f"Found '{lib}' in fixture source files"


def test_no_broker_trading_imports():
    """Source files must not import broker/trading/execution modules."""
    source = _read_all_sources()
    for pattern in ["import broker", "import trading", "import execution",
                    "from broker", "from trading", "from execution"]:
        assert pattern not in source, f"Found '{pattern}' in fixture source files"
