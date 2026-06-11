# Safety Boundary — Z-SkillOS Frontend Dashboard

## A1_CONTRACT_FREEZE — Permanent Restrictions

### Runtime
- **DISABLED_DEFAULT** — No pipeline/runner execution

### Runner
- **DISABLED** — All pipeline runners muted

### Paper Trading
- **DISABLED** — No simulated trading

### Production
- **BLOCKED** — No production deployment

### Broker
- **BLOCKED** — No broker connection

### Real Trade
- **BLOCKED** — No actual trades

## Enforcement Mechanisms

### 1. API Layer
- `client.ts` throws on any non-GET method attempt
- Runtime check before every `fetch()` call

### 2. UI Layer
- No buy/sell/order/position buttons rendered
- No broker connection interfaces
- No trade confirmation dialogs

### 3. Component Layer
- `SafetyBadge` component on every page
- `readonly` and `disabled-default` badges in topbar
- RESTRICTIONS banner on home and settings pages
- `BlockedActionPanel` lists all 48 blocked actions

### 4. Schema Level
- All Zod schemas enforce `readonly: z.literal(true)`
- All Zod schemas enforce `enabled_count: z.literal(0)` where applicable
