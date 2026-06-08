# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — REVIEW RISK REGISTER

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_REVIEW_RISK_REGISTER_READY

## Scope
This document catalogs 12 identified risks for the SkillOS Readonly Invocation Sandbox Evidence Planning package.

## Evidence
Each risk entry includes a unique ID, description, assessment, mitigation, and tracking status.

### Risk Register (12 risks)

| ID | Risk | Likelihood | Impact | Severity | Mitigation | Status |
|----|------|------------|--------|----------|------------|--------|
| R01 | Hash chain link ordering attack through canonical serialization ambiguity | LOW | HIGH | MEDIUM | Canonical JSON with sorted keys in OUTPUT_CONTRACT_PLAN | OPEN |
| R02 | Ephemeral key generation weakness (weak CSPRNG seeding) | LOW | CRITICAL | HIGH | CSPRNG requirement in PRIVACY_BOUNDARY_PLAN | OPEN |
| R03 | Memory arena isolation bypass via OS-level shared memory | LOW | CRITICAL | HIGH | Syscall filter F06 in FORBIDDEN_ACTIONS_MATRIX | OPEN |
| R04 | TTL-based evidence destruction race condition with consumer acknowledgment | MEDIUM | MEDIUM | MEDIUM | TTL grace period; DELIVERED state prevents premature destruction | OPEN |
| R05 | Audit sink capacity exhaustion under high invocation rate | MEDIUM | LOW | LOW | Max 10,000 bundle cap with LRU eviction | OPEN |
| R06 | Consumer callback failure leaving evidence unacknowledged | MEDIUM | LOW | LOW | TTL-based automatic cleanup; no retry to prevent resource leak | OPEN |
| R07 | Rollback state machine deadlock in concurrent invocation scenarios | LOW | MEDIUM | LOW | Per-invocation state machine; deterministic transitions | OPEN |
| R08 | Timing side-channel leaking invocation count or activity | LOW | LOW | LOW | Fixed-time operations; TIMING forbidden action F35 | OPEN |
| R09 | False-positive hash chain verification failure from null_anchor collision | VERY_LOW | HIGH | MEDIUM | null_anchor is 64 bytes of 0x00 (not a valid SHA-256 output) | OPEN |
| R10 | Documentation drift between planning and implementation phases | MEDIUM | MEDIUM | MEDIUM | SEAL guarantees immutability; merge checklist validates | OPEN |
| R11 | WAVE0 dependency not resolved before merge (blocking dependency) | HIGH | CRITICAL | CRITICAL | Dependency declared in SCOPE/PLANNING_SEAL; MERGE_CHECKLIST gates | OPEN |
| R12 | Human reviewer error (checklist fatigue, incomplete review) | MEDIUM | HIGH | HIGH | 35-item checklist with explicit sign-off; decision record traceable | OPEN |

### Risk Summary
- CRITICAL impact: 3 (R02, R03, R11)
- HIGH impact: 3 (R01, R09, R12)
- MEDIUM impact: 4 (R04, R07, R10)
- LOW impact: 3 (R05, R06, R08)
- Open risks: 12 | Mitigated: 0 | Accepted: 0

## Boundary
- Risk register covers planning-phase risks only
- Implementation risks are out of scope (FUTURE_PLAN_ONLY)
- Risk assessment is qualitative, not quantitative

## Forbidden
1. Closing a risk without documented mitigation or acceptance
2. Ignoring CRITICAL impact risks during review
3. Auto-mitigating risks without human review

## Proof
- 12 risks identified across all planning document domains
- Every risk has likelihood, impact, severity, mitigation, and status
- CRITICAL risks have explicit mitigations documented
- R11 (WAVE0 dependency) is the single blocking risk for merge

## Next
- Human reviewer assesses risk severity and acceptance
- Each risk either mitigated, accepted, or escalated
- Risk register feeds into REVIEW_DECISION_RECORD
- Proceed to REVIEW_DECISION_BRIEF
