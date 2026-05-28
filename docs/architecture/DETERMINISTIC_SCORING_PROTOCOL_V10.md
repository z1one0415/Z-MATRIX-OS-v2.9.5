# ZC00 DETERMINISTIC SCORING PROTOCOL V10

## Rule
ALL scores used for strategy decisions MUST be computed by deterministic code.

## Pipeline
1. FactExtractionModel (LLM: BOOL/ENUM/FACTUAL only)
2. FeatureNormalizer (deterministic: normalize to 0-1 or z-score)
3. DeterministicScorer (deterministic: weighted sum, rule-based)
4. ScoreTrace (deterministic: record all intermediate values)
5. Review (human or governance gate)

## Trace Requirements
- Every score must have: input_facts, formula, intermediate_values, final_score
- ScoreTrace must be machine-parseable (JSON)
- Audit must be able to reproduce the score from the trace alone

## Violations
Any module that skips the deterministic scorer and uses LLM output
directly as a score is BLOCKED from entering any batch.
