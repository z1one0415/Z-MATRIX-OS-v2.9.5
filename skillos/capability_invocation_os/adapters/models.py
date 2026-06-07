"""Adapter Framework internal models — no execution, no caller output, no envelope mutation."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class AdapterMode(Enum): DISABLED=0; READ_ONLY=1; PLANNING_ONLY=2; RESEARCH_ONLY=3; ADVISORY_ONLY=4

class AdapterRiskTier(Enum): T0=0; T1=1; T2=2; T3=3; T4=4; T5=5

class AdapterPermissionTier(Enum): DENY=0; READ_ONLY=1; PLANNING_ONLY=2; RESEARCH_ONLY=3; ADVISORY=4; NO_TRADE=5; NO_WRITE=6; NO_PRODUCTION=7; NEVER_REAL_TRADE=8

@dataclass(frozen=True)
class AdapterId: namespace: str = ""; adapter_name: str = ""

@dataclass(frozen=True)
class AdapterContract: skill_id:str=""; risk_tier:AdapterRiskTier=AdapterRiskTier.T5; permission_tier:AdapterPermissionTier=AdapterPermissionTier.DENY; forbidden_actions:List[str]=field(default_factory=list); human_approval_required:bool=True

@dataclass(frozen=True)
class AdapterDescriptor: adapter_id:AdapterId=field(default_factory=AdapterId); mode:AdapterMode=AdapterMode.DISABLED; contract:AdapterContract=field(default_factory=AdapterContract)

@dataclass(frozen=True)
class AdapterRequest: adapter_id:AdapterId=field(default_factory=AdapterId); inputs:dict=field(default_factory=dict); caller_role:str=""

@dataclass(frozen=True)
class AdapterDecision: action:str="DENY"; reason:str="disabled by default"; evidence_required:bool=True

@dataclass(frozen=True)
class AdapterValidationResult: valid:bool=False; errors:List[str]=field(default_factory=list)

@dataclass(frozen=True)
class AdapterEvidenceSpec: pre_hash:str=""; post_hash:str=""; source_snapshot:str=""
