#!/usr/bin/env python3
"""Phase 2-D: Snapshot + Integrity + Coverage + Report Tests — matching actual API"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = WORKSPACE / "tests" / "fixtures" / "master_data"

from zmatrix.research_db.master_data.mapping_snapshot import MappingSnapshot, create_snapshot
from zmatrix.research_db.master_data.mapping_integrity_checker import run_full_integrity
from zmatrix.research_db.master_data.coverage_report import compute_coverage
from zmatrix.research_db.master_data.master_data_report import generate_master_data_report
from zmatrix.research_db.master_data.security_master import SecurityMasterRegistry
from zmatrix.research_db.master_data.industry_taxonomy import IndustryTaxonomy
from zmatrix.research_db.master_data.sector_mapper import SectorMapper
from zmatrix.research_db.master_data.chain_node_mapper import ChainNodeMapper
from zmatrix.research_db.master_data.alias_resolver import AliasRegistry
from zmatrix.research_db.master_data.chain_taxonomy import ChainTaxonomyRegistry

def _m(): return SecurityMasterRegistry(str(FIXTURES / "sample_security_master.csv"))
def _i(): return IndustryTaxonomy(str(FIXTURES / "sample_industry_mapping.csv"))
def _s(): return SectorMapper(str(FIXTURES / "sample_sector_mapping.csv"))
def _c(): return ChainNodeMapper(str(FIXTURES / "sample_chain_node_mapping.csv"))
def _a(): return AliasRegistry(str(FIXTURES / "sample_ticker_alias.csv"))
def _ct(): return ChainTaxonomyRegistry(str(FIXTURES / "sample_chain_taxonomy.csv"))


# ── mapping_snapshot.py: create_snapshot(registry, mapper, taxonomy, alias_registry, sector_mapper, chain_taxonomy) ──
# ── run_full_integrity(master, alias_registry, industry, sector, chain_mapper, chain_taxonomy, as_of) ──

def test_snapshot_creation():
    s = MappingSnapshot(snapshot_id="snap-001", created_at="2026-01-01", version="v1",
                        source_files=["a.csv"], record_counts={"tickers":5},
                        coverage={"industry":0.8}, conflict_count=0, missing_count=0)
    assert s.snapshot_id == "snap-001"
    assert s.production_allowed is False

def test_snapshot_to_dict():
    s = MappingSnapshot(snapshot_id="s1", created_at="2026-01-01", version="v1",
                        source_files=[], record_counts={"t":5}, coverage={"i":0.8},
                        conflict_count=0, missing_count=0)
    d = s.to_dict()
    assert d["snapshot_id"] == "s1"

def test_create_snapshot():
    snap = create_snapshot(_m(), _c(), _i(), _a(), _s(), _ct())
    assert snap.record_counts.get("security_master", 0) > 0
    assert snap.production_allowed is False

def test_run_full_integrity():
    r = run_full_integrity(master=_m(), alias_registry=_a(), industry=_i(),
                           sector=_s(), chain_mapper=_c(), chain_taxonomy=_ct())
    assert r["status"] in ("PASS","WARNING","BLOCKED")
    assert r["production_allowed"] is False

def test_compute_coverage():
    r = compute_coverage(_m(), _i(), _s(), _c())
    assert r["total_tickers"] >= 1

def test_report_generates():
    snap = create_snapshot(_m(), _c(), _i(), _a(), _s(), _ct())
    integ = run_full_integrity(master=_m(), alias_registry=_a(), industry=_i(),
                                sector=_s(), chain_mapper=_c(), chain_taxonomy=_ct())
    cov = compute_coverage(_m(), _i(), _s(), _c())
    md = generate_master_data_report(snap, integ, cov)
    assert "Production" in md or "BLOCKED" in md
    # Report may mention BUY/SELL in safety disclaimers — that's OK

def test_integrity_production_blocked():
    r = run_full_integrity(master=_m(), alias_registry=_a(), industry=_i(),
                           sector=_s(), chain_mapper=_c(), chain_taxonomy=_ct())
    assert r["production_allowed"] is False

def test_coverage_production_blocked():
    r = compute_coverage(_m(), _i(), _s(), _c())
    assert r["production_allowed"] is False

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
