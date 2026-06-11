# Z-SkillOS Frontend Handoff — Observability Runbook

> Version: v0.1.0-rc | Agent: A6 QA/Release | Date: 2026-06-12

## Overview

The observability layer provides logging, health checking, audit trail, and error monitoring for the Z-SkillOS Frontend Handoff backend. All observability data conforms to JSON schemas defined in `skillos/frontend_handoff/observability/`.

## Log Format

All application logs use structured JSON format. See `skillos/frontend_handoff/observability/log_schema.json` for the full schema.

### Log Level Conventions

| Level | Usage |
|-------|-------|
| `DEBUG` | Detailed diagnostic info (development only) |
| `INFO` | Normal operational events |
| `WARNING` | Degraded responses, fixture fallback |
| `ERROR` | Unhandled exceptions, blocked mutation attempts |
| `CRITICAL` | Service unreachable, startup failures |

### Log Entry Structure

```json
{
  "timestamp": "2026-06-12T00:00:00.000Z",
  "level": "INFO",
  "logger": "skillos.frontend_handoff",
  "message": "Request processed",
  "module": "backend.routes",
  "endpoint": "/api/health",
  "method": "GET",
  "status_code": 200,
  "duration_ms": 1.5,
  "request_id": "req-abc123"
}
```

## Health Check

### Endpoint

```
GET /api/health
```

### Response Schema

See `skillos/frontend_handoff/observability/healthcheck_schema.json`.

### Expected Response

```json
{
  "status": "ok",
  "version": "v0.1.0-rc"
}
```

### Monitoring Integration

```bash
# Shell-based health check
curl -s http://localhost:5500/api/health | grep -q '"status":"ok"' && echo "OK" || echo "FAIL"

# Python-based health check
python3 -c "
import requests
r = requests.get('http://localhost:5500/api/health')
assert r.json()['status'] == 'ok'
print('OK')
"
```

## Audit Trail

### Endpoint

```
GET /api/audit-trail
```

### Schema

See `skillos/frontend_handoff/observability/audit_trail_schema.json`.

### Audit Event Types

| Event Type | Description |
|------------|-------------|
| `request_received` | API request received |
| `response_sent` | API response emitted |
| `mutation_blocked` | POST/PUT/PATCH/DELETE blocked |
| `fixture_served` | Fixture data returned |
| `error_occurred` | Error condition triggered |
| `health_check` | Health check performed |

## Error Monitoring

### Error Response Format

All errors return JSON with consistent structure:

```json
{
  "status": "BLOCKED",
  "reason": "readonly_disabled_default",
  "method": "POST"
}
```

HTTP status codes:
- `200`: Normal GET response
- `405`: Blocked mutation attempt
- `500`: Internal server error

### Monitoring Alert Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Health check failure | > 3 consecutive | Alert on-call |
| 405 rate spike | > 10/min | Investigate unauthorized mutation attempts |
| 500 errors | Any | Immediate investigation |
| Response latency | > 500ms p95 | Performance review |
| Memory usage | > 512MB | Restart service |

### Log Location

Logs are written to stdout by default. For file-based logging:

```bash
python3 -c "from skillos.frontend_handoff.backend.app import app; app.run(port=5500)" 2>&1 | tee skillos_frontend_handoff.log
```
