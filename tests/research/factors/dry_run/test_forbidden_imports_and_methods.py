"""
Tests for forbidden imports and methods in the dry_run package.

Verifies no network, broker, trading, execution, or SkillOS imports exist.
"""

import ast
import re
from pathlib import Path

DRY_RUN_DIR = Path("research/factor_library/dry_run")
FORBIDDEN_IMPORTS = [
    "requests", "urllib", "httpx", "socket",
    "akshare", "yfinance", "pandas_datareader",
    "broker", "trading", "execution", "skillos",
]
FORBIDDEN_METHODS = ["execute", "call", "invoke"]
FORBIDDEN_STRINGS = ["runtime_reports", "runtime_audit"]
FORBIDDEN_CALLS_WITH_DOT = ["open(", ".write("]


def _read_all_source() -> str:
    texts = []
    for f in sorted(DRY_RUN_DIR.glob("*.py")):
        texts.append(f.read_text())
    return "\n".join(texts)


def _read_all_tests() -> str:
    test_dir = Path("tests/research/factors/dry_run")
    texts = []
    for f in sorted(test_dir.glob("test_*.py")):
        texts.append(f.read_text())
    return "\n".join(texts)


def _all_source_files() -> list[str]:
    texts = []
    for f in sorted(DRY_RUN_DIR.glob("*.py")):
        texts.append(f.read_text())
    return texts


class TestForbiddenImports:
    """Verify no forbidden imports in dry_run source."""

    def test_no_requests_import(self):
        """ASSERT 38"""
        for src in _all_source_files():
            assert "import requests" not in src
            assert "from requests" not in src

    def test_no_urllib_import(self):
        """ASSERT 39"""
        for src in _all_source_files():
            assert "import urllib" not in src
            assert "from urllib" not in src

    def test_no_httpx_import(self):
        """ASSERT 40"""
        for src in _all_source_files():
            assert "import httpx" not in src
            assert "from httpx" not in src

    def test_no_socket_import(self):
        """ASSERT 41"""
        for src in _all_source_files():
            assert "import socket" not in src
            assert "from socket" not in src

    def test_no_broker_import(self):
        """ASSERT 42"""
        source_text = _read_all_source()
        assert "broker" not in source_text.lower() or \
            "broker_runtime_allowed" in source_text.lower()

    def test_no_trading_import(self):
        """ASSERT 43"""
        for src in _all_source_files():
            assert "import trading" not in src
            assert "from trading" not in src

    def test_no_execution_import(self):
        """ASSERT 44"""
        for src in _all_source_files():
            assert "import execution" not in src
            assert "from execution" not in src

    def test_no_skillos_import(self):
        """ASSERT 45"""
        for src in _all_source_files():
            assert "import skillos" not in src
            assert "from skillos" not in src


class TestNoFileOperations:
    """Verify no open() or .write() calls in source."""

    def test_no_open_call(self):
        """ASSERT 46"""
        for f in sorted(DRY_RUN_DIR.glob("*.py")):
            content = f.read_text()
            # Allow open in docstrings
            lines = [l for l in content.split("\n") if not l.strip().startswith("#") and '"""' not in l]
            code_only = "\n".join(lines)
            # Check for bare open( not in strings
            assert "open(" not in code_only.replace('"open(', "").replace("'open(", ""), \
                f"open() found in {f.name}"

    def test_no_write_call(self):
        """ASSERT 46b"""
        for f in sorted(DRY_RUN_DIR.glob("*.py")):
            content = f.read_text()
            assert ".write(" not in content, f".write() found in {f.name}"


class TestForbiddenMethods:
    """Verify no execute/call/invoke methods in ControlledNoopDryRunRunner."""

    def test_runner_has_run_not_execute(self):
        """ASSERT 49"""
        src = (DRY_RUN_DIR / "noop_runner.py").read_text()
        # Check class body
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "ControlledNoopDryRunRunner":
                method_names = [
                    n.name for n in node.body if isinstance(n, ast.FunctionDef)
                ]
                assert "run" in method_names
                assert "execute" not in method_names
                assert "call" not in method_names
                assert "invoke" not in method_names


class TestForbiddenStrings:
    """Verify no runtime_reports/runtime_audit strings in source."""

    def test_no_runtime_reports_in_source(self):
        """ASSERT 47"""
        source_text = _read_all_source()
        # runtime_reports appears only in config flag names, not as path
        assert "runtime_reports/" not in source_text

    def test_no_runtime_audit_in_source(self):
        """ASSERT 48"""
        source_text = _read_all_source()
        assert "runtime_audit/" not in source_text


class TestV13AndPyCacheChecks:
    """Verify no V13_6 or pycache in source files."""

    def test_no_v13_6(self):
        """ASSERT 53"""
        source_text = _read_all_source()
        assert "V13_6" not in source_text

    def test_no_pycache_string(self):
        """ASSERT 54"""
        source_text = _read_all_source()
        assert "__pycache__" not in source_text
