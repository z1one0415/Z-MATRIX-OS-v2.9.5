# Z-SkillOS Frontend Dashboard — README

> Version: v0.1.0-rc | Seal: A1_CONTRACT_FREEZE | 2026-06-12

## Overview

The Z-SkillOS Frontend Dashboard is a **read-only safety boundary viewer** for the Z-MATRIX-OS v2.9.5+ platform.

### Safety Guarantees

- **All API calls are GET-only** — POST/PUT/PATCH/DELETE blocked at runtime
- **All dangerous actions disabled** — No buy/sell/order/position buttons
- **No trade language rendered** — No trading terminology in UI
- **Safety boundary enforced** — DISABLED_DEFAULT, BLOCKED badges everywhere

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | React 18 + TypeScript |
| Build | Vite 5 |
| Styling | Tailwind CSS 3 |
| Routing | React Router 6 |
| Data Fetching | TanStack Query |
| Validation | Zod |
| Charts | Recharts |

## Pages (11 total)

| Route | Page | Description |
|-------|------|-------------|
| `/` | HomeDashboard | System overview, gates, RESTRICTIONS banner |
| `/capabilities` | CapabilityInvocationOS | Skill catalog (read-only) |
| `/factor-library` | FactorLibrary | 23 factors, diagnostic-only |
| `/composition-graph` | CompositionGraph | B1 graph summary |
| `/research-report` | ResearchReportNode | Z2 report sections preview |
| `/z9-review` | Z9ReviewNode | Z9 review status, disabled-default |
| `/evidence-chain` | EvidenceChain | Evidence chain traversal |
| `/run-state` | RunStateRegistry | Pipeline run state viewer |
| `/gate-state` | GateStateRegistry | Gate pass/fail/pending |
| `/audit-trail` | AuditTrail | Audit log viewer |
| `/settings` | SafetyBoundary | All blocked actions, safety flags |

## Development

```bash
# Install
npm install

# Dev server
npm run dev

# Build
npm run build

# Lint
npm run lint
```

## File Structure

```
apps/z-skillos-dashboard/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── styles/globals.css
    ├── api/
    │   ├── client.ts        # GET-only fetch wrapper
    │   ├── endpoints.ts     # 15 typed API functions
    │   ├── schemas.ts       # Zod validation schemas
    │   └── mockClient.ts    # Mock data for offline dev
    ├── app/
    │   ├── router.tsx       # 11 routes
    │   ├── layout.tsx       # Main layout
    │   ├── sidebar.tsx      # Navigation sidebar
    │   └── topbar.tsx       # Status bar
    ├── pages/               # 11 page components
    └── components/
        ├── cards/           # SummaryCard, MetricCard
        ├── status/          # StatusBadge, SafetyBadge
        ├── evidence/        # EvidenceCard
        ├── gates/           # GateTimeline
        ├── charts/          # GateStatusChart
        ├── layout/          # BlockedActionPanel
        ├── empty/           # EmptyState
        └── errors/          # DegradedState
```

## Contracts

Referenced from `skillos/frontend_handoff/contracts/`:
- `dashboard_contract.json`
- `navigation_contract.json`
- `page_data_contract.json`
- `error_abort_degraded_contract.json`
- `component_state_contract.json`
- `api_schema.json`

## Fixtures

Mock data from `skillos/frontend_handoff/fixtures/`:
- 12 JSON files covering all API responses
