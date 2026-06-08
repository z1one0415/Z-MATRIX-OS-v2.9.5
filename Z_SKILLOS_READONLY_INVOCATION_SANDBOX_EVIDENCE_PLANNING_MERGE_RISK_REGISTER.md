# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — MERGE RISK REGISTER

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_MERGE_RISK_REGISTER_READY

## Scope
This document catalogs 10 merge-specific risks, distinct from the review-phase risks.

## Evidence
Each risk entry includes a unique ID, description, assessment, mitigation, and tracking status.

### Merge Risk Register (10 risks)

| ID | Risk | Likelihood | Impact | Severity | Mitigation | Status |
|----|------|------------|--------|----------|------------|--------|
| MR-01 | Premature merge before WAVE0 dependency resolution | MEDIUM | CRITICAL | HIGH | MC-10 gates merge on dependency RESOLVED; MERGE_DECISION_BRIEF requires dependency status | OPEN |
| MR-02 | Planning documents diverge from main branch after merge without implementation | MEDIUM | MEDIUM | MEDIUM | SEAL prevents document modification; merge commit is single source of truth | OPEN |
| MR-03 | Merge conflict with other planning packages on same target branch | LOW | LOW | LOW | Docs-only; unique filename prefix minimizes collision risk | OPEN |
| MR-04 | Human reviewer bypass: merge signed without actual review | LOW | CRITICAL | HIGH | Multi-gate design; signed closeout required; decision record traceable | OPEN |
| MR-05 | Post-merge document tampering (modification after merge to main) | LOW | MEDIUM | LOW | Git history provides tamper evidence; SEAL references document identities | OPEN |
| MR-06 | Missing merge artifact: incomplete document set merged to main | LOW | HIGH | MEDIUM | MC-04 verifies 26 documents present; merge commit verified by MERGE_CLOSEOUT | OPEN |
| MR-07 | Incorrect branch naming or commit message convention violation | LOW | LOW | LOW | MERGE_REVIEW verifies branch name; commit message documented in task spec | OPEN |
| MR-08 | Merge to wrong target branch (e.g., main instead of integration) | LOW | HIGH | MEDIUM | MERGE_REVIEW requires target_branch identification; human sign-off | OPEN |
| MR-09 | Post-merge drift: implementation begins before merge documentation is archived | MEDIUM | MEDIUM | MEDIUM | FUTURE_PLAN_ONLY constraint documented; implementation phase is separate | OPEN |
| MR-10 | Incomplete human sign-off chain (missing signatures on closeout documents) | LOW | MEDIUM | LOW | All three closeout documents require explicit human signature | OPEN |

### Merge Risk Summary
- CRITICAL impact: 2 (MR-01, MR-04)
- HIGH impact: 2 (MR-06, MR-08)
- MEDIUM impact: 4 (MR-02, MR-05, MR-09, MR-10)
- LOW impact: 2 (MR-03, MR-07)

### Merge Blocking Risks
- MR-01: Merge cannot proceed with UNRESOLVED WAVE0 dependency (BLOCKING)
- MR-04: Merge requires active human verification (PROCEDURAL BLOCKING)

## Boundary
- Merge risk register covers merge-operation risks only
- Does not re-catalog review-phase risks (see REVIEW_RISK_REGISTER)
- Does not cover post-merge implementation risks

## Forbidden
1. Merging with blocking risks unresolved
2. Ignoring CRITICAL impact merge risks
3. Auto-mitigating merge risks without human review
4. Skipping merge risk register entirely

## Proof
- 10 merge-specific risks identified
- 2 blocking risks with clear resolution criteria
- All risks have documented mitigations
- MR-01 directly enforces MC-10 compliance

## Next
- Human reviewer assesses merge risk severity
- Blocking risks (MR-01, MR-04) must be actively resolved
- Risk register feeds into MERGE_DECISION_BRIEF
- Proceed to MERGE_DECISION_BRIEF
