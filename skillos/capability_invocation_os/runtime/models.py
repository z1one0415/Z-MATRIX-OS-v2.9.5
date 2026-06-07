"""Capability Invocation OS internal data models."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class RiskTier(Enum): T0=0; T1=1; T2=2; T3=3; T4=4; T5=5

class PermissionTier(Enum): DENY=0; READONLY=1; ANALYSIS=2; CODE_LOCAL=3; ADVISORY=4; EXTERNAL=5; BLOCKED=6

@dataclass(frozen=True)
class CapabilityId: module: str = ""; capability_name: str = ""

@dataclass(frozen=True)
class CapabilityContract:
    skill_id: str = ""; risk_tier: RiskTier = RiskTier.T5; permission_required: PermissionTier = PermissionTier.BLOCKED
    forbidden_actions: List[str] = field(default_factory=list); human_approval_required: bool = True

@dataclass(frozen=True)
class InvocationRequest: capability_id: CapabilityId = field(default_factory=CapabilityId); caller_role: str = ""; inputs: dict = field(default_factory=dict)

@dataclass(frozen=True)
class InvocationDecision: action: str = "DENY"; reason: str = "disabled by default"; evidence_required: bool = True

@dataclass
class EvidenceRecord: invocation_id: str = ""; pre_hash: str = ""; post_hash: str = ""; outcome: str = "CAPTURED"

@dataclass(frozen=True)
class GuardResult: action: str = "CONTINUE"; stage_results: List[str] = field(default_factory=list); degraded: bool = True
