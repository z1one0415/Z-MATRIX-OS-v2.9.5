#!/usr/bin/env python3
"""Phase 2-C: Chain Taxonomy/Node Mapping Tests."""
from __future__ import annotations

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from zmatrix.research_db.master_data.chain_taxonomy import ChainTaxonomyRegistry
from zmatrix.research_db.master_data.chain_node_mapper import ChainNodeMapper

FIXTURE_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures" / "master_data"
TAXONOMY_CSV = str(FIXTURE_DIR / "sample_chain_taxonomy.csv")
NODE_CSV = str(FIXTURE_DIR / "sample_chain_node_mapping.csv")


# ── ChainTaxonomyRegistry Tests ──

def test_chain_registry_loads_all():
    reg = ChainTaxonomyRegistry(TAXONOMY_CSV)
    assert len(reg._all) == 5


def test_chain_get_chain():
    reg = ChainTaxonomyRegistry(TAXONOMY_CSV)
    chain = reg.get_chain("CHN001")
    assert chain["chain_id"] == "CHN001"
    assert chain["chain_name"] == "人形机器人链"
    assert chain["chain_type"] == "MANUFACTURING"
    assert chain["parent_chain_id"] is None


def test_chain_get_child_chains():
    reg = ChainTaxonomyRegistry(TAXONOMY_CSV)
    children = reg.get_child_chains("CHN001")
    assert children == ["CHN004"]


def test_chain_get_child_chains_empty():
    reg = ChainTaxonomyRegistry(TAXONOMY_CSV)
    children = reg.get_child_chains("CHN005")
    assert children == []


def test_chain_list_chains():
    reg = ChainTaxonomyRegistry(TAXONOMY_CSV)
    chains = reg.list_chains()
    assert len(chains) == 5
    chain_ids = {c["chain_id"] for c in chains}
    assert chain_ids == {"CHN001", "CHN002", "CHN003", "CHN004", "CHN005"}


def test_chain_get_parent():
    reg = ChainTaxonomyRegistry(TAXONOMY_CSV)
    assert reg.get_parent("CHN004") == "CHN001"
    assert reg.get_parent("CHN001") is None


def test_chain_all_production_allowed_false():
    reg = ChainTaxonomyRegistry(TAXONOMY_CSV)
    for ct in reg._all:
        assert ct.production_allowed is False


# ── ChainNodeMapper Tests ──

def test_node_mapper_loads_all():
    mapper = ChainNodeMapper(NODE_CSV)
    assert len(mapper._all) == 6


def test_node_get_chain_exposure():
    mapper = ChainNodeMapper(NODE_CSV)
    exposure = mapper.get_chain_exposure("002472")
    assert len(exposure) == 2
    chain_ids = {e["chain_id"] for e in exposure}
    assert chain_ids == {"CHN001", "CHN004"}


def test_node_get_chain_exposure_empty():
    mapper = ChainNodeMapper(NODE_CSV)
    exposure = mapper.get_chain_exposure("999999")
    assert exposure == []


def test_node_get_primary_chain():
    mapper = ChainNodeMapper(NODE_CSV)
    primary = mapper.get_primary_chain("300750")
    assert primary is not None
    assert primary["chain_id"] in ("CHN003", "CHN005")
    assert primary["value_capture_grade"] == "A"
    assert primary["evidence_grade"] == "A"


def test_node_get_primary_chain_none():
    mapper = ChainNodeMapper(NODE_CSV)
    primary = mapper.get_primary_chain("999999")
    assert primary is None


def test_node_get_secondary_chains():
    mapper = ChainNodeMapper(NODE_CSV)
    sc = mapper.get_secondary_chains("002472")
    assert len(sc) == 1
    assert sc[0]["chain_id"] == "CHN004"


def test_node_get_secondary_chains_empty():
    mapper = ChainNodeMapper(NODE_CSV)
    sc = mapper.get_secondary_chains("688981")
    assert sc == []


def test_node_get_tickers_in_chain():
    mapper = ChainNodeMapper(NODE_CSV)
    tickers = mapper.get_tickers_in_chain("CHN001")
    assert tickers == ["002472"]


def test_node_detect_speculative_theme():
    mapper = ChainNodeMapper(NODE_CSV)
    assert mapper.detect_speculative_theme("002472") is False
    assert mapper.detect_speculative_theme("300750") is False


def test_node_detect_missing_evidence():
    mapper = ChainNodeMapper(NODE_CSV)
    assert mapper.detect_missing_evidence("300750") is False
    assert mapper.detect_missing_evidence("999999") is True


def test_node_all_production_allowed_false():
    mapper = ChainNodeMapper(NODE_CSV)
    for node in mapper._all:
        assert node.production_allowed is False


if __name__ == "__main__":
    test_chain_registry_loads_all()
    test_chain_get_chain()
    test_chain_get_child_chains()
    test_chain_get_child_chains_empty()
    test_chain_list_chains()
    test_chain_get_parent()
    test_chain_all_production_allowed_false()
    test_node_mapper_loads_all()
    test_node_get_chain_exposure()
    test_node_get_chain_exposure_empty()
    test_node_get_primary_chain()
    test_node_get_primary_chain_none()
    test_node_get_secondary_chains()
    test_node_get_secondary_chains_empty()
    test_node_get_tickers_in_chain()
    test_node_detect_speculative_theme()
    test_node_detect_missing_evidence()
    test_node_all_production_allowed_false()
    print("✅ Phase 2-C Chain Taxonomy/Node Mapping tests PASS")
