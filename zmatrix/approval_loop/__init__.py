"""Approval Loop v1.0 — Approval-Required Reflection Loop (v2.9.13-dev)

Approval Loop provides the safety gate for v3.0 self-evolution.
MemoryCandidate / CalibrationEvent / PromptPatch must pass human approval
before they can enter the "write candidate" zone in future versions.

This version does NOT execute automatic writes.
"""
from __future__ import annotations

__version__ = "APPROVAL_LOOP_V10"
