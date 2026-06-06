# Z-SkillOS v1.1-B Semantic Drift Decision Matrix

## Status

Z_SKILLOS_V1_1_B_SEMANTIC_DRIFT_DECISION_MATRIX_READY

---

## Drift Target Assessment

| Target | Detectable | Baseline Exists | CI Value | Risk | Priority |
|:--|:--:|:--:|:--:|:--:|:--:|
| Contract registry drift | Yes | contract_registry.json | High | Low | 1 |
| Schema drift | Yes | contract_registry.json | High | Low | 1 |
| Hash policy drift | Yes | skill_hash_policy.py | High | Low | 2 |
| Golden case drift | Yes | golden_cases.json | High | Medium | 2 |
| Regression coverage drift | Yes | regression_cases.json | Medium | Low | 3 |

---

## Implementation Staging

### v1.1-B Standalone Drift Auditor

```
Scope:
- Read current contract_registry.json
- Compare against frozen baseline snapshot
- Read current hash policy
- Compare against frozen baseline snapshot
- Re-run golden and regression hash audits
- Report drift to stdout
- No file writes
- No blocking
```

### v1.1-B.x CI Integration (after standalone verified)

```
Scope:
- Add drift audit to v1.1-A CI wrapper
- Drift FAIL_CI blocks CI gate
- Drift WARN/INFO passes CI gate
```

### Explicit Rejection

```
- No runtime drift detection
- No invoke_skill hook
- No baseline auto-update
- No production path
```

---

## Conditions Required Before GO

1. Planning gate approved by human
2. Baseline snapshots exist (submitted with implementation)
3. Drift auditor test cases defined
4. CI integration path planned (not implemented)

## Recommended Next

```
v1.1-B standalone semantic drift auditor
→ v1.1-B.x CI integration
→ then v1.1-C Golden Coverage Expansion
```

NOT hard enforcement.
