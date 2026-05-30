# Data Trust Level Policy

## Levels

| Level | Name | Description | Usable For |
|:-----:|------|------|------|
| T0 | RAW_IMPORT | Raw imported, format unchecked | Storage only |
| T1 | FORMAT_VALIDATED | Fields valid, source unchecked | Internal review |
| T2 | SOURCE_VALIDATED | Source trusted, fields explained | Research |
| T3 | CROSS_SOURCE_VALIDATED | Cross-source consistent | High-confidence research |
| T4 | OUTCOME_VALIDATED | Verified against outcomes | Factor/case analysis |
| T5 | RESEARCH_ACCEPTED | Cross-case cross-sample validated | Research rule |

## Rules

- T0/T1 data must NOT enter factor promotion.
- T0/T1 data must NOT enter conclusive reports.
- Unmarked trust_level data must NOT enter ResearchDB main flow.
- T4+ required for factor_validation.
- T5 required for rule promotion.
