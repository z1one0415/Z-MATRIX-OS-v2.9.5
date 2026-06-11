# Z-SkillOS Frontend Handoff Route Map

## Page Routes

| Route | Page | Description | Data Sources |
|:--|:--|:--|:--|
| / | Home Dashboard | System overview, gate status, recent activity | dashboard_summary |
| /capabilities | Capability Invocation OS | Skill catalog, invocation status | capability_list |
| /factor-library | Factor Library | Seal status, evaluation matrix | factor_library_summary |
| /composition-graph | Composition Graph | Visual graph, node/edge status | composition_graph_summary |
| /research-report | Research Report Node | Report preview, evidence chain | research_report_summary |
| /z9-review | Z9 Review Node | Review queue, feedback status | z9_review_summary |
| /evidence-chain | Evidence Chain Viewer | Full evidence chain traversal | evidence_chain_demo |
| /run-state | Run State Registry | Pipeline run status, abort reasons | run_state_demo |
| /gate-state | Gate State Registry | Gate pass/fail/pending matrix | gate_state_demo |
| /audit-trail | Audit Trail | All actions, decisions, timestamps | audit_trail_demo |
| /settings | Settings / Safety | Permission view, blocked actions list | auth/permission matrix |

## API Endpoints (all GET)

| Endpoint | Returns |
|:--|:--|
| /api/dashboard/summary | DashboardSummary |
| /api/capabilities | CapabilityList |
| /api/factor-library/summary | FactorLibrarySummary |
| /api/composition-graph/summary | CompositionGraphSummary |
| /api/research-report/summary | ResearchReportSummary |
| /api/z9-review/summary | Z9ReviewSummary |
| /api/evidence-chain | EvidenceChainDemo |
| /api/run-state | RunStateDemo |
| /api/gate-state | GateStateDemo |
| /api/audit-trail | AuditTrailDemo |
