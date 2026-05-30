"""Batch-A: Attribution Report Generator."""
from __future__ import annotations
from pathlib import Path
import json
from typing import Optional

class AttributionReport:
    @staticmethod
    def generate_markdown(attributions: list, cost_breakdowns: list, reasons: list, title: str = "Attribution Report") -> str:
        lines = [f"# {title}", "", "## Summary", f"- Signals analyzed: {len(attributions)}",
                 f"- Cost-analyzed: {len(cost_breakdowns)}", f"- Reasons classified: {len(reasons)}", "",
                 "## Attribution"]
        if attributions:
            total_gross = sum(a.gross_return for a in attributions)
            total_alpha = sum(a.selection_alpha for a in attributions)
            lines.append(f"- Total gross return: {total_gross:.4f}")
            lines.append(f"- Total selection alpha: {total_alpha:.4f}")
        lines.extend(["", "## Cost Attribution", ""])
        if cost_breakdowns:
            total_cost = sum(c.total_cost_drag for c in cost_breakdowns)
            lines.append(f"- Total cost drag: {total_cost:.4f}")
        lines.extend(["", "## Outcome Reasons", ""])
        for reason_type in ["OUTPERFORM_MARKET","OUTPERFORM_INDUSTRY","SELECTION_ALPHA","COST_EROSION","MARKET_BETA_ONLY"]:
            count = sum(1 for r in reasons if reason_type in [r.primary_reason] + r.secondary_reasons)
            lines.append(f"- {reason_type}: {count}")
        lines.extend(["", "## Safety", "- Production: BLOCKED", "- Broker/runtime: BLOCKED"])
        return "\n".join(lines)

    @staticmethod
    def generate_json(attributions: list, filepath: Optional[str] = None) -> dict:
        result = {"attributions": [], "production_allowed": False}
        for a in attributions:
            result["attributions"].append({"ticker": a.ticker, "gross_return": a.gross_return,
                "market": a.market_contribution, "industry": a.industry_contribution,
                "selection_alpha": a.selection_alpha, "residual": a.residual})
        if filepath: Path(filepath).write_text(json.dumps(result, indent=2))
        return result
