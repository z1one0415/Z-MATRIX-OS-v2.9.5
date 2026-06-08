# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — INPUT SOURCE PLAN

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_INPUT_SOURCE_PLAN_READY

## Scope
This document defines the input source taxonomy, validation rules, and trust assignment for invocations entering the SkillOS Readonly Invocation Sandbox.

## Evidence
Input source evidence is captured at gate entry:
- `source_class` — Primary classification derived from input origin
- `adapter_id` — Skill adapter identifier extracted from input metadata
- `request_hash` — Computed from canonical serialization of the raw input

### Input Source Taxonomy
| Source | Detection Method | Default Trust | Risk Profile |
|--------|------------------|---------------|--------------|
| Webchat Message | Channel routing header | MEDIUM | User-facing, potentially untrusted payload |
| Agent-to-Agent RPC | Internal routing token | HIGH | Signed internal communication |
| Scheduled Trigger | Cron/scheduler origin marker | MEDIUM | Time-bound, replayable |
| System Event | Event bus origin marker | HIGH | System-internal, authenticated |
| API Gateway | External API token | LOW | External, requires full validation |
| CLI Direct | Process ancestry check | HIGH | Local machine, authenticated user |

### Input Validation Rules
1. adapter_id MUST match regex: ^[a-z][a-z0-9_-]{2,63}$
2. request_hash MUST be present and non-empty (32-byte hex-encoded SHA-256)
3. Input payload MUST NOT exceed MAX_INPUT_SIZE
4. Input MUST be valid UTF-8 text
5. Binary inputs MUST be rejected at the sandbox boundary
6. Input MUST NOT contain executable code fragments

## Boundary
- Input validation occurs at the sandbox boundary, before gate evaluation
- Rejected inputs produce a rejection evidence record
- Input payloads are never logged or persisted
- Input source detection is stateless per invocation

## Forbidden
1. Blind trust of API Gateway sources without full validation
2. Input payload logging or persistence
3. Binary input acceptance
4. Input source spoofing tolerance
5. Dynamic trust re-evaluation mid-invocation
6. Input forwarding to non-sandbox contexts

## Proof
- All 6 input sources have explicit detection methods
- Validation rules are deterministic and testable
- Binary input rejection is absolute (no escape hatch)
- Input payload amnesia is guaranteed by in-memory-only design

## Next
- Align input validation with GATE_MODEL tier restrictions
- Ensure OUTPUT_CONTRACT_PLAN does not echo raw inputs
- Proceed to OUTPUT_CONTRACT_PLAN
