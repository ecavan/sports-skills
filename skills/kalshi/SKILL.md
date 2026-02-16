---
name: kalshi
description: |
  Kalshi prediction markets — events, series, markets, trades, and candlestick data. Public API, no auth required for reads. US-regulated exchange (CFTC).

  Use when: user asks about Kalshi-specific markets, event contracts, or CFTC-regulated prediction markets. Also useful for candlestick/OHLC price history on sports outcomes.
  Don't use when: user asks about actual match results, scores, or statistics — use football-data or fastf1 instead. Don't use for general "who will win" questions unless Kalshi is specifically mentioned — try polymarket first (broader sports coverage). Don't use for news — use sports-news instead.
triggers:
  - kalshi
  - kalshi markets
  - kalshi events
  - prediction market
  - event contracts
---

# Kalshi — Prediction Markets

## Quick Start

```bash
npx skills add sports-skills
```

```python
from sports_skills import kalshi

markets = kalshi.get_markets(series_ticker="KXNBA")
event = kalshi.get_event(event_ticker="KXNBA-26FEB14")
```

Or via CLI:
```bash
sports-skills kalshi get_markets --series_ticker=KXNBA
sports-skills kalshi get_events --series_ticker=KXNBA --status=open
```

## Commands

### get_exchange_status
Get exchange status (trading active, maintenance). No params.

### get_exchange_schedule
Get exchange operating schedule. No params.

### get_series_list
Get all available series.
- `category` (str, optional): Filter by category
- `tags` (str, optional): Filter by tags

### get_series
Get details for a specific series.
- `series_ticker` (str, required): Series ticker (e.g., "KXNBA", "KXMLB")

### get_events
Get events with optional filtering.
- `limit` (int, optional): Max results (default: 100, max: 200)
- `cursor` (str, optional): Pagination cursor
- `status` (str, optional): Filter by status ("open", "closed", "settled")
- `series_ticker` (str, optional): Filter by series ticker
- `with_nested_markets` (bool, optional): Include nested markets

### get_event
Get details for a specific event.
- `event_ticker` (str, required): Event ticker
- `with_nested_markets` (bool, optional): Include nested markets

### get_markets
Get markets with optional filtering.
- `limit` (int, optional): Max results (default: 100)
- `cursor` (str, optional): Pagination cursor
- `event_ticker` (str, optional): Filter by event
- `series_ticker` (str, optional): Filter by series
- `status` (str, optional): Filter ("unopened", "open", "closed", "settled")
- `tickers` (str, optional): Comma-separated market tickers

### get_market
Get details for a specific market.
- `ticker` (str, required): Market ticker

### get_trades
Get recent trades.
- `limit` (int, optional): Max results (default: 100, max: 1000)
- `cursor` (str, optional): Pagination cursor
- `ticker` (str, optional): Filter by market ticker
- `min_ts` (int, optional): After Unix timestamp
- `max_ts` (int, optional): Before Unix timestamp

### get_market_candlesticks
Get OHLC candlestick data.
- `series_ticker` (str, required): Series ticker
- `ticker` (str, required): Market ticker
- `start_ts` (int, required): Start Unix timestamp
- `end_ts` (int, required): End Unix timestamp
- `period_interval` (int, required): Interval in minutes (1, 60, or 1440)

### get_sports_filters
Get available sports filter categories. No params.

## API

- **Base URL:** `https://api.elections.kalshi.com/trade-api/v2`
- All endpoints are public, read-only. No authentication required.
