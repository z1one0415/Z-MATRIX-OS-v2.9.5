# Z-SkillOS v1.2 Scope Decision Matrix

## Status

Z_SKILLOS_V1_2_SCOPE_DECISION_MATRIX_READY

## Candidate Track Evaluation

| Track | Goal | Value | Risk | Recommendation |
|:--|------|:--:|:--:|:--|
| A | Level 3 readiness matrix | High | Low | PRIORITY_1 |
| B | Runtime isolation design | Very High | Medium | PRIORITY_2 |
| C | Rollback / kill-switch policy | Very High | Medium | PRIORITY_3 |
| D | Human approval policy | High | Low | PRIORITY_4 |
| E | Expanded golden coverage 24→40 | Medium | Low | OPTIONAL |
| F | Actual Level 3 runtime observation | High | High | DEFER |
| G | Level 4 soft warning | Medium | Very High | REJECT |
| H | Level 5 fail-closed | High | Extreme | REJECT |

## Recommended v1.2 Order

```
1. v1.2-A Level 3 Readiness Formalization
2. v1.2-B Runtime Isolation Spec
3. v1.2-C Rollback / Kill-Switch Spec
4. v1.2-D Human Approval Policy
5. optional: v1.2-E Golden Coverage 24→40 Planning Gate
```

## Explicit Rejection

- v1.2 must not start with Level 3 implementation
- v1.2 must not modify invoke_skill
- v1.2 must not modify result_envelope
- v1.2 must not create runtime warning path
- v1.2 must not implement fail-closed
- v1.2 must not touch production / broker / real_trade

## Final Recommendation

Use v1.2 to prepare Level 3 safely. Do not implement Level 3 inside v1.2 planning gate.
