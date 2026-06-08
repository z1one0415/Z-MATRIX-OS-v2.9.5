# Z-SkillOS Skill Composition Graph P0 Implementation Planning — MERGE RISK REGISTER

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft
> Minimum: ≥10 risks

---

## 1. Purpose

This document registers all risks specific to the merge operation for the Skill Composition Graph P0
Implementation Planning package. These are risks related to the merge process itself — branch
operations, commit integrity, push verification — not the content risks already covered in the
Review Risk Register. Minimum: 10 risks.

## 2. Merge Risk Register (≥10 Risks)

### Risk M-01: Wrong Branch Merged
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R01 |
| Severity | CRITICAL |
| Likelihood | LOW |
| Impact | Planning docs merged into wrong branch, polluting unrelated history |
| Mitigation | Explicit branch name verification before commit |
| Contingency | `git revert` or `git reset` to undo incorrect merge |
| Status | PENDING VERIFICATION |

### Risk M-02: Missing Files in Commit
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R02 |
| Severity | HIGH |
| Likelihood | MEDIUM |
| Impact | One or more of the 26 files not included in commit |
| Mitigation | Automated count verification; `git status` before commit |
| Contingency | Amend commit or create follow-up commit |
| Status | PENDING VERIFICATION |

### Risk M-03: Incorrect Commit Message
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R03 |
| Severity | LOW |
| Likelihood | LOW |
| Impact | Commit message doesn't follow convention; harder to find later |
| Mitigation | Use exact template: "docs: add SkillOS skill composition graph P0 implementation planning package" |
| Contingency | `git commit --amend` to fix message |
| Status | PENDING VERIFICATION |

### Risk M-04: Push to Wrong Remote
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R04 |
| Severity | MEDIUM |
| Likelihood | VERY LOW |
| Impact | Code pushed to wrong remote (e.g., fork instead of origin) |
| Mitigation | Explicit `git push origin <branch>` with remote verification |
| Contingency | Delete remote branch on wrong remote; push to correct one |
| Status | PENDING VERIFICATION |

### Risk M-05: Merge Conflict with Parent
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R05 |
| Severity | LOW |
| Likelihood | LOW |
| Impact | Merge conflicts when eventually merging into parent branch |
| Mitigation | This branch is docs-only under a unique subdirectory |
| Contingency | Manual merge resolution; docs don't conflict with code |
| Status | PENDING VERIFICATION |

### Risk M-06: File Name Collision with Existing Files
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R06 |
| Severity | LOW |
| Likelihood | VERY LOW |
| Impact | New files have same name as existing files on parent branch |
| Mitigation | Unique prefix `Z_SKILLOS_SKILL_COMPOSITION_GRAPH_P0_IMPLEMENTATION_PLANNING_` |
| Contingency | Rename files if collision detected |
| Status | PENDING VERIFICATION |

### Risk M-07: Line Ending Corruption
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R07 |
| Severity | LOW |
| Likelihood | VERY LOW |
| Impact | CRLF/LF mismatch causes diff noise |
| Mitigation | All .md files; Git handles line endings |
| Contingency | `.gitattributes` or `dos2unix` |
| Status | PENDING VERIFICATION |

### Risk M-08: Partial Push Failure
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R08 |
| Severity | MEDIUM |
| Likelihood | LOW |
| Impact | Push interrupted; some objects not transferred |
| Mitigation | Verify push completion; check remote branch after push |
| Contingency | Retry push; Git is atomic for push |
| Status | PENDING VERIFICATION |

### Risk M-09: Stale Local Branch State
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R09 |
| Severity | LOW |
| Likelihood | LOW |
| Impact | Local branch behind remote; push rejected |
| Mitigation | `git fetch` before push; verify up-to-date |
| Contingency | `git pull --rebase` if behind |
| Status | PENDING VERIFICATION |

