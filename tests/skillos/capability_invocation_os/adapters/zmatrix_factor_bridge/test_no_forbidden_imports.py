import pytest
import os

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.constants import (
    FORBIDDEN_BRIDGE_METHOD_NAMES,
)

BRIDGE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "..",
    "skillos", "capability_invocation_os", "adapters", "zmatrix_factor_bridge",
)
BRIDGE_DIR = os.path.normpath(BRIDGE_DIR)

FORBIDDEN_METHODS = list(FORBIDDEN_BRIDGE_METHOD_NAMES)


def _read_all_source_files():
    """Yield (filename, content) for all .py files in bridge dir."""
    if not os.path.isdir(BRIDGE_DIR):
        pytest.skip("Bridge directory not found")
    for fname in sorted(os.listdir(BRIDGE_DIR)):
        if not fname.endswith(".py") or fname.startswith("__"):
            continue
        fpath = os.path.join(BRIDGE_DIR, fname)
        with open(fpath) as f:
            content = f.read()
        yield fname, content


def test_no_requests():
    for fname, content in _read_all_source_files():
        assert "import requests" not in content, f"{fname}: imports requests"
        assert "from requests" not in content, f"{fname}: imports requests"


def test_no_urllib():
    for fname, content in _read_all_source_files():
        assert "import urllib" not in content, f"{fname}: imports urllib"
        assert "from urllib" not in content, f"{fname}: imports urllib"


def test_no_httpx():
    for fname, content in _read_all_source_files():
        assert "import httpx" not in content, f"{fname}: imports httpx"
        assert "from httpx" not in content, f"{fname}: imports httpx"


def test_no_socket():
    for fname, content in _read_all_source_files():
        assert "import socket" not in content, f"{fname}: imports socket"
        assert "from socket" not in content, f"{fname}: imports socket"


def test_no_broker():
    for fname, content in _read_all_source_files():
        assert "import broker" not in content, f"{fname}: imports broker"
        assert "from broker" not in content, f"{fname}: imports broker"


def test_no_trading():
    for fname, content in _read_all_source_files():
        assert "import trading" not in content, f"{fname}: imports trading"
        assert "from trading" not in content, f"{fname}: imports trading"


def test_no_execution():
    for fname, content in _read_all_source_files():
        assert "import execution" not in content, f"{fname}: imports execution"
        assert "from execution" not in content, f"{fname}: imports execution"


def test_no_runtime_reports():
    for fname, content in _read_all_source_files():
        assert "import runtime_reports" not in content, f"{fname}: imports runtime_reports"
        assert "from runtime_reports" not in content, f"{fname}: imports runtime_reports"


def test_no_research_factor_library_import():
    for fname, content in _read_all_source_files():
        assert "research.factor_library" not in content,             f"{fname}: imports research.factor_library"


def test_no_z2_z8_z9_v3_direct_import():
    for fname, content in _read_all_source_files():
        for mod in ["z2", "z8", "z9", "v3"]:
            assert f"import {mod}" not in content, f"{fname}: imports {mod}"
            assert f"from {mod} " not in content, f"{fname}: imports {mod}"
            assert f"from {mod}." not in content, f"{fname}: imports {mod}"


def test_no_forbidden_method_names():
    for fname, content in _read_all_source_files():
        for method in FORBIDDEN_METHODS:
            assert f"def {method}(" not in content,                 f"{fname}: defines forbidden method '{method}'"
