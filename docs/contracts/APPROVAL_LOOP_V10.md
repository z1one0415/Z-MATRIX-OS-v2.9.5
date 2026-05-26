# Approval Loop Contract v1.0 — Approval-Required Reflection Loop

## Purpose

Approval Loop is the safety gate for v3.0 self-evolution.
MemoryCandidate / CalibrationEvent / PromptPatch must pass human approval
before they can enter the "write candidate" zone.

## Current Version

This version does NOT execute automatic writes.
APPROVE only records human approval — it does NOT:
- Write Hermes memory
- Auto calibrate parameters
- Auto inject prompts
- Auto trade

## Link

MemoryCandidatePreview → ApprovalRequest → HumanApprovalDecision → HumanApprovalEvent → EventStore

## Event Types

- ApprovalRequestEvent records approval request creation.
- HumanApprovalEvent records human approval decisions.
- MemoryCandidateEvent must NOT be used for approval requests.
