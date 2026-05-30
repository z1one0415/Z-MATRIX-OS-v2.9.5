# Agent Workspace Policy

## Default Write Scope
Agent default write path:
```
runtime/agent_workspace/{agent_id}/
```

## Forbidden Write Paths
- zmatrix/
- docs/
- scripts/
- data/research_db/account/raw/
- .github/

## Exception
Write to forbidden paths ONLY through:
```
proposal → approval → execution
```
