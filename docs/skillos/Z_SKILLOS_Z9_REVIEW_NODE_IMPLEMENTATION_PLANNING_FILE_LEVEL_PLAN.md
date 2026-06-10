---
title: "Z9 Review Node Implementation Planning — File-Level Plan"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — File-Level Plan

## Section 1: Directory Structure Planning

### 1.1 Code Module Directory
```
skillos/capability_invocation_os/review_node/
├── __init__.py              # Package init + DISABLED_DEFAULT guard
├── constants.py             # Review labels, degradation decisions, forbidden enums
├── config.py                # Kill switch, runtime configuration, env bindings
├── kill_switch.py           # DISABLED_DEFAULT_NOOP enforcement logic
├── models.py                # Pydantic models: ReviewLabel, Evidence, Attribution, Degradation
├── contracts.py             # Input/output contract validation (15-field input, 6-label output)
├── evidence.py              # Evidence pass-through, immutability guard, 19-field mapping
├── attribution.py           # 9-type attribution computation (profit attribution blocked)
├── degradation.py           # 10-decision degradation framework with 2 hard blockers
├── review_builder.py        # Review label assignment engine, explanation construction
├── z2_feedback.py           # Advisory/readonly Z2 feedback channel, 10 allowed / 8 forbidden
└── registry.py              # SkillOS capability registration, node metadata
```

### 1.2 Test Module Directory
```
tests/skillos/capability_invocation_os/review_node/
├── test_disabled_default.py    # Verify DISABLED_DEFAULT_NOOP passthrough in all configs
├── test_models.py              # Pydantic model validation, serialization, edge cases
├── test_contracts.py           # Contract validation: source check, field presence, shape
├── test_evidence.py            # Evidence pass-through, immutability, 19-field integrity
├── test_attribution.py         # 9 attribution types, profit block enforcement
├── test_degradation.py         # All 10 degradation paths including 2 hard blockers
├── test_review_builder.py      # 6-label classification correctness, explanation integrity
├── test_z2_feedback.py         # Advisory/readonly enforcement, 8 forbidden field blocks
└── test_no_forbidden_imports.py # Static import safety: no trade/broker/memory/PNL imports
```

## Section 2: Module Responsibility Matrix

| # | Module | Primary Responsibility | Key Enums/Models | Line Count Est. |
|---|--------|----------------------|-----------------|:---:|
| 1 | __init__.py | Package init + DISABLED_DEFAULT guard | ReviewNode class | ~40 |
| 2 | constants.py | All enum definitions: labels, decisions, forbidden | 6 labels, 10 decisions, 8 forbidden | ~80 |
| 3 | config.py | Kill switch + runtime config | KillSwitchConfig, RuntimeConfig | ~60 |
| 4 | kill_switch.py | DISABLED_DEFAULT enforcement | NOOP passthrough | ~70 |
| 5 | models.py | Pydantic models for all data types | 5 model classes | ~120 |
| 6 | contracts.py | Input/output contract validation | 2 validators | ~100 |
| 7 | evidence.py | Evidence pass-through + immutability | 19-field mapping | ~90 |
| 8 | attribution.py | 9 attribution types | AttributionEngine | ~100 |
| 9 | degradation.py | 10 degradation decisions | DegradationManager | ~110 |
| 10 | review_builder.py | Review label assignment | ReviewBuilder | ~100 |
| 11 | z2_feedback.py | Advisory Z2 feedback channel | Z2FeedbackChannel | ~80 |
| 12 | registry.py | SkillOS registration | NodeRegistry | ~50 |

**Total estimated code: ~1,000 lines (12 modules)**

## Section 3: Module Dependency Graph

```
__init__.py
  ├── kill_switch.py ←── config.py
  │     └── DISABLED_DEFAULT_NOOP pass-through
  │
  ├── models.py ←── constants.py
  │     ├── ReviewLabel (6 enum values)
  │     ├── EvidenceEnvelope (19 fields)
  │     ├── AttributionResult (9 types)
  │     ├── DegradationDecision (10 decisions)
  │     └── Z9ReviewOutput (label + explanation)
  │
  ├── contracts.py ←── models.py
  │     ├── InputContractValidator (15-field check)
  │     └── OutputContractValidator (6-label check)
  │
  ├── evidence.py ←── models.py
  │     ├── EvidencePassThrough (19-field mapping)
  │     └── EvidenceImmutabilityGuard
  │
  ├── attribution.py ←── models.py
  │     └── AttributionEngine (9 types, profit blocked)
  │
  ├── degradation.py ←── models.py, contracts.py
  │     ├── DegradationManager (10 decisions)
  │     ├── TradeResultBlock (hard blocker)
  │     └── MemoryMutationBlock (hard blocker)
  │
  ├── review_builder.py ←── models.py, evidence.py, attribution.py, degradation.py
  │     └── ReviewBuilder (6-label classification)
  │
  ├── z2_feedback.py ←── models.py
  │     └── Z2FeedbackChannel (10 allowed / 8 forbidden)
  │
  └── registry.py ←── models.py, config.py
        └── NodeRegistry (SkillOS registration)
```

## Section 4: File Creation Sequence

The following sequence ensures no forward-reference errors during implementation:

