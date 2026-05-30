#!/usr/bin/env python3
"""Phase 2-A: Private Master Data Guardrail Tests — no raw/vendor/xlsx tracked."""
from __future__ import annotations

import sys
import os
import subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent


def test_master_data_module_no_production():
    from zmatrix.research_db.master_data import SecurityMaster, TickerAlias, IndustryMapping
    sm = SecurityMaster(ticker="000001", name="test", exchange="SSE")
    assert sm.production_allowed is False
    ta = TickerAlias(ticker="000001", alias="t", alias_type="SHORT_NAME")
    assert ta.production_allowed is False
    im = IndustryMapping(ticker="000001")
    assert im.production_allowed is False


def test_gitignore_covers_research_db_vendor_protection():
    gi = (WORKSPACE / ".gitignore").read_text()
    assert "data/research_db/account/**/*.xlsx" in gi, "missing vendor protection pattern in .gitignore"


def test_gitignore_covers_xlsx():
    gi = (WORKSPACE / ".gitignore").read_text()
    for ext in ["*.xlsx", "*.xls"]:
        assert ext in gi, f"missing {ext} in .gitignore"


def test_no_xlsx_vendor_files_tracked():
    r = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=str(WORKSPACE))
    lines = r.stdout.split("\n")
    for bad_ext in [".xlsx", ".xls"]:
        tracked = [l for l in lines if l.endswith(bad_ext)]
        assert len(tracked) == 0, f"tracked {bad_ext} files: {tracked}"


def test_no_vendor_files_in_data():
    r = subprocess.run(["git", "ls-files", "data/research_db/universe/raw/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    tracked = [l for l in r.stdout.split("\n") if l.strip() and not l.endswith(".gitkeep")]
    assert len(tracked) == 0, f"tracked vendor data: {tracked}"


def test_fixtures_are_synthetic_csv_only():
    fixture_dir = WORKSPACE / "tests" / "fixtures" / "master_data"
    assert fixture_dir.exists()
    for f in fixture_dir.iterdir():
        assert f.suffix == ".csv", f"non-CSV fixture: {f.name}"
        content = f.read_text()
        assert len(content.splitlines()) <= 50, f"fixture {f.name} too large ({len(content.splitlines())} lines)"


def test_all_dataclasses_production_allowed_defaults_false():
    from zmatrix.research_db.master_data import (
        SecurityMaster, TickerAlias, IndustryMapping,
        SectorMapping, ChainTaxonomy, ChainNodeMapping,
    )
    import dataclasses
    for dc in [SecurityMaster, TickerAlias, IndustryMapping, SectorMapping, ChainTaxonomy, ChainNodeMapping]:
        fields = {f.name: f for f in dataclasses.fields(dc)}
        assert "production_allowed" in fields, f"{dc.__name__} missing production_allowed field"
        assert fields["production_allowed"].default is False, f"{dc.__name__} production_allowed default is not False"
        assert fields["production_allowed"].repr is False, f"{dc.__name__} production_allowed not hidden from repr"


def test_no_real_data_in_committed_csvs():
    r = subprocess.run(["git", "ls-files", "data/research_db/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    for line in r.stdout.strip().split("\n"):
        if not line:
            continue
        if line.endswith(".csv") and not line.endswith("template.csv"):
            p = WORKSPACE / line
            if p.exists():
                content = p.read_text().lower()
                for token in ["balance:", "持仓:", "pnl:", "capital:"]:
                    assert token not in content, f"possible real data token in {line}: '{token}'"


if __name__ == "__main__":
    test_master_data_module_no_production()
    test_gitignore_covers_research_db_vendor_protection()
    test_gitignore_covers_xlsx()
    test_no_xlsx_vendor_files_tracked()
    test_no_vendor_files_in_data()
    test_fixtures_are_synthetic_csv_only()
    test_all_dataclasses_production_allowed_defaults_false()
    test_no_real_data_in_committed_csvs()
    print("✅ Phase 2-A Private Master Data Guardrail tests PASS")
