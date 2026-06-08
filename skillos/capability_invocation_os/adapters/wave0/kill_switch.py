"""Wave0 Kill Switch — all defaults active. Overrides all requested True.

- Master kill overrides all requested true
- Per-adapter kill overrides individual gate
- Evidence kill blocks evidence sink
- Output kill blocks output generation
- Kill switch check must run before any planned adapter action
- All kills default active or safe-disabled
- Kill false must not enable anything unless future explicit gate exists
"""

from dataclasses import dataclass
from typing import Optional
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


@dataclass
class Wave0KillSwitch:
    """All kills default active (True means BLOCKED)."""
    master: bool = True
    github: bool = True
    docgen: bool = True
    docs: bool = True
    report: bool = True
    evidence: bool = True
    output: bool = True

    def disable_all(self):
        """Activate all kill switches."""
        for attr in vars(self):
            if isinstance(getattr(self, attr), bool):
                setattr(self, attr, True)

    def is_any_active(self) -> bool:
        """True if any kill switch is active."""
        return self.master or self.github or self.docgen or self.docs or self.report

    def is_master_active(self) -> bool:
        return self.master

    def is_adapter_killed(self, kind: Wave0AdapterKind) -> bool:
        """Check if a specific adapter is killed."""
        if self.master:
            return True
        adapter_map = {
            Wave0AdapterKind.GITHUB_READONLY: self.github,
            Wave0AdapterKind.DOCUMENT_GENERATION: self.docgen,
            Wave0AdapterKind.LOCAL_DOCS: self.docs,
            Wave0AdapterKind.REPORT_READING: self.report,
        }
        return adapter_map.get(kind, True)  # unknown = killed

    def is_evidence_killed(self) -> bool:
        """Check if evidence sink is blocked."""
        return self.evidence

    def is_output_killed(self) -> bool:
        """Check if output generation is blocked."""
        return self.output

    def overrides(self, cfg) -> bool:
        """Backward-compatible: True if kill overrides config."""
        return self.is_any_active()


# Module-level singleton (backward-compatible)
_global_kill_switch = Wave0KillSwitch()


def get_kill_switch() -> Wave0KillSwitch:
    return _global_kill_switch


def reset_kill_switch():
    """Reset to all-active default."""
    _global_kill_switch.disable_all()


def ks() -> Wave0KillSwitch:
    """Backward-compatible alias."""
    return _global_kill_switch

# ── Controlled Read-Only Kill ────────────────────────────
def is_controlled_readonly_killed() -> bool:
    from .kill_switch import get_kill_switch
    return get_kill_switch().is_any_active()
