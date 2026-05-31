"""Physical Signal Loader v1.2 — fixture-only, no external API"""
import json, os
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "data" / "research_db" / "zg16" / "fixtures"

def load_fixture(filename: str) -> list[dict]:
    path = FIXTURE_ROOT / filename
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)

def load_physical_signals() -> list[dict]:
    return load_fixture("physical_signals_fixture.json")

def load_narrative_events() -> list[dict]:
    return load_fixture("narrative_events_fixture.json")

def load_reality_checks() -> list[dict]:
    return load_fixture("reality_checks_fixture.json")
