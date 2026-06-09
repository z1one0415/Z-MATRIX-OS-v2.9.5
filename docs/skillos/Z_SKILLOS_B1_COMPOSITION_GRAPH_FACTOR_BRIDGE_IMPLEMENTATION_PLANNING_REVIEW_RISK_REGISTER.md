# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — REVIEW RISK REGISTER

## 1. Status

- Phase: REVIEW
- Risk Count: 22 (≥20 required)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Decision: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING

## 2. Scope

Risk register for the review of B1 Composition Graph Factor Bridge Implementation
Planning. B1 consumes A1FactorBridgeResponse ONLY. Denied context cannot become
valid node. Each risk has severity, likelihood, mitigation, control, and rollback trigger.

### 2.1 Risk Register (22 risks)

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|---|---|---|---|---|---|---|
| R-01 | Blocked node type accidentally allowed in implementation | CRITICAL | LOW | Enumeration in constants.py + test_no_forbidden_imports | Code review + CI | Any blocked node instantiated |
| R-02 | Blocked edge type accidentally allowed | CRITICAL | LOW | Enumeration in constants.py + test_edge_builder | Code review + CI | Any blocked edge instantiated |
| R-03 | FactorInvocationResponse consumed directly | CRITICAL | LOW | Type checking at a1_factor_bridge_response_node | Import guard + test | Direct import detected |
| R-04 | DAG cycle introduced | HIGH | MEDIUM | dag_validator with Kahn's algorithm | Pre-processing validation | Cycle detected at runtime |
| R-05 | Real source data enters graph | CRITICAL | LOW | no_real_source_flag enforcement | Evidence chain check | no_real_source_flag = False |
| R-06 | alpha_claim output not filtered | CRITICAL | LOW | blocked_output_filter_edge | Output type whitelist | alpha_claim in output |
| R-07 | position_weight output not filtered | CRITICAL | LOW | blocked_output_filter_edge | Output type whitelist | position_weight in output |
| R-08 | buy/sell signal output not filtered | CRITICAL | LOW | blocked_output_filter_edge | Output type whitelist | buy/sell signal in output |
| R-09 | order_signal output not filtered | CRITICAL | LOW | blocked_output_filter_edge | Output type whitelist | order_signal in output |
| R-10 | c1_handoff_marker lost in propagation | HIGH | MEDIUM | Terminal node assertion | Evidence chain validation | Marker absent at terminal |
| R-11 | Evidence hash chain broken | HIGH | MEDIUM | Hash computation at every node/edge | Chain integrity check | Missing hash field |
| R-12 | Permission escalation in edge direction | HIGH | LOW | Monotonicity enforcement | permission_tier_edge validation | Higher permission downstream |
| R-13 | Kill switch defaults to enabled | CRITICAL | LOW | DISABLED_DEFAULT_NOOP as default | Config validation | Graph processes without enable |
| R-14 | Denied context routed to valid processing | CRITICAL | LOW | Denied node has no valid-processing edges | DAG validator rule V-008 | Denied node reaches summary |
| R-15 | Execution edge introduced | CRITICAL | LOW | Blocked edge enumeration | Import guard + constant check | execution_edge type created |
| R-16 | Autonomous retry edge introduced | HIGH | LOW | Blocked edge enumeration | Import guard + constant check | autonomous_retry_edge created |
| R-17 | Code accidentally created on planning branch | HIGH | LOW | CI check for .py files | Branch protection rule | .py file on planning branch |
| R-18 | Privacy marker not set at doc gen | MEDIUM | LOW | Node contract enforcement | Document review | privacy_marker absent |
| R-19 | Rollback marker not set on DENY decisions | HIGH | MEDIUM | Degradation engine contract | Test coverage | DENY without rollback_marker |
| R-20 | Implementation proceeds without review approval | CRITICAL | LOW | Review gate enforcement | Branch protection | Code merged without approval |
| R-21 | Dependency seal tampered | CRITICAL | VERY LOW | Commit hash verification | Git integrity check | Seal hash mismatch |
| R-22 | Graph exceeds structural limits (nodes/edges/depth) | MEDIUM | LOW | Configurable limits in dag_validator | Pre-construction validation | Limit exceeded |

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- Risk register covers planning review risks only
- Implementation-phase risks will require separate register
- Each risk must have all 5 fields (severity/likelihood/mitigation/control/rollback trigger)
- Risks are ordered by severity then likelihood

## 5. Forbidden Actions

- NO runtime enablement (runtime enablement is not authorized)
- NO risk acceptance without documented justification
- NO waiver of CRITICAL risks
- NO code creation to mitigate planning-phase risks

## 6. Proof / Review Requirements

- All 22 risks must be acknowledged by reviewer
- CRITICAL risks require explicit sign-off
- Mitigation plans must trace to specific planning documents
- Rollback triggers must be testable

## 7. Next Legal Entry

- REVIEW_DECISION_BRIEF: executive summary incorporating risk assessment
- REVIEW_DECISION_RECORD: formal decision

---
