# Z-SkillOS Level 3 Result Envelope Non-Mutation Contract

## Status

Z_SKILLOS_LEVEL3_RESULT_ENVELOPE_NON_MUTATION_CONTRACT_READY

## Core Rule

Future invoke_skill integration must not mutate result_envelope.

## Forbidden

Adding Level 3/warning/audit metadata. Changing output/status/error/result. Attaching adapter result. Returning adapter failure.

## Required Future Tests

Disabled/enabled/adapter success/failure/redaction/writer/observer failure all leave result_envelope unchanged.

## Final

Any result_envelope mutation blocks merge.
