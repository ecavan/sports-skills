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

**search_markets** - Full-text search across all Polymarket markets.

```
Params:
  query (string, required) - Search query
  limit (int, optional, default: 20, max: 50)
Returns: { markets: [...], count, query }
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

### Trades (Gamma API)

**get_trades** - Get recent trade history.

```
Params:
  market_id (string, optional) - Filter by market
  limit (int, optional, default: 50, max: 100)
Returns: { trades: [{ id, market_id, side, size, price, outcome, created_at }], count }
```

## Workflow: Finding Sports Market Odds

1. Call `get_sports_events` to browse current sports events by volume
2. Pick an event and call `get_event_details` to see all markets for it
3. For real-time pricing, take `clob_token_ids` from a market and call `get_market_prices`
4. For order book depth, call `get_order_book` with a specific token ID

Alternative: call `search_markets` with a query like "NBA Finals" or "World Cup" to find markets directly.

## Caching & Rate Limits

- Gamma API: Cached for 120s (markets/events), 600s (series), 60s (details/search)
- CLOB API: Cached for 30s (prices and order books refresh frequently)
- Rate limits are generous: 4,000 req/10s (Gamma general), 1,500 req/10s (CLOB price endpoints)

## Usage Examples

Browse sports markets:
> "What sports markets are live on Polymarket right now?"
> Uses: get_sports_markets

Find specific game odds:
> "What are the Polymarket odds for the Champions League final?"
> Uses: search_markets with query="Champions League final"

Check real-time prices:
> "What's the current price on this Polymarket market?"
> Uses: get_market_prices with the CLOB token ID

View order book:
> "Show me the order book depth for this market"
> Uses: get_order_book

Compare market types:
> "What kinds of bets can I make on Polymarket for NBA?"
> Uses: get_sports_market_types, then get_sports_markets with sports_market_types filter
