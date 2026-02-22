from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def kalshi_get_exchange_status() -> str:
    """Get exchange status (trading active, maintenance windows)."""
    from sports_skills import kalshi

    return _json(kalshi.get_exchange_status())


@tool(parse_docstring=True)
def kalshi_get_exchange_schedule() -> str:
    """Get exchange operating schedule."""
    from sports_skills import kalshi

    return _json(kalshi.get_exchange_schedule())


@tool(parse_docstring=True)
def kalshi_get_series_list(
    category: str | None = None, tags: str | None = None
) -> str:
    """Get all available series (leagues, recurring event groups).

    Args:
        category: Filter by category.
        tags: Filter by tags.
    """
    from sports_skills import kalshi

    return _json(kalshi.get_series_list(category=category, tags=tags))


@tool(parse_docstring=True)
def kalshi_get_series(series_ticker: str) -> str:
    """Get details for a specific series.

    Args:
        series_ticker: Series ticker symbol.
    """
    from sports_skills import kalshi

    return _json(kalshi.get_series(series_ticker=series_ticker))


@tool(parse_docstring=True)
def kalshi_get_events(
    limit: int = 100,
    cursor: str | None = None,
    status: str | None = None,
    series_ticker: str | None = None,
    with_nested_markets: bool = False,
) -> str:
    """Get events with optional filtering.

    Args:
        limit: Max number of events to return (default 100).
        cursor: Pagination cursor.
        status: Filter by event status.
        series_ticker: Filter by series ticker.
        with_nested_markets: Include nested market data (default False).
    """
    from sports_skills import kalshi

    return _json(
        kalshi.get_events(
            limit=limit,
            cursor=cursor,
            status=status,
            series_ticker=series_ticker,
            with_nested_markets=with_nested_markets,
        )
    )


@tool(parse_docstring=True)
def kalshi_get_event(
    event_ticker: str, with_nested_markets: bool = False
) -> str:
    """Get details for a specific event.

    Args:
        event_ticker: Event ticker symbol.
        with_nested_markets: Include nested market data (default False).
    """
    from sports_skills import kalshi

    return _json(
        kalshi.get_event(
            event_ticker=event_ticker, with_nested_markets=with_nested_markets
        )
    )


@tool(parse_docstring=True)
def kalshi_get_markets(
    limit: int = 100,
    cursor: str | None = None,
    event_ticker: str | None = None,
    series_ticker: str | None = None,
    status: str | None = None,
    tickers: str | None = None,
) -> str:
    """Get markets with optional filtering.

    Args:
        limit: Max number of markets to return (default 100).
        cursor: Pagination cursor.
        event_ticker: Filter by event ticker.
        series_ticker: Filter by series ticker.
        status: Filter by market status.
        tickers: Filter by market tickers.
    """
    from sports_skills import kalshi

    return _json(
        kalshi.get_markets(
            limit=limit,
            cursor=cursor,
            event_ticker=event_ticker,
            series_ticker=series_ticker,
            status=status,
            tickers=tickers,
        )
    )


@tool(parse_docstring=True)
def kalshi_get_market(ticker: str) -> str:
    """Get details for a specific market.

    Args:
        ticker: Market ticker symbol.
    """
    from sports_skills import kalshi

    return _json(kalshi.get_market(ticker=ticker))


@tool(parse_docstring=True)
def kalshi_get_trades(
    limit: int = 100,
    cursor: str | None = None,
    ticker: str | None = None,
    min_ts: int | None = None,
    max_ts: int | None = None,
) -> str:
    """Get recent trades with optional filtering.

    Args:
        limit: Max number of trades to return (default 100).
        cursor: Pagination cursor.
        ticker: Filter by market ticker.
        min_ts: Minimum timestamp (unix seconds).
        max_ts: Maximum timestamp (unix seconds).
    """
    from sports_skills import kalshi

    return _json(
        kalshi.get_trades(
            limit=limit,
            cursor=cursor,
            ticker=ticker,
            min_ts=min_ts,
            max_ts=max_ts,
        )
    )


@tool(parse_docstring=True)
def kalshi_get_market_candlesticks(
    series_ticker: str,
    ticker: str,
    start_ts: int,
    end_ts: int,
    period_interval: int,
) -> str:
    """Get candlestick (OHLC) data for a market.

    Args:
        series_ticker: Series ticker symbol.
        ticker: Market ticker symbol.
        start_ts: Start timestamp (unix seconds).
        end_ts: End timestamp (unix seconds).
        period_interval: Candlestick interval in minutes (1, 60, or 1440).
    """
    from sports_skills import kalshi

    return _json(
        kalshi.get_market_candlesticks(
            series_ticker=series_ticker,
            ticker=ticker,
            start_ts=start_ts,
            end_ts=end_ts,
            period_interval=period_interval,
        )
    )


@tool(parse_docstring=True)
def kalshi_get_sports_filters() -> str:
    """Get available sports filter categories (leagues, teams, etc.)."""
    from sports_skills import kalshi

    return _json(kalshi.get_sports_filters())


ALL_TOOLS = [
    kalshi_get_exchange_status,
    kalshi_get_exchange_schedule,
    kalshi_get_series_list,
    kalshi_get_series,
    kalshi_get_events,
    kalshi_get_event,
    kalshi_get_markets,
    kalshi_get_market,
    kalshi_get_trades,
    kalshi_get_market_candlesticks,
    kalshi_get_sports_filters,
]
