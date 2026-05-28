#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.10 Sector Mapping Ingestion Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1
for t in source_discovery mapping_normalizer mapping_merger mapping_validator mapping_artifact_writer replay_sector_join_validator ingestion_report_builder; do
    PYTHONPATH=. python3 tests/test_v3510_${t}.py && echo "  ✅ $t"
done
git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"
echo "═══ v3.5.10 Sector Mapping Ingestion PASS ═══"
