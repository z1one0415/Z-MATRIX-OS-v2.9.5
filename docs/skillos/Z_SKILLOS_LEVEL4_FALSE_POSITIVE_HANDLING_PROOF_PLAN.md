# Z-SkillOS Level 4 False-Positive Handling Proof Plan

## Status

Z_SKILLOS_LEVEL4_FALSE_POSITIVE_HANDLING_PROOF_PLAN_READY

## Purpose

Define the proof plan for Gate-8: False-Positive Handling. This document is a proof plan only. No proof execution. No code.

## Future Proof Objective

False-positive warnings can be downgraded, suppressed, retracted, and audited. All actions are reversible and do not affect skill execution.

## Warning Lifecycle

```
EMITTED → FLAGGED_FP → DOWNGRADED → SUPPRESSED → RETRACTED
   ↑          ↑             ↑             ↑            ↑
   └──── reinstated ────────┴─ reinstated ─┴─ unretracted
```

| State | Meaning |
|:--|:--|
| EMITTED | Warning emitted to audit file |
| FLAGGED_FP | Human or auto-detected false-positive |
| DOWNGRADED | Severity reduced by one level |
| SUPPRESSED | Same (gate, cat) FP × 3 → auto-suppressed for 90 days |
| RETRACTED | Human-confirmed permanent non-issue |

## Required Future Evidence

| # | Evidence Item | Verification Method |
|:--|:--|:--|
| 1 | Downgrade path works | Manual trigger → verify severity change |
| 2 | Suppression path works | Auto-suppress after FP×3 → verify no re-emission |
| 3 | Retraction path works | Human retract → verify audit marker |
| 4 | Audit trail preserved | Original warning still readable after all state changes |
| 5 | Human review threshold respected | ESCALATE_REVIEW only from human |
| 6 | Suppression is reversible | Un-suppress → verify warning re-emitted |
| 7 | Auto-expire works | 90-day suppression lift → verify normal emission resumes |

## Forbidden

- FP handling blocks execution
- FP handling mutates result_envelope
- Suppression hides hard evidence
- Retraction deletes audit evidence
- Auto-escalation to ESCALATE_REVIEW or BLOCK/FAIL_CLOSED

## Evidence Retention Rule

```
Suppression never deletes evidence.
- Original warning records preserved in audit file
- FP flag history preserved in separate journal
- Suppressed warnings: emit marker instead of full warning
- Audit trail: "suppressed: (source_gate, category) since YYYY-MM-DD, reason: FP×3"
```

## Explicit Statement

This document is a proof plan only. No proof execution. No code.
