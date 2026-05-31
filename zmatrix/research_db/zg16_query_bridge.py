"""ZG16 Query Bridge v1.2 — Agent Kernel compliant query layer"""
from __future__ import annotations

def get_zg16_research_summary() -> dict:
    return {"system_version":"ZG16_v1.2","event_layers":11,"status":"STUB_ONLY","production_allowed":False,"external_api_used":False,"shadowbroker_deployed":False,"token_estimate":60}

def get_zg16_layer_versions() -> dict:
    from .event_layer_store import get_layer_versions
    return get_layer_versions()

def get_zg16_changed_layers(since_versions: dict) -> dict:
    from .event_layer_store import get_changed_layers
    return get_changed_layers(since_versions)

def get_zg16_layer_slice(layer_ids: list, limit: int = 100) -> dict:
    if limit <= 0 or limit > 100:
        return {"error":True,"code":"NEED_NARROWER_QUERY","message":f"limit must be 1-100"}
    from .event_layer_store import get_layer_slice
    return get_layer_slice(layer_ids)

def get_zg16_source_health(source_id: str) -> dict | None:
    from .source_health_registry import get_source_health
    h = get_source_health(source_id)
    if h: h["production_allowed"] = False
    return h

def get_zg16_source_attribution(source_id: str) -> dict | None:
    from .data_attribution_ledger import get_attribution
    a = get_attribution(source_id)
    if a: a["production_allowed"] = False
    return a

def get_zg16_all_sources() -> dict:
    from .source_health_registry import list_all_sources
    sources = list_all_sources()
    return {"sources":sources,"total":len(sources),"token_estimate":len(sources)*80}
