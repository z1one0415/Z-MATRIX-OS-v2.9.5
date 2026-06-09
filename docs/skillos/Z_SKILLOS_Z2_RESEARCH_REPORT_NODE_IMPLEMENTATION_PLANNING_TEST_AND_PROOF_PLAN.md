# Z2 Research Report Node Implementation Planning — TEST AND PROOF PLAN

> Status: PLANNING_COMPLETE
> Seal: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED
> Date: 2026-06-09
> Branch: plan/skillos-z2-research-report-node-implementation-planning
> Base: c5f69f5

---

## 1. Status

| Field | Value |
|-------|-------|
| Phase | Planning (docs-only) |
| Confidence | HIGH_WITH_STRUCTURE_ONLY |
| Total proof categories | 50 |
| Coverage target | ≥95% |
| Test framework | pytest |

## 2. Scope

Exhaustive test and proof plan covering all aspects of the Z2 Research Report Node implementation.

## 3. Dependency

- Test structure follows sealed upstream patterns
- All dependencies merged; postmerge HEAD = c5f69f5
- pytest + pydantic as test foundation

## 4. Boundary

- Tests run in isolation (no network, no DB, no filesystem)
- Tests use only in-memory fixtures
- Tests complete in <5s individually, <60s total suite
- No test depends on execution order

## 5. Forbidden

- Tests MUST NOT use forbidden fields as valid data
- Tests MUST verify rejection of forbidden fields
- Tests MUST NOT bypass kill-switch

## 6. Proof

### Proof Categories (50 categories)

| # | Category | Test File | Description |
|---|----------|-----------|-------------|
| 1 | Kill-switch disabled when env unset | test_disabled_default.py | Verify DISABLED state when Z2_RESEARCH_REPORT_NODE_ENABLED not set |
| 2 | Kill-switch disabled when env empty | test_disabled_default.py | Verify DISABLED state when env="" |
| 3 | Kill-switch disabled when env=false | test_disabled_default.py | Verify DISABLED for "false", "False", "FALSE" |
| 4 | Kill-switch disabled when env=TRUE (case) | test_disabled_default.py | Only "true" (lowercase) enables |
| 5 | Kill-switch enabled when env=true | test_disabled_default.py | Verify ENABLED only for exact "true" |
| 6 | Kill-switch produces DENY_Z2_OUTPUTS_UNSAFE | test_disabled_default.py | Degradation response when disabled |
| 7 | Kill-switch no side effects | test_disabled_default.py | No logging/state change on check |
| 8 | Model instantiation (all 8 models) | test_models.py | All models create without error |
| 9 | Model immutability (frozen) | test_models.py | Assignment raises ValidationError |
| 10 | Model serialization round-trip | test_models.py | to_dict → from_dict identity |
| 11 | Model forbidden field rejection | test_models.py | Introspect model_fields for forbidden names |
| 12 | Model required field enforcement | test_models.py | Missing required field raises error |
| 13 | Model optional field default | test_models.py | Optional fields default to None |
| 14 | Model enum field validation | test_models.py | Invalid enum value rejected |
| 15 | Model datetime UTC enforcement | test_models.py | Non-UTC datetime rejected |
| 16 | Input contract schema validation | test_contracts.py | B1 CompositionGraphResponse accepted |
| 17 | Input contract rejection (wrong type) | test_contracts.py | Non-B1 input rejected |
| 18 | Input contract rejection (None) | test_contracts.py | None input triggers degradation |
| 19 | Output contract schema compliance | test_contracts.py | Response matches output schema |
| 20 | Output contract z9 field presence | test_contracts.py | z9_candidate always present |
| 21 | Output contract degradation field | test_contracts.py | Degradation field correct type |
| 22 | Z9 snapshot contract compliance | test_z9_snapshot.py | Snapshot matches Z9 spec |
| 23 | Z9 snapshot required fields | test_z9_snapshot.py | All required fields present |
| 24 | Z9 snapshot source_node literal | test_z9_snapshot.py | source_node="z2_research_report" |
| 25 | Z9 snapshot confidence level | test_z9_snapshot.py | confidence=HIGH_WITH_STRUCTURE_ONLY |
| 26 | Z9 snapshot serialization | test_z9_snapshot.py | JSON-serializable output |
| 27 | Section builder single section | test_section_builder.py | One section builds correctly |
| 28 | Section builder max sections | test_section_builder.py | Respects MAX_SECTIONS limit |
| 29 | Section builder empty input | test_section_builder.py | Empty graph → degradation |
| 30 | Section builder determinism | test_section_builder.py | Same input → same output |
| 31 | Section builder evidence attachment | test_section_builder.py | Evidence links to section |
| 32 | Evidence validation accepts valid | test_evidence.py | Well-formed evidence passes |
| 33 | Evidence validation rejects invalid | test_evidence.py | Malformed evidence rejected |
| 34 | Evidence count enforcement | test_evidence.py | Exceeding MAX_EVIDENCE_PER_SECTION rejected |
| 35 | Evidence minimum threshold | test_evidence.py | Below MIN_EVIDENCE triggers warning |
| 36 | Evidence deduplication | test_evidence.py | Duplicate evidence collapsed |
| 37 | Degradation mode DENY | test_degradation.py | DENY_Z2_OUTPUTS_UNSAFE mode |
| 38 | Degradation mode INPUT_INVALID | test_degradation.py | Invalid input degradation |
| 39 | Degradation mode SECTION_FAILURE | test_degradation.py | Section failure degradation |
| 40 | Degradation mode TIMEOUT | test_degradation.py | Timeout degradation |
| 41 | Degradation escalation L1→L2 | test_degradation.py | Threshold-based escalation |
| 42 | Degradation response schema | test_degradation.py | All fields present and typed |
| 43 | Report builder full assembly | test_report_builder.py | Complete report from sections |
| 44 | Report builder partial handling | test_report_builder.py | Partial completion with flag |
| 45 | Report builder timeout enforcement | test_report_builder.py | 30s timeout triggers degradation |
| 46 | Report builder completion flag | test_report_builder.py | Complete report has is_complete=True |
| 47 | No forbidden imports (all source) | test_no_forbidden_imports.py | AST scan of all .py files |
| 48 | No forbidden imports (network) | test_no_forbidden_imports.py | requests/httpx/socket banned |
| 49 | No forbidden imports (database) | test_no_forbidden_imports.py | sqlalchemy/psycopg2/sqlite3 banned |
| 50 | No forbidden imports (subprocess) | test_no_forbidden_imports.py | subprocess/os.system banned |

### Coverage Matrix

| Test File | Source File | Min Coverage |
|-----------|------------|-------------|
| test_disabled_default.py | kill_switch.py | 100% |
| test_models.py | models.py | 95% |
| test_contracts.py | contracts.py | 95% |
| test_section_builder.py | section_builder.py | 95% |
| test_evidence.py | evidence.py | 95% |
| test_degradation.py | degradation.py | 100% |
| test_report_builder.py | report_builder.py | 95% |
| test_z9_snapshot.py | z9_snapshot.py | 95% |
| test_no_forbidden_imports.py | ALL source files | N/A (scan) |

## 7. Next

- Tests written BEFORE implementation (TDD)
- Each batch starts with failing tests
- Green tests required before batch merge
- Coverage report generated per batch

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
