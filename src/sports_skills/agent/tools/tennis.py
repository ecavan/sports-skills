from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def tennis_get_scoreboard(tour: str, date: str | None = None) -> str:
    """Get active tennis tournaments with matches for a tour.

    Args:
        tour: Tour name — "atp" or "wta".
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    from sports_skills import tennis

    return _json(tennis.get_scoreboard(tour=tour, date=date))


@tool(parse_docstring=True)
def tennis_get_calendar(tour: str, year: int | None = None) -> str:
    """Get full season tennis tournament calendar.

    Args:
        tour: Tour name — "atp" or "wta".
        year: Season year. Defaults to current.
    """
    from sports_skills import tennis

    return _json(tennis.get_calendar(tour=tour, year=year))


@tool(parse_docstring=True)
def tennis_get_rankings(tour: str, limit: int | None = None) -> str:
    """Get current ATP or WTA rankings.

    Args:
        tour: Tour name — "atp" or "wta".
        limit: Max number of ranked players to return. Defaults to 50.
    """
    from sports_skills import tennis

    return _json(tennis.get_rankings(tour=tour, limit=limit))


@tool(parse_docstring=True)
def tennis_get_player_info(player_id: str) -> str:
    """Get individual tennis player profile.

    Args:
        player_id: ESPN athlete ID (e.g. "3782" for Carlos Alcaraz).
    """
    from sports_skills import tennis

    return _json(tennis.get_player_info(player_id=player_id))


@tool(parse_docstring=True)
def tennis_get_news(tour: str) -> str:
    """Get tennis news articles.

    Args:
        tour: Tour name — "atp" or "wta".
    """
    from sports_skills import tennis

    return _json(tennis.get_news(tour=tour))


ALL_TOOLS = [
    tennis_get_scoreboard,
    tennis_get_calendar,
    tennis_get_rankings,
    tennis_get_player_info,
    tennis_get_news,
]
