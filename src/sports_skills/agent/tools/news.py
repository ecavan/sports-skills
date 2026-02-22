from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def news_fetch_feed(
    google_news: bool = False,
    query: str | None = None,
    url: str | None = None,
    language: str = "en-US",
    country: str = "US",
    after: str | None = None,
    before: str | None = None,
    sort_by_date: bool = False,
) -> str:
    """Fetch and parse an RSS/Atom feed.

    Args:
        google_news: If True, use Google News RSS. Requires query.
        query: Search query for Google News.
        url: RSS feed URL (required if google_news=False).
        language: Language code for Google News (default: "en-US").
        country: Country code for Google News (default: "US").
        after: Filter articles after this date (YYYY-MM-DD).
        before: Filter articles before this date (YYYY-MM-DD).
        sort_by_date: Sort entries by publication date (newest first).
    """
    from sports_skills import news

    return _json(
        news.fetch_feed(
            google_news=google_news,
            query=query,
            url=url,
            language=language,
            country=country,
            after=after,
            before=before,
            sort_by_date=sort_by_date,
        )
    )


@tool(parse_docstring=True)
def news_fetch_items(
    google_news: bool = False,
    query: str | None = None,
    url: str | None = None,
    limit: int | None = None,
    language: str = "en-US",
    country: str = "US",
    after: str | None = None,
    before: str | None = None,
    sort_by_date: bool = False,
) -> str:
    """Fetch items from an RSS/Atom feed, optionally limited by count.

    Args:
        google_news: If True, use Google News RSS. Requires query.
        query: Search query for Google News.
        url: RSS feed URL (required if google_news=False).
        limit: Max number of items to return.
        language: Language code for Google News (default: "en-US").
        country: Country code for Google News (default: "US").
        after: Filter articles after this date (YYYY-MM-DD).
        before: Filter articles before this date (YYYY-MM-DD).
        sort_by_date: Sort entries by publication date (newest first).
    """
    from sports_skills import news

    return _json(
        news.fetch_items(
            google_news=google_news,
            query=query,
            url=url,
            limit=limit,
            language=language,
            country=country,
            after=after,
            before=before,
            sort_by_date=sort_by_date,
        )
    )


ALL_TOOLS = [
    news_fetch_feed,
    news_fetch_items,
]
