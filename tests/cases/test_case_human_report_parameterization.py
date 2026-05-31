"""Test each Core 12 case's human report has correct metadata (from registry)."""
import json
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
REGISTRY = json.loads((WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())

def _case_data(case_id: str) -> dict:
    for c in REGISTRY:
        if c["case_id"] == case_id:
            return c
    return {}

def _report(case_id: str) -> str:
    base = WORKSPACE / "runtime_reports" / "cases" / "core_12"
    for d in base.iterdir():
        if d.name.startswith(case_id) and d.is_dir():
            for f in d.glob("*_human_report.md"):
                return f.read_text()
    return ""


@pytest.mark.parametrize("case_id", [f"CORE_{i:03d}" for i in range(1, 13)])
def test_report_name_correct(case_id):
    c = _case_data(case_id)
    text = _report(case_id)
    assert c["name"] in text, f"{case_id}: missing name '{c['name']}'"


@pytest.mark.parametrize("case_id", [f"CORE_{i:03d}" for i in range(1, 13)])
def test_report_industry_correct(case_id):
    c = _case_data(case_id)
    text = _report(case_id)
    assert f"**行业**：{c['industry']}" in text, f"{case_id}: expected '{c['industry']}'"


@pytest.mark.parametrize("case_id", [f"CORE_{i:03d}" for i in range(1, 13)])
def test_report_sector_correct(case_id):
    c = _case_data(case_id)
    text = _report(case_id)
    assert f"**板块**：{c['sector']}" in text, f"{case_id}: expected '{c['sector']}'"


@pytest.mark.parametrize("case_id", [f"CORE_{i:03d}" for i in range(1, 13)])
def test_report_chain_correct(case_id):
    c = _case_data(case_id)
    text = _report(case_id)
    assert f"**产业链**：{c['chain']}" in text, f"{case_id}: expected '{c['chain']}'"


@pytest.mark.parametrize("case_id", [f"CORE_{i:03d}" for i in range(1, 13)])
def test_report_ticker_correct(case_id):
    c = _case_data(case_id)
    text = _report(case_id)
    assert f"（{c['ticker']}）" in text, f"{case_id}: missing ticker {c['ticker']}"


def test_core_002_not_maotai():
    text = _report("CORE_002")
    assert "宁德时代" in text
    assert "300750" in text
    assert "食品饮料" not in text
    assert "白酒" not in text


def test_audit_paths_relative():
    base = WORKSPACE / "runtime_reports" / "cases" / "core_12"
    for p in sorted(base.glob("CORE_*_*/*_audit.json")):
        d = json.loads(p.read_text())
        hr = d.get("human_report", "")
        assert not hr.startswith("/"), f"{p.name}: absolute path"
        assert "Users/" not in hr, f"{p.name}: contains Users/"
        assert hr.startswith("runtime_reports/"), f"{p.name}: not relative"


def test_summary_paths_relative():
    s = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_summary.json").read_text())
    for r in s.get("results", []):
        hr = r.get("human_report", "")
        assert not hr.startswith("/"), f"summary: absolute path"
        assert "Users/" not in hr, f"summary: contains Users/"


def test_all_12_reports_exist():
    base = WORKSPACE / "runtime_reports" / "cases" / "core_12"
    reports = list(base.glob("CORE_*_*/*_human_report.md"))
    assert len(reports) == 12, f"Found {len(reports)} reports, expected 12"


def test_all_12_audits_exist():
    base = WORKSPACE / "runtime_reports" / "cases" / "core_12"
    audits = list(base.glob("CORE_*_*/*_audit.json"))
    assert len(audits) == 12, f"Found {len(audits)} audits, expected 12"
