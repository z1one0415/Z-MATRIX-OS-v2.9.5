# Z-SkillOS Level 3 Integration Failure Isolation Contract

## Status

Z_SKILLOS_LEVEL3_INTEGRATION_FAILURE_ISOLATION_CONTRACT_READY

## Core Rule

Level 3 integration failure must not affect invoke_skill behavior.

## Required Failure Behavior

All failures (config/adapter/observer/writer/redaction) = CONTINUE, no caller warning, no result mutation.

## Required Future Tests

adapter/observer/writer/redaction failures don't change result, don't produce warning, don't produce blocking.

## Final

Failure isolation mandatory.
