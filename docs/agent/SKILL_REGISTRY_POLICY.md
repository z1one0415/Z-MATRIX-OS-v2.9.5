# Skill Registry Policy

## Rules
- Every skill must be registered before use
- unknown skill → REJECT
- disabled skill → REJECT
- production_allowed=true → ERROR
- write_layers non-empty → requires_human_review=true
- verify_script missing and risk_level>=R3 → ERROR

## Skill Domains
ACCOUNT_TRUTH, MARKET_OUTCOME, FACTOR_FACTORY, AUTOCASEFORGE,
ZC35_CATALYST, B_MATRIX, R_MATRIX, D_MATRIX, Z_G16_PHYSICAL,
REPORTING, RESEARCH_COUNCIL, COCKPIT, SYSTEM_VERIFY

## Registry Fields
- skill_id, skill_name, domain, version
- input_schema_ref, output_schema_ref
- allowed_callers, risk_level, requires_human_review
- read_layers, write_layers, verify_script
- enabled, production_allowed
