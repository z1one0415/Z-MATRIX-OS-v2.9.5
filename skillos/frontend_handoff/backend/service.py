"""Service layer — reads exclusively from fixtures, no file writes."""

from . import fixtures


class ReadonlyService:
    """All data served from in-memory fixtures. No disk I/O."""

    def get_health(self) -> dict:
        return dict(fixtures.HEALTH)

    def get_version(self) -> dict:
        return dict(fixtures.VERSION_INFO)

    def get_dashboard_summary(self) -> dict:
        return dict(fixtures.DASHBOARD_SUMMARY)

    def get_capabilities(self) -> dict:
        return dict(fixtures.CAPABILITIES)

    def get_factor_library_summary(self) -> dict:
        return dict(fixtures.FACTOR_LIBRARY_SUMMARY)

    def get_composition_graph_summary(self) -> dict:
        return dict(fixtures.COMPOSITION_GRAPH_SUMMARY)

    def get_research_report_summary(self) -> dict:
        return dict(fixtures.RESEARCH_REPORT_SUMMARY)

    def get_z9_review_summary(self) -> dict:
        return dict(fixtures.Z9_REVIEW_SUMMARY)

    def get_evidence_chain(self) -> dict:
        return dict(fixtures.EVIDENCE_CHAIN)

    def get_run_state(self) -> dict:
        return dict(fixtures.RUN_STATE)

    def get_gate_state(self) -> dict:
        return dict(fixtures.GATE_STATE)

    def get_audit_trail(self) -> dict:
        return dict(fixtures.AUDIT_TRAIL)

    def get_frontend_routes(self) -> dict:
        return dict(fixtures.FRONTEND_ROUTES)

    def get_frontend_contracts(self) -> dict:
        return dict(fixtures.FRONTEND_CONTRACTS)


# Singleton
service = ReadonlyService()
