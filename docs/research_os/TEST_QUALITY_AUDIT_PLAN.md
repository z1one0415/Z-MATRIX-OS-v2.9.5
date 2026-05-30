# Research OS V3 — Test Quality Audit Plan

## Classification System

| Class | Definition | Example |
|-------|------|---------|
| REAL_LOGIC | Tests actual computation logic | `assert compute_ic([1,2,3]) == pytest.approx(1.0)` |
| FIXTURE_TEST | Tests using fixture data correctly | `assert CAL.is_trade_day("2024-01-02")` |
| EXISTENCE_TEST | Only checks file/module exists | `assert Path("x.py").exists()` |
| SAFETY_TEST | Checks production/broker/runtime blocks | `assert r.production_allowed is False` |
| DUPLICATE_TEST | Same logic, same assertion as another test | Repetitive identical assertions |
| WEAK_TEST | Trivially passing assertion | `assert True` or `assert 1 == 1` |

## Audit Questions

1. Are there tests that only check file existence?
2. Are there tests that always pass (weak assertions)?
3. Are there duplicate tests?
4. Do safety tests catch real violations?
5. Do fixture tests use realistic data scenarios?
6. Are fail-closed paths tested?
7. Are hash stability tests present?
8. Are edge cases (empty input, None, boundary) covered?

## Audit Commands

```bash
# Count test functions per category
grep -r "def test_" tests/research_db/ | wc -l

# Find only-existence tests
grep -r "\.exists()" tests/research_db/ | wc -l

# Find safety tests
grep -r "production_allowed" tests/research_db/ | wc -l

# Find weak assertions
grep -r "assert True" tests/research_db/
```

## Target

After audit: 80%+ tests should be REAL_LOGIC or FIXTURE_TEST, <10% EXISTENCE_TEST, 0% WEAK_TEST.
