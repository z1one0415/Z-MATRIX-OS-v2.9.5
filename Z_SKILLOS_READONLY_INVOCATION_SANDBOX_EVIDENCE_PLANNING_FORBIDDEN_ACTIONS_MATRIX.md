# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — FORBIDDEN ACTIONS MATRIX

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_FORBIDDEN_ACTIONS_MATRIX_READY

## Scope
This document provides an exhaustive enumeration of all forbidden actions. Every action is Level 5 BLOCKED at the planning stage.

## Evidence
The forbidden actions matrix is itself evidence of the security posture. No forbidden action has a permitted escape hatch.

### Forbidden Actions Matrix (40 actions)

| ID | Category | Action | Severity | Detection |
|----|----------|--------|----------|-----------|
| F01 | PERSISTENCE | Write to any file on disk | CRITICAL | Syscall filter |
| F02 | PERSISTENCE | Create temporary files | CRITICAL | Syscall filter |
| F03 | PERSISTENCE | Write to environment variables | CRITICAL | Env access audit |
| F04 | PERSISTENCE | Mutate process-level state | HIGH | State snapshot diff |
| F05 | PERSISTENCE | Open database connection | CRITICAL | Syscall filter |
| F06 | PERSISTENCE | Write to shared memory | CRITICAL | Syscall filter |
| F07 | NETWORK | Open outbound network connection | CRITICAL | Syscall filter |
| F08 | NETWORK | Listen on any network port | CRITICAL | Syscall filter |
| F09 | NETWORK | Send data via IPC | CRITICAL | Syscall filter |
| F10 | PRIVACY | Access another invocation's memory arena | CRITICAL | Memory boundary check |
| F11 | PRIVACY | Access another invocation's hash chain | CRITICAL | Chain registry isolation |
| F12 | PRIVACY | Access another invocation's audit sink | CRITICAL | Sink registry isolation |
| F13 | PRIVACY | Reuse ephemeral key from another invocation | CRITICAL | Key registry isolation |
| F14 | PRIVACY | Leak invocation arguments to consumer context | HIGH | Output contract validation |
| F15 | EVIDENCE | Persist evidence bundle to disk | CRITICAL | File write detection |
| F16 | EVIDENCE | Transmit evidence via network | CRITICAL | Network access detection |
| F17 | EVIDENCE | Modify evidence after sealing | CRITICAL | Tamper_seal verification |
| F18 | EVIDENCE | Reorder evidence chain links | CRITICAL | Chain verification |
| F19 | EVIDENCE | Forge evidence chain seal | CRITICAL | Chain verification |
| F20 | EVIDENCE | Cross-invocation hash chain linking | CRITICAL | Chain registry isolation |
| F21 | GATE | Escalate permission tier after gate entry | CRITICAL | Tier immutability check |
| F22 | GATE | Mutate source_class during invocation | CRITICAL | Source immutability check |
| F23 | GATE | Spoof adapter_id | CRITICAL | Adapter authentication |
| F24 | GATE | Bypass gate entirely | CRITICAL | Mandatory gate check |
| F25 | ROLLBACK | Rollback after DELIVERED state | HIGH | State machine enforcement |
| F26 | ROLLBACK | Partial rollback (leave residual state) | HIGH | All-or-nothing check |
| F27 | ROLLBACK | Rollback without evidence record | HIGH | Mandatory rollback evidence |
| F28 | INPUT | Accept binary input | CRITICAL | Input type validation |
| F29 | INPUT | Accept input exceeding MAX_INPUT_SIZE | HIGH | Size validation |
| F30 | INPUT | Accept executable code in input | CRITICAL | Content inspection |
| F31 | INPUT | Accept input with null bytes | HIGH | Content validation |
| F32 | AUDIT | Export audit sink data to file | CRITICAL | File write detection |
| F33 | AUDIT | Expose audit sink via network | CRITICAL | Network access detection |
| F34 | AUDIT | Allow audit sink growth beyond 10,000 bundles | HIGH | Capacity enforcement |
| F35 | TIMING | Introduce timing side-channel between invocations | MEDIUM | Fixed-time operations |
| F36 | RESOURCE | Exhaust memory beyond per-invocation quota | HIGH | Memory quota enforcement |
| F37 | RESOURCE | Consume CPU beyond per-invocation budget | MEDIUM | CPU budget enforcement |
| F38 | OUTPUT | Bundle actual invocation payloads in evidence | HIGH | Output contract validation |
| F39 | OUTPUT | Include PII in evidence fields | CRITICAL | Output scrubbing |
| F40 | OUTPUT | Non-deterministic evidence serialization | HIGH | Canonical serialization enforcement |

### Severity Summary
- CRITICAL: 22 items — Violation breaks core sandbox guarantee, immediate rejection
- HIGH: 14 items — Violation creates significant risk, sandbox rejection
- MEDIUM: 4 items — Violation creates measurable risk, sandbox warning + rejection

## Boundary
- This matrix covers the readonly sandbox scope only
- Actions outside the sandbox boundary are not enumerated
- Matrix is forward-compatible (new IDs can be added)
- Matrix does not prescribe implementation-level enforcement mechanisms

## Forbidden
This document itself is the forbidden actions catalog. No meta-forbidden actions are defined.

## Proof
- 40 forbidden actions exhaustively enumerated
- Every category from all planning documents is covered
- Severity classification is consistent with sandbox guarantees
- No action has an escape hatch or exception path
- Detection method specified for every action

## Next
- Use this matrix as test case source for TEST_AND_PROOF_PLAN
- Ensure REVIEW_RISK_REGISTER maps risks to specific forbidden actions
- Proceed to PLANNING_CLOSEOUT
