#!/usr/bin/env python3
"""Validate SkillOS v1.0 contract registry."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CONTRACT_PATH = ROOT / "data/research_db/agent/registry/skill_contract_registry.json"
REGISTRY_PATH = ROOT / "data/research_db/agent/registry/skill_registry.generated.json"

FORBIDDEN_WORDS = [
    "production", "broker", "real_trade", "broker_runtime",
    "auto_buy", "auto_sell", "trade_allowed",
    "buy", "sell", "order", "execution",
]


def fail(msg: str):
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def check_forbidden(data: dict) -> list:
    """Scan contract data for forbidden runtime words."""
    text = json.dumps(data).lower()
    return [w for w in FORBIDDEN_WORDS if w in text]


def validate() -> bool:
    errors = []

    # 1. Contract registry exists
    if not CONTRACT_PATH.exists():
        errors.append("contract registry file not found")

    # 2. Parseable JSON
    try:
        registry = json.loads(CONTRACT_PATH.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"invalid JSON: {e}")

    # Load existing skill registry for count comparison
    skills = json.loads(REGISTRY_PATH.read_text())

    # 3. Contracts list exists
    contracts = registry.get("contracts", [])
    if not contracts:
        errors.append("contracts list is empty")

    # 4. skill_id uniqueness
    ids = [c.get("skill_id") for c in contracts]
    dupes = [i for i in ids if ids.count(i) > 1]
    if dupes:
        errors.append(f"duplicate skill_ids: {list(set(dupes))}")

    # 5. Contract count matches
    if len(contracts) != len(skills):
        errors.append(f"contract count {len(contracts)} != registered skills {len(skills)}")

    # 6. Every registered skill has a contract
    registered_ids = {s.get("skill_id") for s in skills}
    contract_ids = set(ids)
    missing = registered_ids - contract_ids
    extra = contract_ids - registered_ids
    if missing:
        errors.append(f"missing contracts for: {sorted(missing)[:10]}...")
    if extra:
        errors.append(f"extra contracts not in registry: {sorted(extra)[:10]}...")

    # 7/8/9 Per-contract checks
    cores = ["skill_id", "skill_version", "status", "risk_level", "input_hash", "output_hash"]
    for c in contracts:
        sid = c.get("skill_id", "?")
        if not c.get("input_schema"):
            errors.append(f"{sid}: missing input_schema")
        if not c.get("output_schema"):
            errors.append(f"{sid}: missing output_schema")
        out_req = c.get("output_schema", {}).get("required", [])
        for core in cores:
            if core not in out_req:
                errors.append(f"{sid}: output_schema.required missing '{core}'")
        rl = c.get("risk_level", "?")
        risk_rank = {"R0_READ": 0, "R1_ANNOTATE": 1, "R2_DRAFT": 2}
        if risk_rank.get(rl, 99) > 2:
            errors.append(f"{sid}: risk_level {rl} exceeds R2_DRAFT")

    # 10. No forbidden runtime fields
    forbidden = check_forbidden(registry)
    if forbidden:
        errors.append(f"forbidden words found: {forbidden}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return False

    # Summary
    domains = set(c.get("domain") for c in contracts)
    cats = set(c.get("semantic_category") for c in contracts)
    print(f"contract_count: {len(contracts)}")
    print(f"registered_count: {len(skills)}")
    print(f"missing_contracts: {len(missing)}")
    print(f"extra_contracts: {len(extra)}")
    print(f"unique_skill_ids: {len(contract_ids)}")
    print(f"domains: {len(domains)}")
    print(f"max_risk: R2_DRAFT")
    print(f"semantic_categories: {sorted(cats)}")
    print("Z_SKILLOS_V1_0_A_CONTRACT_REGISTRY_INFRA_VERIFY_PASS")
    return True


if __name__ == "__main__":
    ok = validate()
    sys.exit(0 if ok else 1)
