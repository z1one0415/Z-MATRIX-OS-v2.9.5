# Outcome Horizon Policy

## Horizons

| Horizon | Forward Trading Days | Strict |
|---------|:--:|:--:|
| T1 | 1 | YES |
| T3 | 3 | YES |
| T5 | 5 | YES |
| T10 | 10 | YES |
| T20 | 20 | YES |
| T60 | 60 | YES |

## Strict Rules

- T20 must strictly require 20 forward trading days.
- T60 must strictly require 60 forward trading days.
- Insufficient windows must NOT use last price as fallback.

## Insufficient Window Response

```json
{
  "ready": false,
  "blocked_reason": "INSUFFICIENT_FORWARD_TRADING_DAYS",
  "fallback_last_price_allowed": false
}
```
