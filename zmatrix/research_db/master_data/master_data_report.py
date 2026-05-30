"""Phase 2-D: Master Data Report — aggregated report generation from snapshot/integrity/coverage."""
from __future__ import annotations

from zmatrix.research_db.master_data.mapping_snapshot import MappingSnapshot


def generate_master_data_report(
    snapshot: MappingSnapshot,
    integrity: dict,
    coverage: dict,
) -> str:
    lines = [
        "# Master Data Report",
        "",
        f"**Phase**: 2-D",
        f"**Snapshot ID**: {snapshot.snapshot_id}",
        f"**Generated**: {snapshot.created_at}",
        f"**Version**: {snapshot.version}",
        "",
        "---",
        "",
        "## Coverage Summary",
        "",
        f"| Dimension | Value |",
        f"|-----------|-------|",
        f"| Total Tickers | {coverage.get('total_tickers', 0)} |",
        f"| Security Master Coverage | {coverage.get('security_master_coverage', 0):.2%} |",
        f"| Industry Coverage | {coverage.get('industry_coverage', 0):.2%} |",
        f"| Sector Coverage | {coverage.get('sector_coverage', 0):.2%} |",
        f"| Chain Coverage | {coverage.get('chain_coverage', 0):.2%} |",
        f"| Alias Coverage | {coverage.get('alias_coverage', 0):.2%} |",
        "",
        "## Integrity Status",
        "",
        f"**Status**: {integrity.get('status', 'UNKNOWN')}",
        f"**Issue Count**: {integrity.get('issue_count', 0)}",
        "",
    ]

    strategy_issues = integrity.get("issues", [])
    if strategy_issues:
        lines.append("| Ticker | Issue |")
        lines.append("|--------|-------|")
        for issue in strategy_issues:
            ticker = issue.get("ticker", issue.get("alias", "N/A"))
            issue_type = issue.get("issue", "UNKNOWN")
            lines.append(f"| {ticker} | {issue_type} |")
        lines.append("")

    lines.extend([
        "## Conflict Summary",
        "",
        f"**Conflict Count**: {snapshot.conflict_count}",
        "",
        "## Missing Data Summary",
        "",
        f"**Missing Count**: {snapshot.missing_count}",
        f"**Missing Industry**: {coverage.get('missing_industry_count', 0)}",
        f"**Missing Sector**: {coverage.get('missing_sector_count', 0)}",
        f"**Missing Chain**: {coverage.get('missing_chain_count', 0)}",
        f"**Low Confidence**: {coverage.get('low_confidence_count', 0)}",
        "",
        "## Safety Statement",
        "",
        "| Gate | Status |",
        "|------|--------|",
        "| Production | BLOCKED |",
        "| Broker/runtime | BLOCKED |",
        "| Real trade | BLOCKED |",
        "| production_allowed | False |",
        "",
        "---",
        "",
        "*This report is generated for research purposes only. No BUY/SELL/AUTO_EXECUTE decisions.*",
    ])

    return "\n".join(lines)
