# allowlist: forbidden-token-definition
"""EventStore validators — schema validation + lineage validation"""
from __future__ import annotations
import re

from zmatrix.event_store.schemas import EVENT_TYPES, BASE_EVENT_FIELDS


_32_HEX_RE = re.compile(r"^[0-9a-f]{32}$")


def validate_event(event: dict) -> list[str]:
    """Validate an event dict against all safety and schema rules.

    Returns a list of violation messages (empty = valid).
    """
    violations = []

    # Required fields
    if not event.get("event_id"):
        violations.append("event_id is required")
    if event.get("event_type") not in EVENT_TYPES:
        violations.append(f"event_type '{event.get('event_type')}' not in EVENT_TYPES")
    if not event.get("schema_version"):
        violations.append("schema_version is required")
    if not event.get("created_at"):
        violations.append("created_at is required")
    if not event.get("producer_module"):
        violations.append("producer_module is required")
    if not isinstance(event.get("payload"), dict):
        violations.append("payload must be a dict")
    if not isinstance(event.get("safety"), dict):
        violations.append("safety must be a dict")

    safety = event.get("safety", {})
    if safety.get("real_trade_allowed") is True:
        violations.append("real_trade_allowed must be False")
    if safety.get("broker_order_allowed") is True:
        violations.append("broker_order_allowed must be False")
    if safety.get("real_z9_write_allowed") is True:
        violations.append("real_z9_write_allowed must be False")
    if safety.get("hermes_memory_write_allowed") is True:
        violations.append("hermes_memory_write_allowed must be False")
    if safety.get("auto_calibration_allowed") is True:
        violations.append("auto_calibration_allowed must be False")
    if safety.get("prompt_auto_injection_allowed") is True:
        violations.append("prompt_auto_injection_allowed must be False")

    return violations


def validate_event_lineage(event: dict) -> list[str]:
    """Validate event lineage fields (source_event_id / parent_event_id)."""
    violations = []
    source = event.get("source_event_id")
    parent = event.get("parent_event_id")
    if source is not None and not _32_HEX_RE.match(str(source)):
        violations.append(f"source_event_id '{source}' not 32-char hex")
    if parent is not None and not _32_HEX_RE.match(str(parent)):
        violations.append(f"parent_event_id '{parent}' not 32-char hex")
    return violations
