# Page Data Contract Freeze — A1 Contract

## Status: FROZEN

- **Seal**: A1_CONTRACT_FREEZE
- **Version**: v0.1.0-rc
- **Contract File**: `skillos/frontend_handoff/contracts/page_data_contract.json`
- **Frozen Date**: 2026-06-12

## Page Inventory (11 pages)

| # | Page ID | Route | Description |
|:--|:--|:--|:--|
| 1 | home_dashboard | / | System overview, gate status, activity feed |
| 2 | capabilities | /capabilities | Skill catalog viewer |
| 3 | factor_library | /factor-library | Factor seal status browser |
| 4 | composition_graph | /composition-graph | Graph visualizer (view-only) |
| 5 | research_report | /research-report | Report preview viewer |
| 6 | z9_review | /z9-review | Review queue viewer |
| 7 | evidence_chain | /evidence-chain | Evidence chain traversal |
| 8 | run_state | /run-state | Pipeline run status |
| 9 | gate_state | /gate-state | Gate pass/fail matrix |
| 10 | audit_trail | /audit-trail | Full audit log |
| 11 | settings | /settings | Safety boundary viewer |

## State Contract per Page

Every page MUST implement all 6 states:

| State | Component | Trigger |
|:--|:--|:--|
| loading | loading_spinner | Data fetch initiated |
| empty | empty_state | API returns no data |
| error | error_card | API call fails |
| degraded | degraded_badge | Partial data returned |
| blocked | blocked_overlay | Permission denied or feature disabled |
| success | success_indicator | Data loaded successfully |

## Forbidden Actions per Page

Each page defines its own forbidden_actions list:
- **home_dashboard** (3): start_pipeline, stop_pipeline, enable_skill, disable_skill, modify_config
- **capabilities** (5): invoke_skill, enable_skill, disable_skill, configure_skill, promote_skill
- **factor_library** (6): create_factor, modify_factor, delete_factor, promote_factor, advance_f8, unseal_factor
- **composition_graph** (6): add_node, remove_node, add_edge, remove_edge, modify_graph, reconfigure_flow
- **research_report** (5): generate_report, modify_report, delete_report, promote_to_production, set_confidence
- **z9_review** (5): start_review, submit_review, approve_review, reject_review, modify_review_criteria
- **evidence_chain** (4): modify_evidence, delete_evidence, inject_evidence, tamper_hash
- **run_state** (5): start_run, stop_run, abort_run, retry_run, modify_run_config
- **gate_state** (4): open_gate, close_gate, bypass_gate, modify_gate_rules
- **audit_trail** (4): modify_audit, delete_audit, redact_entry, purge_trail
- **settings** (6): modify_permissions, enable_runtime, enable_production, enable_paper_trading, modify_safety_boundary, change_contract

## Global Forbidden Fields

These fields MUST NOT appear anywhere in the system:
`buy`, `sell`, `order`, `position`, `broker_action`, `runtime_enable`, `production_enable`, `paper_trading_start`, `alpha_claim`

## Fixture Payloads

Each page includes a `fixture_payload` for development/testing. All fixtures:
- Return empty arrays for list fields
- Set all mutation flags to `false`
- Set `readonly` to `true`
- Set `generation_enabled` and `review_enabled` to `false` for research_report and z9_review

## Compliance Verification

- [x] 11 pages defined with unique routes and page_ids
- [x] All 11 pages have loading/empty/error/degraded/blocked/success states
- [x] All pages have non-empty forbidden_actions
- [x] All forbidden_actions are mutation/execution actions
- [x] No buy/sell/order/position in any field
- [x] No broker_action/runtime_enable/production_enable/paper_trading_start/alpha_claim
- [x] All fixture_payloads respect disabled-default constraints
