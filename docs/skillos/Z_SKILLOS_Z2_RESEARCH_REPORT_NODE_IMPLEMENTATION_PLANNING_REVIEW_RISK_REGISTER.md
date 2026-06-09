# Z2 Research Report Node Implementation Planning — REVIEW RISK REGISTER

> Status: REVIEW_PENDING
> Seal: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED
> Date: 2026-06-09
> Branch: plan/skillos-z2-research-report-node-implementation-planning
> Base: c5f69f5

---

## 1. Status

| Field | Value |
|-------|-------|
| Phase | Review |
| Total review risks | 26 |
| P0 risks | 7 |
| P1 risks | 11 |
| P2 risks | 8 |
| Confidence | HIGH_WITH_STRUCTURE_ONLY |

## 2. Scope

Risk register specific to the REVIEW phase. These risks assess what could go wrong during the review process itself, or what review might miss that impacts implementation safety.

## 3. Dependency

- Planning phase SEALED (Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED)
- All upstream dependencies verified at c5f69f5
- Risk assessment based on planning document quality

## 4. Boundary

- Risks scoped to review-phase concerns only
- Implementation risks tracked separately in planning RISK_REGISTER
- Review risks inform reviewer attention allocation

## 5. Forbidden

- No risk mitigation may introduce or approve forbidden fields
- No risk workaround may bypass the review gate

## 6. Proof

### Review Risk Register (26 Risks)

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|---|------|----------|-----------|------------|---------|-----------------|
| RR01 | Reviewer misses forbidden field in model spec | P0-Critical | Low | Checklist CHECK-25 through CHECK-30 explicitly verify | Cross-reference scan of all docs | Any forbidden field survives review |
| RR02 | Kill-switch bypass not caught in review | P0-Critical | Very Low | Dedicated CHECK-22 + CHECK-36 in checklist | Kill-switch doc explicit about sole env-var | Bypass path discovered post-review |
| RR03 | Dependency seal marker invalid/stale | P1-High | Low | CHECK-11 through CHECK-16 verify each seal | Git log verification of merge commits | Seal marker references non-existent merge |
| RR04 | Scope creep approved without detection | P1-High | Medium | Explicit in/out-of-scope tables in SCOPE doc | Boundary doc cross-reference | Implementation exceeds planning scope |
| RR05 | Contract incompatibility with Z9 not detected | P0-Critical | Low | Z9 contract explicitly defined in CONTRACTS | CHECK-38 verifies Z9 test cases | Z9 rejects snapshot at integration |
| RR06 | Test plan insufficient coverage | P1-High | Medium | 50 proof categories + ≥95% target | CHECK-33 and CHECK-34 verify | Coverage gap found in implementation |
| RR07 | Risk register risks too generic | P2-Medium | Medium | Each risk has specific rollback trigger | Reviewer validates trigger specificity | Risk materializes without clear trigger |
| RR08 | Reviewer rubber-stamps without reading | P0-Critical | Low | 42-item checklist forces granular verification | Multiple cross-reference checks | Critical issue found post-approval |
| RR09 | Document internal inconsistency missed | P1-High | Medium | CHECK-39 through CHECK-42 cover consistency | Cross-document terminology check | Conflicting specs in implementation |
| RR10 | Batch ordering dependency violation | P1-High | Low | CHECK-10 verifies acyclic batch plan | FUTURE_CODE_MAP explicit ordering | Batch 2 depends on uncommitted Batch 1 code |
| RR11 | Model relationship diagram inaccurate | P2-Medium | Medium | MODELS doc has explicit relationship tree | CHECK-41 cross-references with CONTRACTS | Model mismatch at implementation |
| RR12 | Degradation escalation logic ambiguous | P1-High | Medium | DEGRADATION doc has explicit L1-L4 levels | CHECK-37 verifies degradation test cases | Incorrect escalation behavior |
| RR13 | Config override injection vector missed | P2-Medium | Low | CONTRACTS doc documents config validation | Risk R19 in planning register | Injection at runtime |
| RR14 | Review takes too long, blocking implementation | P2-Medium | Medium | Structured checklist enables rapid review | Time-boxed review cycle (48h) | Review exceeds 1 week |
| RR15 | postmerge HEAD diverges during review | P1-High | Low | Pin to c5f69f5 explicitly | Verify HEAD before approval | HEAD != c5f69f5 at approval time |
| RR16 | Missing edge case in proof plan | P1-High | Medium | 50 categories is comprehensive | Reviewer adds missing cases | Edge case causes failure in implementation |
| RR17 | Reviewer unfamiliar with upstream contracts | P2-Medium | Medium | DEPENDENCY_MAP provides full context | Sealed upstream docs available for reference | Misunderstanding of B1 contract |
| RR18 | Forbidden field list incomplete | P0-Critical | Very Low | Canonical 14-item list verified against upstream | Cross-reference with all sealed plans | New forbidden field discovered post-implementation |
| RR19 | Kill-switch env-var name collision | P2-Medium | Very Low | Unique name: Z2_RESEARCH_REPORT_NODE_ENABLED | Grep across codebase for conflicts | Env-var inadvertently set by other service |
| RR20 | Review docs themselves have structural issues | P2-Medium | Low | Self-referential 7-section check | Line count and structure validation | Review doc missing section |
| RR21 | Approval granted with unresolved TODO | P1-High | Low | No TODO markers in sealed docs | Grep for TODO/FIXME/HACK | Implementation blocked by unresolved item |
| RR22 | Z9 snapshot confidence level misspecified | P1-High | Low | Explicit: HIGH_WITH_STRUCTURE_ONLY in CONTRACTS | CHECK-24 verifies | Z9 receives unexpected confidence |
| RR23 | Determinism requirement underspecified | P2-Medium | Medium | Section builder determinism in test plan (proof #30) | CHECK-39 consistency check | Non-deterministic output in production |
| RR24 | Timeout value (30s) inappropriate | P2-Medium | Medium | Configurable via config.py (future) | Benchmark in Batch 3 integration test | Timeout too aggressive or too lenient |
| RR25 | Immutability (frozen=True) breaks downstream | P1-High | Low | Frozen models documented in MODELS | Z9 contract test validates serializability | Z9 can't consume frozen model |
| RR26 | Review approval without merge readiness | P0-Critical | Low | CLOSEOUT explicitly states ready-for-review | MERGE docs define post-approval steps | Approved but can't merge cleanly |

## 7. Next

- Reviewer acknowledges all 26 risks
- P0 risks require explicit sign-off
- P1 risks require acknowledgment of mitigation
- P2 risks noted for monitoring
- Review decision recorded in REVIEW_DECISION_RECORD

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
