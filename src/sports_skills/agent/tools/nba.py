from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def nba_get_scoreboard(date: str | None = None) -> str:
    """Get live/recent NBA scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    from sports_skills import nba

    return _json(nba.get_scoreboard(date=date))


@tool(parse_docstring=True)
def nba_get_standings(season: int | None = None) -> str:
    """Get NBA standings by conference.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
    """
    from sports_skills import nba

    return _json(nba.get_standings(season=season))


@tool(parse_docstring=True)
def nba_get_teams() -> str:
    """Get all 30 NBA teams."""
    from sports_skills import nba

    return _json(nba.get_teams())


@tool(parse_docstring=True)
def nba_get_team_roster(team_id: str) -> str:
    """Get full roster for an NBA team.

    Args:
        team_id: ESPN team ID (e.g. "13" for Los Angeles Lakers).
    """
    from sports_skills import nba

    return _json(nba.get_team_roster(team_id=team_id))


@tool(parse_docstring=True)
def nba_get_team_schedule(team_id: str, season: int | None = None) -> str:
    """Get schedule for a specific NBA team.

    Args:
        team_id: ESPN team ID.
        season: Season year. Defaults to current.
    """
    from sports_skills import nba

    return _json(nba.get_team_schedule(team_id=team_id, season=season))


@tool(parse_docstring=True)
def nba_get_game_summary(event_id: str) -> str:
    """Get detailed game summary with box score and scoring plays.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import nba

    return _json(nba.get_game_summary(event_id=event_id))


@tool(parse_docstring=True)
def nba_get_leaders(season: int | None = None) -> str:
    """Get NBA statistical leaders (points, rebounds, assists, etc.).

    Args:
        season: Season year. Defaults to current.
    """
    from sports_skills import nba

    return _json(nba.get_leaders(season=season))


@tool(parse_docstring=True)
def nba_get_news(team_id: str | None = None) -> str:
    """Get NBA news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    from sports_skills import nba

    return _json(nba.get_news(team_id=team_id))


@tool(parse_docstring=True)
def nba_get_schedule(date: str | None = None, season: int | None = None) -> str:
    """Get NBA schedule.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        season: Season year. Defaults to current.
    """
    from sports_skills import nba

    return _json(nba.get_schedule(date=date, season=season))


@tool(parse_docstring=True)
def nba_get_play_by_play(event_id: str) -> str:
    """Get full play-by-play log for an NBA game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import nba

    return _json(nba.get_play_by_play(event_id=event_id))


@tool(parse_docstring=True)
def nba_get_win_probability(event_id: str) -> str:
    """Get win probability timeline for an NBA game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import nba

    return _json(nba.get_win_probability(event_id=event_id))


@tool(parse_docstring=True)
def nba_get_injuries() -> str:
    """Get current NBA injury report for all teams."""
    from sports_skills import nba

    return _json(nba.get_injuries())


@tool(parse_docstring=True)
def nba_get_transactions(limit: int | None = None) -> str:
    """Get recent NBA transactions (trades, signings, releases).

    Args:
        limit: Max number of transactions. Defaults to 50.
    """
    from sports_skills import nba

    return _json(nba.get_transactions(limit=limit))


@tool(parse_docstring=True)
def nba_get_futures(
    limit: int | None = None, season_year: int | None = None
) -> str:
    """Get NBA futures odds (championship winner, MVP, etc.).

    Args:
        limit: Max entries per futures market. Defaults to 10.
        season_year: Season year. Defaults to current.
    """
    from sports_skills import nba

    return _json(nba.get_futures(limit=limit, season_year=season_year))


@tool(parse_docstring=True)
def nba_get_depth_chart(team_id: str) -> str:
    """Get NBA depth chart for a team.

    Args:
        team_id: ESPN team ID.
    """
    from sports_skills import nba

    return _json(nba.get_depth_chart(team_id=team_id))


@tool(parse_docstring=True)
def nba_get_team_stats(
    team_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get NBA team season statistics.

    Args:
        team_id: ESPN team ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import nba

    return _json(
        nba.get_team_stats(
            team_id=team_id, season_year=season_year, season_type=season_type
        )
    )


@tool(parse_docstring=True)
def nba_get_player_stats(
    player_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get NBA player season statistics.

    Args:
        player_id: ESPN athlete ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import nba

    return _json(
        nba.get_player_stats(
            player_id=player_id, season_year=season_year, season_type=season_type
        )
    )


ALL_TOOLS = [
    nba_get_scoreboard,
    nba_get_standings,
    nba_get_teams,
    nba_get_team_roster,
    nba_get_team_schedule,
    nba_get_game_summary,
    nba_get_leaders,
    nba_get_news,
    nba_get_schedule,
    nba_get_play_by_play,
    nba_get_win_probability,
    nba_get_injuries,
    nba_get_transactions,
    nba_get_futures,
    nba_get_depth_chart,
    nba_get_team_stats,
    nba_get_player_stats,
]
