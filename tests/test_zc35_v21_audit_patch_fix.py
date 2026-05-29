"""test_zc35_v21_audit_patch_fix — ZC35-v2.1 Audit Patch Fix 验证

验证:
- Scorecard 未受 ZC35 patch 污染
- Verify 脚本使用 repo-relative 路径
- 档案状态标记完整
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_rc1_scorecard_not_polluted():
    text = (ROOT / "docs" / "rc1_audit" / "RC1_READINESS_SCORECARD.md").read_text(encoding="utf-8")
    assert "Score: **100/100**" in text
    assert "RC1_READY_RECOMMENDED" in text
    assert "RC1_BLOCKED" not in text
    assert "Safety Scan: PASS" in text
    assert "Safety Flags: PASS" in text
    assert "ZC35-v2.1 remains Research Prototype" in text
    assert "excluded from RC1 approval scope" in text


def test_verify_script_is_repo_relative():
    text = (ROOT / "scripts" / "verify_zc35_v21_audit_patch.sh").read_text(encoding="utf-8")
    assert 'BASE="$HOME/Documents' not in text
    assert 'ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"' in text
    assert 'PYTHONPATH=. python3 -m pytest tests/test_zc35_catalyst_v2.py -q' in text
    assert "| tail" not in text


def test_profile_status_flags():
    path = ROOT / "data" / "stock_profiles" / "002472_双环传动_catalyst_profile.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    meta = data["_meta"]
    assert meta["data_status"] == "LIVE_CASE_STUDY"
    assert meta["backtest_validated"] is False
    assert meta["cross_ticker_validated"] is False
    assert meta["production_allowed"] is False


def test_engine_no_tradeable_field():
    text = (ROOT / "zmatrix" / "zc35" / "catalyst_lifecycle.py").read_text(encoding="utf-8")
    assert '"tradeable"' not in text
    assert 'paper_trackable' in text


def test_closeout_doc_exists():
    path = ROOT / "docs" / "release" / "ZC35_V21_AUDIT_PATCH_FIX_CLOSEOUT.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Research Prototype" in text
    assert "RC1 inclusion: FALSE" in text
    assert "Production inclusion: FALSE" in text
