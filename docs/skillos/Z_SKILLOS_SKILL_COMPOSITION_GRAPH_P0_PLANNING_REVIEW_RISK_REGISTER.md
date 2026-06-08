# Z-SkillOS Skill Composition Graph P0 Planning — REVIEW RISK REGISTER

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Review Risk Register Definition

This register catalogues all identified risks associated with the Skill Composition Graph P0 design.
Each risk is assessed for severity, likelihood, and assigned mitigation, control, and rollback measures.
Minimum: 12 risks.

## 2. Risk Matrix

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback |
|---|------|----------|------------|------------|---------|----------|
| RR-01 | Permission escalation not detected at compile time | CRITICAL | LOW | Compile-time tier comparison in edge validation; 10 EC rules cover this | Static analysis of all edge contracts before graph build | Reject graph; increment validation rules |
| RR-02 | Node degradation produces side effects | CRITICAL | LOW | allowed_side_effects must be empty; degradation_result is a static field | Compile-time check of degradation_result schema | Reject node contract; add side-effect audit |
| RR-03 | Hidden execution path in node capability | CRITICAL | MEDIUM | no_hidden_execution = true on all edges; empty side_effects list | Static analysis of capability call graph | Reject graph; capability registry block |
| RR-04 | Cycle introduced via future P1 expansion | HIGH | MEDIUM | P0 max 2 nodes structurally prevents cycles; P1 must re-validate | P1 entry gate requires cycle detection re-run | Rollback to P0 topology; reject P1 plan |
| RR-05 | Evidence hash collision (SHA-256 weakness) | MEDIUM | VERY LOW | SHA-256 is industry standard; collision requires 2^128 operations | Hash verification on graph build | Accept as theoretical only; no action needed |
| RR-06 | result_envelope mutation by future code | HIGH | MEDIUM | Envelope schema is immutable; no mutation API exists | Code review for any envelope access | Reject PR; enforce envelope immutability test |
| RR-07 | P0 topology too restrictive for real use cases | MEDIUM | HIGH | P0 is explicitly minimum viable; P1-P5 expand topology | Review phase includes "is P0 scope appropriate" check | Expand to P1 if review demands it |
| RR-08 | Missing degradation path for edge failure | HIGH | LOW | D1/D2/D3 cover node/graph failures; edge failure triggers D2 | Test all edge failure modes | Add edge-specific degradation (D4) |
| RR-09 | Evidence chain broken by partial graph invalidation | MEDIUM | LOW | D3 specifies upstream hash preserved; graph hash includes both valid and degraded | Test partial invalidation evidence chain | Fix evidence hash aggregation |
| RR-10 | Tool recursion undetected due to indirect capability call | HIGH | LOW | Capability call graph analysis at compile time; registry lookup validation | Exhaustive capability dependency mapping | Reject graph; add indirect call detection |
| RR-11 | Timeout watchdog not implemented (P0 docs-only) | LOW | N/A | P0 is docs-only; timeouts are specified but not enforced | Time bounds documented in FAILURE_DEGRADATION_PLAN.md | N/A until implementation |
| RR-12 | Human reviewer misunderstands docs-only constraint | MEDIUM | MEDIUM | Every doc explicitly states FUTURE_PLAN_ONLY and Level 5 BLOCKED in header | Review checklist RC-38/RC-39 verify this | Clarify in review decision brief |
| RR-13 | Planning docs contain contradictory specifications | MEDIUM | LOW | Cross-reference audit: all 14 docs checked for consistency | Review checklist covers all doc categories | Reconcile contradictions; re-seal planning |
| RR-14 | P0 node count limit (max 2) blocks legitimate 3-node linear plans | LOW | HIGH | P0 is minimum viable; real use cases wait for P1 | Documented as out-of-scope in SCOPE.md §3 | Escalate to P1 if blocking critical path |

## 3. Severity Definitions

| Severity | Definition |
|----------|------------|
| CRITICAL | Violates core safety invariant; could cause unauthorized execution, data leak, or system compromise |
| HIGH | Degrades system integrity or audit capability; may cause incorrect but safe behavior |
| MEDIUM | Reduces effectiveness or usability; no safety impact |
| LOW | Cosmetic, documentation, or theoretical concern |

## 4. Likelihood Definitions

| Likelihood | Definition |
|------------|------------|
| VERY LOW | Requires extraordinary circumstances (e.g., cryptographic breakthrough) |
| LOW | Possible but unlikely given current design and controls |
| MEDIUM | Reasonably foreseeable; requires active mitigation |
| HIGH | Expected to occur without specific mitigation |

## 5. Risk Response Matrix

| Severity / Likelihood | VERY LOW | LOW | MEDIUM | HIGH |
|----------------------|----------|-----|--------|------|
| CRITICAL | Monitor | Active Mitigation | BLOCKING | BLOCKING |
| HIGH | Accept | Monitor | Active Mitigation | BLOCKING |
| MEDIUM | Accept | Accept | Monitor | Active Mitigation |
| LOW | Accept | Accept | Accept | Monitor |

## 6. Residual Risk Assessment

After applying all mitigations:
- No CRITICAL risks remain unmitigated
- No HIGH risks remain without monitoring
- All MEDIUM risks are accepted or monitored
- No risks block the Review phase

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|REVIEW|RISK_REGISTER|v1.0.0-draft`
