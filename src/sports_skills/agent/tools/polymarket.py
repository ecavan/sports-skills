from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def polymarket_get_sports_markets(
    limit: int = 50,
    offset: int = 0,
    sports_market_types: str | None = None,
    game_id: str | None = None,
    active: bool = True,
    closed: bool = False,
    order: str = "volume",
    ascending: bool = False,
) -> str:
    """Get active sports prediction markets with optional filtering.

    Args:
        limit: Max number of markets to return (default 50).
        offset: Pagination offset (default 0).
        sports_market_types: Filter by market type (e.g. moneyline, spreads).
        game_id: Filter by game ID.
        active: Only return active markets (default True).
        closed: Include closed markets (default False).
        order: Sort field (default "volume").
        ascending: Sort ascending (default False).
    """
    from sports_skills import polymarket

    return _json(
        polymarket.get_sports_markets(
            limit=limit,
            offset=offset,
            sports_market_types=sports_market_types,
            game_id=game_id,
            active=active,
            closed=closed,
            order=order,
            ascending=ascending,
        )
    )


@tool(parse_docstring=True)
def polymarket_get_sports_events(
    limit: int = 50,
    offset: int = 0,
    active: bool = True,
    closed: bool = False,
    order: str = "volume",
    ascending: bool = False,
    series_id: str | None = None,
) -> str:
    """Get sports events (each event groups related markets).

    Args:
        limit: Max number of events to return (default 50).
        offset: Pagination offset (default 0).
        active: Only return active events (default True).
        closed: Include closed events (default False).
        order: Sort field (default "volume").
        ascending: Sort ascending (default False).
        series_id: Filter by series ID.
    """
    from sports_skills import polymarket

    return _json(
        polymarket.get_sports_events(
            limit=limit,
            offset=offset,
            active=active,
            closed=closed,
            order=order,
            ascending=ascending,
            series_id=series_id,
        )
    )


@tool(parse_docstring=True)
def polymarket_get_series(limit: int = 100, offset: int = 0) -> str:
    """Get all series (leagues, recurring event groups).

    Args:
        limit: Max number of series to return (default 100).
        offset: Pagination offset (default 0).
    """
    from sports_skills import polymarket

    return _json(polymarket.get_series(limit=limit, offset=offset))


@tool(parse_docstring=True)
def polymarket_get_market_details(
    market_id: str | None = None, slug: str | None = None
) -> str:
    """Get detailed information for a specific market.

    Args:
        market_id: Polymarket market ID.
        slug: Market URL slug.
    """
    from sports_skills import polymarket

    return _json(polymarket.get_market_details(market_id=market_id, slug=slug))


@tool(parse_docstring=True)
def polymarket_get_event_details(
    event_id: str | None = None, slug: str | None = None
) -> str:
    """Get detailed information for a specific event (includes nested markets).

    Args:
        event_id: Polymarket event ID.
        slug: Event URL slug.
    """
    from sports_skills import polymarket

    return _json(polymarket.get_event_details(event_id=event_id, slug=slug))


@tool(parse_docstring=True)
def polymarket_get_market_prices(
    token_id: str | None = None, token_ids: str | None = None
) -> str:
    """Get current prices for one or more markets from the CLOB API.

    Args:
        token_id: Single CLOB token ID.
        token_ids: Comma-separated CLOB token IDs for batch lookup.
    """
    from sports_skills import polymarket

    ids_list = [t.strip() for t in token_ids.split(",")] if token_ids else None
    return _json(
        polymarket.get_market_prices(token_id=token_id, token_ids=ids_list)
    )


@tool(parse_docstring=True)
def polymarket_get_order_book(token_id: str) -> str:
    """Get the full order book for a market.

    Args:
        token_id: CLOB token ID.
    """
    from sports_skills import polymarket

    return _json(polymarket.get_order_book(token_id=token_id))


@tool(parse_docstring=True)
def polymarket_get_sports_market_types() -> str:
    """Get all valid sports market types (moneyline, spreads, totals, props, etc.)."""
    from sports_skills import polymarket

    return _json(polymarket.get_sports_market_types())


@tool(parse_docstring=True)
def polymarket_search_markets(
    query: str | None = None,
    sports_market_types: str | None = None,
    tag_id: int | None = None,
    limit: int = 20,
) -> str:
    """Find sports markets by keyword and filters.

    Args:
        query: Search keyword.
        sports_market_types: Filter by market type.
        tag_id: Filter by tag ID.
        limit: Max number of results (default 20).
    """
    from sports_skills import polymarket

    return _json(
        polymarket.search_markets(
            query=query,
            sports_market_types=sports_market_types,
            tag_id=tag_id,
            limit=limit,
        )
    )


@tool(parse_docstring=True)
def polymarket_get_price_history(
    token_id: str, interval: str = "max", fidelity: int = 120
) -> str:
    """Get historical price data for a market over time.

    Args:
        token_id: CLOB token ID.
        interval: Time interval (default "max").
        fidelity: Data point resolution in minutes (default 120).
    """
    from sports_skills import polymarket

    return _json(
        polymarket.get_price_history(
            token_id=token_id, interval=interval, fidelity=fidelity
        )
    )


@tool(parse_docstring=True)
def polymarket_get_last_trade_price(token_id: str) -> str:
    """Get the most recent trade price for a market.

    Args:
        token_id: CLOB token ID.
    """
    from sports_skills import polymarket

    return _json(polymarket.get_last_trade_price(token_id=token_id))


ALL_TOOLS = [
    polymarket_get_sports_markets,
    polymarket_get_sports_events,
    polymarket_get_series,
    polymarket_get_market_details,
    polymarket_get_event_details,
    polymarket_get_market_prices,
    polymarket_get_order_book,
    polymarket_get_sports_market_types,
    polymarket_search_markets,
    polymarket_get_price_history,
    polymarket_get_last_trade_price,
]
