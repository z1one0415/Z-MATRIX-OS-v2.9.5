"""Prompt Middleware v1.0 — Prompt Hot-Patching Middleware Preview (v2.9.14-dev)

Prompt Middleware provides a preview-only, auditable pipeline for
rendering prompt patches as middleware. This version does NOT:
- Write real system prompts
- Inject into OpenClaw runtime
- Modify prompt configuration files
- Auto-activate any patches
"""
from __future__ import annotations

__version__ = "PROMPT_MIDDLEWARE_V10"
