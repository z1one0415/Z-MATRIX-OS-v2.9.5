# Research OS V3 — Onboarding Guide

## What This System Is

Research OS V3 is a **personal quantitative research operating system**. It reconstructs your trading history, validates factors, replays strategies, runs 12-seat council review, and generates human-readable research reports.

## What It Is NOT

- ❌ A trading robot
- ❌ A broker execution platform
- ❌ A real-time market monitor
- ❌ An automated buy/sell system
- ❌ A production deployment

## Why Architecture Freeze

After building 160 modules across 6 architectural layers, the system has reached functional maturity. Further expansion risks fragmentation. The freeze ensures stability for onboarding, auditing, and reproducible research.

## Quick Start

### Prerequisites

```bash
cd ~/Documents/Z-MATRIX-OS\ v2.9.5
pip install pytest
```

### Run Your First Research

```bash
bash scripts/run_golden_path_600519.sh --dry-run
```

This traces a full research cycle for Kweichow Moutai (600519) through all stages.

### Read the Report

```bash
cat runtime_reports/golden_path/golden_path_human_report.md
```

## Understanding the Output

| File | Content |
|------|---------|
| `golden_path_600519.json` | Structured machine output |
| `golden_path_600519.md` | Technical pipeline report |
| `golden_path_human_report.md` | Human-readable research report |

## Safety Check

```bash
bash scripts/verify_research_os_architecture_freeze.sh
```

All research is paper-only. Production, broker, runtime, and real trade are permanently blocked.

## Next Steps

1. Read the [User Operation Manual](USER_OPERATION_MANUAL.md)
2. Browse the [Delivery Index](DELIVERY_INDEX.md)
3. Read the [Whitepaper](../research_db/RESEARCH_OS_V3_WHITEPAPER.md)
