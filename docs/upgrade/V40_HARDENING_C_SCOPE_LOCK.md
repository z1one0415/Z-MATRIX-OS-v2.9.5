# V40 Hardening-C Scope Lock
# Current: SMOKE_PROTOTYPE → Target: INTEGRATION_COMPLETE_CANDIDATE
# RC1: NOT_APPROVED | Production: BLOCKED

## C0-C8 Sub-Batches
| C# | Name | Status |
|:--:|------|:--:|
| C0 | Scope + Acceptance Matrix | IN_PROGRESS |
| C1 | DataForge | NOT_STARTED |
| C2 | FactorFactory | NOT_STARTED |
| C3 | Research Council 12 Reviewers | NOT_STARTED |
| C4 | Report Template Renderer | NOT_STARTED |
| C5 | ExecutionQuality | NOT_STARTED |
| C6 | AccountGovernance | NOT_STARTED |
| C7 | Cockpit + Audit | NOT_STARTED |
| C8 | IRF-01~08 Pipelines | NOT_STARTED |

## Safety Lock
real_trade_allowed=False | broker_order_allowed=False | runtime_enabled=False
production_allowed=False | human_review_required=True | paper_only=True

## C0 Acceptance Items
HC-C0-001: Scope Lock Document | HC-C0-002: Acceptance Matrix | HC-C0-003: Truth Report Update
HC-C0-004: C0 Verify Script | HC-C0-005: pytest compile check
