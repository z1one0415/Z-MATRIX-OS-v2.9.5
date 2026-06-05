"""Read-only loader for SkillOS v1.0 contract registry.

Provides:
- load_skill_contract_registry()
- get_skill_contract(skill_id)
- list_skill_contracts()

Does NOT:
- enforce schemas on invocation
- write any data
- connect to invoke_skill
"""

import json
from pathlib import Path
from typing import Optional

_CONTRACT_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "research_db" / "agent" / "registry" / "skill_contract_registry.json"
_cache: Optional[dict] = None


def _load() -> dict:
    global _cache
    if _cache is None:
        if not _CONTRACT_PATH.exists():
            raise FileNotFoundError(f"Contract registry not found: {_CONTRACT_PATH}")
        _cache = json.loads(_CONTRACT_PATH.read_text())
    return _cache


def load_skill_contract_registry() -> dict:
    """Return full contract registry document."""
    return _load()


def get_skill_contract(skill_id: str) -> Optional[dict]:
    """Get contract entry for a specific skill_id, or None."""
    reg = _load()
    for c in reg.get("contracts", []):
        if c.get("skill_id") == skill_id:
            return c
    return None


def list_skill_contracts(domain: Optional[str] = None) -> list:
    """List all contract entries, optionally filtered by domain."""
    reg = _load()
    contracts = reg.get("contracts", [])
    if domain:
        contracts = [c for c in contracts if c.get("domain") == domain]
    return contracts
