# Z-SkillOS Level 4 Disabled-Default Implementation P0 Merge Risk Register

## Status

Z_SKILLOS_LEVEL4_DISABLED_DEFAULT_IMPLEMENTATION_P0_MERGE_RISK_REGISTER_READY

## Risk Catalog

### R1: P0 Skeleton Merged Then Accidentally Wired Into Runtime

| Field | Value |
|:--|:--|
| **Severity** | Critical |
| **Likelihood** | Low |
| **Description** | After merge, production code imports skillos.level4 and calls evaluate_level4 in a live path |
| **Current Mitigation** | Level 4 package is isolated; no zmatrix module imports skillos |
| **Required Post-Merge Control** | Import guard CI; runtime call requires explicit approval gate |
| **Rollback Trigger** | Any production code calling skillos.level4 |

### R2: Enabled Placeholder Mistaken for Working Warning

| Field | Value |
|:--|:--|
| **Severity** | Medium |
| **Likelihood** | Low |
| **Description** | Future developer assumes enabled path works and merges P1 without gate review |
| **Current Mitigation** | enabled path returns disabled_guard explicit placeholder |
| **Required Post-Merge Control** | P1 requires separate human approval |
| **Rollback Trigger** | Enabled path produces any output before P1 gate approval |

### R3: Future Config Change Enables Warning by Default

| Field | Value |
|:--|:--|
| **Severity** | Critical |
| **Likelihood** | Very Low |
| **Description** | LEVEL4_WARNING_ENABLED default changed from False to True in config |
| **Current Mitigation** | Guard hardening: strict bool True only; getattr default False; test coverage |
| **Required Post-Merge Control** | CI-level default-disabled regression test |
| **Rollback Trigger** | Default value check fails |

### R4: Side-Channel Later Writes Files Without Approval

| Field | Value |
|:--|:--|
| **Severity** | Medium |
| **Likelihood** | Low |
| **Description** | NoopSideChannel replaced with file writer without warning delivery boundary gate |
| **Current Mitigation** | P0 always returns NoopSideChannel |
| **Required Post-Merge Control** | File-based delivery requires warning delivery boundary gate proof |
| **Rollback Trigger** | Any file write from side_channel module |

### R5: result_envelope Mutation Introduced After Merge

| Field | Value |
|:--|:--|
| **Severity** | Critical |
| **Likelihood** | Low |
| **Description** | New P1 code adds result_envelope write |
| **Current Mitigation** | P0 has zero result_envelope references; envelope immutability proof test exists |
| **Required Post-Merge Control** | Envelope immutability CI gate |
| **Rollback Trigger** | Hash mismatch detected |

### R6: Caller-Visible Leakage After Merge

| Field | Value |
|:--|:--|
| **Severity** | Critical |
| **Likelihood** | Low |
| **Description** | Future P1 code writes to stdout/stderr or adds caller-visible output |
| **Current Mitigation** | NoopSideChannel; envelope immutability test; no emission path |
| **Required Post-Merge Control** | Caller visibility boundary CI gate |
| **Rollback Trigger** | Caller-visible warning detected |

### R7: P1 Starts Without Post-Merge Seal

| Field | Value |
|:--|:--|
| **Severity** | Medium |
| **Likelihood** | Low |
| **Description** | P1 work begins before the merge review is sealed |
| **Current Mitigation** | Decision seal requires post-merge seal first |
| **Required Post-Merge Control** | P1 can only start after post-merge seal |
| **Rollback Trigger** | Any P1-related commit before post-merge seal |

### R8: Tests Overfit Skeleton

| Field | Value |
|:--|:--|
| **Severity** | Low |
| **Likelihood** | Medium |
| **Description** | Tests tightly coupled to current skeleton; refactoring breaks them |
| **Current Mitigation** | Tests test behavioral contracts (disabled default, CONTINUE, no side effects) |
| **Required Post-Merge Control** | P1 must not break P0 behavioral contracts |
| **Rollback Trigger** | Test behavioral regression |

### R9: Production/Broker/Real-Trade Coupling Added Later

| Field | Value |
|:--|:--|
| **Severity** | Critical |
| **Likelihood** | Very Low |
| **Description** | Future P1 code adds production imports |
| **Current Mitigation** | No-production proof test; static analysis; import allowlist |
| **Required Post-Merge Control** | CI-level static analysis gate |
| **Rollback Trigger** | Production/broker import detected |

### R10: Level 5 Semantic Drift

| Field | Value |
|:--|:--|
| **Severity** | Medium |
| **Likelihood** | Low |
| **Description** | Future docs/code reference Level 5 planning or enablement |
| **Current Mitigation** | All docs state "Level 5 remains BLOCKED" |
| **Required Post-Merge Control** | CI grep check for Level 5 planning language |
| **Rollback Trigger** | Level 5 drift detected |

### R11: Rollback Path Incomplete After Merge

| Field | Value |
|:--|:--|
| **Severity** | High |
| **Likelihood** | Low |
| **Description** | Disabling Level 4 after merge leaves residual artifacts |
| **Current Mitigation** | P0 creates no files, no side effects; disabling is stateless |
| **Required Post-Merge Control** | P1 must include rollback proof |
| **Rollback Trigger** | Artifacts remain after disable |

### R12: Direct Merge Without Human Approval

| Field | Value |
|:--|:--|
| **Severity** | Critical |
| **Likelihood** | Very Low |
| **Description** | P0 branch merged without human approver completing decision record |
| **Current Mitigation** | This merge review explicitly rejects direct merge |
| **Required Post-Merge Control** | Merge gate closure requires human decision record |
| **Rollback Trigger** | Branch merged without review gate closure |

## Risk Summary

| # | Risk | Severity | Likelihood | Residual |
|:--|:--|:--:|:--:|:--:|
| R1 | Runtime wiring after merge | Critical | Low | Low |
| R2 | Placeholder mistaken for warning | Medium | Low | Low |
| R3 | Config default changed | Critical | Very Low | Very Low |
| R4 | Side-channel file write | Medium | Low | Low |
| R5 | Envelope mutation after merge | Critical | Low | Very Low |
| R6 | Caller-visible leakage | Critical | Low | Low |
| R7 | P1 without seal | Medium | Low | Low |
| R8 | Test overfit | Low | Medium | Low |
| R9 | Production coupling later | Critical | Very Low | Very Low |
| R10 | Level 5 drift | Medium | Low | Low |
| R11 | Rollback incomplete | High | Low | Low |
| R12 | Direct merge without approval | Critical | Very Low | Very Low |
