# V40 Hardening-C Acceptance Matrix
# Current: INTEGRATION_SMOKE_CANDIDATE | RC1: NOT_APPROVED | Production: BLOCKED

## Status Definitions
NOT_STARTED | IN_PROGRESS | MINIMAL_CORE_DONE | INTEGRATION_SMOKE_DONE | DEPTH_PARTIAL | INTEGRATION_DONE | ACCEPTANCE_DONE | NOT_DONE | BLOCKED

| ID | Name | C# | Status |
|---|---:|---|
| HC-C0-001 | Scope Lock Document | C0 | MINIMAL_CORE_DONE |
| HC-C0-002 | Acceptance Matrix | C0 | MINIMAL_CORE_DONE |
| HC-C1-001 | DataForge Source Registry | C1 | DEPTH_PARTIAL |
| HC-C1-002 | DataForge Evidence Card | C1 | DEPTH_PARTIAL |
| HC-C1-003 | DataForge PIT Snapshot | C1 | DEPTH_PARTIAL |
| HC-C2-001 | FactorFactory IC/RankIC | C2 | DEPTH_PARTIAL |
| HC-C2-002 | FactorFactory T20/T60 Strict | C2 | DEPTH_PARTIAL |
| HC-C2-003 | FactorFactory Net Return | C2 | DEPTH_PARTIAL |
| HC-C3-001 | Research Council 12 Skills | C3 | MINIMAL_CORE_DONE |
| HC-C3-002 | Council Aggregator | C3 | MINIMAL_CORE_DONE |
| HC-C4-001 | Report Templates | C4 | MINIMAL_CORE_DONE |
| HC-C5-001 | Transaction Cost Model | C5 | DEPTH_PARTIAL |
| HC-C5-002 | LimitBoard + Suspension | C5 | DEPTH_PARTIAL |
| HC-C6-001 | Capital Curve | C6 | DEPTH_PARTIAL |
| HC-C6-002 | Holding Alpha | C6 | DEPTH_PARTIAL |
| HC-C7-001 | Output Envelope | C7 | MINIMAL_CORE_DONE |
| HC-C7-002 | Audit Export | C7 | MINIMAL_CORE_DONE |
| HC-C8-001 | IRF-01~08 | C8 | INTEGRATION_SMOKE_DONE |
| HC-C8-002 | IRF Chain Integration | C8 | INTEGRATION_SMOKE_DONE |

## Current Closeout Decision
Current release status: INTEGRATION_SMOKE_CANDIDATE
RC1 status: NOT_APPROVED
Production status: BLOCKED
Reason: C1/C2/C5/C6 have depth-partial. C3/C4/C7 remain minimal-core. Acceptance closeout incomplete.
