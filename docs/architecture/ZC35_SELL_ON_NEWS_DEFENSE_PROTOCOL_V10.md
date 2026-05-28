# ZC35 SELL-ON-NEWS DEFENSE PROTOCOL V10

## Detection Rules
1. Pre-event price appreciation > 20% in 20 days → elevated sell-on-news risk
2. Evidence level D → sell-on-news risk HIGH regardless of price
3. Multiple overlapping events on same ticker → residual_power capped at 0.5
4. Post-event volume collapse → signal expiry

## Actions
- sell_on_news_risk HIGH: PAPER_ONLY_OBSERVE
- sell_on_news_risk MEDIUM: reduce position size, shorten horizon
- sell_on_news_risk LOW: normal catalyst lifecycle tracking

## Forbidden
- BUY before event without sell-on-news check
- AUTO_BUY on event announcement
- Real trade based on pre-event price run-up
