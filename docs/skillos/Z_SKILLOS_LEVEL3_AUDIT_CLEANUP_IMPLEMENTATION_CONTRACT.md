# Z-SkillOS Level 3 Audit Cleanup Implementation Contract

## Status

Z_SKILLOS_LEVEL3_AUDIT_CLEANUP_IMPLEMENTATION_CONTRACT_READY

## Allowed Path

`runtime_audit/skillos_level3_shadow/`

## Forbidden Paths

runtime_reports, production, broker_runtime, real_trade, data, docs, zmatrix, scripts, tests, root, parent directories.

## Required Commands

`cleanup_level3_audit_retention.py --dry-run` and `--apply`.

## Behavior

Dry-run: lists, deletes nothing, no runtime_reports, no forbidden paths. Apply: scoped audit only, refuses symlink escape/parent traversal/absolute unsafe, deterministic summary.

## Required Tests

Dry-run deletes nothing. Apply scoped. Forbidden/symlink/parent/traversal refused. Max bytes/files/days enforced. No runtime_reports/production/broker/real_trade.

## Final

Cleanup implementation requires separate branch.
