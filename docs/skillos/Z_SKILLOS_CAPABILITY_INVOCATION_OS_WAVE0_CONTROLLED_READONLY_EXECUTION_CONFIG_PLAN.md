# Wave0 Controlled Read-Only Execution Config Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_CONFIG_PLAN_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED

## Config Architecture
FUTURE_PLAN_ONLY. The config plan defines strict requested/enabled separation for controlled execution.

## Requested Flags (record intent, never enable)
| Flag | Type | Default | Description |
|:--|:--|:--|:--|
| `wave0_controlled_execution_requested` | strict bool | False | Master controlled execution request |
| `wave0_github_readonly_controlled_requested` | strict bool | False | GitHub adapter controlled request |
| `wave0_document_generation_controlled_requested` | strict bool | False | Doc gen adapter controlled request |
| `wave0_local_docs_inspection_controlled_requested` | strict bool | False | Local docs adapter controlled request |
| `wave0_report_reading_controlled_requested` | strict bool | False | Report reading adapter controlled request |

## Enabled Functions (always return False in planning phase)
- `is_wave0_controlled_execution_enabled(config) -> False`
- `is_github_readonly_controlled_enabled(config) -> False`
- `is_document_generation_controlled_enabled(config) -> False`
- `is_local_docs_inspection_controlled_enabled(config) -> False`
- `is_report_reading_controlled_enabled(config) -> False`

## Config Strictness Rules
- **Strict bool only**: only `True` (the bool) accepted as requested
- **Non-bool truthy disabled**: string "true", int 1, "True" all rejected
- **Env cannot enable**: no `os.environ` bypass path
- **Parse error = disabled**: malformed JSON/config → all disabled
- **Missing config = disabled**: absent keys → default False
- **No default true**: every field starts disabled

## Evidence
Dependency: WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4). P0 config already implements strict requested/enabled separation.

## Boundary
No runtime enablement. No adapter execution enablement. No capability execution. Level 5 remains BLOCKED.

## Next
Config plan → kill switch plan → permission plan → implementation gate

> Cap OS Wave0 | Controlled Exec Planning | Config Plan | FUTURE_PLAN_ONLY | Level 5 BLOCKED