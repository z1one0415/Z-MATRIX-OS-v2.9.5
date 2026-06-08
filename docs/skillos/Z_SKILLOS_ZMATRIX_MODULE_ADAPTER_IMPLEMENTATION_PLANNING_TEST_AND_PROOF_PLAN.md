# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — TEST_AND_PROOF_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Test Philosophy

Every Z-MATRIX Module Adapter must be accompanied by a comprehensive test
suite before any code is considered complete. Tests are NOT optional — they
are the primary evidence that adapters behave correctly, safely, and
deterministically. Minimum 18 proof categories are required.

---

## §2 — Proof Matrix (≥18 Proofs)

| # | Proof ID | Category | Description |
|---|----------|----------|-------------|
| P01 | DISABLED_DEFAULT | Safety | All adapters start DISABLED — no invocation possible |
| P02 | CONTRACT_PRESENT | Safety | Every adapter has a valid, complete contract |
| P03 | CONTRACT_IMMUTABLE | Safety | Contract cannot be mutated after registration |
| P04 | PERMISSION_DENY | Safety | Adapter rejects invocation when permissions missing |
| P05 | FORBIDDEN_BLOCK | Safety | Adapter blocks forbidden action attempts |
| P06 | READONLY_ENFORCE | Safety | Read-only adapters (A1-A4) reject all writes |
| P07 | MEMORY_ONLY_WRITE | Safety | A5 writes only to memory, never disk/network |
| P08 | SCHEMA_INPUT_VALID | Correctness | Valid input passes schema validation |
| P09 | SCHEMA_INPUT_INVALID | Correctness | Invalid input is rejected with evidence |
| P10 | SCHEMA_OUTPUT_VALID | Correctness | Adapter output matches declared schema |
| P11 | EVIDENCE_CAPTURED | Traceability | Every invocation produces evidence record |
| P12 | EVIDENCE_HASH_CHAIN | Traceability | Evidence chain is continuous and verifiable |
| P13 | TIMEOUT_ENFORCED | Safety | Adapter terminates within declared timeout |
| P14 | OUTPUT_SIZE_CAPPED | Safety | Output does not exceed max_output_size_bytes |
| P15 | REGISTRY_LOOKUP | Correctness | Registered adapters are discoverable |
| P16 | KILL_SWITCH_WORKS | Safety | Global kill switch stops all invocations |
| P17 | DEGRADE_MODE | Safety | Degradation mode blocks writes while allowing reads |
| P18 | ROLLBACK_PRESERVE | Safety | Rollback preserves evidence chain integrity |
| P19 | CONCURRENT_SAFE | Correctness | Concurrent invocations produce valid evidence |
| P20 | NO_SIDE_EFFECT | Safety | Read-only adapters produce zero observable side effects |

---

## §3 — Test Categories

| Category | Count | Description |
|----------|-------|-------------|
| Unit Tests | ≥40 | Per-function, per-method tests |
| Integration Tests | ≥10 | Cross-adapter, cross-module tests |
| Contract Tests | ≥5 | Contract validation and enforcement |
| Safety Tests | ≥8 | Permission, forbidden action, kill switch |
| Evidence Tests | ≥5 | Evidence capture, hash chain, integrity |
| Performance Tests | ≥3 | Timeout, output size, concurrency |
| Golden Regression | ≥1 | Deterministic output comparison |

---

## §4 — Test Harness Architecture

```
tests/
├── conftest.py              # Shared fixtures: mock adapters, registry, evidence store
├── test_disabled_default.py # P01
├── test_contract.py         # P02, P03
├── test_permissions.py      # P04, P05
├── test_readonly.py         # P06, P07, P20
├── test_schema.py           # P08, P09, P10
├── test_evidence.py         # P11, P12
├── test_timeout.py          # P13
├── test_output_size.py      # P14
├── test_registry.py         # P15
├── test_kill_switch.py      # P16
├── test_degrade.py          # P17
├── test_rollback.py         # P18
├── test_concurrent.py       # P19
└── golden/                  # Golden regression fixtures
    ├── A1_golden.json
    ├── A2_golden.json
    ├── A3_golden.json
    ├── A4_golden.json
    └── A5_golden.json
```

---

## §5 — Proof Execution Order

Proofs are executed in dependency order:
1. Safety proofs (P01-P07) — must pass first
2. Correctness proofs (P08-P10, P15) — core functionality
3. Traceability proofs (P11-P12) — evidence integrity
4. Safety boundary proofs (P13-P14, P16-P18, P20) — limits
5. Concurrency proof (P19) — last, depends on all above

---

## §6 — Proof Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| All safety proofs pass | 100% |
| All correctness proofs pass | 100% |
| All traceability proofs pass | 100% |
| Golden regression match | Exact match |
| Test coverage (line) | ≥90% |
| Test coverage (branch) | ≥85% |
| No flaky tests | 0 flaky in 100 runs |

---

## §7 — Governance

This test and proof plan is FUTURE_PLAN_ONLY. No test has been written,
no proof has been executed. All tests are gated behind the full
planning-review-merge pipeline. Proof execution is mandatory before any
adapter transitions from DISABLED to ENABLED.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Test and Proof Plan
