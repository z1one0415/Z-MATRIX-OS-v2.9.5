# Test Classification Standard

## REAL_LOGIC_TEST
Tests that verify actual computation, state machines, boundary conditions, hash stability, or fail-closed behavior.
Must have at least one non-trivial assertion on a computed value.

## WEAK_TEST
Tests that only verify existence, strings, default returns, or have no behavioral assertion.
Includes: `assert x is not None`, `assert True`, `assert len(x) >= 0`.

## SAFETY_TEST
Tests that verify forbidden flags, BLOCKED states, privacy protection, no real trade instructions.
Core: `production_allowed=False`, no BUY/SELL/AUTO_EXECUTE in output.

## FIXTURE_TEST
Tests that primarily verify fixture data loads correctly but do not prove business logic.
Acceptable when combined with REAL_LOGIC classification.

## EXISTENCE_TEST
Tests that only verify file/field/document/entry existence.
`assert Path("x.py").exists()` is the canonical example.

## DUPLICATE_TEST
Tests with substantially identical input and assertion as another test.
