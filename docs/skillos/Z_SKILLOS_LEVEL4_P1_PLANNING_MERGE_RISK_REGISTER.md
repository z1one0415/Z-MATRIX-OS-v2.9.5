# Z-SkillOS Level 4 P1 Planning Merge Risk Register

## Status

Z_SKILLOS_LEVEL4_P1_PLANNING_MERGE_RISK_REGISTER_READY

### R1: Docs-Only Merge Interpreted as Implementation Auth

| **S**: Critical | **L**: Medium | **Mitigation**: All docs state "no implementation" |
|:--|:--|:--|
| **Future control** | Separate implementation gate required |
| **Rollback** | Implementation code committed without approval |

### R2: P1 Implementation Starts After Merge Without Approval

| **S**: Critical | **L**: Low | **Mitigation**: Merge review decision explicitly forbids P1 implementation |
|:--|:--|:--|
| **Future control** | P1 implementation requires separate review gate |
| **Rollback** | P1 code committed before gate |

### R3: Warning Enablement Inferred From Planning Docs

| **S**: Critical | **L**: Low | **Mitigation**: All docs: "no warning enablement" |
|:--|:--|:--|
| **Future control** | Enablement requires explicit human approval |
| **Rollback** | LEVEL4_WARNING_ENABLED=true without approval |

### R4: Side-Channel Plan Becomes Runtime Code

| **S**: Medium | **L**: Low | **Mitigation**: All plans: "FUTURE_PLAN_ONLY" |
|:--|:--|:--|
| **Future control** | Side-channel implementation needs delivery boundary gate |
| **Rollback** | file I/O code committed |

### R5: Operator Report Becomes Caller-Visible

| **S**: Critical | **L**: Low | **Mitigation**: Contract: "never appears in caller response" |
|:--|:--|:--|
| **Future control** | Visibility boundary CI gate |
| **Rollback** | Caller-visible warning detected |

### R6: Envelope Mutation in Future Implementation

| **S**: Critical | **L**: Very Low | **Mitigation**: Immutability plan: 12 rules |
|:--|:--|:--|
| **Future control** | Envelope immutability CI gate |
| **Rollback** | Hash mismatch |

### R7: Blocking/Fail-Closed Leaks Into Design

| **S**: Critical | **L**: Very Low | **Mitigation**: No-blocking plan: 10 scenarios all CONTINUE |
|:--|:--|:--|
| **Future control** | No-blocking CI gate |
| **Rollback** | BLOCKED/FAIL_CLOSED action |

### R8: Production/Broker/Real-Trade Coupling

| **S**: Critical | **L**: Very Low | **Mitigation**: All docs forbid production paths |
|:--|:--|:--|
| **Future control** | No-production CI gate; import allowlist |
| **Rollback** | Production import detected |

### R9: Post-Merge Seal Skipped

| **S**: Medium | **L**: Low | **Mitigation**: Merge checklist requires post-merge seal |
|:--|:--|:--|
| **Future control** | Merge gate closure requires seal |
| **Rollback** | Merge without seal |

### R10: Level 5 Semantic Drift

| **S**: Medium | **L**: Low | **Mitigation**: All docs: "Level 5 remains BLOCKED" |
|:--|:--|:--|
| **Future control** | CI grep check |
| **Rollback** | Level 5 planning language |