### Phase 1: Foundation (constants → config → models → kill_switch)
1. `constants.py` — All enum definitions first (no deps)
2. `config.py` — Runtime configuration (depends on constants)
3. `models.py` — Pydantic models (depends on constants)
4. `kill_switch.py` — DISABLED_DEFAULT enforcement (depends on config, models)

### Phase 2: Contracts (contracts → evidence)
5. `contracts.py` — Input/output validators (depends on models)
6. `evidence.py` — Evidence pass-through (depends on models)

### Phase 3: Logic (attribution → degradation)
7. `attribution.py` — 9-type attribution (depends on models)
8. `degradation.py` — 10-decision degradation (depends on models, contracts)

### Phase 4: Integration (review_builder → z2_feedback → registry → __init__)
9. `review_builder.py` — Review engine (depends on models, evidence, attribution, degradation)
10. `z2_feedback.py` — Z2 feedback channel (depends on models)
11. `registry.py` — SkillOS registration (depends on models, config)
12. `__init__.py` — Package init (depends on all)

## Section 5: Test File Mapping

| Source Module | Test Module | Test Focus |
|--------------|------------|-----------|
| __init__.py + kill_switch.py | test_disabled_default.py | DISABLED_DEFAULT_NOOP, kill switch states |
| models.py + constants.py | test_models.py | Model validation, enum correctness, serialization |
| contracts.py | test_contracts.py | Input source validation, field presence, output shape |
| evidence.py | test_evidence.py | 19-field pass-through, immutability, tamper detection |
| attribution.py | test_attribution.py | 9 type coverage, profit block, edge cases |
| degradation.py | test_degradation.py | All 10 paths, hard blockers, decision tree |
| review_builder.py | test_review_builder.py | 6-label classification, explanation integrity |
| z2_feedback.py | test_z2_feedback.py | 10 allowed / 8 forbidden field enforcement |
| ALL modules | test_no_forbidden_imports.py | Static import safety scan |

## Section 6: Implementation Constraints

### 6.1 Coding Standards
- All modules use Pydantic v2 for data validation
- Type hints mandatory on all public functions
- Docstrings follow Google-style format
- No wildcard imports; explicit imports only
- Maximum function length: 50 lines
- Maximum file length: 200 lines

### 6.2 Safety Constraints (PER-FILE)
- `constants.py`: Must define all 6 labels, 10 decisions, 8 forbidden as Enum classes
- `config.py`: Must default kill_switch to ENABLED (node OFF by default)
- `kill_switch.py`: Must return DISABLED_DEFAULT_NOOP when switch is ON, no exceptions
- `models.py`: Must validate all fields with Pydantic validators, no raw dict acceptance
- `contracts.py`: Must reject any input not matching z9_review_snapshot_candidate shape
- `evidence.py`: Must pass through all 19 fields without modification; must detect any tampering
- `attribution.py`: Must block profit/PNL computation; must cover all 9 types
- `degradation.py`: TRADE_RESULT_FORBIDDEN and MEMORY_MUTATION_FORBIDDEN are non-overridable
- `review_builder.py`: Must assign exactly one label per invocation
- `z2_feedback.py`: Must enforce 10 allowed / 8 forbidden field boundaries
- `registry.py`: Must register with readonly/advisory capability flags

### 6.3 Forbidden Patterns (ALL FILES)
- No `import` from trade/broker/profit/PNL modules
- No file I/O beyond audit trail
- No network calls
- No subprocess spawning
- No dynamic code execution (eval, exec, compile)
- No monkey-patching of system modules

## Section 7: Future File Map (DO NOT CREATE NOW)

The following files are specified for future implementation branches only. They MUST NOT be created during this planning phase.

### Code files (12 total):
```
skillos/capability_invocation_os/review_node/__init__.py
skillos/capability_invocation_os/review_node/constants.py
skillos/capability_invocation_os/review_node/config.py
skillos/capability_invocation_os/review_node/kill_switch.py
skillos/capability_invocation_os/review_node/models.py
skillos/capability_invocation_os/review_node/contracts.py
skillos/capability_invocation_os/review_node/evidence.py
skillos/capability_invocation_os/review_node/attribution.py
skillos/capability_invocation_os/review_node/degradation.py
skillos/capability_invocation_os/review_node/review_builder.py
skillos/capability_invocation_os/review_node/z2_feedback.py
skillos/capability_invocation_os/review_node/registry.py
```

### Test files (9 total):
```
tests/skillos/capability_invocation_os/review_node/test_disabled_default.py
tests/skillos/capability_invocation_os/review_node/test_models.py
tests/skillos/capability_invocation_os/review_node/test_contracts.py
tests/skillos/capability_invocation_os/review_node/test_evidence.py
tests/skillos/capability_invocation_os/review_node/test_attribution.py
tests/skillos/capability_invocation_os/review_node/test_degradation.py
tests/skillos/capability_invocation_os/review_node/test_review_builder.py
tests/skillos/capability_invocation_os/review_node/test_z2_feedback.py
tests/skillos/capability_invocation_os/review_node/test_no_forbidden_imports.py
```

**TOTAL: 21 future implementation files (12 code + 9 test)**
