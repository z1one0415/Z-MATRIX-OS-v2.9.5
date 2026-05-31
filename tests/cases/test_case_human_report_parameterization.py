"""Test each Core 12 case's human report has correct metadata."""
import json
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
REGISTRY = json.loads((WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())

EXPECTED = {
    "CORE_001": {"name": "贵州茅台", "industry": "食品饮料", "sector": "消费", "chain": "白酒"},
    "CORE_002": {"name": "宁德时代", "industry": "电力设备", "sector": "新能源", "chain": "电池"},
    "CORE_003": {"name": "中芯国际", "industry": "电子", "sector": "半导体", "chain": "代工"},
    "CORE_004": {"name": "紫金矿业", "industry": "有色金属", "sector": "矿业", "chain": "金铜"},
    "CORE_005": {"name": "汇川技术", "industry": "自动化设备", "sector": "工控", "chain": "伺服"},
    "CORE_006": {"name": "比亚迪", "industry": "汽车", "sector": "新能源车", "chain": "整车"},
    "CORE_007": {"name": "阳光电源", "industry": "电力设备", "sector": "新能源", "chain": "逆变器"},
    "CORE_008": {"name": "北方华创", "industry": "电子", "sector": "半导体设备", "chain": "设备"},
    "CORE_009": {"name": "中信证券", "industry": "金融", "sector": "券商", "chain": "金融"},
    "CORE_010": {"name": "恒瑞医药", "industry": "医药", "sector": "医药", "chain": "创新药"},
    "CORE_011": {"name": "三花智控", "industry": "家电", "sector": "零部件", "chain": "阀件"},
    "CORE_012": {"name": "锦浪科技", "industry": "电力设备", "sector": "新能源", "chain": "逆变器"},
}

WRONG_METADATA = {"食品饮料", "消费", "白酒"}  # CORE_001 only

def _report(case_id: str) -> str:
    """Find and read a case's human report."""
    base = WORKSPACE / "runtime_reports" / "cases" / "core_12"
    for d in base.iterdir():
        if d.name.startswith(case_id) and d.is_dir():
            for f in d.glob("*_human_report.md"):
                return f.read_text()
    return ""


@pytest.mark.parametrize("case_id,expected", list(EXPECTED.items()))
def test_report_name_correct(case_id, expected):
    text = _report(case_id)
    assert expected["name"] in text, f"{case_id}: missing name '{expected['name']}'"


@pytest.mark.parametrize("case_id,expected", list(EXPECTED.items()))
def test_report_industry_correct(case_id, expected):
    text = _report(case_id)
    assert f"**行业**：{expected['industry']}" in text, f"{case_id}: wrong industry, expected '{expected['industry']}'"


@pytest.mark.parametrize("case_id,expected", list(EXPECTED.items()))
def test_report_sector_correct(case_id, expected):
    text = _report(case_id)
    assert f"**板块**：{expected['sector']}" in text, f"{case_id}: wrong sector"


@pytest.mark.parametrize("case_id,expected", list(EXPECTED.items()))
def test_report_chain_correct(case_id, expected):
    text = _report(case_id)
    assert f"**产业链**：{expected['chain']}" in text, f"{case_id}: wrong chain"


def test_core_002_not_maotai():
    text = _report("CORE_002")
    assert "宁德时代" in text
    assert "食品饮料" not in text
    assert "白酒" not in text


def test_audit_paths_relative():
    base = WORKSPACE / "runtime_reports" / "cases" / "core_12"
    for p in sorted(base.glob("CORE_*_*/*_audit.json")):
        d = json.loads(p.read_text())
        hr = d.get("human_report", "")
        assert not hr.startswith("/"), f"{p.name}: absolute path {hr}"
        assert "Users/" not in hr, f"{p.name}: contains Users/ in {hr}"
        assert hr.startswith("runtime_reports/"), f"{p.name}: not relative: {hr}"


def test_summary_paths_relative():
    s = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_summary.json").read_text())
    for r in s.get("results", []):
        hr = r.get("human_report", "")
        assert not hr.startswith("/"), f"summary: absolute path {hr}"
        assert "Users/" not in hr, f"summary: contains Users/ in {hr}"
