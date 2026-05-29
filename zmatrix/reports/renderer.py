"""V4.0-C4 Reports — Markdown template renderer"""
from __future__ import annotations

SAFETY_DISCLAIMER = "\n\n---\n**⚠️ SAFETY DISCLAIMER**\nThis is a PAPER-ONLY research report. No real trading recommendation.\nProduction: BLOCKED | Real Trade: NOT ALLOWED | Broker Order: NOT ALLOWED\n"

TEMPLATE_NAMES = ["single_stock_research","research_council_review","evidence_data_quality","strategy_validation","factor_validation","multi_strategy_portfolio","paper_execution_plan","execution_route_competition","portfolio_alpha_daily","account_risk_weekly","missed_opportunity_postmortem","audit_trail"]

class ReportRenderer:
    def render(self, template_name, context):
        if template_name not in TEMPLATE_NAMES: return f"# Unknown template: {template_name}\n{SAFETY_DISCLAIMER}"
        lines = [f"# {template_name.replace('_',' ').title()} Report", "", f"Generated at: {context.get('timestamp','N/A')}", ""]
        for k, v in (context or {}).items():
            if k == 'timestamp': continue
            if v is None: lines.append(f"- **{k}**: DATA_INSUFFICIENT")
            else: lines.append(f"- **{k}**: {v}")
        lines.extend(["", "## Safety", "- real_trade_allowed: False", "- broker_order_allowed: False", "- production_allowed: False", SAFETY_DISCLAIMER])
        return "\n".join(lines)

class MissingFieldPolicy:
    @staticmethod
    def handle(field_name, value):
        if value is None: return {"field":field_name,"rendered":"DATA_INSUFFICIENT","reason":"MISSING_FIELD","not_rendered_reason":"Value is None"}
        return {"field":field_name,"rendered":str(value),"status":"OK"}
