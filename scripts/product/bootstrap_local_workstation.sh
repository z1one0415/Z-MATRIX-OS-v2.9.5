#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

MODE="install"
SKIP_PYTHON=0
SKIP_NODE=0

usage() {
  cat <<'EOF'
Usage: bash scripts/product/bootstrap_local_workstation.sh [--check] [--skip-python] [--skip-node]

Default mode prepares a local Python virtual environment, installs the cockpit
dependencies, and creates .env from .env.example when .env does not exist.

--check validates that the bootstrap inputs and local toolchain are present
without installing packages.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)
      MODE="check"
      ;;
    --skip-python)
      SKIP_PYTHON=1
      ;;
    --skip-node)
      SKIP_NODE=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

require_file() {
  if [[ ! -f "$1" ]]; then
    echo "Missing required file: $1" >&2
    exit 1
  fi
}

require_command python3
require_command npm
require_file ".env.example"
require_file "apps/cockpit_web/package.json"
require_file "apps/cockpit_web/package-lock.json"
require_file "scripts/product/start_backend_service.py"
require_file "scripts/product/start_local_workstation.sh"

if [[ "$MODE" == "check" ]]; then
  echo "Z_MATRIX_LOCAL_BOOTSTRAP_CHECK_PASS"
  exit 0
fi

if [[ "$SKIP_PYTHON" == "0" ]]; then
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  python3 -m pip install -U pip pytest
fi

if [[ "$SKIP_NODE" == "0" ]]; then
  npm --prefix apps/cockpit_web install
fi

if [[ ! -f ".env" ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
else
  echo ".env already exists; leaving it unchanged"
fi

echo "Z_MATRIX_LOCAL_BOOTSTRAP_READY"
