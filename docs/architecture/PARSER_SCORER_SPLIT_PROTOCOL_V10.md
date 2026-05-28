# ZC00 PARSER-SCORER SPLIT PROTOCOL V10

## Core Principle
LLM reads the world. Z-MATRIX computes the world.

## LLM Output Restrictions
LLM models may ONLY output:
- BOOL
- ENUM
- FACTUAL_NUMBER (raw data, not derived scores)
- DATE
- TEXT_SPAN (quoted evidence)
- EVIDENCE_REF (pointer to source)
- AMBIGUITY_FLAG
- MISSING_EVIDENCE
- CONTRADICTION_FLAG

## LLM Output BAN
LLM models MUST NOT output any subjective continuous score:
- moat_score, risk_score, support_score, growth_score
- buy_score, sell_score, conviction_score, recommendation_score
- catalyst_score, event_power_score, hedge_score, defensive_score
- fillability_score, expected_return, position_size
- target_weight, probability_of_success

## Scoring Pipeline
FactExtractionModel → FeatureNormalizer → DeterministicScorer → ScoreTrace → Review

## Applicable
All batches (0-5). Any violation blocks the batch.
