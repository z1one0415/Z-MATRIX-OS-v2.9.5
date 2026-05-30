# Golden Path Execution Guide — 贵州茅台 (600519)

## Quick Start

```bash
# Dry run (no output files)
bash scripts/run_golden_path_600519.sh --dry-run

# Full run (generates JSON + Markdown)
bash scripts/run_golden_path_600519.sh
```

## What It Does

Traces a complete research cycle for 600519 (Kweichow Moutai) through 9 stages:

```
IDEA → DATA → FACTOR → OUTCOME → ATTRIBUTION → REPLAY → COUNCIL → DECISION → MEMORY
```

## Output

| File | Content |
|------|------|
| `runtime_reports/golden_path/golden_path_600519.json` | Structured stage outputs |
| `runtime_reports/golden_path/golden_path_600519.md` | Human-readable report |

## Safety

- Uses existing synthetic fixtures ONLY
- No real market data accessed
- No broker connection
- No runtime daemon
- No trade execution
- Production: BLOCKED
