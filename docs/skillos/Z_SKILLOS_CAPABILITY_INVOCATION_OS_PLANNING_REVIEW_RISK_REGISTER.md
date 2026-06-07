# Z-SkillOS Capability Invocation OS Planning Review Risk Register

## Status

Z_SKILLOS_CAPABILITY_INVOCATION_OS_PLANNING_REVIEW_RISK_REGISTER_READY

### R1: Planning Confounded with Implementation Approval
S: Critical | L: Medium | Mitigation: All docs state "FUTURE_PLAN_ONLY"
Future control: Separate implementation gate | Rollback: Code committed without gate

### R2: Adapter Roadmap Misinterpreted as Adapter Approval
S: Critical | L: Medium | Mitigation: Roadmap states "Planning, no implementation"
Future control: Separate adapter gate per wave | Rollback: Adapter code without gate

### R3: Registry Becomes Executable Without Gate
S: Medium | L: Low | Mitigation: Registry schema only; no code
Future control: Registry implementation requires separate gate | Rollback: Executable registry

### R4: Router Design Becomes Runtime Router Without Approval
S: Critical | L: Low | Mitigation: "FUTURE_PLAN_ONLY" in router design
Future control: Router runtime requires separate gate | Rollback: Runtime router code

### R5: Composition Enables Unsafe Skill Chaining
S: Critical | L: Low | Mitigation: Forbidden composition rules defined
Future control: Composition CI gate | Rollback: Unsafe chain detected

### R6: Permission Tier T5 Accidentally Unblocked
S: Critical | L: Very Low | Mitigation: T5 explicitly "NEVER GRANTED"
Future control: Tier model CI check | Rollback: T5 invocation attempted

### R7: Evidence Bus Permits Deletion or Mutation
S: Critical | L: Low | Mitigation: "No evidence deletion" rule
Future control: Evidence immutability CI gate | Rollback: Evidence mutation detected

### R8: Guard Design Skips Preflight Check
S: Critical | L: Very Low | Mitigation: 10-stage guard pipeline all mandatory
Future control: Guard CI regression | Rollback: Skipped stage detected

### R9: Adapter Touches Production/Broker/Real-Trade
S: Critical | L: Very Low | Mitigation: All adapters: "production permanently excluded"
Future control: No-production CI gate | Rollback: Production import detected

### R10: Scenario Tests Overtrusted as Runtime Proof
S: Medium | L: Medium | Mitigation: Tests are design docs only
Future control: Runtime tests require separate gate | Rollback: Untested behavior

### R11: GitHub Adapter Writes Without Approval
S: High | L: Low | Mitigation: Risk tier T2, permission required
Future control: Write requires explicit permission | Rollback: Unauthorized write

### R12: Z8 Crosses Into Real-Trade
S: Critical | L: Very Low | Mitigation: Z8 "advisory-only, forbidden: broker/trade"
Future control: Z8 CI gate | Rollback: Broker/real_trade detected

### R13: Warning Enablement Inferred From SkillOS Lineage
S: Medium | L: Low | Mitigation: "No warning enablement" in all docs
Future control: Warning enablement requires explicit gate | Rollback: Warning enabled

### R14: Level 5 Semantic Drift
S: Medium | L: Low | Mitigation: "Level 5 remains BLOCKED" in all docs
Future control: CI grep check | Rollback: Level 5 planning language
