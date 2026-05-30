# Test Quality Audit Report

Audit: 2026-05-30T13:57:23.841298+00:00

## Summary
- Total: 1191
- Verdict: **REVIEW_HIGH**

## Distribution
| Category | % | Status |
|----------|:-:|:--:|
| WEAK_TEST | 58.0% | ❌ |
| SAFETY_TEST | 31.3% | ✅ |
| REAL_LOGIC_TEST | 5.8% | ❌ |
| FIXTURE_TEST | 3.6% | ❌ |
| EXISTENCE_TEST | 1.3% | ❌ |

## Thresholds
- REAL_LOGIC >= 35%: ❌
- WEAK <= 15%: ❌

## Finding
- High: REAL_LOGIC low + WEAK high — manual sampling required
- Methodology: heuristic classification, may misclassify. Manual review recommended for Pack B.