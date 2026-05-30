"""OutcomeReport — Markdown + JSON report generator from snapshot and integrity results."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import json


@dataclass
class OutcomeReport:
    report_id: str
    snapshot_id: str
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False

    @staticmethod
    def generate_markdown(snapshot, integrity_result=None) -> str:
        from .outcome_snapshot import OutcomeSnapshot
        from .outcome_integrity import IntegrityResult
        lines = []
        lines.append("# Outcome Reality Report")
        lines.append("")
        lines.append(f"**Report Generated**: {datetime.now(timezone.utc).isoformat()}")
        lines.append(f"**Snapshot ID**: {snapshot.snapshot_id}")
        lines.append(f"**As Of Date**: {snapshot.as_of_date}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Universe")
        lines.append(f"| Field | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| Universe ID | {snapshot.universe_id} |")
        lines.append(f"| Total Events | {snapshot.total_events} |")
        lines.append(f"| Avg Market Return | {snapshot.market_return:.4f} |")
        lines.append(f"| As Of Date | {snapshot.as_of_date} |")
        lines.append("")
        lines.append("## Distribution")
        if snapshot.regime_distribution:
            lines.append("| Regime | Count |")
            lines.append("|---|---|")
            for regime, count in sorted(snapshot.regime_distribution.items()):
                lines.append(f"| {regime} | {count} |")
        else:
            lines.append("*(No regime distribution data)*")
        lines.append("")
        lines.append("## Coverage")
        if snapshot.event_coverage:
            lines.append("| Year | Events |")
            lines.append("|---|---|")
            for year, count in sorted(snapshot.event_coverage.items()):
                lines.append(f"| {year} | {count} |")
        else:
            lines.append("*(No coverage data)*")
        lines.append("")
        lines.append("## Hash")
        try:
            import hashlib
            raw = json.dumps(snapshot.to_dict(), sort_keys=True, default=str).encode("utf-8")
            h = hashlib.sha256(raw).hexdigest()
            lines.append(f"| Algorithm | Hash |")
            lines.append(f"|---|---|")
            lines.append(f"| SHA-256 | `{h}` |")
        except Exception:
            lines.append("*(Hash computation failed)*")
        lines.append("")
        lines.append("## Integrity")
        if integrity_result is not None:
            lines.append(f"| Check | Status | Detail |")
            lines.append(f"|---|---|---|")
            lines.append(f"| Coverage | {integrity_result.coverage_status.value} | {integrity_result.coverage_detail} |")
            lines.append(f"| Consistency | {integrity_result.consistency_status.value} | {integrity_result.consistency_detail} |")
            lines.append(f"| Duplicates | {integrity_result.duplicates_status.value} | {integrity_result.duplicates_detail} |")
            lines.append(f"| Hash | {integrity_result.hash_status.value} | {integrity_result.hash_detail} |")
            lines.append(f"| **Overall** | **{integrity_result.overall_status.value}** | |")
            if integrity_result.issues:
                lines.append("")
                lines.append("### Issues")
                for issue in integrity_result.issues:
                    lines.append(f"- {issue}")
        else:
            lines.append("*(No integrity check results)*")
        lines.append("")
        lines.append("## Safety")
        lines.append("| Flag | Value |")
        lines.append("|---|---|")
        lines.append(f"| Production Allowed | **BLOCKED** |")
        lines.append(f"| Real Trade Allowed | **BLOCKED** |")
        lines.append(f"| Broker Order Allowed | **BLOCKED** |")
        lines.append(f"| Paper Only | **TRUE** |")
        lines.append(f"| Human Review Required | **TRUE** |")
        return "\n".join(lines)

    @staticmethod
    def generate_json(snapshot, filepath: str | None = None) -> dict:
        output = {
            "report_type": "outcome_reality_report",
            "snapshot_id": snapshot.snapshot_id,
            "as_of_date": snapshot.as_of_date,
            "snapshot": snapshot.to_dict(),
            "production_allowed": False,
            "safety": {
                "real_trade_allowed": "BLOCKED",
                "broker_order_allowed": "BLOCKED",
                "production_allowed": "BLOCKED",
                "paper_only": True,
                "human_review_required": True,
            },
        }
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        return output

    @staticmethod
    def generate_full(snapshot, integrity_result=None, json_filepath: str | None = None) -> dict:
        md = OutcomeReport.generate_markdown(snapshot, integrity_result)
        js = OutcomeReport.generate_json(snapshot, json_filepath)
        return {
            "markdown": md,
            "json": js,
            "production_allowed": False,
        }
