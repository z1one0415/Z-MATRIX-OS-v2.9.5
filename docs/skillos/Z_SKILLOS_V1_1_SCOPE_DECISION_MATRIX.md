# Z-SkillOS v1.1 Scope Decision Matrix

## Status

Z_SKILLOS_V1_1_SCOPE_DECISION_MATRIX_READY

---

## Track A: CI Audit Integration

| Aspect | Assessment |
|:--|:--|
| Goal | Wire v1.0 audit scripts into CI / verify chain |
| Value | Highest — makes v1.0 continuously verifiable |
| Allowed Work | verify script wrapper, CI-safe audit command, no runtime integration |
| Risk | Low |
| Recommendation | **PRIORITY_1** |

---

## Track B: Semantic Drift Audit

| Aspect | Assessment |
|:--|:--|
| Goal | Detect output schema / golden cases / narrative-excluded field / registry contract drift |
| Value | High — v1.0 has hash/golden baseline, v1.1 should detect drift |
| Risk | Medium |
| Recommendation | **PRIORITY_2** |

---

## Track C: Golden Coverage Expansion

| Aspect | Assessment |
|:--|:--|
| Goal | Expand golden regression from 12 to more registry-exact skills |
| Value | Medium-High — better coverage but marginal return below CI and drift |
| Risk | Low |
| Recommendation | **PRIORITY_3** |

---

## Track D: Staged Enforcement Proposal

| Aspect | Assessment |
|:--|:--|
| Goal | Design future enforcement stage model |
| Value | Medium — plan now, implement later |
| Risk | High if implemented prematurely |
| Recommendation | **PLANNING_ONLY** |

---

## Track E: Runtime Integration Readiness

| Aspect | Assessment |
|:--|:--|
| Goal | Assess readiness for invoke_skill / result_envelope integration |
| Value | Future-important, not now |
| Risk | Very high |
| Recommendation | **DEFER** |

---

## Recommended v1.1 Order

```
1. v1.1-A CI Audit Integration
2. v1.1-B Semantic Drift Audit
3. v1.1-C Golden Coverage Expansion
4. v1.1-D Staged Enforcement Proposal
5. Runtime Integration deferred to later version
```

## Explicit Rejection

- v1.1 must not start with hard enforcement
- v1.1 must not modify invoke_skill
- v1.1 must not modify result_envelope
