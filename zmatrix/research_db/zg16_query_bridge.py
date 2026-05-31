"""ZG16 Query Bridge v1.2 — unified contract with quality_status"""

def _envelope(status="OK", quality="STUB_ONLY", data=None, token_estimate=60):
    return {"status":status,"quality_status":quality,"production_allowed":False,"external_api_used":False,"shadowbroker_deployed":False,"token_estimate":token_estimate,"data":data or {}}

def get_zg16_research_summary() -> dict:
    return _envelope("OK","STUB_ONLY",{"system_version":"ZG16_v1.2","event_layers":11,"hypothesis_types":7},60)

def get_zg16_layer_versions() -> dict:
    from .event_layer_store import get_layer_versions
    r = get_layer_versions()
    return _envelope("OK","STUB_ONLY",r,r.get("token_estimate",100))

def get_zg16_changed_layers(since_versions: dict) -> dict:
    from .event_layer_store import get_changed_layers
    r = get_changed_layers(since_versions)
    return _envelope("OK","STUB_ONLY",r,r.get("token_estimate",100))

def get_zg16_layer_slice(layer_ids: list, limit: int = 100) -> dict:
    if limit <= 0 or limit > 100:
        return {"error":True,"code":"NEED_NARROWER_QUERY","message":f"limit must be 1-100, got {limit}"}
    from .event_layer_store import get_layer_slice
    r = get_layer_slice(layer_ids)
    return _envelope("OK","STUB_ONLY",r,r.get("token_estimate",100))

def get_zg16_source_health(source_id: str) -> dict:
    from .source_health_registry import get_source_health
    h = get_source_health(source_id)
    if h is None:
        return {"status":"MISSING","quality_status":"SOURCE_NOT_REGISTERED","production_allowed":False,"data":None}
    return _envelope("OK","STUB_ONLY",h)

def get_zg16_source_attribution(source_id: str) -> dict:
    from .data_attribution_ledger import get_attribution
    a = get_attribution(source_id)
    if a is None:
        return {"status":"MISSING","quality_status":"SOURCE_NOT_REGISTERED","production_allowed":False,"data":None}
    return _envelope("OK","STUB_ONLY",a)

def get_zg16_all_sources() -> dict:
    from .source_health_registry import list_all_sources
    sources = list_all_sources()
    return _envelope("OK","STUB_ONLY",{"sources":sources,"total":len(sources)},len(sources)*80)

def get_zg16_source_readiness(source_id: str) -> str:
    from .source_health_registry import is_source_usable
    from .data_attribution_ledger import is_licensed
    health = get_zg16_source_health(source_id)
    if health.get("quality_status") == "SOURCE_NOT_REGISTERED":
        return "SOURCE_NOT_REGISTERED"
    if not is_source_usable(source_id):
        return "DATA_SOURCE_BLOCKED"
    if not is_licensed(source_id):
        return "LICENSE_REVIEW_REQUIRED"
    return "SOURCE_READY"
