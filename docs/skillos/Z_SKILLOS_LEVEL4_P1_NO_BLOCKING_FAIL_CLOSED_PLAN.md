# Z-SkillOS Level 4 P1 No-Blocking / Fail-Closed Plan

## Status

Z_SKILLOS_LEVEL4_P1_NO_BLOCKING_FAIL_CLOSED_PLAN_READY

## Scope

FUTURE_PLAN_ONLY. Defines CONTINUE safety for all Level 4 failure paths. No code.

## CONTINUE Rules

| # | Failure Scenario | Must Return |
|:--|:--|:--:|
| 1 | Config missing/unreadable/malformed | CONTINUE |
| 2 | Unknown warning category | CONTINUE |
| 3 | Malformed evidence data | CONTINUE |
| 4 | Severity mapping error | CONTINUE |
| 5 | Audit sink write failure | CONTINUE |
| 6 | Operator report generation failure | CONTINUE |
| 7 | Level 4 processing timeout (500ms) | CONTINUE |
| 8 | False-positive suppression triggered | CONTINUE |
| 9 | Kill-switch engaged mid-cycle | CONTINUE |
| 10 | Any unhandled exception | CONTINUE |

## Forbidden

| Behavior | Rationale |
|:--|:--|
| `BLOCKED` action | Safety boundary |
| `FAIL_CLOSED` action | Level 5 territory |
| `HARD_STOP` action | Not scoped |
| Exception to caller | Visibility boundary |
| `raise` in Level 4 code (uncaught) | Blocking risk |
| `sys.exit` / `os._exit` | Process termination |
| Result change on failure | Immutability boundary |

## P0 Evidence

* 18 no-blocking test cases passing
* All Level 4 code wrapped in try/except → CONTINUE
* Action field enforced to always be CONTINUE in models

## Design Principle

```
try:
    Level 4 evaluation + side-channel emission
except Exception:
    return CONTINUE  # never raise, never block
```

## No implementation. No warning enablement.Level 5 remains BLOCKED.
