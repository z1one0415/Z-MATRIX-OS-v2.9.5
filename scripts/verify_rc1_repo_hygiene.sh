#!/usr/bin/env bash
set -euo pipefail

echo "═══ RC1 Repository Hygiene Audit ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

git status --short

# forbidden tracked paths
for path in runtime_reports .pytest_cache __pycache__ .DS_Store; do
  if git ls-files | grep -q "^${path}"; then
    echo "❌ forbidden tracked path: $path"
    exit 1
  fi
done

# no generated audit zip tracked
if git ls-files | grep -qE '\.zip$'; then
  echo "❌ generated .zip artifact tracked"
  exit 1
fi

# no audit_exports tracked
if git ls-files | grep -q 'audit_exports'; then
  echo "❌ audit_exports tracked"
  exit 1
fi

# ensure .gitignore exists and covers runtime
if [ ! -f .gitignore ]; then
  echo "⚠️  .gitignore missing, creating..."
  cat > .gitignore <<'GITIGNORE'
runtime_reports/
*.zip
.pytest_cache/
__pycache__/
*.pyc
.DS_Store
GITIGNORE
fi

# verify .gitignore covers key paths
for pattern in "runtime_reports" ".pytest_cache" "__pycache__" ".DS_Store"; do
  if ! grep -q "$pattern" .gitignore 2>/dev/null; then
    echo "$pattern" >> .gitignore
  fi
done

echo "✅ repository hygiene PASS"
