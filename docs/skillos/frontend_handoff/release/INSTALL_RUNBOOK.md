# Z-SkillOS Frontend Handoff — Install Runbook

> Version: v0.1.0-rc | Agent: A6 QA/Release | Date: 2026-06-12

## Prerequisites

| Requirement | Minimum Version | Notes |
|-------------|----------------|-------|
| Python | 3.10+ | CPython; PyPy not tested |
| pip | 21.0+ | Required for Flask-Cors dependency |
| Git | 2.30+ | For repository clone and branch checkout |
| OS | macOS / Linux | Windows not validated for v0.1.0-rc |

## Installation Steps

### 1. Clone Repository

```bash
git clone <repository-url> "Z-MATRIX-OS v2.9.5"
cd "Z-MATRIX-OS v2.9.5"
```

### 2. Checkout Integration Branch

```bash
git checkout integration/z-skillos-frontend-handoff-rc
git pull origin integration/z-skillos-frontend-handoff-rc
```

### 3. Create Virtual Environment (Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows (not validated)
```

### 4. Install Dependencies

```bash
pip install flask flask-cors
```

Additional test dependencies:
```bash
pip install pytest
```

### 5. Verify Installation

```bash
python3 -c "from skillos.frontend_handoff.backend.app import app; print('OK')"
```

Expected output: `OK`

### 6. Run Tests

```bash
python3 -m pytest tests/skillos/frontend_handoff/ -q
```

All tests should pass with exit code 0.

### 7. Start Development Server

```bash
python3 -c "from skillos.frontend_handoff.backend.app import app; app.run(port=5500)"
```

Verify at: `http://localhost:5500/api/health`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: flask` | Run `pip install flask flask-cors` |
| `ModuleNotFoundError: skillos` | Ensure you are in the repo root directory |
| Port 5500 already in use | Set `ZSKILLOS_BACKEND_PORT` env var or kill existing process |
| Import errors | Verify Python version ≥ 3.10 with `python3 --version` |
