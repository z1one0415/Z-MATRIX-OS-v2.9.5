# Z-SkillOS Level 4 Implementation Gate — False-Positive Feedback Loop Spec

## Status

Z_SKILLOS_LEVEL4_IMPL_GATE_FALSE_POSITIVE_LOOP_SPEC_READY

## Purpose

Define the closed-loop mechanism for detecting, recording, downgrading, suppressing, and retracting false-positive warnings. This refines the existing False-Positive Policy with implementation-ready detail.

## Lifecycle States

```
  EMITTED → FLAGGED_FP → DOWNGRADED → SUPPRESSED → RETRACTED
     │          │             │             │            │
     │          │             │             │            │
     └── can be re-emitted ──┴── can be re-instated ────┘
```

| State | Meaning | Action |
|:--|:--|:--|
| EMITTED | Warning emitted normally | Audit file entry exists |
| FLAGGED_FP | Human or auto marks as false-positive | Severity downgraded one level |
| DOWNGRADED | 2nd FP flag confirmed | Severity downgraded again |
| SUPPRESSED | 3rd FP flag (same gate/cat) | Warning suppressed, not emitted |
| RETRACTED | Human confirms permanent non-issue | Prior warnings retracted, audit trail preserved |

## Auto-Suppression Threshold

```
Rule: 3 repeat false-positives for same (source_gate, category) in 30 days
Action: Auto-suppress future warnings for this (source_gate, category)
Duration: 90 days, then auto-expire
Override: Human can un-suppress at any time
```

## FP Detection Methods

| Method | Trigger | Confidence |
|:--|:--|:--:|
| Human review flag | Operator marks warning as FP | High |
| Repeated same-pattern | Same (gate, cat, evidence_ref) 3+ times, no action taken | Medium |
| Cross-reference | Warning contradicts other evidence that passed | Medium |
| Temporal decay | Warning never recurs after 30 days | Low (auto-flag candidate) |

## Evidence Retention

```
Rule: Suppression never deletes evidence
- Original warning records preserved in audit file
- FP flag history preserved in separate journal
- Suppressed warnings: emit marker instead of full warning
- Audit trail: "suppressed: (source_gate, category) since YYYY-MM-DD, reason: FP×3"
```

## Test Specification

```
test_level4_false_positive_loop:
  setup:
    - LEVEL4_WARNING_ENABLED=true
    - Clean FP state

  tests:
    1. Single FP flag → severity downgraded, warning still emitted
    2. 2nd FP flag → severity downgraded again
    3. 3rd FP flag (30d window) → auto-suppressed, marker emitted instead
    4. Suppressed warning not emitted on next trigger
    5. Human un-suppress → warning emitted normally again
    6. 90-day auto-expire → suppression lifted
    7. Evidence preserved after suppression
    8. Cross-reference FP detection triggers
    9. Temporal decay auto-flag (30d no recurrence)
    10. RETRACTED state preserves full audit trail

  assert for all:
    - No envelope mutation
    - No blocking
    - All state changes recorded in audit journal
```

## Constraints

- Evidence never deleted (suppression = emission suppression only)
- Human override always available
- Auto-suppression is reversible
- FP journal is append-only
- FP state survives restarts
- Maximum suppression duration: 90 days (auto-expire)
