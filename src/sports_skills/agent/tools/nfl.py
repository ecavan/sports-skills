from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def nfl_get_scoreboard(date: str | None = None, week: int | None = None) -> str:
    """Get live/recent NFL scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        week: NFL week number (1-18 regular season, 19+ postseason).
    """
    from sports_skills import nfl

    return _json(nfl.get_scoreboard(date=date, week=week))


@tool(parse_docstring=True)
def nfl_get_standings(season: int | None = None) -> str:
    """Get NFL standings by conference and division.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
    """
    from sports_skills import nfl

    return _json(nfl.get_standings(season=season))


@tool(parse_docstring=True)
def nfl_get_teams() -> str:
    """Get all 32 NFL teams."""
    from sports_skills import nfl

    return _json(nfl.get_teams())


@tool(parse_docstring=True)
def nfl_get_team_roster(team_id: str) -> str:
    """Get full roster for an NFL team.

    Args:
        team_id: ESPN team ID (e.g. "12" for Kansas City Chiefs).
    """
    from sports_skills import nfl

    return _json(nfl.get_team_roster(team_id=team_id))


@tool(parse_docstring=True)
def nfl_get_team_schedule(team_id: str, season: int | None = None) -> str:
    """Get schedule for a specific NFL team.

    Args:
        team_id: ESPN team ID.
        season: Season year. Defaults to current.
    """
    from sports_skills import nfl

    return _json(nfl.get_team_schedule(team_id=team_id, season=season))


@tool(parse_docstring=True)
def nfl_get_game_summary(event_id: str) -> str:
    """Get detailed game summary with box score and scoring plays.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import nfl

    return _json(nfl.get_game_summary(event_id=event_id))


@tool(parse_docstring=True)
def nfl_get_leaders(season: int | None = None) -> str:
    """Get NFL statistical leaders (passing, rushing, receiving, etc.).

    Args:
        season: Season year. Defaults to current.
    """
    from sports_skills import nfl

    return _json(nfl.get_leaders(season=season))


@tool(parse_docstring=True)
def nfl_get_news(team_id: str | None = None) -> str:
    """Get NFL news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    from sports_skills import nfl

    return _json(nfl.get_news(team_id=team_id))


@tool(parse_docstring=True)
def nfl_get_schedule(season: int | None = None, week: int | None = None) -> str:
    """Get NFL season schedule.

    Args:
        season: Season year. Defaults to current.
        week: NFL week number. Defaults to current week.
    """
    from sports_skills import nfl

    return _json(nfl.get_schedule(season=season, week=week))


@tool(parse_docstring=True)
def nfl_get_play_by_play(event_id: str) -> str:
    """Get drive-by-drive play-by-play data for an NFL game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import nfl

    return _json(nfl.get_play_by_play(event_id=event_id))


@tool(parse_docstring=True)
def nfl_get_win_probability(event_id: str) -> str:
    """Get win probability timeline for an NFL game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import nfl

    return _json(nfl.get_win_probability(event_id=event_id))


@tool(parse_docstring=True)
def nfl_get_injuries() -> str:
    """Get current NFL injury report for all teams."""
    from sports_skills import nfl

    return _json(nfl.get_injuries())


@tool(parse_docstring=True)
def nfl_get_transactions(limit: int | None = None) -> str:
    """Get recent NFL transactions (trades, signings, releases).

    Args:
        limit: Max number of transactions. Defaults to 50.
    """
    from sports_skills import nfl

    return _json(nfl.get_transactions(limit=limit))


@tool(parse_docstring=True)
def nfl_get_futures(
    limit: int | None = None, season_year: int | None = None
) -> str:
    """Get NFL futures odds (Super Bowl winner, MVP, etc.).

    Args:
        limit: Max entries per futures market. Defaults to 10.
        season_year: Season year. Defaults to current.
    """
    from sports_skills import nfl

    return _json(nfl.get_futures(limit=limit, season_year=season_year))


@tool(parse_docstring=True)
def nfl_get_depth_chart(team_id: str) -> str:
    """Get NFL depth chart for a team.

    Args:
        team_id: ESPN team ID.
    """
    from sports_skills import nfl

    return _json(nfl.get_depth_chart(team_id=team_id))


@tool(parse_docstring=True)
def nfl_get_team_stats(
    team_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get NFL team season statistics.

    Args:
        team_id: ESPN team ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import nfl

    return _json(
        nfl.get_team_stats(
            team_id=team_id, season_year=season_year, season_type=season_type
        )
    )


@tool(parse_docstring=True)
def nfl_get_player_stats(
    player_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get NFL player season statistics.

    Args:
        player_id: ESPN athlete ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import nfl

    return _json(
        nfl.get_player_stats(
            player_id=player_id, season_year=season_year, season_type=season_type
        )
    )


ALL_TOOLS = [
    nfl_get_scoreboard,
    nfl_get_standings,
    nfl_get_teams,
    nfl_get_team_roster,
    nfl_get_team_schedule,
    nfl_get_game_summary,
    nfl_get_leaders,
    nfl_get_news,
    nfl_get_schedule,
    nfl_get_play_by_play,
    nfl_get_win_probability,
    nfl_get_injuries,
    nfl_get_transactions,
    nfl_get_futures,
    nfl_get_depth_chart,
    nfl_get_team_stats,
    nfl_get_player_stats,
]
