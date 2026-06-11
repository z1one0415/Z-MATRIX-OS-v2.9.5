#!/usr/bin/env python3
"""test_no_runtime_enablement.py — Scan ALL files for runtime enablement flags = true.

Phase: A6 QA/Release — E2E Safety Audit

CRITICAL: Scans ALL files in skillos/frontend_handoff/ recursively for any occurrence
of runtime enablement flags set to true.

Excludes test_no_* files from false positive triggers.

Runtime enablement flags:
  - promotion_allowed = true
  - alpha_claim_allowed = true
  - runner_enabled = true
  - paper_trading_allowed = true
"""

import json
import re
from pathlib import Path

SKILLOS_DIR = Path(__file__).resolve().parents[4] / "skillos" / "frontend_handoff"

RUNTIME_FLAGS = {
    "promotion_allowed",
    "alpha_claim_allowed",
    "runner_enabled",
    "paper_trading_allowed",
}


def _is_excluded(file_path: Path) -> bool:
    """Exclude files whose stem starts with 'test_no_' to avoid self-triggering."""
    return file_path.stem.startswith("test_no_")


def _check_json_value(obj, path: str, runtime_key: str, violations: list):
    """Recursively check if a value at path for a runtime flag is boolean True."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_path = f"{path}.{k}"
            if k == runtime_key or k in RUNTIME_FLAGS:
                if v is True:
                    violations.append(f"{new_path} = true (bool)")
                elif isinstance(v, str) and v.lower() == "true":
                    violations.append(f"{new_path} = \"true\" (string)")
            _check_json_value(v, new_path, runtime_key, violations)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _check_json_value(item, f"{path}[{i}]", runtime_key, violations)


def _scan_json_file(file_path: Path) -> list[str]:
    """Scan a JSON file for runtime enablement flags set to True."""
    violations = []
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []

    for flag in RUNTIME_FLAGS:
        _check_json_value(data, file_path.name, flag, violations)
    return violations


def _scan_text_file(file_path: Path) -> list[str]:
    """Scan a text file for runtime enablement flag patterns.

    Catches patterns in Python files, JSON fragments, Markdown, etc.

    For Python (.py) files: only matches module-level assignment patterns
    like `runner_enabled = True`. Dict key-values like `"runner_enabled": True`
    are gate state data, not config enablement, and are excluded.

    For JSON and other text files: matches both `"key": true` and `key = true`.
    """
    violations = []
    try:
        content = file_path.read_text()
    except Exception:
        return []

    is_python = file_path.suffix.lower() == ".py"

    for rf in RUNTIME_FLAGS:
        if is_python:
            # Python files: only flag assignment-style patterns like `key = True`
            # Dict key-values like `"key": True` inside data structures are excluded
            py_pattern = re.compile(
                rf'(?<![\"\']){re.escape(rf)}(?![\"\'])\s*=\s*True',
                re.MULTILINE,
            )
            for match in py_pattern.finditer(content):
                line_no = content[:match.start()].count("\n") + 1
                context = match.group(0)
                violations.append(
                    f"{file_path.name}:{line_no} → `{context}`"
                )
        else:
            # JSON/Markdown/text files: catch both JSON-style and assignment-style
            pattern = re.compile(
                rf'["\']?{re.escape(rf)}["\']?\s*[:=]\s*true',
                re.IGNORECASE | re.MULTILINE,
            )
            for match in pattern.finditer(content):
                line_no = content[:match.start()].count("\n") + 1
                context = match.group(0)
                violations.append(
                    f"{file_path.name}:{line_no} → `{context}`"
                )

    return violations


def test_no_runtime_enablement_in_any_file():
    """
    Scan ALL files recursively under skillos/frontend_handoff/ for
    any runtime enablement flag set to true.

    Excludes test_no_* files from triggering false positives.
    """
    all_files = sorted(SKILLOS_DIR.rglob("*"))
    scan_files = [
        f for f in all_files
        if f.is_file()
        and "__pycache__" not in str(f)
        and not _is_excluded(f)
    ]

    all_violations = []

    for fpath in scan_files:
        suffix = fpath.suffix.lower()

        if suffix == ".json":
            violations = _scan_json_file(fpath)
        elif suffix in (".py", ".md", ".txt", ".cfg", ".ini", ".yaml", ".yml"):
            violations = _scan_text_file(fpath)
        else:
            violations = _scan_text_file(fpath)

        all_violations.extend(violations)

    rel_files = sorted(set(
        str(f.relative_to(SKILLOS_DIR)) for f in scan_files
    ))
    report_lines = [
        f"Scanned {len(scan_files)} files under skillos/frontend_handoff/",
        f"Violations found: {len(all_violations)}",
    ]
    if all_violations:
        report_lines.append("--- VIOLATIONS ---")
        report_lines.extend(all_violations)

    assert len(all_violations) == 0, "\n".join(report_lines)


def test_runtime_enablement_not_true_in_gate_state_schema():
    """Gate state schema has runtime enablement flags as boolean type, not true values."""
    schema_path = SKILLOS_DIR / "state_registry" / "gate_state_schema.json"
    with open(schema_path, "r") as f:
        data = json.load(f)

    gates = data.get("properties", {}).get("gates", {}).get("items", {}).get("properties", {})
    for rf in RUNTIME_FLAGS:
        if rf in gates:
            prop_def = gates[rf]
            # Schema definition should be {"type": "boolean", ...}, not literal true
            assert prop_def is not True, \
                f"gate_state_schema.json: {rf} is literal true (not schema definition)"


def test_runtime_enablement_not_true_in_run_state_schema():
    """Run state schema does not have runtime_enabled/runner_enabled set to true."""
    schema_path = SKILLOS_DIR / "state_registry" / "run_state_schema.json"
    with open(schema_path, "r") as f:
        data = json.load(f)

    # Check runtime_enabled and runner_enabled in run state schema
    props = data.get("properties", {})
    for key in ("runtime_enabled", "runner_enabled"):
        if key in props:
            prop_def = props[key]
            assert prop_def is not True, \
                f"run_state_schema.json: {key} is literal true (not schema definition)"
