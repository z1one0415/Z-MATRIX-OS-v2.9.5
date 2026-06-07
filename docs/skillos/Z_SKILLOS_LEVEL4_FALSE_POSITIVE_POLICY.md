# Z-SkillOS Level 4 False Positive Policy

## Status

Z_SKILLOS_LEVEL4_FALSE_POSITIVE_POLICY_READY

## Definition

A warning candidate signaling risk later judged harmless, expected, or non-actionable.

## Handling

Record, downgrade, suppress, retract. Preserve evidence. Human review for repeated FPs. Rollback threshold.

## Required Tests

Downgrade possible. No result mutation. No blocking. No broker/real_trade. Suppression doesn't hide hard evidence. Rollback removes warning.

## Constraints

Advisory only. Reversible. No result change. No trade/broker action. No fail-closed escalation.
