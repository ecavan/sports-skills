from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def wnba_get_scoreboard(date: str | None = None) -> str:
    """Get live/recent WNBA scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    from sports_skills import wnba

    return _json(wnba.get_scoreboard(date=date))


@tool(parse_docstring=True)
def wnba_get_standings(season: int | None = None) -> str:
    """Get WNBA standings by conference.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
    """
    from sports_skills import wnba

    return _json(wnba.get_standings(season=season))


@tool(parse_docstring=True)
def wnba_get_teams() -> str:
    """Get all WNBA teams."""
    from sports_skills import wnba

    return _json(wnba.get_teams())


@tool(parse_docstring=True)
def wnba_get_team_roster(team_id: str) -> str:
    """Get full roster for a WNBA team.

    Args:
        team_id: ESPN team ID (e.g. "14" for Las Vegas Aces).
    """
    from sports_skills import wnba

    return _json(wnba.get_team_roster(team_id=team_id))


@tool(parse_docstring=True)
def wnba_get_team_schedule(team_id: str, season: int | None = None) -> str:
    """Get schedule for a specific WNBA team.

    Args:
        team_id: ESPN team ID.
        season: Season year. Defaults to current.
    """
    from sports_skills import wnba

    return _json(wnba.get_team_schedule(team_id=team_id, season=season))


@tool(parse_docstring=True)
def wnba_get_game_summary(event_id: str) -> str:
    """Get detailed game summary with box score and scoring plays.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import wnba

    return _json(wnba.get_game_summary(event_id=event_id))


@tool(parse_docstring=True)
def wnba_get_leaders(season: int | None = None) -> str:
    """Get WNBA statistical leaders (points, rebounds, assists, etc.).

    Args:
        season: Season year. Defaults to current.
    """
    from sports_skills import wnba

    return _json(wnba.get_leaders(season=season))


@tool(parse_docstring=True)
def wnba_get_news(team_id: str | None = None) -> str:
    """Get WNBA news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    from sports_skills import wnba

    return _json(wnba.get_news(team_id=team_id))


@tool(parse_docstring=True)
def wnba_get_schedule(date: str | None = None, season: int | None = None) -> str:
    """Get WNBA schedule.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        season: Season year. Defaults to current.
    """
    from sports_skills import wnba

    return _json(wnba.get_schedule(date=date, season=season))


@tool(parse_docstring=True)
def wnba_get_play_by_play(event_id: str) -> str:
    """Get full play-by-play log for a WNBA game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import wnba

    return _json(wnba.get_play_by_play(event_id=event_id))


@tool(parse_docstring=True)
def wnba_get_win_probability(event_id: str) -> str:
    """Get win probability timeline for a WNBA game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import wnba

    return _json(wnba.get_win_probability(event_id=event_id))


@tool(parse_docstring=True)
def wnba_get_injuries() -> str:
    """Get current WNBA injury report for all teams."""
    from sports_skills import wnba

    return _json(wnba.get_injuries())


@tool(parse_docstring=True)
def wnba_get_transactions(limit: int | None = None) -> str:
    """Get recent WNBA transactions (trades, signings, releases).

    Args:
        limit: Max number of transactions. Defaults to 50.
    """
    from sports_skills import wnba

    return _json(wnba.get_transactions(limit=limit))


@tool(parse_docstring=True)
def wnba_get_futures(
    limit: int | None = None, season_year: int | None = None
) -> str:
    """Get WNBA futures odds (championship winner, MVP, etc.).

    Args:
        limit: Max entries per futures market. Defaults to 10.
        season_year: Season year. Defaults to current.
    """
    from sports_skills import wnba

    return _json(wnba.get_futures(limit=limit, season_year=season_year))


@tool(parse_docstring=True)
def wnba_get_team_stats(
    team_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get WNBA team season statistics.

    Args:
        team_id: ESPN team ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import wnba

    return _json(
        wnba.get_team_stats(
            team_id=team_id, season_year=season_year, season_type=season_type
        )
    )


@tool(parse_docstring=True)
def wnba_get_player_stats(
    player_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get WNBA player season statistics.

    Args:
        player_id: ESPN athlete ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import wnba

    return _json(
        wnba.get_player_stats(
            player_id=player_id, season_year=season_year, season_type=season_type
        )
    )


ALL_TOOLS = [
    wnba_get_scoreboard,
    wnba_get_standings,
    wnba_get_teams,
    wnba_get_team_roster,
    wnba_get_team_schedule,
    wnba_get_game_summary,
    wnba_get_leaders,
    wnba_get_news,
    wnba_get_schedule,
    wnba_get_play_by_play,
    wnba_get_win_probability,
    wnba_get_injuries,
    wnba_get_transactions,
    wnba_get_futures,
    wnba_get_team_stats,
    wnba_get_player_stats,
]
