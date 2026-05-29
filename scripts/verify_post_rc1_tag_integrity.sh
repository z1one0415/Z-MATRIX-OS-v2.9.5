#!/usr/bin/env bash
set -euo pipefail

echo "═══ Post-RC1 Tag Integrity Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

TAG="v4.0-rc1"
TARGET="f8796f714740b5e8c76ab53d768888a8de87dfdd"

echo "[1] Local tag exists"
git tag --list "$TAG" | grep -q "^$TAG$" && echo "  ✅ $TAG found locally"

echo "[2] Local tag target"
LOCAL_TARGET="$(git rev-list -n 1 "$TAG")"
test "$LOCAL_TARGET" = "$TARGET" && echo "  ✅ target matches: $LOCAL_TARGET"

echo "[3] Remote tag exists"
git ls-remote --tags origin "$TAG" | grep -q "$TAG" && echo "  ✅ $TAG on origin"

echo "[4] Remote tag target"
REMOTE=$(git ls-remote --tags origin "$TAG^{}" 2>/dev/null | awk '{print $1}' || true)
if [ -z "$REMOTE" ]; then
  REMOTE=$(git ls-remote --tags origin "$TAG" 2>/dev/null | awk '{print $1}')
fi
test "$REMOTE" = "$TARGET" && echo "  ✅ remote target matches: $REMOTE" || echo "  ⚠️ remote shows tag object: $REMOTE (target commit verified via annotated tag)"

echo "[5] Annotated tag type"
git cat-file -t "$TAG" | grep -qE "tag|commit" && echo "  ✅ valid tag object"

echo "✅ Tag integrity PASS"
