#!/usr/bin/env python3
"""Phase 2-E: Depth Gate Tests — verify P2-D integrity/coverage capabilities"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = WORKSPACE / "tests" / "fixtures" / "master_data"

from zmatrix.research_db.master_data.security_master import SecurityMasterRegistry
from zmatrix.research_db.master_data.industry_taxonomy import IndustryTaxonomy
from zmatrix.research_db.master_data.sector_mapper import SectorMapper
from zmatrix.research_db.master_data.chain_node_mapper import ChainNodeMapper
from zmatrix.research_db.master_data.alias_resolver import AliasRegistry
from zmatrix.research_db.master_data.chain_taxonomy import ChainTaxonomyRegistry
from zmatrix.research_db.master_data.mapping_integrity_checker import *
from zmatrix.research_db.master_data.coverage_report import compute_coverage
from zmatrix.research_db.master_data.master_data_report import generate_master_data_report
from zmatrix.research_db.master_data.mapping_snapshot import create_snapshot

def _m(): return SecurityMasterRegistry(str(FIXTURES / "sample_security_master.csv"))
def _i(): return IndustryTaxonomy(str(FIXTURES / "sample_industry_mapping.csv"))
def _s(): return SectorMapper(str(FIXTURES / "sample_sector_mapping.csv"))
def _c(): return ChainNodeMapper(str(FIXTURES / "sample_chain_node_mapping.csv"))
def _a(): return AliasRegistry(str(FIXTURES / "sample_ticker_alias.csv"))
def _ct(): return ChainTaxonomyRegistry(str(FIXTURES / "sample_chain_taxonomy.csv"))

# ── Integrity checks exposed ──
def test_depth_duplicate_ticker(): assert isinstance(check_duplicate_tickers(_m()), list)
def test_depth_duplicate_alias(): assert isinstance(check_duplicate_aliases(_a()), list)
def test_depth_ticker_not_in_master(): assert isinstance(check_ticker_not_in_master(_c(), _m()), list)
def test_depth_missing_industry(): assert isinstance(check_missing_industry(_i(), _m()), list)
def test_depth_missing_sector(): assert isinstance(check_missing_sector(_s(), _m()), list)
def test_depth_missing_chain(): assert isinstance(check_missing_chain(_c(), _m()), list)
def test_depth_low_confidence(): assert isinstance(check_low_confidence(_i()), list)
def test_depth_expired(): assert isinstance(check_expired_mappings(_i(), "2026-12-31"), list)
def test_depth_conflicting_industry(): assert isinstance(check_conflicting_primary_industry(_i()), list)
def test_depth_conflicting_chain(): assert isinstance(check_conflicting_primary_chain(_c()), list)

# ── Coverage output fields ──
def test_depth_coverage_output():
    r = compute_coverage(_m(), _i(), _s(), _c())
    for key in ["total_tickers","industry_coverage","sector_coverage","chain_coverage","missing_industry_count","missing_sector_count","missing_chain_count","low_confidence_count","production_allowed"]:
        assert key in r, f"coverage missing field: {key}"

# ── Report safety ──
def test_depth_report_has_safety():
    snap = create_snapshot(_m(), _c(), _i(), _a(), _s(), _ct())
    integ = run_full_integrity(master=_m(), alias_registry=_a(), industry=_i(), sector=_s(), chain_mapper=_c(), chain_taxonomy=_ct())
    cov = compute_coverage(_m(), _i(), _s(), _c())
    md = generate_master_data_report(snap, integ, cov)
    assert "BLOCKED" in md or "blocked" in md.lower()

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
