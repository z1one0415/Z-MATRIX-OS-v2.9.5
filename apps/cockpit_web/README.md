# Z-MATRIX Cockpit Web

React/Vite cockpit shell integrated from the design prototype.

## Backend packet bridge

The holdings, selection, history, control compass, and Dayan ask pages can read backend-exported packets before falling back to local mock data:

```bash
PYTHONPATH=. python3 scripts/cockpit/export_all_packets.py
```

The frontend default packet URLs are:

```text
/api/cockpit/holdings_packet.json
/api/cockpit/selection_packet.json
/api/cockpit/history_packet.json
/api/cockpit/control_compass_packet.json
/api/cockpit/dayan_ask_packet.json
```

Override with:

```text
VITE_ZMATRIX_PRODUCT_STATUS_URL=http://127.0.0.1:8765/api/product/status.json
VITE_ZMATRIX_OPERATOR_ACTIONS_URL=http://127.0.0.1:8765/api/product/operator_actions.json
VITE_ZMATRIX_RESEARCH_STATUS_URL=http://127.0.0.1:8765/api/product/research_status.json
VITE_ZMATRIX_AGENT_BRIDGE_URL=http://127.0.0.1:8765/api/product/agent_bridge.json
VITE_ZMATRIX_AGENT_DRAFT_URL=http://127.0.0.1:8765/api/product/agent_draft.json
VITE_ZMATRIX_HOLDINGS_PACKET_URL=/api/cockpit/holdings_packet.json
VITE_ZMATRIX_SELECTION_PACKET_URL=/api/cockpit/selection_packet.json
VITE_ZMATRIX_HISTORY_PACKET_URL=/api/cockpit/history_packet.json
VITE_ZMATRIX_CONTROL_COMPASS_PACKET_URL=/api/cockpit/control_compass_packet.json
VITE_ZMATRIX_DAYAN_ASK_PACKET_URL=/api/cockpit/dayan_ask_packet.json
```

The settings page reads product runtime status from `VITE_ZMATRIX_PRODUCT_STATUS_URL`.
It reads local workstation action cards from `VITE_ZMATRIX_OPERATOR_ACTIONS_URL`.
It reads research capability status cards from `VITE_ZMATRIX_RESEARCH_STATUS_URL`.
It reads the read-only Hermes bridge status from `VITE_ZMATRIX_AGENT_BRIDGE_URL`.
It posts research questions for local draft generation to `VITE_ZMATRIX_AGENT_DRAFT_URL`.
If the local backend is not running, the page falls back to a degraded offline preview.

The current bridge is read-only. Local workstation action cards expose copyable commands, but the browser does not start shell tasks by itself. The safety state keeps `paperOnly=true`, `brokerRuntime=BLOCKED`, and `realTrade=BLOCKED`.
