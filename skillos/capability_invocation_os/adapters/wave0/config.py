"""Wave0 Execution Enablement Config — strict requested/enabled separation.

All enabled functions return False in P0.
Requested flags record intent only — no enablement.
Non-bool truthy, env override, malformed config, missing config → disabled.
Default: false. No default true.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Wave0ExecutionConfig:
    """All True values stored as requested only. Enabled is always False in P0."""

    # Requested flags (record intent, never enable)
    wave0_runtime_requested: bool = False
    wave0_adapter_framework_requested: bool = False
    wave0_github_readonly_requested: bool = False
    wave0_document_generation_requested: bool = False
    wave0_local_docs_inspection_requested: bool = False
    wave0_report_reading_requested: bool = False

    @classmethod
    def from_dict(cls, d: Optional[Dict[str, Any]] = None) -> "Wave0ExecutionConfig":
        if not isinstance(d, dict):
            return cls()
        c = cls()
        strict_bool_keys = [
            ("wave0_runtime_requested", "WAVE0_RUNTIME_ENABLED"),
            ("wave0_adapter_framework_requested", "WAVE0_ADAPTER_FRAMEWORK_ENABLED"),
            ("wave0_github_readonly_requested", "WAVE0_GITHUB_READONLY_ENABLED"),
            ("wave0_document_generation_requested", "WAVE0_DOCUMENT_GENERATION_ENABLED"),
            ("wave0_local_docs_inspection_requested", "WAVE0_LOCAL_DOCS_INSPECTION_ENABLED"),
            ("wave0_report_reading_requested", "WAVE0_REPORT_READING_ENABLED"),
        ]
        for attr, key in strict_bool_keys:
            v = d.get(key, False)
            # strict: only True (the bool) is accepted as requested
            if isinstance(v, bool) and v is True:
                setattr(c, attr, True)
            # non-bool, truthy string, None, anything else → not requested
        return c


# ── Enabled functions — ALL return False in P0 ──────────────────────────

def is_wave0_runtime_enabled(cfg: Wave0ExecutionConfig) -> bool:
    """P0: always False. No env override. No config bypass."""
    return False


def is_wave0_adapter_framework_enabled(cfg: Wave0ExecutionConfig) -> bool:
    """P0: always False."""
    return False


def is_github_readonly_execution_enabled(cfg: Wave0ExecutionConfig) -> bool:
    """P0: always False."""
    return False


def is_document_generation_execution_enabled(cfg: Wave0ExecutionConfig) -> bool:
    """P0: always False."""
    return False


def is_local_docs_inspection_execution_enabled(cfg: Wave0ExecutionConfig) -> bool:
    """P0: always False."""
    return False


def is_report_reading_execution_enabled(cfg: Wave0ExecutionConfig) -> bool:
    """P0: always False."""
    return False


# ── Backward-compatible aliases (for existing callers) ───────────────────

def load(d: Optional[Dict[str, Any]] = None) -> Wave0ExecutionConfig:
    return Wave0ExecutionConfig.from_dict(d)


def is_wave0_enabled(cfg: Wave0ExecutionConfig) -> bool:
    return False


def is_github_readonly_enabled(cfg: Wave0ExecutionConfig) -> bool:
    return False


def is_document_generation_enabled(cfg: Wave0ExecutionConfig) -> bool:
    return False


def is_local_docs_inspection_enabled(cfg: Wave0ExecutionConfig) -> bool:
    return False


def is_report_reading_enabled(cfg: Wave0ExecutionConfig) -> bool:
    return False


def env_override() -> bool:
    """Environment cannot enable. Always False."""
    return False

class Wave0Config:
    """Backward-compatible wrapper."""
    def __init__(self, s=None):
        self._exec = Wave0ExecutionConfig.from_dict(s) if isinstance(s, dict) else Wave0ExecutionConfig()


# ── Controlled Read-Only Execution flags (P0: all disabled) ────────
def is_controlled_readonly_enabled(cfg) -> bool: return False
def is_controlled_report_reading_enabled(cfg) -> bool: return False
def is_controlled_document_generation_enabled(cfg) -> bool: return False
def is_controlled_local_docs_inspection_enabled(cfg) -> bool: return False
def is_controlled_github_metadata_enabled(cfg) -> bool: return False


# ── Controlled Read-Only ────────────────────────────────
def is_controlled_readonly_enabled(cfg) -> bool: return False
def is_controlled_report_reading_enabled(cfg) -> bool: return False
def is_controlled_document_generation_enabled(cfg) -> bool: return False
def is_controlled_local_docs_inspection_enabled(cfg) -> bool: return False
def is_controlled_github_metadata_enabled(cfg) -> bool: return False
