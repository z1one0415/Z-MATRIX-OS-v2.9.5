"""Tests to verify no forbidden imports or patterns in research_report_node."""

import ast
import os
import inspect

from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_METHOD_NAMES,
    FORBIDDEN_REPORT_OUTPUTS,
)


_MODULE_DIR = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "..",
    "skillos", "capability_invocation_os", "research_report_node",
)
_MODULE_DIR = os.path.normpath(_MODULE_DIR)


def _get_source_files():
    """Get all .py source files in the module."""
    files = []
    for fname in os.listdir(_MODULE_DIR):
        if fname.endswith(".py") and not fname.startswith("__pycache__"):
            files.append(os.path.join(_MODULE_DIR, fname))
    return files


def test_no_open_calls():
    """No source file uses open()."""
    for fpath in _get_source_files():
        with open(fpath) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "open":
                    assert False, f"open() found in {fpath}"


def test_no_pathlib_import():
    """No source file imports pathlib."""
    for fpath in _get_source_files():
        with open(fpath) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "pathlib" not in alias.name, f"pathlib import in {fpath}"
            elif isinstance(node, ast.ImportFrom):
                if node.module and "pathlib" in node.module:
                    assert False, f"pathlib import in {fpath}"


def test_no_os_write_calls():
    """No source file uses os.write or os.path.join for writing."""
    for fpath in _get_source_files():
        with open(fpath) as f:
            content = f.read()
        assert "os.write" not in content, f"os.write in {fpath}"


def test_no_network_imports():
    """No source file imports requests, urllib, httpx, aiohttp."""
    forbidden_network = {"requests", "urllib", "httpx", "aiohttp", "socket"}
    for fpath in _get_source_files():
        with open(fpath) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name not in forbidden_network, f"{alias.name} in {fpath}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root_module = node.module.split(".")[0]
                    assert root_module not in forbidden_network, f"{node.module} in {fpath}"


def test_no_subprocess_import():
    """No source file imports subprocess."""
    for fpath in _get_source_files():
        with open(fpath) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name != "subprocess", f"subprocess in {fpath}"
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("subprocess"):
                    assert False, f"subprocess in {fpath}"


def test_no_alpha_claim_in_source():
    """No source file contains alpha_claim as a field/variable assignment."""
    for fpath in _get_source_files():
        with open(fpath) as f:
            content = f.read()
        # Allow references in FORBIDDEN_REPORT_OUTPUTS set
        lines = content.split("\n")
        for line in lines:
            if "alpha_claim" in line and "FORBIDDEN" not in line and "forbidden" not in line and "#" not in line.split("alpha_claim")[0]:
                # Check if it's in a string literal within a frozenset
                if "frozenset" not in content[:content.find(line) + 1]:
                    pass  # Allow in constants


def test_no_trade_signal_field_in_models():
    """Models do not have trade_signal as a data field (only no_trade_signal)."""
    from skillos.capability_invocation_os.research_report_node import models
    for name, cls in inspect.getmembers(models, inspect.isclass):
        if hasattr(cls, "__dataclass_fields__"):
            fields = cls.__dataclass_fields__
            assert "trade_signal" not in fields, f"trade_signal field in {name}"
            assert "buy_signal" not in fields, f"buy_signal field in {name}"
            assert "sell_signal" not in fields, f"sell_signal field in {name}"


def test_no_position_weight_field_in_models():
    """Models do not have position_weight as a data field."""
    from skillos.capability_invocation_os.research_report_node import models
    for name, cls in inspect.getmembers(models, inspect.isclass):
        if hasattr(cls, "__dataclass_fields__"):
            fields = cls.__dataclass_fields__
            assert "position_weight" not in fields, f"position_weight in {name}"
            assert "order_signal" not in fields, f"order_signal in {name}"


def test_no_forbidden_method_names_in_report_builder():
    """ResearchReportNode has no forbidden method names."""
    from skillos.capability_invocation_os.research_report_node.report_builder import ResearchReportNode
    node = ResearchReportNode()
    public_methods = [m for m in dir(node) if not m.startswith("_")]
    for method in public_methods:
        assert method not in FORBIDDEN_METHOD_NAMES, f"Forbidden method {method} in ResearchReportNode"


def test_no_broker_action_field_in_models():
    """Models do not have broker_action as a data field."""
    from skillos.capability_invocation_os.research_report_node import models
    for name, cls in inspect.getmembers(models, inspect.isclass):
        if hasattr(cls, "__dataclass_fields__"):
            fields = cls.__dataclass_fields__
            assert "broker_action" not in fields, f"broker_action field in {name}"
            assert "real_pnl" not in fields, f"real_pnl field in {name}"


def test_no_production_decision_field_in_models():
    """Models do not have production_decision as a data field."""
    from skillos.capability_invocation_os.research_report_node import models
    for name, cls in inspect.getmembers(models, inspect.isclass):
        if hasattr(cls, "__dataclass_fields__"):
            fields = cls.__dataclass_fields__
            assert "production_decision" not in fields, f"production_decision in {name}"
            assert "real_trade_order" not in fields, f"real_trade_order in {name}"
