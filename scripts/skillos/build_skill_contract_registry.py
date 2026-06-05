#!/usr/bin/env python3
"""Build SkillOS v1.0 contract registry from existing skill registry.

Reads: skill_registry.generated.json (READ-ONLY)
Writes: skill_contract_registry.json
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY_IN = ROOT / "data/research_db/agent/registry/skill_registry.generated.json"
CONTRACT_OUT = ROOT / "data/research_db/agent/registry/skill_contract_registry.json"


def derive_semantic_category(entry: dict) -> str:
    """Derive semantic category from skill_id function verb."""
    sid = entry.get("skill_id", "")
    verb = sid.split(".")[-1].split("_")[0] if "." in sid else ""
    risk = entry.get("risk_level", "R0_READ")
    has_writes = bool(entry.get("write_layers"))

    deterministic_verbs = {
        "GET", "SCAN", "VALIDATE", "BUILD", "CALCULATE", "CHECK",
        "LIST", "FIND", "LOAD", "QUERY", "INSPECT", "VERIFY",
    }
    structured_verbs = {
        "DRAFT", "REVIEW", "PROPOSE", "GENERATE", "AUDIT",
        "ASSESS", "EVALUATE", "ANNOTATE", "CLASSIFY",
    }
    narrative_verbs = {
        "REPORT", "NARRATIVE", "EXPLAIN", "SUMMARIZE",
    }

    if verb in narrative_verbs or (risk == "R2_DRAFT" and has_writes):
        return "NARRATIVE_RENDERER"
    if verb in structured_verbs or risk == "R1_ANNOTATE":
        return "STRUCTURED_DRAFT"
    return "DETERMINISTIC"


def build_base_output_schema() -> dict:
    """Base output schema required for all skills."""
    return {
        "type": "object",
        "required": [
            "skill_id",
            "skill_version",
            "status",
            "risk_level",
            "input_hash",
            "output_hash",
        ],
        "properties": {
            "skill_id": {"type": "string"},
            "skill_version": {"type": "string"},
            "status": {
                "type": "string",
                "enum": ["SUCCESS", "PARTIAL", "FAILED", "BLOCKED"],
            },
            "risk_level": {
                "type": "string",
                "enum": ["R0_READ", "R1_ANNOTATE", "R2_DRAFT"],
            },
            "input_hash": {"type": "string"},
            "output_hash": {"type": "string"},
            "data_snapshot_id": {"type": ["string", "null"]},
            "evidence_refs": {"type": "array", "items": {"type": "string"}},
            "safety_envelope": {
                "type": "object",
                "properties": {
                    "blocked": {"type": "boolean"},
                    "blocking_reasons": {"type": "array", "items": {"type": "string"}},
                    "risk_flags": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "additionalProperties": True,
    }


def build_input_schema(entry: dict) -> dict:
    """Build input_schema based on skill domain and type."""
    domain = entry.get("domain", "")
    has_writes = bool(entry.get("write_layers"))

    schema = {
        "type": "object",
        "properties": {},
        "additionalProperties": True,
    }

    if domain in {
        "RESEARCHDB", "FACTOR", "MATRIX", "COUNCIL", "PORTFOLIO",
        "BMATRIX", "DMATRIX", "WORKFLOW", "CASEFORGE", "AUTOCASE",
        "DATAFORGE", "ZC35",
    }:
        schema["properties"]["data_snapshot_id"] = {"type": ["string", "null"]}

    if has_writes:
        schema["properties"]["dry_run"] = {"type": "boolean", "default": True}

    return schema


def build() -> dict:
    """Read existing registry, produce contract entries."""
    if not REGISTRY_IN.exists():
        print(f"FAIL: {REGISTRY_IN} not found", file=sys.stderr)
        sys.exit(1)

    skills = json.loads(REGISTRY_IN.read_text())
    contracts = []

    for entry in skills:
        sid = entry.get("skill_id", "")
        if not sid:
            continue

        category = derive_semantic_category(entry)
        output_schema = build_base_output_schema()

        contract = {
            "skill_id": sid,
            "skill_version": "1.0.0",
            "domain": entry.get("domain", ""),
            "risk_level": entry.get("risk_level", "R0_READ"),
            "semantic_category": category,
            "input_schema": build_input_schema(entry),
            "output_schema": output_schema,
            "status": "ACTIVE",
            "write_layers": entry.get("write_layers", []),
            "requires_human_review": entry.get("requires_human_review", True),
            "proposal_required": entry.get("proposal_required", True),
        }
        contracts.append(contract)

    return {
        "contract_version": "1.0.0",
        "source_registry": "skill_registry.generated.json",
        "skill_count": len(contracts),
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "contracts": contracts,
    }


if __name__ == "__main__":
    registry = build()
    CONTRACT_OUT.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_OUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")
    print(f"Built contract registry: {len(registry['contracts'])} skills → {CONTRACT_OUT}")
