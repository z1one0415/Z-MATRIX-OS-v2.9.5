# Z-SkillOS Frontend Handoff — Deploy Config Runbook

> Version: v0.1.0-rc | Agent: A6 QA/Release | Date: 2026-06-12

## Flask Configuration

### Default Configuration

| Setting | Default Value | Description |
|---------|--------------|-------------|
| `HOST` | `0.0.0.0` | Bind address for Flask |
| `PORT` | `5500` | Listen port |
| `DEBUG` | `False` | Debug mode (must remain False in production) |
| `DISABLED_DEFAULT` | `True` | All POST/PUT/PATCH/DELETE blocked |
| `READONLY_MODE` | `True` | GET-only; service reads from fixtures |
| `VERSION` | `v0.1.0-rc` | Release version string |

### Environment Variables

All configuration is overridable via environment variables:

| Variable | Type | Default | Example |
|----------|------|---------|---------|
| `ZSKILLOS_BACKEND_HOST` | string | `0.0.0.0` | `127.0.0.1` |
| `ZSKILLOS_BACKEND_PORT` | integer | `5500` | `8080` |

### CORS Configuration

CORS is enabled with open origins for development/readonly shell:

```python
from flask_cors import CORS
CORS(app)  # Allows all origins
```

**Production note**: For production deployment, restrict CORS origins to the frontend domain:

```python
CORS(app, origins=["https://frontend.example.com"])
```

### Disabled-Default Mode

The backend runs in **disabled-default** mode by design:

1. All GET endpoints return fixture data with HTTP 200
2. All POST / PUT / PATCH / DELETE requests return HTTP 405 BLOCKED
3. No mutation is possible through the API

```json
{
  "status": "BLOCKED",
  "reason": "readonly_disabled_default",
  "method": "POST"
}
```

### Deployment Checklist

- [ ] Python 3.10+ installed
- [ ] `pip install flask flask-cors` completed
- [ ] Port 5500 available (or override via `ZSKILLOS_BACKEND_PORT`)
- [ ] DEBUG remains `False`
- [ ] DISABLED_DEFAULT remains `True`
- [ ] READONLY_MODE remains `True`
- [ ] CORS origins locked down for production (non-default)
- [ ] Health check endpoint (`/api/health`) returns `{"status": "ok"}`

### Startup Commands

```bash
# Development
python3 -c "from skillos.frontend_handoff.backend.app import app; app.run(port=5500)"

# With WSGI (gunicorn — production)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5500 skillos.frontend_handoff.backend.app:app

# Custom port
ZSKILLOS_BACKEND_PORT=8080 python3 -c "from skillos.frontend_handoff.backend.app import app; app.run(port=8080)"
```

### Health Check Verification

```bash
curl http://localhost:5500/api/health
# Expected: {"status":"ok","version":"v0.1.0-rc"}
```
