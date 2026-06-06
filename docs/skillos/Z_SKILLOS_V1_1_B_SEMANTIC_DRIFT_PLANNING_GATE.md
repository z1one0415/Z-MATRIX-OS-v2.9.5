# Z-SkillOS v1.1-B Semantic Drift Planning Gate

## Status

Z_SKILLOS_V1_1_B_SEMANTIC_DRIFT_PLANNING_GATE_READY

## Current Baseline

- v1.1-A CI audit integration: COMPLETE (`b84acd5`)
- v1.0 post-merge sealed
- Level 2 enforcement ladder: reached
- Level 3-5: BLOCKED

## Planning Objective

Define drift detection scope, thresholds, output format, and false-positive handling before any implementation.

## Drift Monitoring Targets

| # | Target | Description |
|:--:|------|------|
| 1 | Contract registry drift | New/removed/changed contract entries vs baseline |
| 2 | Schema drift | input_schema / output_schema changes in contracts |
| 3 | Hash policy drift | canonical_json policy, excluded fields, algorithm changes |
| 4 | Golden case drift | expected hash mismatch in golden/regression cases |
| 5 | Regression coverage drift | Added/dropped cases, domain coverage loss |

## Drift Severity Levels

| Level | Name | CI Action | Runtime Action |
|:--:|------|------|------|
| INFO | Informational | Log only | None |
| WARN | Warning | CI warning (non-blocking) | None |
| FAIL_CI | CI failure | CI gate fails | None (never runtime) |
| FAIL_CLOSED | Runtime fail | (forbidden in v1.1) | (forbidden in v1.1) |

## Output Format

- stdout only
- Markdown table or structured JSON lines
- No runtime_reports
- No file writes
- No blocking of existing invoke_skill paths

## False-Positive Handling

- Drift auditor must compare against frozen baseline snapshots
- Snapshot update requires explicit approval gate
- No automatic baseline overwrite

## Decision

PENDING

- [ ] GO: allow v1.1-B standalone drift auditor implementation
- [ ] NO-GO: remain at v1.1-A

## Explicit Non-Scope

- no implementation
- no runtime integration
- no hard enforcement
- no invoke_skill modification
- no result_envelope modification
- no production / broker / real_trade
