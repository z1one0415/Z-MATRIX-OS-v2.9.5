"""Phase 2-D: Coverage Report — dimension-level coverage metrics across all taxonomies."""
from __future__ import annotations

from typing import Optional

from zmatrix.research_db.master_data.security_master import SecurityMasterRegistry
from zmatrix.research_db.master_data.industry_taxonomy import IndustryTaxonomy
from zmatrix.research_db.master_data.sector_mapper import SectorMapper
from zmatrix.research_db.master_data.chain_node_mapper import ChainNodeMapper
from zmatrix.research_db.master_data.alias_resolver import AliasRegistry
from zmatrix.research_db.master_data import Confidence


def compute_coverage(
    master: SecurityMasterRegistry,
    industry: IndustryTaxonomy,
    sector: SectorMapper,
    chain: ChainNodeMapper,
    alias_registry: Optional[AliasRegistry] = None,
) -> dict:
    total_tickers = master.count()
    security_master_coverage = 1.0 if total_tickers > 0 else 0.0

    industry_covered = 0
    sector_covered = 0
    chain_covered = 0
    alias_covered = 0
    missing_industry = 0
    missing_sector = 0
    missing_chain = 0
    low_confidence = 0

    for sm in master._all:
        ticker = sm.ticker

        if ticker in industry._by_ticker:
            im = industry._by_ticker[ticker]
            if im.sw_l1 is not None:
                industry_covered += 1
            else:
                missing_industry += 1
            if im.confidence in (Confidence.LOW, Confidence.UNVERIFIED):
                low_confidence += 1
        else:
            missing_industry += 1

        if not sector.detect_missing_sector(ticker):
            sector_covered += 1
        else:
            missing_sector += 1

        if chain.get_chain_exposure(ticker):
            chain_covered += 1
        else:
            missing_chain += 1

        if alias_registry and alias_registry.get_aliases(ticker):
            alias_covered += 1

    return {
        "total_tickers": total_tickers,
        "security_master_coverage": security_master_coverage,
        "industry_coverage": industry_covered / total_tickers if total_tickers else 0.0,
        "sector_coverage": sector_covered / total_tickers if total_tickers else 0.0,
        "chain_coverage": chain_covered / total_tickers if total_tickers else 0.0,
        "alias_coverage": alias_covered / total_tickers if total_tickers else 0.0,
        "missing_industry_count": missing_industry,
        "missing_sector_count": missing_sector,
        "missing_chain_count": missing_chain,
        "low_confidence_count": low_confidence,
        "production_allowed": False,
    }
