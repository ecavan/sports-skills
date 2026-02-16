---
name: polymarket
description: |
  Polymarket sports prediction markets — live odds, prices, order books, events, series, and market search. No auth required.

  Use when: user asks about sports betting odds, prediction markets, win probabilities, or market sentiment for upcoming games/events. Good for "who is favored to win" questions.
  Don't use when: user asks about actual match results, scores, or statistics — use football-data or fastf1 instead. Don't use for historical match data. Don't use for news — use sports-news instead. Don't confuse with Kalshi — Polymarket focuses on crypto-native prediction markets with deeper sports coverage; Kalshi is a US-regulated exchange with different market structure.
triggers:
  - polymarket
  - prediction market
  - sports odds
  - market prices
  - betting odds
---

# Polymarket — Sports Prediction Markets

## Quick Start

```bash
npx skills add sports-skills
```

```python
from sports_skills import polymarket

markets = polymarket.get_sports_markets(limit=20)
prices = polymarket.get_market_prices(token_id="abc123")
```

Or via CLI:
```bash
sports-skills polymarket get_sports_markets --limit=20
sports-skills polymarket search_markets --query="NBA Finals"
```

## Commands

### get_sports_markets
Get active sports prediction markets.
- `limit` (int, optional): Max results (default: 50, max: 100)
- `offset` (int, optional): Pagination offset
- `sports_market_types` (str, optional): Filter by type ("moneyline", "spreads", "totals")
- `game_id` (str, optional): Filter by game
- `active` (bool, optional): Only active markets (default: true)
- `closed` (bool, optional): Include closed markets (default: false)
- `order` (str, optional): Sort field (default: "volume")
- `ascending` (bool, optional): Sort ascending (default: false)

### get_sports_events
Get sports events (each groups related markets).
- `limit`, `offset`, `active`, `closed`, `order`, `ascending` (same as above)
- `series_id` (str, optional): Filter by series (league) ID

### get_series
Get all series (leagues, recurring event groups).
- `limit` (int, optional): Max results (default: 100)
- `offset` (int, optional): Pagination offset

### get_market_details
Get detailed info for a specific market.
- `market_id` (str): Market ID
- `slug` (str): Market slug (alternative to ID)

### get_event_details
Get detailed info for a specific event.
- `event_id` (str): Event ID
- `slug` (str): Event slug (alternative to ID)

### get_market_prices
Get current prices from the CLOB API.
- `token_id` (str): Single CLOB token ID
- `token_ids` (list): Multiple CLOB token IDs (batch)

### get_order_book
Get full order book for a market.
- `token_id` (str, required): CLOB token ID

### get_sports_market_types
Get all valid sports market types. No params.

### search_markets
Find markets by keyword and filters.
- `query` (str, optional): Keyword to search
- `sports_market_types` (str, optional): Filter by type
- `tag_id` (int, optional): Tag ID (default: 1 = Sports)
- `limit` (int, optional): Max results (default: 20)

### get_price_history
Get historical price data.
- `token_id` (str, required): CLOB token ID
- `interval` (str, optional): Time range ("1d", "1w", "1m", "max"). Default: "max"
- `fidelity` (int, optional): Seconds between data points. Default: 120

### get_last_trade_price
Get the most recent trade price.
- `token_id` (str, required): CLOB token ID

## APIs

- **Gamma API** (gamma-api.polymarket.com): Market metadata, events, series. Public, no auth.
- **CLOB API** (clob.polymarket.com): Prices, order books, trades. Public reads, no auth.