### Risk M-10: Accidental Inclusion of Non-Doc Files
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R10 |
| Severity | HIGH |
| Likelihood | LOW |
| Impact | Non-documentation files (scripts, binaries, .pyc) included in commit |
| Mitigation | `git add docs/skillos/*.md` explicitly instead of `git add -A` |
| Contingency | Amend commit to remove unintended files |
| Status | PENDING VERIFICATION |

### Risk M-11: Remote Branch Already Exists with Different History
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R11 |
| Severity | MEDIUM |
| Likelihood | LOW |
| Impact | Remote branch has diverged; force push may be needed |
| Mitigation | Check remote branch state before push |
| Contingency | Coordinate with team if force push needed |
| Status | PENDING VERIFICATION |

### Risk M-12: Post-Merge Verification Gap
| Attribute | Value |
|-----------|-------|
| Risk ID | M-R12 |
| Severity | LOW |
| Likelihood | LOW |
| Impact | Merge completed but files not verified on remote |
| Mitigation | Post-push verification step in MERGE_CLOSEOUT |
| Contingency | Re-push if verification fails |
| Status | PENDING VERIFICATION |

## 3. Risk Summary

| Severity | Count | Risk IDs |
|----------|:---:|------|
| CRITICAL | 1 | M-R01 |
| HIGH | 2 | M-R02, M-R10 |
| MEDIUM | 3 | M-R04, M-R08, M-R11 |
| LOW | 6 | M-R03, M-R05, M-R06, M-R07, M-R09, M-R12 |
| **Total** | **12 risks** | ✅ ≥ 10 |

## 4. Merge Risk Heat Map

```
Likelihood
  HIGH    │ [   ] [   ] [   ]
  MEDIUM  │ [   ] [M02] [   ]
  LOW     │ [M03] [M04] [M01]
          │ [M05] [M08] [M10]
          │ [M06] [M11]
          │ [M07]
          │ [M09]
          │ [M12]
  VERY LOW│ [M04] [   ] [   ]
          │ [M06] [   ] [   ]
          │ [M07] [   ] [   ]
          └──────────────────
            LOW   MED   HIGH  CRIT
                 Severity
```

## 5. Mitigation Verification

| Risk | Pre-Commit Check | Post-Commit Check | Post-Push Check |
|------|:---:|:---:|:---:|
| M-R01 (Wrong branch) | `git branch --show-current` | — | Verify branch name on remote |
| M-R02 (Missing files) | File count = 26 | `git diff --stat HEAD~1` | `ls` on remote |
| M-R03 (Commit message) | Template verification | `git log -1` | — |
| M-R04 (Wrong remote) | `git remote -v` | — | Verify URL |
| M-R05 (Merge conflict) | — | — | Future PR check |
| M-R06 (Name collision) | `ls docs/skillos/` | — | — |
| M-R07 (Line endings) | `.gitattributes` | — | — |
| M-R08 (Partial push) | — | — | Verify all files on remote |
| M-R09 (Stale branch) | `git fetch` | — | — |
| M-R10 (Non-doc files) | Explicit `git add` path | `git diff --stat` | — |
| M-R11 (Diverged history) | `git fetch` + compare | — | — |
| M-R12 (Verification gap) | — | — | MERGE_CLOSEOUT verification |

## 6. Contingency Plans

| Scenario | Immediate Action | Recovery Time |
|----------|-----------------|:---:|
| Wrong branch merged | `git revert` or `git reset` | < 5 min |
| Missing files | `git commit --amend` or new commit | < 5 min |
| Push failure | Retry; check network | < 5 min |
| Force push needed | Coordinate; use `--force-with-lease` | < 10 min |
| File collision | Rename and recommit | < 10 min |
| History divergence | `git pull --rebase` then push | < 10 min |

## 7. Merge Risk Governance

- All merge risks are specific to the git merge operation
- Content risks are covered in REVIEW_RISK_REGISTER
- No CRITICAL risk may remain unmitigated at MERGE_CLOSEOUT
- All HIGH risks must have verified mitigations before merge execution
- Residual risks accepted in MERGE_CLOSEOUT
