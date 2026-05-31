"""Data Attribution & License Ledger v1.2 — track data source provenance"""
from __future__ import annotations
from dataclasses import dataclass
import csv, os

ATTRIBUTION_PATH = os.environ.get("Z_ATTRIBUTION_LEDGER_PATH",
    os.path.join(os.path.dirname(__file__),"..","..","data","research_db","governance","data_source_attribution_ledger.csv"))

ATTRIBUTION_FIELDS = [
    "source_id","source_name","source_url","license","terms_url",
    "attribution_required","commercial_allowed","redistribution_allowed",
    "research_only","usable_for_backtest","usable_for_current_snapshot",
    "usable_for_report","notes",
]

def load_attributions() -> list[dict]:
    if not os.path.exists(ATTRIBUTION_PATH):
        return []
    with open(ATTRIBUTION_PATH) as f:
        return list(csv.DictReader(f))

def get_attribution(source_id: str) -> dict | None:
    for a in load_attributions():
        if a["source_id"] == source_id:
            return a
    return None

def is_licensed(source_id: str) -> bool:
    a = get_attribution(source_id)
    if a is None:
        return False
    return a.get("license", "UNKNOWN") != "UNKNOWN"

def can_use_for_report(source_id: str) -> bool:
    a = get_attribution(source_id)
    if a is None:
        return False
    return a.get("usable_for_report","false").lower() == "true"

def validate_attribution(source_id: str) -> dict:
    a = get_attribution(source_id)
    if a is None:
        return {"valid": False, "errors": ["source not registered"]}
    errors = []
    lic = a.get("license","UNKNOWN")
    if lic == "UNKNOWN":
        errors.append("license unknown — source may only be used in sandbox")
    if a.get("commercial_allowed","false").lower() == "false":
        errors.append("not cleared for commercial use")
    return {"valid": len(errors)==0, "errors": errors}
