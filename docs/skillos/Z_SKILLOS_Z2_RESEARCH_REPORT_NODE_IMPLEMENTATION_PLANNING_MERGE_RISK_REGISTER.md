# Z2 Research Report Node Implementation Planning — MERGE RISK REGISTER

> Status: MERGE_PENDING
> Seal: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED
> Date: 2026-06-09
> Branch: plan/skillos-z2-research-report-node-implementation-planning
> Base: c5f69f5

---

## 1. Status

| Field | Value |
|-------|-------|
| Phase | Merge preparation |
| Total merge risks | 22 |
| P0 risks | 5 |
| P1 risks | 10 |
| P2 risks | 7 |
| Confidence | HIGH_WITH_STRUCTURE_ONLY |

## 2. Scope

Risk register specific to the MERGE phase. These risks assess what could go wrong during or after the merge of planning docs to main.

## 3. Dependency

- Review APPROVED
- Planning SEALED
- postmerge HEAD = c5f69f5
- Branch clean and rebased

## 4. Boundary

- Merge risks cover the merge operation and immediate post-merge state
- Implementation risks are out of scope (tracked separately)
- Merge risks are time-bounded (resolve within merge cycle)

## 5. Forbidden

- No merge risk mitigation may introduce forbidden fields
- No merge workaround may bypass review approval gate
- No force-merge allowed

## 6. Proof

### Merge Risk Register (22 Risks)

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|---|------|----------|-----------|------------|---------|-----------------|
| MR01 | Merge conflict with concurrent branch | P1-High | Medium | Rebase before merge; verify clean merge | git merge --no-ff dry-run | Conflict markers in merged files |
| MR02 | HEAD diverged from c5f69f5 during review | P0-Critical | Low | Re-verify HEAD at merge time | git log --oneline HEAD comparison | HEAD != c5f69f5 at merge time |
| MR03 | Accidental code file in merge | P0-Critical | Very Low | MERGE-24 through MERGE-28 verify no code | File extension scan | Any .py file in commit |
| MR04 | File corruption during merge | P1-High | Very Low | Post-merge checksum verification | md5sum of all 26 files | Checksum mismatch |
| MR05 | Wrong branch merged | P0-Critical | Very Low | Branch name verification in merge command | MERGE-01 explicit check | Branch name mismatch |
| MR06 | Partial merge (not all 26 files) | P1-High | Low | Post-merge file count verification | ls docs/skillos/ | wc -l != 26 | Count != 26 |
| MR07 | Merge squash loses commit history | P1-High | Medium | Use --no-ff merge (preserve history) | Merge commit includes all file additions | Missing commits in history |
| MR08 | Permissions changed on merge | P2-Medium | Very Low | MERGE-14 checks no executable perms | find -perm check post-merge | Executable docs |
| MR09 | Encoding corruption (non-UTF8) | P2-Medium | Very Low | MERGE-11 verifies UTF-8 | file --mime-encoding check | Non-UTF8 file detected |
| MR10 | Seal markers lost in merge | P1-High | Very Low | Post-merge grep for all 4 markers | grep -r across merged docs | Missing seal marker |
| MR11 | Duplicate file from parallel work | P2-Medium | Low | Unique prefix prevents collision | ls for prefix duplicates | Duplicate filename |
| MR12 | Git hook rejects merge | P1-High | Low | Pre-verify hooks locally | git merge dry-run | Hook failure message |
| MR13 | CI pipeline fails on merge | P1-High | Low | Docs-only merge unlikely to trigger CI failure | Monitor CI after merge | CI red after merge |
| MR14 | Review approval expires during merge | P2-Medium | Very Low | Merge within 48h of approval | Timestamp check | >7 days since approval |
| MR15 | Post-merge docs inaccessible | P1-High | Very Low | Verify docs render in repository | Browser check of merged docs | 404 or render failure |
| MR16 | Merge message inadequate | P2-Medium | Medium | Template merge commit message | Merge message includes seal marker | Missing seal reference in commit |
| MR17 | Reviewer approval not recorded before merge | P0-Critical | Low | MERGE-31 verifies REVIEW_DECISION_RECORD | Check for APPROVE status | Decision still PENDING |
| MR18 | Branch protection bypass | P0-Critical | Very Low | Branch protection rules on main | GitHub/GitLab branch protection | Unreviewed merge to main |
| MR19 | Post-merge dependency tracker not updated | P2-Medium | Medium | Update dependency docs post-merge | Checklist includes tracker update | Downstream plans reference wrong seal |
| MR20 | Merge creates unexpectedly large diff | P2-Medium | Low | Expected: 26 new files only | git diff --stat verification | >26 files changed |
| MR21 | Concurrent merge from another planning branch | P1-High | Low | Coordinate merge timing | Check for pending merges | Merge conflict from parallel merge |
| MR22 | Post-merge HEAD becomes new dependency reference | P1-High | Medium | Document new HEAD in MERGE_CLOSEOUT | Record new commit hash | Downstream references stale HEAD |

## 7. Next

- All P0 risks verified BEFORE merge
- P1 risks monitored DURING merge
- P2 risks checked POST-merge
- Any rollback trigger → immediate revert
- MERGE_CLOSEOUT records final merge status

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
