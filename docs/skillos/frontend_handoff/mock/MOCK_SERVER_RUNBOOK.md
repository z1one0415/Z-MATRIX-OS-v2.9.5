# A5 Mock Server Runbook

> **Version**: v1.0 | **RC**: Z-SkillOS Frontend Handoff
> **Server**: Flask mock on port 8080
> **All data**: Synthetic fixtures — no real positions, orders, trades, or PnL.

---

## Quick Start

```bash
cd ~/Documents/"Z-MATRIX-OS v2.9.5"/skillos/frontend_handoff/mock
python3 server.py
```

Server starts on `http://0.0.0.0:8080`.

---

## Endpoints

| Method | Path | Fixture File | Description |
|--------|------|-------------|-------------|
| GET | `/api/v1/health` | (inline) | Server health check |
| GET | `/api/v1/version` | (inline) | Version info |
| GET | `/api/v1/dashboard/summary` | `dashboard_summary.json` | System overview dashboard |
| GET | `/api/v1/capabilities` | `capability_list.json` | Capability inventory |
| GET | `/api/v1/factors/summary` | `factor_library_summary.json` | 23-factor library |
| GET | `/api/v1/composition-graph/summary` | `composition_graph_summary.json` | Node-edge graph |
| GET | `/api/v1/research/report-summary` | `research_report_summary.json` | 12-section report |
| GET | `/api/v1/z9/review-summary` | `z9_review_summary.json` | Z9 review labels |
| GET | `/api/v1/evidence/chain-demo` | `evidence_chain_demo.json` | Hash-chained evidence |
| GET | `/api/v1/pipeline/run-state` | `run_state_demo.json` | Pipeline execution state |
| GET | `/api/v1/gates/state` | `gate_state_demo.json` | F7 gate chain status |
| GET | `/api/v1/audit/trail` | `audit_trail_demo.json` | Decision audit trail |
| GET | `/api/v1/demo/error-abort-degraded` | `error_abort_degraded_demo.json` | Error/abort/degraded states |

---

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| PORT | 8080 | `mock_config.py` |
| DEBUG | False | `mock_config.py` |
| DISABLED_DEFAULT | True | `mock_config.py` |
| Host | 0.0.0.0 | `server.py` |

---

## Fixture Files

All fixtures live in `skillos/frontend_handoff/fixtures/`:

| # | File | Content |
|---|------|---------|
| 1 | `dashboard_summary.json` | System counts, status, indicator lights |
| 2 | `capability_list.json` | 18 capabilities with READY/DISABLED/BLOCKED |
| 3 | `factor_library_summary.json` | 23 factors with seal and matrix status |
| 4 | `composition_graph_summary.json` | 14 nodes, 23 edges |
| 5 | `research_report_summary.json` | 12-section Z-G14 report |
| 6 | `z9_review_summary.json` | Review labels, feedback, escalations |
| 7 | `evidence_chain_demo.json` | FactorLib→A1→B1→Z2→Z9 chain |
| 8 | `run_state_demo.json` | 11-phase pipeline run |
| 9 | `gate_state_demo.json` | F7.0 through F7.2 gates |
| 10 | `audit_trail_demo.json` | 24-event decision audit |
| 11 | `error_abort_degraded_demo.json` | 9 synthetic state scenarios |

---

## Content Constraints (Verified by Tests)

The following content types are **prohibited** in all fixtures:

- ❌ buy / sell / order / position
- ❌ alpha_claim
- ❌ trade_result
- ❌ real_pnl
- ❌ broker_action

All fixtures are synthetic and contain no real market data, stock picks, or portfolio positions.

---

## Test Suite

```bash
cd ~/Documents/"Z-MATRIX-OS v2.9.5"
python3 -m pytest tests/skillos/frontend_handoff/mock/ -q -v

# Specific test files:
python3 -m pytest tests/skillos/frontend_handoff/mock/test_mock_payload_contract_alignment.py -v
python3 -m pytest tests/skillos/frontend_handoff/mock/test_mock_server_routes.py -v
python3 -m pytest tests/skillos/frontend_handoff/mock/test_no_trade_content.py -v
```

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| `Address already in use` | Port 8080 occupied | `lsof -i :8080` to find and kill |
| `ImportError: No module named 'flask'` | Flask not installed | `pip install flask` |
| Fixture not found | Wrong working directory | Run from `skillos/frontend_handoff/mock/` |
| Test failures | Fixture schema mismatch | Check fixture JSON validity with `python3 -m json.tool` |
