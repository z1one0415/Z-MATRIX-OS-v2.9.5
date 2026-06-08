# Wave0 Controlled Read-Only Execution P1 Canary Config Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_P1_CANARY_CONFIG_PLAN_READY
Branch: plan/...p1-canary-planning @ 2c0d7ae | Level 5: BLOCKED

## Config Architecture
FUTURE_PLAN_ONLY. Requested/enabled separation for P1 canary enablement.

### Requested Flags (record intent, never enable)
| Flag | Type | Default | Description |
|:--|:--|:--:|:--|
| `p1_canary_requested` | strict bool | False | Master P1 canary request |
| `p1_synthetic_requested` | strict bool | False | Synthetic input canary request |
| `p1_provided_requested` | strict bool | False | Provided input canary request |
| `p1_sandbox_requested` | strict bool | False | Sandbox canary request |

### Enabled Functions (always return False in planning phase)
- `is_p1_canary_enabled(config) -> False`
- `is_p1_synthetic_canary_enabled(config) -> False`
- `is_p1_provided_canary_enabled(config) -> False`
- `is_p1_sandbox_canary_enabled(config) -> False`

### Config Strictness Rules
- Strict bool True only (only `True` accepted)
- Non-bool truthy disabled (string "true", int 1 rejected)
- Env cannot enable (no os.environ bypass)
- Parse error = disabled (malformed JSON → all disabled)
- Missing config = disabled (absent keys → default False)
- No default true (every field starts disabled)
- Human seal required before any enabled → True

## Dependency
WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED (b3ccd3f). P0 config already implements strict separation.

## Boundary
No implementation. No code change. No runtime enablement. Level 5 BLOCKED.

## Next
Config plan → kill switch plan → permission plan

> Cap OS Wave0 | Controlled Exec P1 Canary | Config Plan | FUTURE_PLAN_ONLY | Level 5 BLOCKED