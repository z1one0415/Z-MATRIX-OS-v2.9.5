"""Phase 2-D: Mapping Integrity Checker — cross-source integrity validation."""
from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional

from zmatrix.research_db.master_data.security_master import SecurityMasterRegistry
from zmatrix.research_db.master_data.alias_resolver import AliasRegistry
from zmatrix.research_db.master_data.industry_taxonomy import IndustryTaxonomy
from zmatrix.research_db.master_data.sector_mapper import SectorMapper
from zmatrix.research_db.master_data.chain_node_mapper import ChainNodeMapper
from zmatrix.research_db.master_data.chain_taxonomy import ChainTaxonomyRegistry
from zmatrix.research_db.master_data import Confidence


def check_duplicate_tickers(master: SecurityMasterRegistry) -> list[dict]:
    seen: dict[str, int] = {}
    duplicates: list[dict] = []
    for sm in master._all:
        ticker = sm.ticker
        seen[ticker] = seen.get(ticker, 0) + 1
    for ticker, count in seen.items():
        if count > 1:
            duplicates.append({"ticker": ticker, "count": count, "issue": "DUPLICATE_TICKER"})
    return duplicates


def check_duplicate_aliases(alias_registry: AliasRegistry) -> list[dict]:
    seen: dict[str, list[str]] = {}
    duplicates: list[dict] = []
    for alias, ticker in alias_registry._alias_to_ticker.items():
        seen.setdefault(alias, []).append(ticker)
    for alias, tickers in seen.items():
        if len(tickers) > 1:
            duplicates.append({"alias": alias, "tickers": tickers, "issue": "DUPLICATE_ALIAS"})
    return duplicates


def check_ticker_not_in_master(mapping: ChainNodeMapper, master: SecurityMasterRegistry) -> list[dict]:
    missing: list[dict] = []
    for node in mapping._all:
        if not master.has_ticker(node.ticker):
            missing.append({"ticker": node.ticker, "source": "chain_node_mapping", "issue": "TICKER_NOT_IN_MASTER"})
    return missing


def check_missing_industry(mapping: IndustryTaxonomy, master: SecurityMasterRegistry) -> list[dict]:
    missing: list[dict] = []
    for sm in master._all:
        if sm.ticker not in mapping._by_ticker:
            missing.append({"ticker": sm.ticker, "issue": "MISSING_INDUSTRY"})
        else:
            im = mapping._by_ticker[sm.ticker]
            if im.sw_l1 is None:
                missing.append({"ticker": sm.ticker, "issue": "MISSING_INDUSTRY_NULL_SW_L1"})
    return missing


def check_missing_sector(mapping: SectorMapper, master: SecurityMasterRegistry) -> list[dict]:
    missing: list[dict] = []
    for sm in master._all:
        if mapping.detect_missing_sector(sm.ticker):
            missing.append({"ticker": sm.ticker, "issue": "MISSING_SECTOR"})
    return missing


def check_missing_chain(mapping: ChainNodeMapper, master: SecurityMasterRegistry) -> list[dict]:
    missing: list[dict] = []
    for sm in master._all:
        exposure = mapping.get_chain_exposure(sm.ticker)
        if not exposure:
            missing.append({"ticker": sm.ticker, "issue": "MISSING_CHAIN"})
    return missing


def check_expired_mappings(mappings: IndustryTaxonomy, as_of: date) -> list[dict]:
    expired: list[dict] = []
    for im in mappings._all:
        if mappings.detect_expired(im.ticker, as_of):
            expired.append({"ticker": im.ticker, "issue": "EXPIRED_MAPPING"})
    return expired


def check_low_confidence(mappings: IndustryTaxonomy) -> list[dict]:
    low: list[dict] = []
    for im in mappings._all:
        if im.confidence in (Confidence.LOW, Confidence.UNVERIFIED):
            low.append({"ticker": im.ticker, "confidence": im.confidence.value, "issue": "LOW_CONFIDENCE"})
    return low


def check_conflicting_primary_industry(mappings: IndustryTaxonomy | None = None) -> list[dict]:
    if mappings is None:
        return []
    conflicts: list[dict] = []
    by_ticker: dict[str, list[str]] = {}
    for ticker, im in mappings._by_ticker.items():
        by_ticker.setdefault(ticker, []).append(im.sw_l1 or "NULL")
    for ticker, industries in by_ticker.items():
        unique = [i for i in industries if i != "NULL"]
        if len(set(unique)) > 1:
            conflicts.append({
                "ticker": ticker,
                "industries": list(set(unique)),
                "issue": "CONFLICTING_PRIMARY_INDUSTRY",
            })
    return conflicts


def check_conflicting_primary_chain(mapper: ChainNodeMapper | None = None) -> list[dict]:
    if mapper is None:
        return []
    conflicts: list[dict] = []
    for ticker, nodes in mapper._by_ticker.items():
        grades = set(node.value_capture_grade for node in nodes)
        if len(nodes) > 1 and len(grades) == 1:
            continue
        chain_ids = [node.chain_id for node in nodes if node.chain_id and node.value_capture_grade not in ("D", "")]
        if len(set(chain_ids)) > 1:
            conflicts.append({
                "ticker": ticker,
                "chain_ids": list(set(chain_ids)),
                "issue": "CONFLICTING_PRIMARY_CHAIN",
            })
    return conflicts


def run_full_integrity(
    master: SecurityMasterRegistry,
    alias_registry: Optional[AliasRegistry] = None,
    industry: Optional[IndustryTaxonomy] = None,
    sector: Optional[SectorMapper] = None,
    chain_mapper: Optional[ChainNodeMapper] = None,
    chain_taxonomy: Optional[ChainTaxonomyRegistry] = None,
    as_of: Optional[date] = None,
) -> dict:
    issues: list[dict] = []

    issues.extend(check_duplicate_tickers(master))
    issues.extend(check_ticker_not_in_master(chain_mapper, master) if chain_mapper else [])

    if industry:
        issues.extend(check_missing_industry(industry, master))
        issues.extend(check_low_confidence(industry))
        issues.extend(check_conflicting_primary_industry(industry))
        if as_of:
            issues.extend(check_expired_mappings(industry, as_of))

    if sector:
        issues.extend(check_missing_sector(sector, master))

    if chain_mapper:
        issues.extend(check_missing_chain(chain_mapper, master))
        issues.extend(check_conflicting_primary_chain(chain_mapper))

    if alias_registry:
        issues.extend(check_duplicate_aliases(alias_registry))

    blocker_issues = ["DUPLICATE_TICKER", "CONFLICTING_PRIMARY_INDUSTRY", "CONFLICTING_PRIMARY_CHAIN"]
    has_blockers = any(i["issue"] in blocker_issues for i in issues)

    status = "BLOCKED" if has_blockers else ("WARNING" if issues else "PASS")

    return {
        "status": status,
        "issue_count": len(issues),
        "issues": issues,
        "production_allowed": False,
    }
