# allowlist: forbidden-token-definition
"""Agent Query Contract — query context and research query functions"""
from __future__ import annotations

from dataclasses import dataclass, field

from .token_budget import estimate_tokens


_SYSTEM_VERSION = "0.5.0-stub"
_LAYER_COUNT = 8
_LAST_AUDIT = "2026-05-31"


def _token_estimate_from_result(result: dict) -> dict:
    text = str(result)
    result["token_estimate"] = estimate_tokens(text)
    return result


def _reject_full_scan(limit: int) -> dict:
    return {
        "error": True,
        "code": "NEED_NARROWER_QUERY",
        "message": f"Full scan rejected: limit={limit}. Must be 1-100.",
        "token_estimate": 0,
    }


@dataclass
class QueryContext:
    agent_id: str
    max_items: int = 100
    token_budget: int = 4000


def get_research_summary() -> dict:
    result = {
        "system_version": _SYSTEM_VERSION,
        "layer_count": _LAYER_COUNT,
        "last_audit": _LAST_AUDIT,
        "status": "operational",
    }
    return _token_estimate_from_result(result)


def get_layer_versions() -> dict:
    layers = {
        "research_summary": "sha256:abc123v1",
        "layer_versions": "sha256:abc123v1",
        "case_data": "sha256:def456v1",
        "case_drafts": "sha256:ghi789v1",
        "research_data": "sha256:jkl012v1",
        "tests": "sha256:mno345v1",
        "docs": "sha256:pqr678v1",
        "agent_registry": "sha256:stu901v1",
    }
    return _token_estimate_from_result(layers)


def get_changed_layers(since_versions: dict) -> dict:
    current = get_layer_versions()
    current.pop("token_estimate", None)

    changes: dict[str, dict] = {}
    for layer_name, new_hash in current.items():
        old_hash = since_versions.get(layer_name, "")
        changed = old_hash != new_hash
        changes[layer_name] = {
            "old": old_hash,
            "new": new_hash,
            "changed": changed,
        }
    result = {"changes": changes}
    return _token_estimate_from_result(result)


def get_layer_slice(layer_ids: list[str], limit: int = 100) -> dict:
    if limit <= 0 or limit > 100:
        return _reject_full_scan(limit)

    layers: dict[str, dict] = {}
    current_versions = get_layer_versions()
    current_versions.pop("token_estimate", None)

    for lid in layer_ids[:limit]:
        version = current_versions.get(lid, "unknown")
        layers[lid] = {
            "layer_id": lid,
            "version": version,
            "item_count": min(limit, 100),
            "data": f"slice data for {lid}",
        }

    result = {"layers": layers}
    return _token_estimate_from_result(result)


def query_case(case_id: str) -> dict:
    result = {
        "case_id": case_id,
        "status": "draft",
        "summary": f"Case {case_id} summary data",
        "created_at": "2026-05-31T00:00:00Z",
        "updated_at": "2026-05-31T00:00:00Z",
    }
    return _token_estimate_from_result(result)


def query_event_window(target_id: str, start: str, end: str) -> dict:
    result = {
        "target_id": target_id,
        "start": start,
        "end": end,
        "events": [],
        "event_count": 0,
    }
    return _token_estimate_from_result(result)


def query_factor(factor_id: str) -> dict:
    result = {
        "factor_id": factor_id,
        "name": factor_id,
        "value": 0.0,
        "timestamp": "2026-05-31T00:00:00Z",
    }
    return _token_estimate_from_result(result)


def query_hypotheses(filters: dict) -> dict:
    result = {
        "filters": filters,
        "hypotheses": [],
        "count": 0,
    }
    return _token_estimate_from_result(result)
