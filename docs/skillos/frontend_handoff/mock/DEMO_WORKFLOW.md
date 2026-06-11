# A5 Mock Server — Demo Workflow

> **Purpose**: Step-by-step demo of the SkillOS Frontend Handoff mock API.
> **Server**: A5 Mock Server on `http://localhost:8080`
> **All data is synthetic fixture data — no real positions, orders, trades, PnL, or broker actions.**

---

## Prerequisites

```bash
cd ~/Documents/"Z-MATRIX-OS v2.9.5"
pip install flask pytest
```

## Start the Mock Server

```bash
cd skillos/frontend_handoff/mock
python3 server.py
```

Expected output:
```
[A5 Mock Server] Starting on port 8080
[A5 Mock Server] DEBUG=False
[A5 Mock Server] DISABLED_DEFAULT=True (per SkillOS policy)
[A5 Mock Server] Endpoints: /api/v1/health, /api/v1/dashboard/summary, ...
```

---

## Demo Walkthrough

### Step 1: View Dashboard Summary

```bash
curl http://localhost:8080/api/v1/dashboard/summary | python3 -m json.tool
```

**What to check**:
- `status.overall` should be `"NOMINAL"`
- `counts.skills` = 18, `counts.factors` = 23
- Indicator lights: TruthGate GREEN, Z9 Calibration AMBER
- No buy/sell/order/position/PnL fields

### Step 2: Browse Capabilities

```bash
curl http://localhost:8080/api/v1/capabilities | python3 -m json.tool
```

**What to check**:
- 18 total capabilities
- 14 READY, 3 DISABLED, 1 BLOCKED
- CAP-008 (Z9 Review Node) is DISABLED — matches disabled-default policy
- CAP-018 (Hermes Memory Kernel) is BLOCKED with reason

### Step 3: Browse Factor Library

```bash
curl http://localhost:8080/api/v1/factors/summary | python3 -m json.tool
```

**What to check**:
- 23 factors total
- 20 SEALED, 3 DRAFT
- B-Matrix: 7 factors, D-Matrix: 7 factors, R-Matrix: 5 factors, Shared: 4 factors
- Each factor has id, name, category, seal status, weight, description

### Step 4: Check Gate States

```bash
curl http://localhost:8080/api/v1/gates/state | python3 -m json.tool
```

**What to check**:
- F7 gate chain: 7 gates, all PASSED
- F7.0 TruthGate has 7 preconditions, all passed
- F7.2 Decision Gate: "28 stock final selection"
- Timestamps in UTC

### Step 5: View Evidence Chain

```bash
curl http://localhost:8080/api/v1/evidence/chain-demo | python3 -m json.tool
```

**What to check**:
- 5 steps: FactorLib → A1 → B1 → Z2 → Z9
- Each step has input_hash, output_hash, timestamp, status
- Hash continuity is UNBROKEN
- No real stock data — hashes are synthetic

### Step 6: View Run State

```bash
curl http://localhost:8080/api/v1/pipeline/run-state | python3 -m json.tool
```

**What to check**:
- 11 phases, all PASSED
- abort_reasons is empty array
- Resource usage metrics present (CPU, memory, disk)
- retry_count = 0

### Step 7: View Research Report

```bash
curl http://localhost:8080/api/v1/research/report-summary | python3 -m json.tool
```

**What to check**:
- 12 sections — exactly matching Z-G14 12-step template
- Each section has status COMPLETE and a human-readable summary
- Evidence chain with 5 hashes
- Z9 snapshot with calibration status CURRENT

### Step 8: View Error/Abort/Degraded States

```bash
curl http://localhost:8080/api/v1/demo/error-abort-degraded | python3 -m json.tool
```

**What to check**:
- 9 scenarios: 3 ERROR, 3 ABORT, 3 DEGRADED
- Each has type, scenario_id, severity, detail, ui_state
- These are synthetic — explicitly labeled "do NOT represent actual system states"

### Step 9: View Audit Trail

```bash
curl http://localhost:8080/api/v1/audit/trail | python3 -m json.tool
```

**What to check**:
- 24 sequential events
- Each has seq, timestamp, actor, action, detail, status
- Actions: PIPELINE_TRIGGER, GATE_CHECK_PASS, SCAN_COMPLETE, etc.

### Step 10: Health Check

```bash
curl http://localhost:8080/api/v1/health
```

Expected: `{"status": "OK", "timestamp_utc": "2026-06-12T04:03:00Z", "uptime_sec": 86400}`

---

## Non-Existent Endpoint Test

```bash
curl http://localhost:8080/api/v1/nonexistent
```

Expected: 404 with JSON body listing all available endpoints.

---

## Run Automated Tests

```bash
cd ~/Documents/"Z-MATRIX-OS v2.9.5"
python3 -m pytest tests/skillos/frontend_handoff/mock/ -q -v
```

---

## Verification Checklist

- [ ] All 11 fixture endpoints return 200
- [ ] Dashboard shows NOMINAL status
- [ ] Z9 Review Node is DISABLED (per P0 policy)
- [ ] Hermes Memory Kernel is BLOCKED
- [ ] No buy/sell/order/position in any fixture
- [ ] No alpha_claim in any fixture
- [ ] No trade_result in any fixture
- [ ] No real_pnl in any fixture
- [ ] No broker_action in any fixture
- [ ] Evidence chain hash continuity verified
- [ ] All gate chain states readable
- [ ] Error/abort/degraded demo shows all 3 categories
