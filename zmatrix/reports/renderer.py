"""V4.0-C4 Reports — Markdown template renderer (Hardening-C3 enhanced)"""
from __future__ import annotations
from pathlib import Path
import json

SAFETY_DISCLAIMER = "\n\n---\n**⚠️ SAFETY DISCLAIMER**\nThis is a PAPER-ONLY research report. No real trading recommendation.\nProduction: BLOCKED | Real Trade: NOT ALLOWED | Broker Order: NOT ALLOWED\n"

TEMPLATE_NAMES = [
    "single_stock_research",
    "research_council_review",
    "evidence_data_quality",
    "strategy_validation",
    "factor_validation",
    "multi_strategy_portfolio",
    "paper_execution_plan",
    "execution_route_competition",
    "portfolio_alpha_daily",
    "account_risk_weekly",
    "missed_opportunity_postmortem",
    "audit_trail",
]

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "report_templates"


class ReportRenderer:
    def render(self, template_name, context):
        """Legacy render: simple key-value output with safety disclaimer."""
        if template_name not in TEMPLATE_NAMES:
            return f"# Unknown template: {template_name}\n{SAFETY_DISCLAIMER}"
        lines = [
            f"# {template_name.replace('_', ' ').title()} Report",
            "",
            f"Generated at: {context.get('timestamp', 'N/A')}",
            "",
        ]
        for k, v in (context or {}).items():
            if k == "timestamp":
                continue
            if v is None:
                lines.append(f"- **{k}**: DATA_INSUFFICIENT")
            else:
                lines.append(f"- **{k}**: {v}")
        lines.extend(
            [
                "",
                "## Safety",
                "- real_trade_allowed: False",
                "- broker_order_allowed: False",
                "- production_allowed: False",
                SAFETY_DISCLAIMER,
            ]
        )
        return "\n".join(lines)

    # ── Hardening-C3: template-file-based snapshot rendering ──────────────

    def render_snapshot(self, template_name, context):
        """Read a .md template from report_templates/ and fill {{ placeholder }} fields.

        Returns the rendered markdown string.
        Uses context dict for values; missing context keys keep their {{ placeholder }}.
        """
        template_path = _TEMPLATE_DIR / f"{template_name}.md"
        if not template_path.exists():
            return f"# Snapshot unavailable: template not found for '{template_name}'\n{SAFETY_DISCLAIMER}"

        raw = template_path.read_text(encoding="utf-8")

        # Merge context with hard-coded safety defaults
        merged = dict(context or {})
        merged.setdefault("real_trade_allowed", "False")
        merged.setdefault("broker_order_allowed", "False")
        merged.setdefault("production_allowed", "False")
        merged.setdefault("human_review_required", "True")

        # Replace {{ key }} placeholders
        for key, val in merged.items():
            placeholder = f"{{{{ {key} }}}}"
            raw = raw.replace(placeholder, str(val))

        # Re-harden safety in rendered output
        raw += SAFETY_DISCLAIMER
        return raw

    def snapshot_to_file(self, template_name, context, output_path):
        """Render a snapshot and write it to *output_path* (overwrites if exists).

        Returns the absolute path written on success, raises OSError on failure.
        """
        rendered = self.render_snapshot(template_name, context)
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
        return str(out.resolve())


class MissingFieldPolicy:
    @staticmethod
    def handle(field_name, value):
        if value is None:
            return {
                "field": field_name,
                "rendered": "DATA_INSUFFICIENT",
                "reason": "MISSING_FIELD",
                "not_rendered_reason": "Value is None",
            }
        return {"field": field_name, "rendered": str(value), "status": "OK"}
