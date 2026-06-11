#!/usr/bin/env python3
"""test_no_dangerous_permissions.py — Scan ALL files for dangerous permissions = true.

Phase: A6 QA/Release — E2E Safety Audit

CRITICAL: Scans ALL files in skillos/frontend_handoff/ recursively for any occurrence
of the 5 dangerous permissions set to true (boolean or truthy literal).

Excludes test_no_* files from false positive triggers.

Dangerous permissions:
  - can_enable_runtime
  - can_enable_runner
  - can_enable_broker
  - can_enable_paper_trading
  - can_enable_production
"""

import json
import re
from pathlib import Path

SKILLOS_DIR = Path(__file__).resolve().parents[4] / "skillos" / "frontend_handoff"

DANGEROUS_KEYS = {
    "can_enable_runtime",
    "can_enable_runner",
    "can_enable_broker",
    "can_enable_paper_trading",
    "can_enable_production",
}


def _is_excluded(file_path: Path) -> bool:
    """Exclude files whose stem starts with 'test_no_' to avoid self-triggering."""
    return file_path.stem.startswith("test_no_")


def _check_json_value(obj, path: str, dangerous_key: str, violations: list):
    """Recursively check if a value at path for a dangerous key is boolean True."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_path = f"{path}.{k}"
            if k == dangerous_key or k in DANGEROUS_KEYS:
                if v is True:
                    violations.append(f"{new_path} = true (bool)")
                elif isinstance(v, str) and v.lower() == "true":
                    violations.append(f"{new_path} = \"true\" (string)")
            _check_json_value(v, new_path, dangerous_key, violations)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _check_json_value(item, f"{path}[{i}]", dangerous_key, violations)


def _scan_json_file(file_path: Path) -> list[str]:
    """Scan a JSON file for dangerous keys set to True. Returns list of violations."""
    violations = []
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []  # Not valid JSON, skip

    _check_json_value(data, file_path.name, "", violations)
    return violations


def _scan_text_file(file_path: Path) -> list[str]:
    """Scan a text file for dangerous permission patterns like 'key': true.

    Uses regex to catch patterns in Python files, JSON fragments, etc.
    """
    violations = []
    try:
        content = file_path.read_text()
    except Exception:
        return []

    for dk in DANGEROUS_KEYS:
        # Pattern: "can_enable_runtime": true  OR  can_enable_runtime = True
        # Match JSON-style: "can_enable_runtime": true (case-insensitive)
        json_pattern = re.compile(
            rf'["\']?{re.escape(dk)}["\']?\s*[:=]\s*true',
            re.IGNORECASE | re.MULTILINE,
        )
        # Also catch Python-style: can_enable_runtime = True
        py_pattern = re.compile(
            rf'{re.escape(dk)}\s*=\s*True',
            re.MULTILINE,
        )
        for pattern in [json_pattern, py_pattern]:
            for match in pattern.finditer(content):
                line_no = content[:match.start()].count("\n") + 1
                context = match.group(0)
                violations.append(
                    f"{file_path.name}:{line_no} → `{context}`"
                )

    return violations


def test_no_dangerous_permissions_in_any_file():
    """
    Scan ALL files recursively under skillos/frontend_handoff/ for
    any dangerous permission set to true.

    Excludes test_no_* files from triggering false positives.
    """
    all_files = sorted(SKILLOS_DIR.rglob("*"))
    # Filter: only regular files, exclude __pycache__, exclude test_no_*
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
            # Unknown file type: try text scan anyway
            violations = _scan_text_file(fpath)

        all_violations.extend(violations)

    # Build a clean report
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


def test_dangerous_permissions_not_true_in_auth_matrix():
    """Auth role permission matrix has all dangerous permissions = false."""
    matrix_path = SKILLOS_DIR / "auth" / "role_permission_matrix.json"
    with open(matrix_path, "r") as f:
        data = json.load(f)

    matrix = data["matrix"]
    violations = []
    for role, perms in matrix.items():
        for dk in DANGEROUS_KEYS:
            if dk in perms and perms[dk] is True:
                violations.append(f"matrix.{role}.{dk} = true")

    assert len(violations) == 0, \
        f"Dangerous permissions true in auth matrix:\n" + "\n".join(violations)


def test_dangerous_permissions_not_true_in_blocked_policy():
    """Blocked action policy confirms all 5 dangerous actions are blocked."""
    policy_path = SKILLOS_DIR / "auth" / "blocked_action_policy.json"
    with open(policy_path, "r") as f:
        data = json.load(f)

    blocked_actions = data.get("blocked_actions", [])
    action_names = {a["action"] for a in blocked_actions}

    # Verify all 5 dangerous action prefixes are blocked
    expected = {"enable_runtime", "enable_runner", "enable_broker",
                "enable_paper_trading", "enable_production"}
    missing = expected - action_names
    assert len(missing) == 0, f"Blocked actions missing: {missing}"

    for action in blocked_actions:
        assert action.get("block_for_all_roles") is True, \
            f"Action {action['action']} not blocked for all roles"


def test_dangerous_permissions_not_true_in_schemas():
    """Auth schema defines dangerous permissions as boolean type, not true values."""
    schema_path = SKILLOS_DIR / "auth" / "auth_schema.json"
    with open(schema_path, "r") as f:
        data = json.load(f)

    props = data.get("properties", {}).get("permissions", {}).get("properties", {})
    for dk in DANGEROUS_KEYS:
        if dk in props:
            # Schema definition: should be {"type": "boolean"}, not true
            assert props[dk] is not True, \
                f"auth_schema.json: {dk} is literal true (not schema definition)"
