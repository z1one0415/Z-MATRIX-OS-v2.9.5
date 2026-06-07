# Z-SkillOS Level 4 Implementation Gate — Severity Escalation Flow Spec

## Status

Z_SKILLOS_LEVEL4_IMPL_GATE_SEVERITY_ESCALATION_SPEC_READY

## Purpose

Define the deterministic rules for how warning severity escalates from INFO through ESCALATE_REVIEW, and how downgrades work. This refines the existing Severity Calibration Policy with implementation-ready detail.

## Severity Levels

| Level | Name | Auto-Trigger | Human-Trigger | Action |
|:--:|:--|:--:|:--:|:--|
| 0 | INFO | Yes | Yes | Record to audit file only |
| 1 | NOTICE | Yes (threshold) | Yes | Record + include in summary |
| 2 | WARN | Yes (threshold) | Yes | Record + flag in operator report |
| 3 | ESCALATE_REVIEW | No | Yes (only) | Record + highlight + recommend review |

## Auto-Escalation Rules

### INFO → NOTICE

```
Condition: Same (source_gate, category) observed ≥ 3 times in 24 hours
Action: Auto-set severity = NOTICE
Reset: Counter resets after 24h quiet period
```

### NOTICE → WARN

```
Condition: Same (source_gate, category) observed ≥ 10 times in 7 days
         OR any single observation with severity_confidence ≥ 0.9
Action: Auto-set severity = WARN
Reset: Counter resets after 7-day quiet period
```

### WARN → ESCALATE_REVIEW

```
Condition: NEVER auto-escalated
Action: Requires explicit human approval
Rationale: ESCALATE_REVIEW = human decision boundary
```

## Auto-Downgrade Rules

### False-Positive Downgrade

```
Condition: Warning flagged as false-positive ≥ 2 times
Action: Downgrade one level (WARN→NOTICE, NOTICE→INFO, INFO→suppressed)
```

### Time-Based Decay

```
Condition: No new occurrence for (source_gate, category) for 14 days
Action: Downgrade one level
Minimum: INFO (never fully deleted)
```

### Human Override

```
Condition: Human explicitly sets severity
Action: Override auto-escalation; auto-downgrade still applies
Lock: Human-set severity persists for 7 days before auto-rules resume
```

## State Machine

```
  ┌──────┐  3x/24h  ┌────────┐  10x/7d  ┌──────┐  human   ┌──────────────────┐
  │ INFO │─────────→│ NOTICE │─────────→│ WARN │─────────→│ ESCALATE_REVIEW  │
  └──────┘          └────────┘          └──────┘          └──────────────────┘
      ↑                 ↑                  ↑                     │
      │                 │                  │                     │
      │    FP×2 or      │    FP×2 or       │    FP×2 or          │ human downgrade
      │    14d quiet    │    14d quiet     │    14d quiet        │
      └─────────────────┴──────────────────┴─────────────────────┘
```

## Test Specification

```
test_level4_severity_escalation_flow:
  setup:
    - LEVEL4_WARNING_ENABLED=true
    - Clean warning state

  tests:
    1. Single INFO → stays INFO
    2. 3 INFOs in 24h (same gate/cat) → NOTICE
    3. 10 NOTICEs in 7d → WARN
    4. WARN never auto-escalates to ESCALATE_REVIEW
    5. 2 FP flags on WARN → downgrade to NOTICE
    6. 14d quiet on NOTICE → downgrade to INFO
    7. Human-set severity overrides auto rules
    8. Human-set severity lock expires after 7d
    9. Counter reset after quiet period
    10. Max severity never exceeds ESCALATE_REVIEW

  forbidden:
    - BLOCK severity
    - FAIL_CLOSED severity
    - HARD_STOP severity
    - Auto-escalation to ESCALATE_REVIEW
```

## Constraints

- ESCALATE_REVIEW is always human-triggered only
- BLOCK / FAIL_CLOSED / HARD_STOP never appear
- All severity changes are reversible
- Downgrade history preserved
- Counter state persisted across restarts
