# Z-SkillOS Level 3 invoke_skill Integration Decision Matrix

## Status

Z_SKILLOS_LEVEL3_INVOKE_SKILL_INTEGRATION_DECISION_MATRIX_READY

## Decision Matrix

| Option | Risk | Recommendation |
|:--|:--:|:--:|
| NO_GO_REMAIN_AT_ADAPTER_PREP | Low | Acceptable |
| GO_FOR_MORE_ADAPTER_TESTING | Low | Acceptable |
| GO_FOR_MINIMAL_WRAPPER_INTEGRATION | Medium | **Recommended** |
| DIRECT_RESULT_ENVELOPE_MUTATION | Very High | REJECTED |
| RUNTIME_WARNING_PATH | Very High | REJECTED |
| RUNTIME_BLOCKING_PATH | Extreme | REJECTED |
| FAIL_CLOSED | Extreme | REJECTED |

## Why Minimal Wrapper Only

The only acceptable next move is a minimal, disabled-by-default wrapper that calls the existing adapter without changing observable runtime behavior.

## Final

No warning/blocking/mutation/fail-closed.
