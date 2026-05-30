# Research OS V3 — User Operation Manual

## Minimal Usage Path

```bash
# Step 1: Dry run (no output files)
bash scripts/run_golden_path_600519.sh --dry-run

# Step 2: Full run (generates reports)
bash scripts/run_golden_path_600519.sh
```

## Output Files

| File | Path |
|------|------|
| JSON | `runtime_reports/golden_path/golden_path_600519.json` |
| Technical MD | `runtime_reports/golden_path/golden_path_600519.md` |
| Human Report | `runtime_reports/golden_path/golden_path_human_report.md` |

## Reading the Output

### JSON
Machine-readable structured output. All 9 pipeline stages with explicit field names.

### Technical Markdown
Pipeline-level summary with stage-by-stage breakdown.

### Human Report
8-section Chinese research report:
1. Research Subject
2. One-line Conclusion (no BUY/SELL)
3. Evidence & Reasoning
4. Return Attribution
5. Risk Analysis
6. Devil's Advocate Opinion
7. Recommended Action (observe/track only)
8. Audit Information

## Audit Hash

Every run produces a unique `_audit_hash` (SHA256, 16 characters). Identical inputs produce identical hashes — this is the reproducibility guarantee.

## Error Handling

| Error | Action |
|-------|--------|
| Import error | Check PYTHONPATH: `PYTHONPATH=.` |
| Fixture missing | Ensure `tests/fixtures/` directory exists |
| Module count changed | Architecture freeze violation — DO NOT proceed |

## Commands Reference

```bash
# Golden Path
bash scripts/run_golden_path_600519.sh [--dry-run]

# Architecture verification
bash scripts/verify_research_os_architecture_freeze.sh

# Full test suite
PYTHONPATH=. python3 -m pytest -q tests/research_db/

# Delivery verification
bash scripts/verify_research_os_delivery_closeout.sh
```
