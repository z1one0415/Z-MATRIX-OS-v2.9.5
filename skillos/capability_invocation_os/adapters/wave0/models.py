"""Wave0 internal models — no execution, no envelope mutation, no caller output."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List
class Wave0AdapterKind(Enum): GITHUB_READONLY=1; DOCUMENT_GENERATION=2; LOCAL_DOCS=3; REPORT_READING=4
class Wave0Permission(Enum): READ_ONLY=1; GENERATION_ONLY=2; DENY=0
@dataclass(frozen=True)
class Wave0Request: kind:Wave0AdapterKind=Wave0AdapterKind.GITHUB_READONLY; inputs:dict=field(default_factory=dict)
@dataclass(frozen=True)
class Wave0Decision: action:str="DENY"; reason:str="disabled"
@dataclass(frozen=True)
class Wave0EvidenceSpec: pre_hash:str=""; post_hash:str=""
@dataclass(frozen=True)
class GitHubReadOnlyPlan: future_actions:List[str]=field(default_factory=lambda:["fetch_file","fetch_commit_metadata","compare_refs","list_changed_files","inspect_branch_head","inspect_commit_message"]); forbidden_actions:List[str]=field(default_factory=lambda:["create_file","update_file","delete_file","merge_branch","update_branch","issue_comment","pr_comment","secret_access"])
@dataclass(frozen=True)
class DocumentGenerationPlan: future_outputs:List[str]=field(default_factory=lambda:["markdown","html","report","structured_summary"]); forbidden_outputs:List[str]=field(default_factory=lambda:["external_publish","filesystem_write","result_envelope_mutation"])
@dataclass(frozen=True)
class LocalDocsInspectionPlan: future_actions:List[str]=field(default_factory=lambda:["read_docs","search_docs","extract_status_strings","verify_seal_strings","compare_expected_status"]); forbidden_actions:List[str]=field(default_factory=lambda:["file_mutation","runtime_artifact_creation","directory_mutation"])
@dataclass(frozen=True)
class ReportReadingPlan: future_actions:List[str]=field(default_factory=lambda:["parse_report","extract_evidence","compare_status","summarize_risks","identify_mismatch"]); forbidden_actions:List[str]=field(default_factory=lambda:["report_write","execution","data_mutation"])
