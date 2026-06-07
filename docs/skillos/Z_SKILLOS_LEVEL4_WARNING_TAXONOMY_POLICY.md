# Z-SkillOS Level 4 Warning Taxonomy Policy

## Status

Z_SKILLOS_LEVEL4_WARNING_TAXONOMY_POLICY_READY

## Categories

SCHEMA_DRIFT, HASH_DRIFT, GOLDEN_MISMATCH, SEMANTIC_DRIFT, RETENTION_BOUND, PRIVACY_REJECTION, OBSERVATION_FAILURE, ADAPTER_FAILURE, CLEANUP_SAFETY, LIFECYCLE_INCOMPLETE.

## Required Fields

warning_id, category, severity, source_gate, evidence_ref, recommended_action, caller_visibility, rollback_policy, created_by.

## Forbidden Fields

raw_prompt/user_data/output, account/broker/trading credentials, production secrets, real_trade payload, PII.

## Rules

No emission. No caller visibility. No envelope mutation.
