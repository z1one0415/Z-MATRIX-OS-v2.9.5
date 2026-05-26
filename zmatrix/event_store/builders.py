"""Event builder helper — builds a fully-formed event dict"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone

from zmatrix.event_store.event_ids import build_event_id, hash_payload
from zmatrix.event_store.schemas import DEFAULT_EVENT_SAFETY, SCHEMA_VERSION


def build_event(
    *,
    event_type: str,
    producer_module: str,
    payload: dict,
    source_event_id: str | None = None,
    parent_event_id: str | None = None,
    created_at: str | None = None,
) -> dict:
    """Build a complete event dict with auto-generated fields.

    Automatically generates:
    - event_id (deterministic 32-char hex)
    - input_hash
    - output_hash
    - safety (DEFAULT_EVENT_SAFETY)
    - schema_version = "EVENT_STORE_V10"
    """
    if created_at is None:
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    event_id = build_event_id(event_type, payload, created_at)
    input_hash = hash_payload(payload)
    output_hash = hashlib.sha256(
        json.dumps(
            {"event_id": event_id, "event_type": event_type, "producer_module": producer_module},
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()

    return {
        "event_id": event_id,
        "event_type": event_type,
        "schema_version": SCHEMA_VERSION,
        "created_at": created_at,
        "producer_module": producer_module,
        "source_event_id": source_event_id,
        "parent_event_id": parent_event_id,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "payload": dict(payload),
        "safety": dict(DEFAULT_EVENT_SAFETY),
    }
