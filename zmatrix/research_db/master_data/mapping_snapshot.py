"""Phase 2-D: Mapping Snapshot — aggregated state capture of all registered sources."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from zmatrix.research_db.master_data.security_master import SecurityMasterRegistry
from zmatrix.research_db.master_data.alias_resolver import AliasRegistry
from zmatrix.research_db.master_data.industry_taxonomy import IndustryTaxonomy
from zmatrix.research_db.master_data.sector_mapper import SectorMapper
from zmatrix.research_db.master_data.chain_node_mapper import ChainNodeMapper
from zmatrix.research_db.master_data.chain_taxonomy import ChainTaxonomyRegistry


@dataclass
class MappingSnapshot:
    snapshot_id: str
    created_at: str
    version: str
    source_files: list[str]
    record_counts: dict[str, int]
    coverage: dict[str, float]
    conflict_count: int
    missing_count: int
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        self.production_allowed = False

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "version": self.version,
            "source_files": self.source_files,
            "record_counts": self.record_counts,
            "coverage": self.coverage,
            "conflict_count": self.conflict_count,
            "missing_count": self.missing_count,
            "production_allowed": self.production_allowed,
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Mapping Snapshot: {self.snapshot_id}",
            "",
            f"**Created**: {self.created_at}",
            f"**Version**: {self.version}",
            "",
            "## Source Files",
            *(f"- {sf}" for sf in self.source_files),
            "",
            "## Record Counts",
            f"| Source | Count |",
            f"|--------|-------|",
            *(f"| {k} | {v} |" for k, v in self.record_counts.items()),
            "",
            "## Coverage",
            f"| Metric | Value |",
            f"|--------|-------|",
            *(f"| {k} | {v:.2%} |" for k, v in self.coverage.items()),
            "",
            f"**Conflict Count**: {self.conflict_count}",
            f"**Missing Count**: {self.missing_count}",
            "",
            f"*production_allowed: {self.production_allowed}*",
        ]
        return "\n".join(lines)


def create_snapshot(
    registry: SecurityMasterRegistry,
    mapper: ChainNodeMapper,
    taxonomy: IndustryTaxonomy,
    alias_registry: AliasRegistry | None = None,
    sector_mapper: SectorMapper | None = None,
    chain_taxonomy: ChainTaxonomyRegistry | None = None,
) -> MappingSnapshot:
    total_tickers = registry.count()
    aliases_total = len(alias_registry._alias_to_ticker) if alias_registry else 0
    chain_nodes = len(mapper._all)
    industry_rows = len(taxonomy._all)
    source_files = []

    missing_count = 0
    conflict_count = 0
    chain_coverage = 0.0
    industry_coverage = 0.0
    alias_coverage = 0.0

    for sm in registry._all:
        ticker = sm.ticker
        source_files.append(sm.source_file)

        has_industry = taxonomy.get_industry(ticker).get("sw_l1") is not None
        if has_industry:
            industry_coverage += 1
        else:
            missing_count += 1

        if mapper.get_chain_exposure(ticker):
            chain_coverage += 1
        else:
            missing_count += 1

        if alias_registry and alias_registry.get_aliases(ticker):
            alias_coverage += 1
        else:
            missing_count += 1

        mapping_nodes = mapper.get_chain_exposure(ticker)
        for node in mapping_nodes:
            if node["chain_id"] and node["value_capture_grade"] in ("D", ""):
                conflict_count += 1

    source_files = sorted(set(sf for sf in source_files if sf))

    record_counts = {
        "security_master": total_tickers,
        "aliases": aliases_total,
        "chain_nodes": chain_nodes,
        "industry_mappings": industry_rows,
    }

    coverage_vals = {
        "industry_coverage": industry_coverage / total_tickers if total_tickers else 0.0,
        "chain_coverage": chain_coverage / total_tickers if total_tickers else 0.0,
        "alias_coverage": alias_coverage / total_tickers if total_tickers else 0.0,
    }

    return MappingSnapshot(
        snapshot_id=f"snap-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}",
        created_at=datetime.now(timezone.utc).isoformat(),
        version="2.9.5",
        source_files=source_files,
        record_counts=record_counts,
        coverage=coverage_vals,
        conflict_count=conflict_count,
        missing_count=missing_count,
    )
