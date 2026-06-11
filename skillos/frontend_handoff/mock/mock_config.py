"""
mock_config.py — Configuration for A5 Mock Server (SkillOS Frontend Handoff RC)

Constrained by task specification:
- PORT=8080
- DEBUG=False
- DISABLED_DEFAULT=True
"""

PORT = 8080
DEBUG = False
DISABLED_DEFAULT = True

# Fixture directory (relative to this config)
import os
FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fixtures")

# All fixture files and their API endpoint paths
FIXTURE_MAP = {
    "/api/v1/dashboard/summary": "dashboard_summary.json",
    "/api/v1/capabilities": "capability_list.json",
    "/api/v1/factors/summary": "factor_library_summary.json",
    "/api/v1/composition-graph/summary": "composition_graph_summary.json",
    "/api/v1/research/report-summary": "research_report_summary.json",
    "/api/v1/z9/review-summary": "z9_review_summary.json",
    "/api/v1/evidence/chain-demo": "evidence_chain_demo.json",
    "/api/v1/pipeline/run-state": "run_state_demo.json",
    "/api/v1/gates/state": "gate_state_demo.json",
    "/api/v1/audit/trail": "audit_trail_demo.json",
    "/api/v1/demo/error-abort-degraded": "error_abort_degraded_demo.json",
}

# Additional mock endpoints with static responses
MOCK_RESPONSES = {
    "/api/v1/health": {"status": "OK", "timestamp_utc": "2026-06-12T04:03:00Z", "uptime_sec": 86400},
    "/api/v1/version": {"version": "v2.9.6-draft", "branch": "agent/a5-frontend-mock-fixtures", "build_utc": "2026-06-12T03:00:00Z"},
}
