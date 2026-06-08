# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — TEST AND PROOF PLAN

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_TEST_AND_PROOF_PLAN_READY

## Scope
This document defines the test methodology, verification vectors, and correctness proofs. All tests are planning-level specifications, not implementation code.

## Evidence
Test evidence is captured as verification vectors — known inputs with expected outputs.

### Verification Categories
| Category | Count | Description |
|----------|-------|-------------|
| Hash Chain Integrity | 8 vectors | Chain construction, link ordering, tamper detection, seal verification |
| Gate Model Correctness | 6 vectors | Tier assignment, source classification, tier cap enforcement |
| Privacy Boundary | 5 vectors | Cross-invocation isolation, memory zero-fill, key uniqueness |
| Rollback Correctness | 7 vectors | All 7 state transitions, denial of DELIVERED rollback |
| Evidence Schema | 4 vectors | Field validation, size bounds, serialization determinism |
| Audit Sink | 4 vectors | CRUD operations, TTL expiry, LRU eviction, capacity bound |
| Input Validation | 5 vectors | Valid inputs, binary rejection, oversized rejection, code rejection |
| Output Contract | 3 vectors | Bundle structure, tamper_seal coverage, canonical serialization |

### Hash Chain Integrity Vectors (Example)
```
Vector 1: Single-link chain — chain_root computed correctly, verification passes
Vector 2: Multi-link chain (3 links) — chain_root matches known value
Vector 3: Reordered chain — verification FAILS
Vector 4: Modified link — verification FAILS
Vector 5: Forged seal — verification FAILS
Vector 6: Missing link — verification FAILS
Vector 7: Duplicate link — verification FAILS
Vector 8: Empty chain — chain_root == null_anchor, verification passes
```

### Formal Property Assertions
1. Determinism: build_chain(events) always produces the same output for the same input
2. Immutability: verify_chain(chain) returns false if any link was modified
3. Ordering: verify_chain(chain) returns false if links are reordered
4. Completeness: verify_chain(chain) returns false if links are missing
5. Privacy: No data from invocation A appears in evidence for invocation B
6. Boundedness: All data structures respect declared size/capacity bounds
7. Termination: Rollback always terminates and leaves sandbox in IDLE state

## Boundary
- Tests are specified, not implemented
- Test vectors are planning artifacts, not executable code
- No test framework is prescribed
- Verification vectors are illustrative, not exhaustive

## Forbidden
1. Implementing tests at planning phase
2. Requiring specific test frameworks or languages
3. Including test code in planning documents
4. Claiming test coverage without specifying vectors
5. Assuming implementation details not in scope

## Proof
- 42 verification vectors across 8 categories
- 7 formal property assertions
- All property assertions are falsifiable
- Test vectors cover all 7 sections of the evidence system
- Coverage includes happy path, edge cases, and attack scenarios

## Next
- Align test vectors with FORBIDDEN_ACTIONS_MATRIX
- Proceed to FORBIDDEN_ACTIONS_MATRIX
