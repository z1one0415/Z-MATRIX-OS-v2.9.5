# Z-SkillOS Frontend App RC Merge Decision Gate

## Status: PENDING | Decision: PENDING_HUMAN_DECISION | Default: NO_MERGE_AUTHORIZED

## Source
- base_commit: 2c17785e
- frontend_handoff_rc: a6dcff2
- frontend_app: 67c9449
- route_alias_patch: a3e533f
- visual_qa: 2c17785e

## Merge: candidate=frontend/z-skillos-dashboard-visual-qa-integration-review → target=integration/z-skillos-frontend-handoff-rc
## Merge executed: false | Visual QA mode: SOURCE_LEVEL_AND_CONTRACT_LEVEL_ONLY | Browser render QA: NOT_EXECUTED

## Available Decisions
1. APPROVE_FRONTEND_APP_RC_MERGE → merge execution only
2. REJECT_FRONTEND_APP_RC_MERGE → revision or closeout
3. REQUEST_FRONTEND_APP_RC_HARDENING → hardening
4. REQUEST_BROWSER_RENDER_QA_BEFORE_MERGE → browser QA first

## Safety
- Runtime: DISABLED_DEFAULT | Runner: DISABLED | Paper Trading: DISABLED
- Production: BLOCKED | Broker: BLOCKED | Real Trade: BLOCKED
- Alpha: false | Promotion: false | F8: BLOCKED

## Next: AWAIT_FRONTEND_APP_RC_MERGE_DECISION
