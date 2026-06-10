"""AST/source scan — no forbidden imports or methods in review_node source."""
import ast
import os
import pathlib

SOURCE_DIR = pathlib.Path("skillos/capability_invocation_os/review_node")

def _get_source_files():
    return list(SOURCE_DIR.glob("*.py"))

FORBIDDEN_IMPORTS = ["requests", "urllib", "httpx", "socket", "broker", "real_trade",
                     "runtime_reports", "research", "z2", "z8", "z9", "v3"]
FORBIDDEN_METHODS = ["execute", "run", "call", "invoke", "trade", "optimize",
                     "backtest_live", "generate_alpha", "generate_signal",
                     "build_portfolio", "place_order", "rebalance",
                     "mutate_memory", "write_memory", "persist_memory",
                     "trigger_z8", "trigger_broker"]

def test_no_requests_import():
    for f in _get_source_files():
        content = f.read_text()
        assert "import requests" not in content, f"{f} imports requests"
        
def test_no_urllib_import():
    for f in _get_source_files():
        content = f.read_text()
        assert "import urllib" not in content, f"{f} imports urllib"

def test_no_httpx_import():
    for f in _get_source_files():
        content = f.read_text()
        assert "import httpx" not in content, f"{f} imports httpx"

def test_no_socket_import():
    for f in _get_source_files():
        content = f.read_text()
        assert "import socket" not in content, f"{f} imports socket"

def test_no_broker_import():
    for f in _get_source_files():
        content = f.read_text()
        assert "import broker" not in content, f"{f} imports broker"

def test_no_real_trade_import():
    for f in _get_source_files():
        content = f.read_text()
        assert "import real_trade" not in content

def test_no_runtime_reports():
    for f in _get_source_files():
        content = f.read_text()
        assert "runtime_reports" not in content

def test_no_research_import():
    for f in _get_source_files():
        content = f.read_text()
        assert "from research" not in content
        assert "import research" not in content

def test_no_z2_z8_z9_v3():
    for f in _get_source_files():
        content = f.read_text()
        for mod in ["from z2", "from z8", "from z9", "from v3", "import z2", "import z8", "import z9", "import v3"]:
            assert mod not in content, f"{f} has {mod}"
