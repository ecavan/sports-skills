from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def golf_get_leaderboard(tour: str) -> str:
    """Get current golf tournament leaderboard.

    Args:
        tour: Tour name — "pga", "lpga", or "eur" (DP World Tour).
    """
    from sports_skills import golf

    return _json(golf.get_leaderboard(tour=tour))


@tool(parse_docstring=True)
def golf_get_schedule(tour: str, year: int | None = None) -> str:
    """Get full season golf tournament schedule.

    Args:
        tour: Tour name — "pga", "lpga", or "eur".
        year: Season year. Defaults to current.
    """
    from sports_skills import golf

    return _json(golf.get_schedule(tour=tour, year=year))


@tool(parse_docstring=True)
def golf_get_player_info(player_id: str, tour: str | None = None) -> str:
    """Get golfer profile.

    Args:
        player_id: ESPN athlete ID.
        tour: Tour for lookup — "pga", "lpga", or "eur". Defaults to "pga".
    """
    from sports_skills import golf

    return _json(golf.get_player_info(player_id=player_id, tour=tour))


@tool(parse_docstring=True)
def golf_get_news(tour: str) -> str:
    """Get golf news articles.

    Args:
        tour: Tour name — "pga", "lpga", or "eur".
    """
    from sports_skills import golf

    return _json(golf.get_news(tour=tour))


@tool(parse_docstring=True)
def golf_get_player_overview(player_id: str, tour: str | None = None) -> str:
    """Get golfer season overview with stats, rankings, and recent results.

    Args:
        player_id: ESPN athlete ID.
        tour: Tour for lookup — "pga", "lpga", or "eur". Defaults to "pga".
    """
    from sports_skills import golf

    return _json(golf.get_player_overview(player_id=player_id, tour=tour))


@tool(parse_docstring=True)
def golf_get_scorecard(tour: str, player_id: str) -> str:
    """Get hole-by-hole scorecard for a golfer in the active tournament.

    Args:
        tour: Tour name — "pga", "lpga", or "eur".
        player_id: ESPN athlete ID.
    """
    from sports_skills import golf

    return _json(golf.get_scorecard(tour=tour, player_id=player_id))


ALL_TOOLS = [
    golf_get_leaderboard,
    golf_get_schedule,
    golf_get_player_info,
    golf_get_news,
    golf_get_player_overview,
    golf_get_scorecard,
]
