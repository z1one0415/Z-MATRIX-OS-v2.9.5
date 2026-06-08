"""V13.F3.0.1 — Coverage expansion repair tests."""
import json
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"

def load_repair(fid):
    p = BATCH / fid / f"{fid.lower()}_coverage_expansion_repair.json"
    return json.loads(p.read_text()) if p.exists() else {}

def test_f04_expansion_attempted():
    r = load_repair("F04")
    assert r.get("coverage_expansion_attempted") is True

def test_f10_expansion_attempted():
    r = load_repair("F10")
    assert r.get("coverage_expansion_attempted") is True

def test_f11_expansion_attempted():
    r = load_repair("F11")
    assert r.get("coverage_expansion_attempted") is True

def test_f04_expanded():
    r = load_repair("F04")
    assert r.get("expanded_covered_ticker_count", 0) > 400

def test_f10_expanded():
    r = load_repair("F10")
    assert r.get("expanded_covered_ticker_count", 0) > 400

def test_f11_expanded():
    r = load_repair("F11")
    assert r.get("expanded_covered_ticker_count", 0) > 400

def test_f04_u475():
    r = load_repair("F04")
    assert r.get("coverage_tier") == "U475"

def test_f10_u475():
    r = load_repair("F10")
    assert r.get("coverage_tier") == "U475"

def test_f11_u475():
    r = load_repair("F11")
    assert r.get("coverage_tier") == "U475"

def test_f04_coverage_pass():
    r = load_repair("F04")
    assert r.get("coverage_passed") is True

def test_f10_coverage_pass():
    r = load_repair("F10")
    assert r.get("coverage_passed") is True

def test_f11_coverage_pass():
    r = load_repair("F11")
    assert r.get("coverage_passed") is True
