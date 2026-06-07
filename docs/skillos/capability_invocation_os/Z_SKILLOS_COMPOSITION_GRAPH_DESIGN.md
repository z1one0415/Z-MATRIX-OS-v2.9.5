# Z-SkillOS Composition Graph Design

## Status

Z_SKILLOS_COMPOSITION_GRAPH_DESIGN_READY

## Scope

FUTURE_PLAN_ONLY. Safe chaining of Z-MATRIX skills. No implementation.

## Composition Types

| Type | Description | Example |
|:--|:--|:--|
| Sequential | A → B → C, evidence handoff at each step | Z2 → V3 → Z9 |
| Parallel | A ∥ B, independent branches | D-Matrix ∥ R-Matrix |
| Conditional | if A.output then B else C | Risk check → recommend or deny |
| Forbidden | Blocked by policy | Anything touching T5 |

## Composition Examples

| Chain | Skills | Evidence Flow |
|:--|:--|:--|
| Z2 → V3 → Z9 | Research → Quant → Predict | Score pipeline |
| Deal Compass → HTML | Analysis → Report | Report generation |
| World Blocks → Evidence | Design → Audit | Validation chain |
| GitHub → Patch → Seal | Audit → Fix → Lock | Engineering chain |

## Safety Rules

| Rule | Description |
|:--|:--|
| Conflict detection | Detect conflicting skill requirements |
| Evidence handoff | Each step captures evidence for next |
| Downstream override | Later steps can override earlier assumptions |
| Failure degrade | Single failure degrades, never blocks |
| Incremental seal | Each composition gets its own seal |

## No implementation. Level 5 remains BLOCKED.
