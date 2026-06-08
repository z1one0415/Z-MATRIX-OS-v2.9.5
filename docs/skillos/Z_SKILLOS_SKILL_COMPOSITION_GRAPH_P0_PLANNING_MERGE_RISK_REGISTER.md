# Z-SkillOS Skill Composition Graph P0 Planning — MERGE RISK REGISTER

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Merge Risk Register Definition

This register catalogues risks specific to the merge operation — the act of integrating this
planning package into the main branch. These risks are distinct from review risks, which address
design quality. Merge risks address branch management, versioning, and downstream impact.
Minimum: 10 risks.

## 2. Merge Risks

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback |
|---|------|----------|------------|------------|---------|----------|
| MRR-01 | Merge conflict with main branch changes | MEDIUM | LOW | Branch is based on clean commit; rebase before merge | Git diff verification before merge | Abort merge; resolve conflicts |
| MRR-02 | Planning docs referenced from other branches before merge complete | LOW | LOW | Branch is isolated; no cross-branch references | Branch dependency audit | Notify dependent branches |
| MRR-03 | P1 planning started before P0 merge, creating divergent specs | MEDIUM | LOW | P1 explicitly depends on merged P0 | P1 gate requires P0 merge SHA | Rebase P1 on merged P0 |
| MRR-04 | Human reviewer rejects package after merge docs prepared | MEDIUM | MEDIUM | Merge closeout includes _MERGE_REVIEW_READY_FOR_HUMAN_DECISION gate | Human decision required before actual merge | Revise per feedback; re-submit |
| MRR-05 | Depth standard regression during merge (accidental truncation) | HIGH | VERY LOW | All docs written as complete artifacts; no truncation possible | Line count verification in merge checklist MC-02 to MC-04 | Re-write affected docs |
| MRR-06 | Wrong branch merged (merge to wrong target) | CRITICAL | VERY LOW | Explicit branch name in all docs; merge command review | Branch verification in merge checklist | Revert merge; re-merge correctly |
| MRR-07 | Post-merge docs modified without re-approval | HIGH | LOW | Docs marked as sealed; modification requires unseal protocol | Post-merge audit of document hashes | Revert unauthorized changes |
| MRR-08 | Merge doc status markers inconsistent with review docs | MEDIUM | LOW | Cross-document consistency audit in MERGE_REVIEW.md §4 | Automated marker consistency check | Fix inconsistent markers |
| MRR-09 | Planning docs archived prematurely (before P1 reference established) | LOW | LOW | Archive only after P1 branch created and references resolved | P1 creation gate check | Restore from git history |
| MRR-10 | Merge commit message does not follow convention | LOW | LOW | Commit message template: "docs: harden SkillOS skill composition graph P0 planning docs" | Commit message review | Amend commit message |
| MRR-11 | File encoding issues during merge (UTF-8 vs ASCII) | LOW | VERY LOW | All files use standard UTF-8; git handles encoding transparently | File encoding check | Re-encode files |
| MRR-12 | Large file count (26 docs) causes review fatigue | MEDIUM | MEDIUM | Documents are organized by phase (Planning/Review/Merge); executive summary in OVERVIEW.md | Merge review scope includes cross-doc consistency audit | Prioritize critical docs for review |

## 3. Severity Definitions

| Severity | Definition |
|----------|------------|
| CRITICAL | Would corrupt the repository or block downstream work indefinitely |
| HIGH | Would require significant rework or cause version confusion |
| MEDIUM | Would cause delay or require additional review cycles |
| LOW | Minor inconvenience; easily correctable |

## 4. Merge Risk Posture

| Severity | Count | Mitigated? |
|----------|-------|------------|
| CRITICAL | 1 | ✅ (VERY LOW likelihood: explicit branch verification) |
| HIGH | 2 | ✅ (VERY LOW/LOW likelihood: line count + post-merge audit) |
| MEDIUM | 5 | ✅ (All with controls and rollback plans) |
| LOW | 4 | ✅ (Acceptable; standard git operations) |
| **Total** | **12** | **All mitigated** |

## 5. Merge Approval Gate

No merge proceeds until:
1. All 25 merge checklist items ✅
2. All 12 merge risks acknowledged and mitigated
3. Human reviewer approves 10 PENDING decision fields
4. _MERGE_REVIEW_READY_FOR_HUMAN_DECISION declared in MERGE_CLOSEOUT.md

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|MERGE|RISK_REGISTER|v1.0.0-draft`
