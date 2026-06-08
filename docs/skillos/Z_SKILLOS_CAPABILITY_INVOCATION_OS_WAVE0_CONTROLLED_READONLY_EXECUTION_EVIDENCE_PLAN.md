# Wave0 Controlled Read-Only Execution Evidence Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_EVIDENCE_PLAN_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED

## Evidence Architecture
FUTURE_PLAN_ONLY. Hash-only, noop-default evidence collection for controlled read-only execution.

## Evidence Fields (future, under explicit evidence gate)
| Field | Type | Description |
|:--|:--|:--|
| source_reference | string | Which artifact/request triggered the call |
| request_hash | SHA256 | Hash of request parameters (no raw content) |
| response_hash | SHA256 | Hash of response (no raw content) |
| decision_hash | SHA256 | Hash of gate evaluation decision |
| adapter_id | enum | Which adapter (github/docgen/docs/report) |
| permission_tier | enum | Which permission tier granted |
| gate_state | dict | Full gate evaluation result per gate |
| timestamp | ISO8601 | When the evidence was created |
| kill_switch_state | dict | State of all kill switches at call time |

## Evidence Rules
- **No hidden write**: all evidence sink defaults to noop
- **Hash-only proof**: no raw content stored in evidence
- **No file writes**: evidence never touches filesystem
- **No stdout/stderr**: no console output from evidence
- **In-memory only under future explicit gate**: even in-memory storage requires gate
- **No telemetry**: no external sending of evidence
- **No runtime_audit/runtime_reports/data**: no artifacts
- **Evidence kill switch**: independently blocks evidence collection

## Evidence Lifecycle (future)
1. CREATE: gate evaluation produces decision_hash
2. HASH: request/response hashed with SHA256
3. STORE: in-memory only (requires evidence gate enabled)
4. ROTATE: >1000 records → rotate (oldest pruned)
5. FLUSH: on kill switch activation or explicit flush

## Dependency
WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4). P0 evidence already implements noop default + in-memory hash-only.

## Boundary
No runtime enablement. No adapter execution enablement. No capability execution. No file writes. Level 5 remains BLOCKED.

## Next
Evidence plan → adapter priority → canary plan

> Cap OS Wave0 | Controlled Exec Planning | Evidence Plan | FUTURE_PLAN_ONLY | Level 5 BLOCKED