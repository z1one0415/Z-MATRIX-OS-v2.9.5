#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0-3 Research Experiment OS Verification ═══"
python3 -c "
from governance.experiment_ledger.experiment_ledger import INITIAL_EXPERIMENTS, RESEARCH_WORKFLOWS, EXPERIMENT_TYPES, EXPERIMENT_PERMISSIONS
assert len(INITIAL_EXPERIMENTS)>=3
for e in INITIAL_EXPERIMENTS:
    assert e.get('experiment_id'); assert e.get('experiment_type')
    assert e.get('git_commit')
assert len(RESEARCH_WORKFLOWS)>=3
assert len(EXPERIMENT_TYPES)>=5
print(f'  ✅ {len(INITIAL_EXPERIMENTS)} experiments registered')
print(f'  ✅ {len(RESEARCH_WORKFLOWS)} workflows')
"
echo "═══ V4.0-3 Experiment OS PASS ═══"
