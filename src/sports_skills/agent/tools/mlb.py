from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def mlb_get_scoreboard(date: str | None = None) -> str:
    """Get live/recent MLB scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    from sports_skills import mlb

    return _json(mlb.get_scoreboard(date=date))


@tool(parse_docstring=True)
def mlb_get_standings(season: int | None = None) -> str:
    """Get MLB standings by league and division.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
    """
    from sports_skills import mlb

    return _json(mlb.get_standings(season=season))


@tool(parse_docstring=True)
def mlb_get_teams() -> str:
    """Get all 30 MLB teams."""
    from sports_skills import mlb

    return _json(mlb.get_teams())


@tool(parse_docstring=True)
def mlb_get_team_roster(team_id: str) -> str:
    """Get full roster for an MLB team.

    Args:
        team_id: ESPN team ID (e.g. "10" for New York Yankees).
    """
    from sports_skills import mlb

    return _json(mlb.get_team_roster(team_id=team_id))


@tool(parse_docstring=True)
def mlb_get_team_schedule(team_id: str, season: int | None = None) -> str:
    """Get schedule for a specific MLB team.

    Args:
        team_id: ESPN team ID.
        season: Season year. Defaults to current.
    """
    from sports_skills import mlb

    return _json(mlb.get_team_schedule(team_id=team_id, season=season))


@tool(parse_docstring=True)
def mlb_get_game_summary(event_id: str) -> str:
    """Get detailed game summary with box score and scoring plays.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import mlb

    return _json(mlb.get_game_summary(event_id=event_id))


@tool(parse_docstring=True)
def mlb_get_leaders(season: int | None = None) -> str:
    """Get MLB statistical leaders (batting avg, home runs, ERA, etc.).

    Args:
        season: Season year. Defaults to current.
    """
    from sports_skills import mlb

    return _json(mlb.get_leaders(season=season))


@tool(parse_docstring=True)
def mlb_get_news(team_id: str | None = None) -> str:
    """Get MLB news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    from sports_skills import mlb

    return _json(mlb.get_news(team_id=team_id))


@tool(parse_docstring=True)
def mlb_get_schedule(date: str | None = None, season: int | None = None) -> str:
    """Get MLB schedule.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        season: Season year. Defaults to current.
    """
    from sports_skills import mlb

    return _json(mlb.get_schedule(date=date, season=season))


@tool(parse_docstring=True)
def mlb_get_play_by_play(event_id: str) -> str:
    """Get play-by-play log for an MLB game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import mlb

    return _json(mlb.get_play_by_play(event_id=event_id))


@tool(parse_docstring=True)
def mlb_get_win_probability(event_id: str) -> str:
    """Get win probability timeline for an MLB game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import mlb

    return _json(mlb.get_win_probability(event_id=event_id))


@tool(parse_docstring=True)
def mlb_get_injuries() -> str:
    """Get current MLB injury report for all teams."""
    from sports_skills import mlb

    return _json(mlb.get_injuries())


@tool(parse_docstring=True)
def mlb_get_transactions(limit: int | None = None) -> str:
    """Get recent MLB transactions (trades, signings, releases).

    Args:
        limit: Max number of transactions. Defaults to 50.
    """
    from sports_skills import mlb

    return _json(mlb.get_transactions(limit=limit))


@tool(parse_docstring=True)
def mlb_get_depth_chart(team_id: str) -> str:
    """Get MLB depth chart for a team.

    Args:
        team_id: ESPN team ID.
    """
    from sports_skills import mlb

    return _json(mlb.get_depth_chart(team_id=team_id))


@tool(parse_docstring=True)
def mlb_get_team_stats(
    team_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get MLB team season statistics.

    Args:
        team_id: ESPN team ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import mlb

    return _json(
        mlb.get_team_stats(
            team_id=team_id, season_year=season_year, season_type=season_type
        )
    )


@tool(parse_docstring=True)
def mlb_get_player_stats(
    player_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get MLB player season statistics.

    Args:
        player_id: ESPN athlete ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import mlb

    return _json(
        mlb.get_player_stats(
            player_id=player_id, season_year=season_year, season_type=season_type
        )
    )


ALL_TOOLS = [
    mlb_get_scoreboard,
    mlb_get_standings,
    mlb_get_teams,
    mlb_get_team_roster,
    mlb_get_team_schedule,
    mlb_get_game_summary,
    mlb_get_leaders,
    mlb_get_news,
    mlb_get_schedule,
    mlb_get_play_by_play,
    mlb_get_win_probability,
    mlb_get_injuries,
    mlb_get_transactions,
    mlb_get_depth_chart,
    mlb_get_team_stats,
    mlb_get_player_stats,
]
