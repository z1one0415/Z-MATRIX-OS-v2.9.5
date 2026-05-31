"""EventLayer Version Store v1.2 — layer-level versioning for incremental reads"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib, json, os

FINANCIAL_LAYERS = [
    "ACCOUNT_TRUTH_LAYER","MARKET_OUTCOME_LAYER","ZC35_CATALYST_LAYER",
    "NARRATIVE_EVENT_LAYER","PHYSICAL_SIGNAL_LAYER","B_MATRIX_SNAPSHOT_LAYER",
    "D_MATRIX_EVENT_LAYER","FACTOR_REGISTRY_LAYER","AUTOCASEFORGE_LAYER",
    "RESEARCH_ANNOTATION_LAYER","PERSONAL_PROFILE_LAYER",
]

VERSION_STORE_PATH = os.environ.get("Z_EVENT_LAYER_VERSION_PATH",
    os.path.join(os.path.dirname(__file__),"..","..","data","research_db","cache","event_layer_versions.json"))

@dataclass
class EventLayerVersion:
    layer_id: str
    layer_name: str = ""
    version: int = 0
    last_updated_at: str = ""
    row_count: int = 0
    content_hash: str = ""
    freshness_status: str = "UNKNOWN"
    quality_status: str = "UNKNOWN"
    production_allowed: bool = False


def _load_store() -> dict:
    if not os.path.exists(VERSION_STORE_PATH):
        return {"layers": {}, "updated_at": ""}
    with open(VERSION_STORE_PATH) as f:
        return json.load(f)


def _save_store(data: dict) -> None:
    os.makedirs(os.path.dirname(VERSION_STORE_PATH), exist_ok=True)
    with open(VERSION_STORE_PATH, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_layer_versions() -> dict:
    store = _load_store()
    layers = {}
    for lid, ldata in store.get("layers", {}).items():
        layers[lid] = {
            "layer_id": lid, "layer_name": ldata.get("layer_name",""),
            "version": ldata.get("version",0),
            "last_updated_at": ldata.get("last_updated_at",""),
            "row_count": ldata.get("row_count",0),
            "content_hash": ldata.get("content_hash",""),
            "freshness_status": ldata.get("freshness_status","UNKNOWN"),
            "quality_status": ldata.get("quality_status","UNKNOWN"),
        }
    return {"versions": layers, "token_estimate": len(layers) * 80}


def get_layer_version(layer_id: str) -> dict | None:
    store = _load_store()
    ldata = store.get("layers", {}).get(layer_id)
    if ldata is None:
        return None
    return {"layer_id": layer_id, **ldata}


def mark_layer_updated(layer_id: str, row_count: int, content_hash: str = "") -> dict:
    store = _load_store()
    now = datetime.now(timezone.utc).isoformat()
    if layer_id not in store["layers"]:
        store["layers"][layer_id] = {"layer_name": layer_id, "version": 0}
    ldata = store["layers"][layer_id]
    ldata["version"] = ldata.get("version",0) + 1
    ldata["last_updated_at"] = now
    ldata["row_count"] = row_count
    ldata["content_hash"] = content_hash or hashlib.sha256(
        f"{layer_id}:{now}:{row_count}".encode()
    ).hexdigest()[:16]
    ldata["freshness_status"] = "FRESH"
    ldata["quality_status"] = "PASS" if row_count > 0 else "DATA_INSUFFICIENT"
    store["updated_at"] = now
    _save_store(store)
    return {"layer_id": layer_id, **ldata}


def get_changed_layers(since_versions: dict) -> dict:
    store = _load_store()
    changed = {}
    for lid, ldata in store.get("layers", {}).items():
        prev = since_versions.get(lid, {}).get("version", 0)
        curr = ldata.get("version", 0)
        if curr > prev:
            changed[lid] = {
                "layer_id": lid, "layer_name": ldata.get("layer_name",""),
                "old_version": prev, "new_version": curr,
                "changed": True, "last_updated_at": ldata.get("last_updated_at",""),
            }
    return {"changed_layers": list(changed.values()), "token_estimate": len(changed) * 120}


def get_layer_slice(layer_ids: list[str], since_versions: dict | None = None) -> dict:
    store = _load_store()
    layers = {}
    for lid in layer_ids:
        ldata = store.get("layers", {}).get(lid)
        if ldata:
            layers[lid] = {
                "layer_id": lid, "layer_name": ldata.get("layer_name",""),
                "version": ldata.get("version",0),
                "row_count": ldata.get("row_count",0),
                "content_hash": ldata.get("content_hash",""),
                "freshness_status": ldata.get("freshness_status",""),
                "quality_status": ldata.get("quality_status",""),
            }
    return {"layers": layers, "token_estimate": len(layers) * 100}


def mark_layer_stale(layer_id: str) -> dict:
    store = _load_store()
    if layer_id not in store["layers"]:
        store["layers"][layer_id] = {"layer_name": layer_id, "version": 0}
    store["layers"][layer_id]["freshness_status"] = "STALE"
    store["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_store(store)
    return {"layer_id": layer_id, **store["layers"][layer_id]}
