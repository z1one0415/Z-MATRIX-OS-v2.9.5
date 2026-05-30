"""Batch-I: Portfolio Report — Markdown + JSON report generator."""
from __future__ import annotations
from pathlib import Path
import json
from typing import Optional


class PortfolioReport:
    @staticmethod
    def generate_markdown(
        snapshots: list,
        capacity_results: list = None,
        liquidity_results: list = None,
        drift_results: list = None,
        audit_closers: list = None,
        title: str = "Portfolio Reality Report",
    ) -> str:
        cap = capacity_results or []
        liq = liquidity_results or []
        drift = drift_results or []
        audit = audit_closers or []
        lines = [
            f"# {title}", "",
            "## Overview",
            f"- Snapshots: {len(snapshots)}",
            f"- Capacity analyses: {len(cap)}",
            f"- Liquidity simulations: {len(liq)}",
            f"- Drift detections: {len(drift)}",
            f"- Audit chains: {len(audit)}", "",
            "## Capacity Analysis", "",
        ]
        for c in cap:
            lines.append(
                f"- {c.portfolio_id} @ {c.aum:,.0f}: "
                f"ADV% {c.adv_pct:.1f}% | Impact {c.impact_bps:.1f}bps | "
                f"Grade {c.grade} | Feasible: {c.feasible}"
            )
        lines.extend(["", "## Liquidity Analysis", ""])
        for lr in liq:
            lines.append(
                f"- {lr.portfolio_id}: Impact {lr.total_impact_pct:.1f}% | "
                f"Fillable {lr.fillable_pct:.1f}% | Blocked {lr.blocked_tickers}"
            )
        lines.extend(["", "## Drift Detection", ""])
        for d in drift:
            lines.append(
                f"- {d.portfolio_id}: Drift {d.drift_type} | "
                f"Magnitude {d.drift_magnitude:.3f} | Detected: {d.drift_detected}"
            )
        lines.extend(["", "## Audit", ""])
        for a in audit:
            lines.append(
                f"- {a.portfolio_id}: {a.verdict} | "
                f"Entries {a.entry_count} | Valid: {a.chain_valid}"
            )
        lines.extend(["", "## Safety", "- Production: BLOCKED",
                       "- PIT Protection: ENABLED"],)
        return "\n".join(lines)

    @staticmethod
    def generate_json(
        snapshots: list,
        capacity_results: list = None,
        liquidity_results: list = None,
        drift_results: list = None,
        audit_closers: list = None,
        filepath: Optional[str] = None,
    ) -> dict:
        result = {
            "snapshots": [],
            "capacity": [],
            "liquidity": [],
            "drift": [],
            "audit": [],
            "production_allowed": False,
        }
        for s in snapshots:
            result["snapshots"].append({
                "snapshot_id": s.snapshot_id,
                "portfolio_id": s.portfolio_id,
                "as_of_date": s.as_of_date,
                "capacity_grade": s.capacity_grade,
                "liquidity_score": s.liquidity_score,
                "crowding_score": s.crowding_score,
                "drift_score": s.drift_score,
                "audit_hash": s.audit_hash,
            })
        if capacity_results:
            for c in capacity_results:
                result["capacity"].append({
                    "portfolio_id": c.portfolio_id, "aum": c.aum,
                    "adv_pct": c.adv_pct, "impact_bps": c.impact_bps,
                    "feasible": c.feasible, "grade": c.grade,
                })
        if liquidity_results:
            for lr in liquidity_results:
                result["liquidity"].append({
                    "portfolio_id": lr.portfolio_id,
                    "total_impact_pct": lr.total_impact_pct,
                    "fillable_pct": lr.fillable_pct,
                    "blocked_tickers": lr.blocked_tickers,
                })
        if drift_results:
            for d in drift_results:
                result["drift"].append({
                    "portfolio_id": d.portfolio_id,
                    "drift_type": d.drift_type,
                    "drift_magnitude": d.drift_magnitude,
                    "drift_detected": d.drift_detected,
                })
        if audit_closers:
            for a in audit_closers:
                result["audit"].append({
                    "portfolio_id": a.portfolio_id,
                    "verdict": a.verdict,
                    "entry_count": a.entry_count,
                    "chain_valid": a.chain_valid,
                })
        if filepath:
            Path(filepath).write_text(json.dumps(result, indent=2))
        return result
