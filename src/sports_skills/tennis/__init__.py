"""Tennis data — ATP and WTA tournament scores, calendars, rankings, players, and news.

Wraps ESPN public endpoints. No API keys required. Zero config.
"""

from sports_skills._response import wrap
from sports_skills.tennis._connector import (
    get_scoreboard as _get_scoreboard,
    get_calendar as _get_calendar,
    get_rankings as _get_rankings,
    get_player_info as _get_player_info,
    get_news as _get_news,
)


def _params(**kwargs):
    """Build params dict, filtering out None values."""
    return {"params": {k: v for k, v in kwargs.items() if v is not None}}


def get_scoreboard(*, tour: str, date: str | None = None) -> dict:
    """Get active tournaments with matches for a tour.

    Args:
        tour: Tour name — "atp" or "wta".
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    return wrap(_get_scoreboard(_params(tour=tour, date=date)))


def get_calendar(*, tour: str, year: int | None = None) -> dict:
    """Get full season tournament calendar.

    Args:
        tour: Tour name — "atp" or "wta".
        year: Season year. Defaults to current.
    """
    return wrap(_get_calendar(_params(tour=tour, year=year)))


def get_rankings(*, tour: str, limit: int | None = None) -> dict:
    """Get current ATP or WTA rankings.

    Args:
        tour: Tour name — "atp" or "wta".
        limit: Max number of ranked players to return. Defaults to 50.
    """
    return wrap(_get_rankings(_params(tour=tour, limit=limit)))


def get_player_info(*, player_id: str) -> dict:
    """Get individual player profile.

    Args:
        player_id: ESPN athlete ID (e.g. "3782" for Carlos Alcaraz).
    """
    return wrap(_get_player_info(_params(player_id=player_id)))


def get_news(*, tour: str) -> dict:
    """Get tennis news articles.

    Args:
        tour: Tour name — "atp" or "wta".
    """
    return wrap(_get_news(_params(tour=tour)))
