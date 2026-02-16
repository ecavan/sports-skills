---
name: kalshi
description: Kalshi prediction market data for sports including series, events, markets, trades, order books, and candlestick price data. Covers Soccer, Basketball, Baseball, Tennis, American Football, and Hockey. Use when the user asks about Kalshi markets, sports betting odds, prediction markets, sports event probabilities, or market prices on Kalshi. Public endpoints only, no API key required for market data.
---

# Kalshi

Public prediction market data from Kalshi. Access sports series, events, markets, trades, and candlestick data. No API key required for read-only market data.

**Base URL:** `https://api.elections.kalshi.com/trade-api/v2`

## Supported Sports

18 sport categories with 80+ competitions. Major sports: `Soccer` (38 competitions), `Basketball` (11), `Hockey` (8), `Tennis` (14), `Football` (2), `Baseball` (2), `Golf` (3), `MMA` (1), `Boxing` (1)

## Commands (Public, No Auth)

### Series

**GetSeriesList** - Get all series templates. Filter by sport category.

```
GET /series
Params:
  category (string, optional) - Filter by category (e.g. "Sports")
  tags (string, optional) - Filter by sport tag (e.g. "Soccer", "Basketball")
Returns: { series: [{ ticker, title, category, frequency, fee_type, settlement_sources: [...] }] }
```

**GetSeries** - Get a specific series by ticker.

```
GET /series/{series_ticker}
Params:
  series_ticker (string, required) - Series ticker symbol
Returns: { ticker, title, category, frequency, fee_type, settlement_sources: [...] }
```

### Events

**GetEvents** - Get events with pagination. Each event groups related markets.

```
GET /events
Params:
  series_ticker (string, recommended) - Filter by series (most reliable for sports)
  category (string, optional) - Filter by category (note: unreliable for sports filtering)
  tags (string, optional) - Filter by sport
  limit (int, optional, default: 200) - Page size
  cursor (string, optional) - Pagination cursor
Returns: { events: [{ event_ticker, series_ticker, title, sub_title, category, strike_date, mutually_exclusive }], cursor }

IMPORTANT: The category=Sports filter on this endpoint does not reliably return sports events.
Always filter by series_ticker instead (e.g. series_ticker=KXNBA for basketball).
Use GetSeriesList with category=Sports first to find valid series tickers.
```

**GetMultivariateEvents** - Get multivariate (combo) events.

```
GET /events/multivariate
Returns: { events: [...] }
```

### Markets

**GetMarkets** - Get markets with filtering. Returns bid/ask prices, volume, and open interest.

```
GET /markets
Params:
  series_ticker (string, optional) - Filter by series
  event_ticker (string, optional) - Filter by event
  status (string, optional) - Filter by status (unopened, open, closed, settled)
  limit (int, optional) - Page size
  cursor (string, optional) - Pagination cursor
Returns: { markets: [{
  ticker, event_ticker, title, subtitle,
  yes_bid, yes_ask, no_bid, no_ask,
  last_price, volume, volume_24h, open_interest,
  status, result, close_time,
  yes_sub_title, no_sub_title, rules_primary
}], cursor }
```

**GetMarket** - Get a single market by ticker.

```
GET /markets/{ticker}
Params:
  ticker (string, required) - Market ticker
Returns: { ... same fields as above ... }
```

### Trades

**GetTrades** - Get trade history across markets.

```
GET /markets/trades
Params:
  ticker (string, optional) - Filter by market ticker
  limit (int, optional) - Page size
  cursor (string, optional) - Pagination cursor
Returns: { trades: [{ trade_id, ticker, count, yes_price, no_price, taker_side, created_time }], cursor }
```

### Price History (Candlesticks)

**GetMarketCandlesticks** - Get OHLCV candlestick data for a market.

```
GET /series/{series_ticker}/markets/{ticker}/candlesticks
Params:
  series_ticker (string, required)
  ticker (string, required)
  start_ts (int, required) - Start Unix timestamp in seconds
  end_ts (int, required) - End Unix timestamp in seconds
  period_interval (int, optional) - Interval in minutes: 1 (1min), 60 (1hour), 1440 (1day)
Returns: { candlesticks: [{
  open, high, low, close, volume, open_interest,
  start_ts, end_ts,
  price: { open, high, low, close },
  yes_ask: { open, high, low, close },
  yes_bid: { open, high, low, close }
}] }
Note: Requires start_ts and end_ts. Without them the endpoint returns empty results.
```

**BatchGetMarketCandlesticks** - Get candlestick data for up to 100 markets at once.

```
GET /markets/candlesticks
Params:
  tickers (string, required) - Comma-separated market tickers (max 100)
  period_interval (string, optional)
Returns: { candlesticks: { [ticker]: [{ open, high, low, close, volume, start_ts, end_ts }] } }
```

### Sports Filters

**GetFiltersForSports** - Get available sports and their competition/scope structure.

```
GET /search/filters_by_sport
Returns: {
  filters_by_sports: {
    [sport_name]: {
      scopes: [...],
      competitions: { [name]: { scopes: [...] } }
    }
  },
  sport_ordering: [...]
}
```

**GetTagsForSeriesCategories** - Get mapping of categories to available tags.

```
GET /search/tags_for_categories
Returns: { ... }
```

### Exchange Info

**GetExchangeStatus** - Check if the exchange is active and trading.

```
GET /exchange/status
Returns: { exchange_active: bool, trading_active: bool }
```

**GetExchangeSchedule** - Get standard operating hours and maintenance windows.

```
GET /exchange/schedule
Returns: { schedule: {...} }
```

## Workflow: Finding Sports Markets

1. Call `GetFiltersForSports` to see available sports (18 categories, 80+ competitions)
2. Call `GetSeriesList` with `category=Sports` and optionally `tags=Soccer` to find series tickers
3. Call `GetEvents` with `series_ticker` (NOT category) to find specific events
4. Call `GetMarkets` with `event_ticker` to see available markets and current prices
5. Call `GetMarketCandlesticks` for price history (requires `start_ts` and `end_ts` as Unix timestamps, `period_interval` in minutes: 1=1min, 60=1hour, 1440=1day)

## Usage Examples

Check what sports are available:
> "What sports does Kalshi have markets for?"
> Uses: GetFiltersForSports

Find NBA markets:
> "Show me current Kalshi basketball markets"
> Uses: GetSeriesList with tags=Basketball, then GetEvents and GetMarkets

Get market prices:
> "What are the odds on the Super Bowl on Kalshi?"
> Uses: GetSeriesList with tags=American Football, then drill into events and markets

Track price movement:
> "Show me the price history for this Kalshi market"
> Uses: GetMarketCandlesticks with period_interval=1hour
