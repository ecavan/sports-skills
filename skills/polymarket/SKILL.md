---
name: polymarket
description: Polymarket prediction market data for sports including markets, events, series, real-time prices, order books, and trade history. Covers 58+ market types across NFL, NBA, MLB, Soccer, Tennis, Cricket, MMA, and Esports. Use when the user asks about Polymarket odds, sports prediction markets, betting probabilities, market prices, or order book data on Polymarket. Public endpoints only, no API key required.
---

# Polymarket

Public prediction market data from Polymarket. Two APIs: Gamma (market metadata) and CLOB (real-time prices and order books). No API key required for all read endpoints.

**Gamma API:** `https://gamma-api.polymarket.com`
**CLOB API:** `https://clob.polymarket.com`

## Supported Sports Market Types

58+ types including: `moneyline`, `spreads`, `totals`, `double_chance`, `correct_score`, `parlays`, `anytime_touchdowns`, `passing_yards`, `points`, `rebounds`, `assists`, `threes`, `nrfi`, `total_goals`, `both_teams_to_score`, `total_corners`, `ufc_method_of_victory`, and more.

## Commands

### Markets (Gamma API)

**get_sports_markets** - Get active sports prediction markets with optional filtering.

```
Params:
  tag_id (int, optional, default: 1) - Tag ID (1 = Sports)
  limit (int, optional, default: 50, max: 100)
  offset (int, optional, default: 0)
  sports_market_types (string, optional) - Filter by type (e.g. "moneyline", "spreads")
  game_id (string, optional) - Filter by specific game
  active (bool, optional, default: true)
  closed (bool, optional, default: false)
  order (string, optional, default: "volume") - Sort field
  ascending (bool, optional, default: false)
Returns: { markets: [{
  id, question, description, slug, status,
  outcomes: [{ name, price, clob_token_id }],
  volume, volume_24h, liquidity, spread,
  start_date, end_date, sports_market_type, game_id, tags
}], count, offset }
```

**get_market_details** - Get detailed information for a specific market.

```
Params:
  market_id (string) - Market ID (numeric)
  slug (string) - Market slug (alternative to ID)
  (at least one required)
Returns: { id, question, description, slug, status, outcomes, volume, ... }
```

**search_markets** - Find markets by filtering events and markets with tag and keyword parameters. The `/search` endpoint requires authentication, so discovery uses the events and markets endpoints with filters instead.

```
Approach: Use get_sports_events or get_sports_markets with filters.
To find a specific market (e.g. "NBA Finals"):
  1. Call get_sports_events with tag_id=1 and order=volume to browse top events
  2. Call get_event_details on a matching event to see all its markets
  3. Or call get_sports_markets with sports_market_types filter (e.g. "moneyline")
```

### Events (Gamma API)

**get_sports_events** - Get sports events. Each event groups related markets.

```
Params:
  tag_id (int, optional, default: 1) - Tag ID (1 = Sports)
  limit (int, optional, default: 50, max: 100)
  offset (int, optional, default: 0)
  active (bool, optional, default: true)
  closed (bool, optional, default: false)
  order (string, optional, default: "volume")
  ascending (bool, optional, default: false)
  series_id (string, optional) - Filter by series (league)
Returns: { events: [{
  id, title, description, slug, status,
  start_date, end_date, volume, liquidity,
  market_count, markets: [...], tags, series_id
}], count, offset }
```

**get_event_details** - Get a specific event with all nested markets.

```
Params:
  event_id (string) - Event ID
  slug (string) - Event slug (alternative to ID)
  (at least one required)
Returns: { id, title, description, markets: [...], ... }
```

### Series (Gamma API)

**get_series** - Get all series (leagues, recurring event groups).

```
Params:
  limit (int, optional, default: 100, max: 200)
  offset (int, optional, default: 0)
Returns: { series: [{ id, title, slug, description, image }], count }
```

### Market Types (Gamma API)

**get_sports_market_types** - Get all valid sports market types.

```
Params: none
Returns: list of valid market type strings
```

### Prices (CLOB API)

**get_market_prices** - Get real-time prices for one or more markets.

```
Params:
  token_id (string) - Single CLOB token ID
  token_ids (list) - Multiple CLOB token IDs (batch, max 20)
  (at least one required)
Returns (single): { token_id, midpoint, buy_price, sell_price }
Returns (batch): { prices: [{ token_id, midpoint }], count }
```

CLOB token IDs are found in market data under `clob_token_ids` or `outcomes[].clob_token_id`.

### Order Book (CLOB API)

**get_order_book** - Get the full order book for a market.

```
Params:
  token_id (string, required) - CLOB token ID
Returns: {
  token_id, best_bid, best_ask, spread,
  bids: [{ price, size }],
  asks: [{ price, size }],
  bid_depth, ask_depth
}
```

### Price History & Last Trade (CLOB API)

**get_price_history** - Get historical price data for a market over time.

```
Params:
  token_id (string, required) - CLOB token ID
  interval (string, optional, default: "max") - Time range ("1d", "1w", "1m", "max")
  fidelity (int, optional, default: 120) - Data point density (seconds between points)
Returns: { history: [{ t: timestamp, p: price }], count }
```

**get_last_trade_price** - Get the most recent trade price for a market.

```
Params:
  token_id (string, required) - CLOB token ID
Returns: { token_id, price, side }
```

## Workflow: Finding Sports Market Odds

1. Call `get_sports_events` with `tag_id=1` and `order=volume` to browse top sports events
2. Pick an event and call `get_event_details` to see all markets for it
3. For real-time pricing, take `clob_token_ids` from a market and call `get_market_prices`
4. For order book depth, call `get_order_book` with a specific token ID
5. For price history, call `get_price_history` with a CLOB token ID

To narrow by sport type, use `get_sports_markets` with `sports_market_types` filter (e.g. "moneyline", "spreads", "totals").

## Caching & Rate Limits

- Gamma API: Cached for 120s (markets/events), 600s (series), 60s (details)
- CLOB API: Cached for 30s (prices and order books refresh frequently)
- Rate limits are generous: 4,000 req/10s (Gamma general), 1,500 req/10s (CLOB price endpoints)

## Known Limitations

- The Gamma `/search` endpoint now requires authentication (token/cookies). Use `get_sports_events` and `get_sports_markets` with filters for market discovery instead.
- The `/core/trades` endpoint has been removed. Use `get_price_history` and `get_last_trade_price` via the CLOB API for trade/price data.

## Usage Examples

Browse sports markets:
> "What sports markets are live on Polymarket right now?"
> Uses: get_sports_markets

Find specific game odds:
> "What are the Polymarket odds for the Champions League final?"
> Uses: get_sports_events with tag_id=1, then get_event_details on the matching event

Check real-time prices:
> "What's the current price on this Polymarket market?"
> Uses: get_market_prices with the CLOB token ID

View order book:
> "Show me the order book depth for this market"
> Uses: get_order_book

Compare market types:
> "What kinds of bets can I make on Polymarket for NBA?"
> Uses: get_sports_market_types, then get_sports_markets with sports_market_types filter
