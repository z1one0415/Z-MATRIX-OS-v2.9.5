# Z-SkillOS v1.2 Planning Gate

## Status

Z_SKILLOS_V1_2_PLANNING_GATE_READY

## Current Baseline

- v1.1 post-merge sealed
- seal_commit: `d0ab227`
- merge_commit: `9fcc031`
- target_branch: `postmerge/skillos-v0-baseline-freeze`
- current maximum: Level 2 CI audit integration
- Level 3 shadow runtime observation: BLOCKED
- Level 4 soft warning: BLOCKED
- Level 5 fail-closed enforcement: BLOCKED

## v1.1 Capability Chain

CI audit wrapper → semantic drift audit → drift CI integration → golden coverage 24/18 → staged enforcement proposal

## v1.2 Planning Objective

Evaluate whether Z-SkillOS can prepare for Level 3 shadow runtime observation in a future implementation branch. This gate does NOT approve implementation.

## Candidate Tracks

1. Level 3 Shadow Runtime Observation Readiness
2. Runtime Isolation Design
3. Rollback and Kill-Switch Policy
4. Human Approval and Governance Policy
5. Expanded Golden Coverage Strategy
6. CI Stability Evidence Review
7. Runtime Telemetry Boundary Design

## Default Recommendation

v1.2 should prioritize:

1. Runtime Isolation Design
2. Rollback and Kill-Switch Policy
3. Level 3 Readiness Matrix
4. Human Approval Policy

v1.2 should not immediately implement Level 3.

## Explicit Non-Scope

- no implementation
- no invoke_skill modification
- no result_envelope modification
- no runtime observation hook
- no runtime warning path
- no runtime blocking
- no soft warning
- no fail-closed behavior
- no runtime_reports write
- no production / broker / real_trade
- no V12.x advancement
- no tag

## Decision

PENDING

## Next If GO

Start v1.2-A planning-approved design/spec branch.

## Next If NO-GO

Remain at `Z_SKILLOS_V1_1_POST_MERGE_SEALED`.
