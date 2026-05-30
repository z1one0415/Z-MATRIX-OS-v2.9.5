#!/usr/bin/env python3
"""Phase 2: Master Data Private Guardrail Tests — master_data path coverage."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent


def test_gitignore_covers_master_data_raw():
    gi = (WORKSPACE / ".gitignore").read_text()
    assert "data/research_db/master_data/raw/" in gi or "master_data/raw/*" in gi


def test_gitignore_covers_master_data_staging():
    gi = (WORKSPACE / ".gitignore").read_text()
    assert "data/research_db/master_data/staging/" in gi or "master_data/staging/*" in gi


def test_gitignore_covers_master_data_vendor():
    gi = (WORKSPACE / ".gitignore").read_text()
    assert "data/research_db/master_data/vendor/" in gi or "master_data/vendor/*" in gi


def test_gitignore_covers_vendor_patterns():
    gi = (WORKSPACE / ".gitignore").read_text()
    for pat in ["*.xlsx", "*.xls", "*.vendor.csv", "*.raw.csv"]:
        assert pat in gi, f"missing {pat}"


def test_gitignore_covers_vendor_sources():
    gi = (WORKSPACE / ".gitignore").read_text()
    for kw in ["wind*", "choice*", "tushare*", "akshare*"]:
        assert kw in gi, f"missing {kw}"


def test_no_xlsx_vendor_files_tracked():
    r = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=str(WORKSPACE))
    for bad in [".xlsx", ".xls", ".vendor.csv", ".raw.csv"]:
        tracked = [l for l in r.stdout.split("\n") if l.endswith(bad)]
        assert len(tracked) == 0, f"tracked {bad}: {tracked}"


def test_no_vendor_files_in_master_data():
    r = subprocess.run(["git", "ls-files", "data/research_db/master_data/raw/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    real = [l for l in r.stdout.split("\n") if l.strip() and not l.endswith(".gitkeep")]
    assert len(real) == 0, f"raw files: {real}"


def test_fixtures_are_synthetic_csv_only():
    r = subprocess.run(["git", "ls-files", "tests/fixtures/master_data/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    for line in r.stdout.split("\n"):
        if line.endswith(".csv"):
            assert "sample_" in line, f"non-sample fixture: {line}"


def test_master_data_module_no_production():
    from zmatrix.research_db.master_data import SecurityMaster, Exchange
    sm = SecurityMaster(ticker="000001", name="PB", exchange=Exchange.SSE)
    assert sm.production_allowed is False


def test_all_dataclasses_production_allowed_defaults_false():
    from zmatrix.research_db.master_data import (
        SecurityMaster, TickerAlias, IndustryMapping,
        SectorMapping, ChainTaxonomy, ChainNodeMapping, Exchange, Confidence,
    )
    for cls, args in [
        (SecurityMaster, {"ticker": "X", "name": "X", "exchange": Exchange.SSE}),
        (TickerAlias, {"ticker": "X", "alias": "Y", "alias_type": "SHORT_NAME"}),
        (IndustryMapping, {"ticker": "X"}),
        (SectorMapping, {"ticker": "X", "sector_id": "S1", "sector_name": "S", "weight": 1.0}),
        (ChainTaxonomy, {"chain_id": "C1", "chain_name": "C", "chain_type": "T"}),
        (ChainNodeMapping, {"ticker": "X", "chain_id": "C1", "chain_layer": "L", "chain_position": "P", "value_capture_grade": "A", "evidence_grade": "HIGH"}),
    ]:
        obj = cls(**args)
        assert obj.production_allowed is False, f"{cls.__name__} has production_allowed=True"


def test_no_real_data_in_committed_csvs():
    import csv
    r = subprocess.run(["git", "ls-files", "tests/fixtures/master_data/", "templates/research_db/master_data/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    for line in r.stdout.split("\n"):
        if not line.endswith(".csv"):
            continue
        with open(WORKSPACE / line) as f:
            for row in csv.DictReader(f):
                ticker = row.get("ticker", "")
                if ticker and not ticker.startswith("sample_"):
                    assert len(ticker) <= 6 or ticker == "sample", f"real ticker {ticker} in {line}"


if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
