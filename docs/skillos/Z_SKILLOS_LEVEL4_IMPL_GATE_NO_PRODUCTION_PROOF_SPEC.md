# Z-SkillOS Level 4 Implementation Gate — No-Production Proof Spec

## Status

Z_SKILLOS_LEVEL4_IMPL_GATE_NO_PRODUCTION_PROOF_SPEC_READY

## Purpose

Prove that Level 4 warning code has zero dependency on production, broker, or real_trade modules. No import, no reference, no indirect call path.

## Definition

"Production linkage" = any of:
- `import` of a production/broker/real_trade module
- `from ... import ...` of production symbols
- Dynamic import (`importlib`, `__import__`) resolving to production path
- Function call crossing into production module
- Class instantiation from production module
- Shared global state with production module
- Reading/writing production configuration
- Any reference to `live_trading`, `order_execution`, `broker_api`, `real_trade`

## Proof Strategy

### Static Import Analysis

```
Forbidden patterns (grep on all Level 4 source files):
  import broker
  from broker import
  import real_trade
  from real_trade import
  import production
  from production import
  import live_trading
  import order_execution
  import broker_api
  importlib.import_module("broker")
  importlib.import_module("real_trade")
  __import__("broker")
  __import__("real_trade")
```

Expected: zero matches across all Level 4 files.

### Transitive Dependency Check

```
1. List all Level 4 module imports
2. For each import, verify it does not transitively import production
3. Build dependency graph of Level 4 modules
4. Verify no path from Level 4 root to production module exists
```

### Runtime Path Audit

At test time:
1. Mock all production modules to raise if imported
2. Run full Level 4 warning cycle
3. Assert no ImportError from production modules

## Test Specification

```
test_level4_no_production_linkage:
  setup:
    - Patch sys.modules: inject mock for broker, real_trade, production, 
      live_trading, order_execution, broker_api
    - Each mock raises AssertionError on any attribute access
    - LEVEL4_WARNING_ENABLED=true

  execute:
    - Import all Level 4 modules
    - Run full warning evaluation cycle
    - Trigger all 10 warning categories
    - Emit warnings to side channels

  assert:
    - No AssertionError from mocked production modules
    - No ImportError for production paths
    - All Level 4 imports resolve to non-production modules

  teardown:
    - Remove mock patches from sys.modules
```

## Static Analysis Checks

| Check | Tool | Expected |
|:--|:--|:--|
| Direct import of broker | `grep -r "import broker\|from broker" skillos/level4/` | 0 matches |
| Direct import of real_trade | `grep -r "real_trade" skillos/level4/` | 0 matches |
| Direct import of production | `grep -r "production" skillos/level4/` | 0 matches |
| Dynamic import | `grep -r "import_module\|__import__" skillos/level4/` | 0 matches |
| Order/execution string | `grep -r "order\|execution\|live_trading" skillos/level4/` | 0 matches |
| Broker API string | `grep -r "broker_api\|trading_api" skillos/level4/` | 0 matches |
| Python AST import scan | `python3 -c "import ast; ..."` | 0 production imports |

## Dependency Allowlist

Level 4 modules may only import from:
- `skillos/contract/` — contract registry (read-only)
- `skillos/audit/` — audit utilities (read-only)
- `skillos/level3/` — observation evidence (read-only)
- `stdlib` — json, os.path, datetime, hashlib, logging
- `zmatrix/config/` — config reader (LEVEL4_* keys only)

Explicitly forbidden:
- `zmatrix/broker/`
- `zmatrix/real_trade/`
- `zmatrix/production/`
- `zmatrix/order/`
- `zmatrix/live/`

## Constraints

- Allowlist enforced at CI via import guard
- New dependency addition requires gate re-approval
- Permanent boundary: production linkage never approved at Level 4
