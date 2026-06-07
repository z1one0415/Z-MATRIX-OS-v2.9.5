# Z-SkillOS Capability Invocation OS Planning Merge Risk Register

## Status

Z_SKILLOS_CAPABILITY_INVOCATION_OS_PLANNING_MERGE_RISK_REGISTER_READY

### R1: Docs Confounded with Implementation | S: Critical | L: Medium
Mitigation: All docs "FUTURE_PLAN_ONLY" | Control: Implementation gate | Rollback: Code without gate

### R2: Adapter Roadmap Misinterpreted | S: Critical | L: Medium
Mitigation: Roadmap "Planning only" | Control: Adapter gate per wave | Rollback: Adapter code without gate

### R3: T5 Unblocked | S: Critical | L: Very Low
Mitigation: T5 "NEVER GRANTED" | Control: Tier model CI | Rollback: T5 invocation

### R4: Evidence Deletion | S: Critical | L: Low
Mitigation: "No evidence deletion" rule | Control: Evidence immutability CI | Rollback: Evidence mutation

### R5: Unsafe Composition | S: Critical | L: Low
Mitigation: Forbidden composition rules | Control: Composition CI gate | Rollback: Unsafe chain

### R6: Router Becomes Runtime | S: Critical | L: Low
Mitigation: "FUTURE_PLAN_ONLY" | Control: Router runtime gate | Rollback: Router code

### R7: GitHub External Write | S: High | L: Low
Mitigation: T2 risk tier, permission required | Control: Write permission gate | Rollback: Unauthorized write

### R8: Z8 Real-Trade | S: Critical | L: Very Low
Mitigation: "advisory-only, forbidden: broker/trade" | Control: Z8 CI gate | Rollback: Broker detected

### R9: Post-Merge Seal Skipped | S: Medium | L: Low
Mitigation: Checklist requires seal | Control: Merge gate closure requires seal | Rollback: Merge without seal

### R10: Level 5 Drift | S: Medium | L: Low
Mitigation: "Level 5 remains BLOCKED" | Control: CI grep check | Rollback: Level 5 language
