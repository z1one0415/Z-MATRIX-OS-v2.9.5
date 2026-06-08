# Impl ✓ TEST_PLAN

## Status: IMPLEMENTATION_PLANNING_TEST_PLAN_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Level 5: BLOCKED

## Test Suite Structure: 11 files in `tests/skillos/.../adapters/wave0/`
conftest.py | test_github_readonly_adapter.py | test_doc_gen_adapter.py | test_report_reader_adapter.py | test_wave0_integration.py | test_wave0_disabled_default.py | test_wave0_permission.py | test_wave0_evidence_sink.py | test_wave0_no_side_effects.py | test_wave0_kill_switch.py | test_wave0_rollback.py

## Test Categories (39 tests: 37 P0 + 2 P1)

### T1: Disabled-by-Default (4 P0)
T1.1-3: Each adapter.enabled==False after import | T1.4: Call disabled→AdapterDisabledError

### T2: Adapter Unit (18 P0)
**GitHub(6)**: read_file(OK/notfound) | list_repos | get_commits | read_file(secrets→DENIED) | write_file(DENIED)
**Doc Gen(6)**: generate(OK) | generate(nonexistent→error) | generate(PDF) | validate_template | generate(/etc/passwd→DENIED) | delete_doc(DENIED)
**Report Reader(6)**: read_report(OK/notfound) | list_reports | parse_report | read_report(.env→DENIED) | write_report(DENIED)

### T3: Permission (5 P0 + 1 P1)
T3.1: Cap OS disabled→DENIED | T3.2: Adapter disabled→DENIED | T3.3: Forbidden op→DENIED | T3.4: Rate limit 31st→DENIED(P1) | T3.5: Kill switch→EmergencyKillSwitchActiveError | T3.6: Unkill→recovered

### T4: Evidence Sink (4 P0)
T4.1: Successful call→evidence | T4.2: Denied call→evidence | T4.3: Params hashed | T4.4: No evidence file on disk

### T5: Side Effects (4 P0)
T5.1: FS before/after snapshot→no diff | T5.2: Env vars→no diff | T5.3: Global state→no diff | T5.4: Socket→no writes

### T6: Integration (2 P0 + 1 P1)
T6.1: Chain 3 adapters→all succeed | T6.2: One fails→others unaffected | T6.3: Cross-adapter evidence all recorded(P1)

## Summary: 6 categories | 39 tests | 37 P0(must pass) | 2 P1(known limitation OK)

> Cap OS Phase 11 | Test Plan | 39 tests | 37 P0 + 2 P1