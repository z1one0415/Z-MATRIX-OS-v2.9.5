#!/usr/bin/env python3
"""test_all_contracts_parse.py — All frontend_handoff JSON files are valid JSON.

Phase: A6 QA/Release — E2E Contract Parse Test

Scans every .json file under skillos/frontend_handoff/ recursively and verifies
each is valid, parseable JSON.
"""

import json
from pathlib import Path

SKILLOS_DIR = Path(__file__).resolve().parents[4] / "skillos" / "frontend_handoff"


def _collect_json_files() -> list[Path]:
    """Return sorted list of all .json files under skillos/frontend_handoff/."""
    return sorted(SKILLOS_DIR.rglob("*.json"))


def test_all_json_files_found():
    """Ensure we find at least the expected minimum number of JSON files."""
    json_files = _collect_json_files()
    # contracts(6) + auth(2) + fixtures(10) + state_registry(3) + observability(3) >= 24
    assert len(json_files) >= 20, \
        f"Expected at least 20 JSON files under frontend_handoff/, found {len(json_files)}"


def test_all_json_files_parse():
    """Every .json file under skillos/frontend_handoff/ parses as valid JSON."""
    failures = []
    json_files = _collect_json_files()
    for fpath in json_files:
        try:
            with open(fpath, "r") as f:
                data = json.load(f)
            # Must be a dict or list (valid JSON root)
            if not isinstance(data, (dict, list)):
                failures.append(f"{fpath.relative_to(SKILLOS_DIR)}: root is not dict/list, got {type(data).__name__}")
        except json.JSONDecodeError as e:
            failures.append(f"{fpath.relative_to(SKILLOS_DIR)}: JSON decode error: {e}")
        except Exception as e:
            failures.append(f"{fpath.relative_to(SKILLOS_DIR)}: unexpected error: {e}")

    assert len(failures) == 0, \
        f"{len(failures)} JSON files failed to parse:\n" + "\n".join(failures)


def test_all_contract_files_parse():
    """All contract JSON files parse."""
    contracts_dir = SKILLOS_DIR / "contracts"
    for fpath in sorted(contracts_dir.glob("*.json")):
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name}: root is not dict/list"


def test_all_auth_files_parse():
    """All auth JSON files parse."""
    auth_dir = SKILLOS_DIR / "auth"
    for fpath in sorted(auth_dir.glob("*.json")):
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name}: root is not dict/list"


def test_all_fixture_files_parse():
    """All fixture JSON files parse."""
    fixtures_dir = SKILLOS_DIR / "fixtures"
    for fpath in sorted(fixtures_dir.glob("*.json")):
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name}: root is not dict/list"


def test_all_state_registry_files_parse():
    """All state registry JSON files parse."""
    sr_dir = SKILLOS_DIR / "state_registry"
    for fpath in sorted(sr_dir.glob("*.json")):
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name}: root is not dict/list"


def test_all_observability_files_parse():
    """All observability JSON files parse."""
    obs_dir = SKILLOS_DIR / "observability"
    for fpath in sorted(obs_dir.glob("*.json")):
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name}: root is not dict/list"


def test_contract_files_not_empty():
    """Contract files are not empty objects."""
    contracts_dir = SKILLOS_DIR / "contracts"
    for fpath in sorted(contracts_dir.glob("*.json")):
        with open(fpath, "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            assert len(data) > 0, f"{fpath.name}: empty dict"
        elif isinstance(data, list):
            assert len(data) > 0, f"{fpath.name}: empty list"
