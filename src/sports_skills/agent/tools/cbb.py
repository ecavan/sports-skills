from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def cbb_get_scoreboard(
    date: str | None = None,
    group: int | None = None,
    limit: int | None = None,
) -> str:
    """Get live/recent college basketball scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        group: Conference group ID to filter by.
        limit: Max number of events to return.
    """
    from sports_skills import cbb

    return _json(cbb.get_scoreboard(date=date, group=group, limit=limit))


@tool(parse_docstring=True)
def cbb_get_standings(season: int | None = None, group: int | None = None) -> str:
    """Get college basketball standings by conference.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
        group: Conference ID to filter (e.g. 2=ACC, 7=Big 12, 8=Big East, 23=SEC).
    """
    from sports_skills import cbb

    return _json(cbb.get_standings(season=season, group=group))


@tool(parse_docstring=True)
def cbb_get_teams() -> str:
    """Get all D1 men's college basketball teams."""
    from sports_skills import cbb

    return _json(cbb.get_teams())


@tool(parse_docstring=True)
def cbb_get_team_roster(team_id: str) -> str:
    """Get full roster for a college basketball team.

    Args:
        team_id: ESPN team ID (e.g. "2250" for Duke).
    """
    from sports_skills import cbb

    return _json(cbb.get_team_roster(team_id=team_id))


@tool(parse_docstring=True)
def cbb_get_team_schedule(team_id: str, season: int | None = None) -> str:
    """Get schedule for a specific college basketball team.

    Args:
        team_id: ESPN team ID.
        season: Season year. Defaults to current.
    """
    from sports_skills import cbb

    return _json(cbb.get_team_schedule(team_id=team_id, season=season))


@tool(parse_docstring=True)
def cbb_get_game_summary(event_id: str) -> str:
    """Get detailed game summary with box score.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import cbb

    return _json(cbb.get_game_summary(event_id=event_id))


@tool(parse_docstring=True)
def cbb_get_rankings(season: int | None = None, week: int | None = None) -> str:
    """Get college basketball rankings (AP Top 25, Coaches Poll).

    Args:
        season: Season year. Defaults to current.
        week: Week number for historical rankings.
    """
    from sports_skills import cbb

    return _json(cbb.get_rankings(season=season, week=week))


@tool(parse_docstring=True)
def cbb_get_news(team_id: str | None = None) -> str:
    """Get college basketball news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    from sports_skills import cbb

    return _json(cbb.get_news(team_id=team_id))


@tool(parse_docstring=True)
def cbb_get_schedule(
    date: str | None = None,
    season: int | None = None,
    group: int | None = None,
) -> str:
    """Get college basketball schedule.

    Args:
        date: Date in YYYY-MM-DD format.
        season: Season year. Defaults to current.
        group: Conference group ID to filter by.
    """
    from sports_skills import cbb

    return _json(cbb.get_schedule(date=date, season=season, group=group))


@tool(parse_docstring=True)
def cbb_get_play_by_play(event_id: str) -> str:
    """Get full play-by-play log for a college basketball game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import cbb

    return _json(cbb.get_play_by_play(event_id=event_id))


@tool(parse_docstring=True)
def cbb_get_win_probability(event_id: str) -> str:
    """Get win probability timeline for a college basketball game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import cbb

    return _json(cbb.get_win_probability(event_id=event_id))


@tool(parse_docstring=True)
def cbb_get_futures(limit: int | None = None, season_year: int | None = None) -> str:
    """Get college basketball futures odds (national championship, etc.).

    Args:
        limit: Max entries per futures market. Defaults to 10.
        season_year: Season year. Defaults to current.
    """
    from sports_skills import cbb

    return _json(cbb.get_futures(limit=limit, season_year=season_year))


@tool(parse_docstring=True)
def cbb_get_team_stats(
    team_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get college basketball team season statistics.

    Args:
        team_id: ESPN team ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import cbb

    return _json(
        cbb.get_team_stats(
            team_id=team_id, season_year=season_year, season_type=season_type
        )
    )


@tool(parse_docstring=True)
def cbb_get_player_stats(
    player_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get college basketball player season statistics.

    Args:
        player_id: ESPN athlete ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import cbb

    return _json(
        cbb.get_player_stats(
            player_id=player_id, season_year=season_year, season_type=season_type
        )
    )


ALL_TOOLS = [
    cbb_get_scoreboard,
    cbb_get_standings,
    cbb_get_teams,
    cbb_get_team_roster,
    cbb_get_team_schedule,
    cbb_get_game_summary,
    cbb_get_rankings,
    cbb_get_news,
    cbb_get_schedule,
    cbb_get_play_by_play,
    cbb_get_win_probability,
    cbb_get_futures,
    cbb_get_team_stats,
    cbb_get_player_stats,
]
