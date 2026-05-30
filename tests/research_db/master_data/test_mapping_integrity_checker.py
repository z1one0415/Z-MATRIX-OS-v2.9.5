#!/usr/bin/env python3
"""Phase 2-D: Integrity Checker Deep Tests — using fixture registries"""
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

def _m(): return SecurityMasterRegistry(str(FIXTURES / "sample_security_master.csv"))
def _i(): return IndustryTaxonomy(str(FIXTURES / "sample_industry_mapping.csv"))
def _s(): return SectorMapper(str(FIXTURES / "sample_sector_mapping.csv"))
def _c(): return ChainNodeMapper(str(FIXTURES / "sample_chain_node_mapping.csv"))
def _a(): return AliasRegistry(str(FIXTURES / "sample_ticker_alias.csv"))
def _ct(): return ChainTaxonomyRegistry(str(FIXTURES / "sample_chain_taxonomy.csv"))

def test_missing_industry():
    r = check_missing_industry(_i(), _m())
    assert isinstance(r, list)

def test_missing_sector():
    r = check_missing_sector(_s(), _m())
    assert isinstance(r, list)

def test_missing_chain():
    r = check_missing_chain(_c(), _m())
    assert isinstance(r, list)

def test_low_confidence():
    r = check_low_confidence(_i())
    assert isinstance(r, list)

def test_expired_mappings():
    r = check_expired_mappings(_i(), "2026-12-31")
    assert isinstance(r, list)

def test_run_full_integrity_blocked():
    r = run_full_integrity(master=_m(), alias_registry=_a(), industry=_i(),
                           sector=_s(), chain_mapper=_c(), chain_taxonomy=_ct())
    assert r["production_allowed"] is False

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
