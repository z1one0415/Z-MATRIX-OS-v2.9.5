# Data Source Capability Policy

## Capability Fields

| Field | Description |
|-------|------|
| data_source | Source identifier |
| coverage | Data coverage scope |
| historical_depth | How far back data goes |
| pit_safe | PIT-compatible |
| cost | Acquisition cost |
| license | Usage license |
| refresh_frequency | Update interval |
| usable_for_backtest | Can be used in historical backtest |
| usable_for_current_snapshot | Can be used for current analysis |
| usable_for_production | Can enter production (ALWAYS FALSE) |

## Default Sources

| Source | Backtest | Snapshot | Production |
|--------|:--:|:--:|:--:|
| manual_trade_import | true | false | false |
| broker_export_file | true | false | false |
| daily_price_csv | true | true | false |
| industry_mapping_manual | false | true | false |
| financial_current_snapshot | false | true | false |
| event_manual_input | conditional | true | false |
| caseforge_auto_event | false | true | false |
| research_note_manual | false | true | false |
