# Z-MATRIX Cockpit Web

React/Vite cockpit shell integrated from the design prototype.

## Backend packet bridge

The holdings page can read a backend-exported packet before falling back to local mock data:

```bash
PYTHONPATH=. python3 scripts/cockpit/export_holdings_packet.py \
  --snapshot data/samples/z_prime_holdings_snapshot_2026-06-04.json \
  --output apps/cockpit_web/public/api/cockpit/holdings_packet.json
```

The frontend default packet URL is:

```text
/api/cockpit/holdings_packet.json
```

Override with:

```text
VITE_ZMATRIX_HOLDINGS_PACKET_URL=/api/cockpit/holdings_packet.json
```

The current bridge is read-only and keeps `paperOnly=true`, `brokerRuntime=BLOCKED`, and `realTrade=BLOCKED`.
