# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — REVIEW RISK REGISTER

> Status: _REVIEW_RISK_REGISTER_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Risks: 12 across 4 categories | C=CRITICAL, H=HIGH, M=MEDIUM, L=LOW

## 1. Status
Phase: Wave 0 — Review Phase | Priority: P0 | 12 risks with full sev/lik/mitigation
Hardened: 2026-06-08

## 2. Scope

| # | Risk | Category | Sev | Lik | Impact | Mitigation |
|:--|:--|:--|:--:|:--:|:--|:--|
| RR1 | Planning→Impl Creep | Boundary | C | L | Docs become impl specs, FUTURE_PLAN_ONLY violated | Marker on every doc. FA01-FA05. Grep audit |
| RR2 | Permission Tier Gap | Governance | H | L | Module assigned wrong tier, unauth access | T0-T7 mapping. C18 cross-ref verification |
| RR3 | Module Priority Wrong | Dependency | H | L | Dependency chain break, CAP-REG-001 not first | Priority rules R1-R5. Dependency graph |
| RR4 | Wave C Implied Ready | Wave Border | C | L | T5-T7 accidentally enabled/specified | FUTURE ONLY marker. No spec. Level 5 BLOCKED |
| RR5 | Evidence Missing Fields | Evidence | M | L | Evidence block incomplete, audit broken | 8-field template. EI-01 through EI-08 |
| RR6 | No Import Enforcement | Compliance | C | L | Import/call refs to Z-MATRIX in docs | grep check. C08 verification |
| RR7 | Scope Creep Wave 1 | Scope | H | M | Review expands scope beyond docs-only | Scope boundary Sec 4. Gate GR1-GR10 |
| RR8 | Doc Quality Too Thin | Quality | M | M | Docs fail depth, unreviewable | Depth standards. C02-C04 |
| RR9 | Review Gate Bypassed | Process | C | L | Docs to merge without review | REVIEW_GATE mandatory. C13-C14 |
| RR10 | Decision Record Incomplete | Process | M | L | PENDING fields unpopulated, decision untraceable | 10 PENDING enumerated. C14 verification |
| RR11 | Merge Wrong Base | Git | C | L | Merge targets incorrect commit, overwrites upstream | Pre-merge verify. Base verification |
| RR12 | Forbidden Violation Undetected | Safety | C | M | FA present but missed, enters merged docs | 5 detection mechanisms. C10 verification |

Risk severity: C=violates fundamental constraint (package invalid), H=undermines integrity (must fix), M=quality/process concern (should fix), L=minor (acceptable with doc).

Likelihood: H=>50%, M=10-50%, L=<10%.

## 3. Evidence / Dependency

All 12 risks reviewed during gate evaluation. Reviewer validates severity/likelihood. New risks added as RR13+.

## 4. Boundary

Register covers planning+review phase risks. NOT: implementation risks, runtime risks, deployment risks, market risks.

## 5. Forbidden Actions

F-RR01 <12 risks (MEDIUM) | F-RR02 No sev/lik/mit (MEDIUM) | F-RR03 Claim resolved no evidence (HIGH) | F-RR04 Sev downgrade bypass (MEDIUM) | F-RR05 Bypass gate (HIGH) | F-RR06 Duplicate entries (MEDIUM) | F-RR07 Critical no mitigation (CRITICAL) | F-RR08 Modified after closeout (MEDIUM) | F-RR09 Claim cover impl risks (MEDIUM) | F-RR10 Unverified mitigation (MEDIUM) | F-RR11 Add without review (MEDIUM) | F-RR12 Imply code exists (CRITICAL) | F-RR13 Blank impact (LOW) | F-RR14 Used as merge auth (CRITICAL) | F-RR15 Accept without reviewer (HIGH) | F-RR16 Nonexistent doc ref (MEDIUM) | F-RR17 Missing category (MEDIUM) | F-RR18 Auto-gen no human (MEDIUM)

## 6. Proof / Requirements

R-RR01: 12 risks unique IDs | R-RR02: All have severity | R-RR03: All have likelihood | R-RR04: All have mitigation | R-RR05: All have impact | R-RR06: 4 categories | R-RR07: Sev/lik definitions | R-RR08: Forbidden >=18 | R-RR09: Review cadence | R-RR10: Expansion RR13+

## 7. Next

REVIEW_DECISION_BRIEF.md → REVIEW_DECISION_RECORD.md → REVIEW_MERGE_READINESS.md → REVIEW_CLOSEOUT.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-REVIEW_RISK_REGISTER-v1.1
