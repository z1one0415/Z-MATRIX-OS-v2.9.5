# Z-SkillOS Frontend Handoff — Version Registry

> Release: v0.1.0-rc | Agent: A6 QA/Release | Date: 2026-06-12

## Release Artifact

| Field | Value |
|-------|-------|
| **Version** | `v0.1.0-rc` |
| **Base Commit** | `1f20dc1b` |
| **Release Date** | 2026-06-12 |
| **Branch** | `integration/z-skillos-frontend-handoff-rc` |
| **QA Branch** | `agent/a6-qa-release-pack` |

## Artifacts

| Artifact | Path | Type |
|----------|------|------|
| Backend Application | `skillos/frontend_handoff/backend/app.py` | Python (Flask) |
| Backend Config | `skillos/frontend_handoff/backend/config.py` | Python |
| Backend Routes | `skillos/frontend_handoff/backend/routes.py` | Python |
| Backend Service | `skillos/frontend_handoff/backend/service.py` | Python |
| Backend Fixtures | `skillos/frontend_handoff/backend/fixtures.py` | Python |
| Backend Errors | `skillos/frontend_handoff/backend/errors.py` | Python |
| Auth Schema | `skillos/frontend_handoff/auth/auth_schema.json` | JSON Schema |
| Role Matrix | `skillos/frontend_handoff/auth/role_permission_matrix.json` | JSON |
| Blocked Actions | `skillos/frontend_handoff/auth/blocked_action_policy.json` | JSON |
| Permission Guard | `skillos/frontend_handoff/auth/permission_guard.py` | Python |
| Run State Schema | `skillos/frontend_handoff/state_registry/run_state_schema.json` | JSON Schema |
| Gate State Schema | `skillos/frontend_handoff/state_registry/gate_state_schema.json` | JSON Schema |
| Event Log Schema | `skillos/frontend_handoff/state_registry/event_log_schema.json` | JSON Schema |
| Registry Loader | `skillos/frontend_handoff/state_registry/registry_loader.py` | Python |
| Registry Fixtures | `skillos/frontend_handoff/state_registry/registry_fixtures.py` | Python |
| API Schema Contract | `skillos/frontend_handoff/contracts/api_schema.json` | JSON Schema |
| Dashboard Contract | `skillos/frontend_handoff/contracts/dashboard_contract.json` | JSON |
| Component State Contract | `skillos/frontend_handoff/contracts/component_state_contract.json` | JSON |
| Page Data Contract | `skillos/frontend_handoff/contracts/page_data_contract.json` | JSON |
| Navigation Contract | `skillos/frontend_handoff/contracts/navigation_contract.json` | JSON |
| Error/Abort Contract | `skillos/frontend_handoff/contracts/error_abort_degraded_contract.json` | JSON |
| Log Schema | `skillos/frontend_handoff/observability/log_schema.json` | JSON Schema |
| Audit Trail Schema | `skillos/frontend_handoff/observability/audit_trail_schema.json` | JSON Schema |
| Health Check Schema | `skillos/frontend_handoff/observability/healthcheck_schema.json` | JSON Schema |
| Version Module | `skillos/frontend_handoff/release/version.py` | Python |
| Install Runbook | `docs/skillos/frontend_handoff/release/INSTALL_RUNBOOK.md` | Markdown |
| Deploy Config Runbook | `docs/skillos/frontend_handoff/release/DEPLOY_CONFIG_RUNBOOK.md` | Markdown |
| Observability Runbook | `docs/skillos/frontend_handoff/release/OBSERVABILITY_RUNBOOK.md` | Markdown |
| Release Notes | `docs/skillos/frontend_handoff/release/RELEASE_NOTES.md` | Markdown |
| Version Registry | `docs/skillos/frontend_handoff/release/VERSION_REGISTRY.md` | Markdown |
| Frontend Handoff Checklist | `docs/skillos/frontend_handoff/release/FRONTEND_HANDOFF_CHECKLIST.md` | Markdown |
| Smoke Test | `tests/skillos/frontend_handoff/e2e/test_frontend_handoff_smoke.py` | Python (pytest) |
| Fixture Alignment Test | `tests/skillos/frontend_handoff/e2e/test_all_routes_have_fixtures.py` | Python (pytest) |
| Contract Parse Test | `tests/skillos/frontend_handoff/e2e/test_all_contracts_parse.py` | Python (pytest) |
| Dangerous Permissions Test | `tests/skillos/frontend_handoff/e2e/test_no_dangerous_permissions.py` | Python (pytest) |
| Runtime Enablement Test | `tests/skillos/frontend_handoff/e2e/test_no_runtime_enablement.py` | Python (pytest) |

## Dependency Versions

| Dependency | Minimum | Tested |
|------------|---------|--------|
| Python | 3.10 | 3.14 |
| Flask | 2.0+ | Latest |
| Flask-Cors | 3.0+ | Latest |
| Pytest | 7.0+ | 9.0.3 |

## Signatures

| Role | Agent | Status |
|------|-------|--------|
| A0 Orchestrator | Foundation | ✅ Sealed |
| A1 Contract Freeze | Contracts | ✅ Sealed |
| A2 Backend Shell | Readonly Shell | ✅ Sealed |
| A3 State Registry | Evidence Registry | ✅ Sealed |
| A4 Auth Matrix | Permission Matrix | ✅ Sealed |
| A5 Mock Fixtures | Frontend Fixtures | ✅ Sealed |
| A6 QA/Release | Release Pack | ✅ Sealed |
