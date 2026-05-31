# allowlist: forbidden-token-definition
"""Agent Workspace Guard — ensures agents can only write to their own workspace"""
from __future__ import annotations

import os
from pathlib import Path

FORBIDDEN_PATHS = [
    "zmatrix/",
    "docs/",
    "scripts/",
    "data/research_db/account/raw/",
    ".github/",
]


def get_agent_workspace_path(agent_id: str) -> str:
    cwd = os.getcwd()
    return os.path.join(cwd, "runtime", "agent_workspace", agent_id)


def is_write_allowed(agent_id: str, target_path: str) -> bool:
    workspace = get_agent_workspace_path(agent_id)
    resolved_workspace = os.path.realpath(workspace)
    resolved_target = os.path.realpath(target_path)
    if not resolved_target.startswith(resolved_workspace + os.sep) and resolved_target != resolved_workspace:
        return False
    relative = os.path.relpath(resolved_target, os.getcwd())
    for forbidden in FORBIDDEN_PATHS:
        if relative == forbidden.rstrip("/") or relative.startswith(forbidden):
            return False
    return True


def validate_write_target(agent_id: str, target_file: str) -> dict:
    workspace = get_agent_workspace_path(agent_id)
    resolved_workspace = os.path.realpath(workspace)
    resolved_target = os.path.realpath(target_file)
    if not resolved_target.startswith(resolved_workspace + os.sep) and resolved_target != resolved_workspace:
        return {"allowed": False, "reason": "write target outside agent workspace"}
    relative = os.path.relpath(resolved_target, os.getcwd())
    for forbidden in FORBIDDEN_PATHS:
        if relative == forbidden.rstrip("/") or relative.startswith(forbidden):
            return {"allowed": False, "reason": f"write target in forbidden path: {forbidden}"}
    return {"allowed": True, "reason": ""}
