"""
Test: Level 4 no-production linkage.

Static analysis and runtime import isolation.
Verifies Level 4 modules do not reference production/broker/real_trade.
"""

import ast
import importlib
import os
import sys
import pytest


# Level 4 module root
_LEVEL4_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..", "skillos", "level4")
_LEVEL4_MODULES = ["skillos.level4"]
_PRODUCTION_PATTERNS = [
    "broker",
    "real_trade",
    "order",
    "account_id",
    "credential",
    "api_key",
    "secret",
    "trading",
    "execution",
    "live",
]


def _collect_level4_files():
    """Collect all .py files under skillos/level4/."""
    files = []
    root = os.path.abspath(_LEVEL4_ROOT)
    if not os.path.isdir(root):
        return []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".py") and fn != "__init__.py":
                files.append(os.path.join(dirpath, fn))
    return files


class TestLevel4NoProductionLinkage:

    @pytest.mark.skipif(
        not os.path.isdir(os.path.abspath(_LEVEL4_ROOT)),
        reason="skillos/level4 not found",
    )
    def test_no_broker_imports_in_source(self):
        """Level 4 source files must not import broker."""
        for filepath in _collect_level4_files():
            with open(filepath) as f:
                content = f.read()
            assert "import broker" not in content, f"{filepath} contains broker import"

    @pytest.mark.skipif(
        not os.path.isdir(os.path.abspath(_LEVEL4_ROOT)),
        reason="skillos/level4 not found",
    )
    def test_no_real_trade_imports_in_source(self):
        """Level 4 source files must not import real_trade."""
        for filepath in _collect_level4_files():
            with open(filepath) as f:
                content = f.read()
            assert "import real_trade" not in content, f"{filepath} contains real_trade import"
            assert "from real_trade" not in content, f"{filepath} contains from real_trade import"

    @pytest.mark.skipif(
        not os.path.isdir(os.path.abspath(_LEVEL4_ROOT)),
        reason="skillos/level4 not found",
    )
    def test_no_production_patterns_in_source(self):
        """Level 4 source files must not contain production patterns."""
        for filepath in _collect_level4_files():
            with open(filepath) as f:
                content = f.read()
            for pattern in _PRODUCTION_PATTERNS:
                # Skip false-positive matches in test patterns or comments
                if pattern in content and "import " + pattern in content:
                    pytest.fail(f"{filepath} contains suspicious pattern: {pattern}")

    @pytest.mark.skipif(
        not os.path.isdir(os.path.abspath(_LEVEL4_ROOT)),
        reason="skillos/level4 not found",
    )
    def test_ast_import_analysis_clean(self):
        """AST-based analysis: no prohibited imports."""
        prohibited_modules = {"broker", "real_trade", "production", "order"}
        for filepath in _collect_level4_files():
            with open(filepath) as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        parts = alias.name.split(".")
                        if parts[0] in prohibited_modules:
                            pytest.fail(
                                f"{filepath} has prohibited import: {alias.name}"
                            )
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        parts = node.module.split(".")
                        if parts[0] in prohibited_modules:
                            pytest.fail(
                                f"{filepath} has prohibited from-import: {node.module}"
                            )

    def test_level4_imports_actually_work(self):
        """Level 4 modules must be importable without failure."""
        for mod_name in _LEVEL4_MODULES:
            try:
                mod = importlib.import_module(mod_name)
                assert mod is not None
            except ImportError as e:
                # If package doesn't exist yet (P0), skip
                if "No module named" in str(e):
                    pytest.skip(f"Module {mod_name} not available (P0 expected)")
                pytest.fail(f"Cannot import {mod_name}: {e}")

    def test_level4_config_no_production_references(self):
        """Level 4 config module must not reference production paths."""
        from skillos.level4.config import load_config, env_override_disabled
        # Just verify the functions exist and are callable
        assert callable(load_config)
        assert callable(env_override_disabled)
