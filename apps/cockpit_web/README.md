# Z-MATRIX Cockpit Web

React/Vite cockpit shell integrated from the design prototype.

## Backend packet bridge

The holdings, selection, and history pages can read backend-exported packets before falling back to local mock data:

```bash
PYTHONPATH=. python3 scripts/cockpit/export_all_packets.py
```

The frontend default packet URLs are:

```text
/api/cockpit/holdings_packet.json
/api/cockpit/selection_packet.json
/api/cockpit/history_packet.json
```

Override with:

```text
VITE_ZMATRIX_HOLDINGS_PACKET_URL=/api/cockpit/holdings_packet.json
VITE_ZMATRIX_SELECTION_PACKET_URL=/api/cockpit/selection_packet.json
VITE_ZMATRIX_HISTORY_PACKET_URL=/api/cockpit/history_packet.json
```

The current bridge is read-only and keeps `paperOnly=true`, `brokerRuntime=BLOCKED`, and `realTrade=BLOCKED`.
