from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def nhl_get_scoreboard(date: str | None = None) -> str:
    """Get live/recent NHL scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    from sports_skills import nhl

    return _json(nhl.get_scoreboard(date=date))


@tool(parse_docstring=True)
def nhl_get_standings(season: int | None = None) -> str:
    """Get NHL standings by conference and division.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
    """
    from sports_skills import nhl

    return _json(nhl.get_standings(season=season))


@tool(parse_docstring=True)
def nhl_get_teams() -> str:
    """Get all 32 NHL teams."""
    from sports_skills import nhl

    return _json(nhl.get_teams())


@tool(parse_docstring=True)
def nhl_get_team_roster(team_id: str) -> str:
    """Get full roster for an NHL team.

    Args:
        team_id: ESPN team ID (e.g. "10" for Toronto Maple Leafs).
    """
    from sports_skills import nhl

    return _json(nhl.get_team_roster(team_id=team_id))


@tool(parse_docstring=True)
def nhl_get_team_schedule(team_id: str, season: int | None = None) -> str:
    """Get schedule for a specific NHL team.

    Args:
        team_id: ESPN team ID.
        season: Season year. Defaults to current.
    """
    from sports_skills import nhl

    return _json(nhl.get_team_schedule(team_id=team_id, season=season))


@tool(parse_docstring=True)
def nhl_get_game_summary(event_id: str) -> str:
    """Get detailed game summary with box score and scoring plays.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import nhl

    return _json(nhl.get_game_summary(event_id=event_id))


@tool(parse_docstring=True)
def nhl_get_leaders(season: int | None = None) -> str:
    """Get NHL statistical leaders (goals, assists, points, etc.).

    Args:
        season: Season year. Defaults to current.
    """
    from sports_skills import nhl

    return _json(nhl.get_leaders(season=season))


@tool(parse_docstring=True)
def nhl_get_news(team_id: str | None = None) -> str:
    """Get NHL news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    from sports_skills import nhl

    return _json(nhl.get_news(team_id=team_id))


@tool(parse_docstring=True)
def nhl_get_schedule(date: str | None = None, season: int | None = None) -> str:
    """Get NHL schedule.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        season: Season year. Defaults to current.
    """
    from sports_skills import nhl

    return _json(nhl.get_schedule(date=date, season=season))


@tool(parse_docstring=True)
def nhl_get_play_by_play(event_id: str) -> str:
    """Get full play-by-play log for an NHL game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import nhl

    return _json(nhl.get_play_by_play(event_id=event_id))


@tool(parse_docstring=True)
def nhl_get_injuries() -> str:
    """Get current NHL injury report for all teams."""
    from sports_skills import nhl

    return _json(nhl.get_injuries())


@tool(parse_docstring=True)
def nhl_get_transactions(limit: int | None = None) -> str:
    """Get recent NHL transactions (trades, signings, releases).

    Args:
        limit: Max number of transactions. Defaults to 50.
    """
    from sports_skills import nhl

    return _json(nhl.get_transactions(limit=limit))


@tool(parse_docstring=True)
def nhl_get_futures(limit: int | None = None, season_year: int | None = None) -> str:
    """Get NHL futures odds (Stanley Cup winner, Hart Trophy, etc.).

    Args:
        limit: Max entries per futures market. Defaults to 10.
        season_year: Season year. Defaults to current.
    """
    from sports_skills import nhl

    return _json(nhl.get_futures(limit=limit, season_year=season_year))


@tool(parse_docstring=True)
def nhl_get_team_stats(
    team_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get NHL team season statistics.

    Args:
        team_id: ESPN team ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import nhl

    return _json(
        nhl.get_team_stats(
            team_id=team_id, season_year=season_year, season_type=season_type
        )
    )


@tool(parse_docstring=True)
def nhl_get_player_stats(
    player_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get NHL player season statistics.

    Args:
        player_id: ESPN athlete ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import nhl

    return _json(
        nhl.get_player_stats(
            player_id=player_id, season_year=season_year, season_type=season_type
        )
    )


ALL_TOOLS = [
    nhl_get_scoreboard,
    nhl_get_standings,
    nhl_get_teams,
    nhl_get_team_roster,
    nhl_get_team_schedule,
    nhl_get_game_summary,
    nhl_get_leaders,
    nhl_get_news,
    nhl_get_schedule,
    nhl_get_play_by_play,
    nhl_get_injuries,
    nhl_get_transactions,
    nhl_get_futures,
    nhl_get_team_stats,
    nhl_get_player_stats,
]
