"""Golf data — tournament leaderboards, schedules, player profiles, and news.

Wraps ESPN public endpoints for PGA Tour, LPGA, and DP World Tour.
No API keys required. Zero config.
"""

from sports_skills._response import wrap
from sports_skills.golf._connector import (
    get_leaderboard as _get_leaderboard,
    get_schedule as _get_schedule,
    get_player_info as _get_player_info,
    get_news as _get_news,
)


def _params(**kwargs):
    """Build params dict, filtering out None values."""
    return {"params": {k: v for k, v in kwargs.items() if v is not None}}


def get_leaderboard(*, tour: str) -> dict:
    """Get current tournament leaderboard.

    Args:
        tour: Tour name — "pga", "lpga", or "eur" (DP World Tour).
    """
    return wrap(_get_leaderboard(_params(tour=tour)))


def get_schedule(*, tour: str, year: int | None = None) -> dict:
    """Get full season tournament schedule.

    Args:
        tour: Tour name — "pga", "lpga", or "eur".
        year: Season year. Defaults to current.
    """
    return wrap(_get_schedule(_params(tour=tour, year=year)))


def get_player_info(*, player_id: str, tour: str | None = None) -> dict:
    """Get golfer profile.

    Args:
        player_id: ESPN athlete ID.
        tour: Tour for lookup — "pga", "lpga", or "eur". Defaults to "pga".
    """
    return wrap(_get_player_info(_params(player_id=player_id, tour=tour)))


def get_news(*, tour: str) -> dict:
    """Get golf news articles.

    Args:
        tour: Tour name — "pga", "lpga", or "eur".
    """
    return wrap(_get_news(_params(tour=tour)))
