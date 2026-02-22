from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def cfb_get_scoreboard(
    date: str | None = None,
    week: int | None = None,
    group: int | None = None,
    limit: int | None = None,
) -> str:
    """Get live/recent college football scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        week: CFB week number.
        group: Conference group ID to filter by.
        limit: Max number of events to return.
    """
    from sports_skills import cfb

    return _json(cfb.get_scoreboard(date=date, week=week, group=group, limit=limit))


@tool(parse_docstring=True)
def cfb_get_standings(season: int | None = None, group: int | None = None) -> str:
    """Get college football standings by conference.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
        group: Conference ID to filter (e.g. 1=ACC, 4=Big 12, 8=SEC, 9=Big Ten, 15=Pac-12).
    """
    from sports_skills import cfb

    return _json(cfb.get_standings(season=season, group=group))


@tool(parse_docstring=True)
def cfb_get_teams() -> str:
    """Get all FBS college football teams."""
    from sports_skills import cfb

    return _json(cfb.get_teams())


@tool(parse_docstring=True)
def cfb_get_team_roster(team_id: str) -> str:
    """Get full roster for a college football team.

    Args:
        team_id: ESPN team ID (e.g. "333" for Alabama).
    """
    from sports_skills import cfb

    return _json(cfb.get_team_roster(team_id=team_id))


@tool(parse_docstring=True)
def cfb_get_team_schedule(team_id: str, season: int | None = None) -> str:
    """Get schedule for a specific college football team.

    Args:
        team_id: ESPN team ID.
        season: Season year. Defaults to current.
    """
    from sports_skills import cfb

    return _json(cfb.get_team_schedule(team_id=team_id, season=season))


@tool(parse_docstring=True)
def cfb_get_game_summary(event_id: str) -> str:
    """Get detailed game summary with box score and scoring plays.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import cfb

    return _json(cfb.get_game_summary(event_id=event_id))


@tool(parse_docstring=True)
def cfb_get_rankings(season: int | None = None, week: int | None = None) -> str:
    """Get college football rankings (AP Top 25, Coaches Poll, CFP).

    Args:
        season: Season year. Defaults to current.
        week: Week number for historical rankings.
    """
    from sports_skills import cfb

    return _json(cfb.get_rankings(season=season, week=week))


@tool(parse_docstring=True)
def cfb_get_news(team_id: str | None = None) -> str:
    """Get college football news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    from sports_skills import cfb

    return _json(cfb.get_news(team_id=team_id))


@tool(parse_docstring=True)
def cfb_get_schedule(
    season: int | None = None,
    week: int | None = None,
    group: int | None = None,
) -> str:
    """Get college football schedule.

    Args:
        season: Season year. Defaults to current.
        week: CFB week number.
        group: Conference group ID to filter by.
    """
    from sports_skills import cfb

    return _json(cfb.get_schedule(season=season, week=week, group=group))


@tool(parse_docstring=True)
def cfb_get_play_by_play(event_id: str) -> str:
    """Get drive-by-drive play-by-play data for a college football game.

    Args:
        event_id: ESPN event ID.
    """
    from sports_skills import cfb

    return _json(cfb.get_play_by_play(event_id=event_id))


@tool(parse_docstring=True)
def cfb_get_injuries() -> str:
    """Get current college football injury report for all teams."""
    from sports_skills import cfb

    return _json(cfb.get_injuries())


@tool(parse_docstring=True)
def cfb_get_futures(limit: int | None = None, season_year: int | None = None) -> str:
    """Get college football futures odds (national championship, Heisman, etc.).

    Args:
        limit: Max entries per futures market. Defaults to 10.
        season_year: Season year. Defaults to current.
    """
    from sports_skills import cfb

    return _json(cfb.get_futures(limit=limit, season_year=season_year))


@tool(parse_docstring=True)
def cfb_get_team_stats(
    team_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get college football team season statistics.

    Args:
        team_id: ESPN team ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import cfb

    return _json(
        cfb.get_team_stats(
            team_id=team_id, season_year=season_year, season_type=season_type
        )
    )


@tool(parse_docstring=True)
def cfb_get_player_stats(
    player_id: str,
    season_year: int | None = None,
    season_type: int | None = None,
) -> str:
    """Get college football player season statistics.

    Args:
        player_id: ESPN athlete ID.
        season_year: Season year. Defaults to current.
        season_type: 2 = regular season (default), 3 = postseason.
    """
    from sports_skills import cfb

    return _json(
        cfb.get_player_stats(
            player_id=player_id, season_year=season_year, season_type=season_type
        )
    )


ALL_TOOLS = [
    cfb_get_scoreboard,
    cfb_get_standings,
    cfb_get_teams,
    cfb_get_team_roster,
    cfb_get_team_schedule,
    cfb_get_game_summary,
    cfb_get_rankings,
    cfb_get_news,
    cfb_get_schedule,
    cfb_get_play_by_play,
    cfb_get_injuries,
    cfb_get_futures,
    cfb_get_team_stats,
    cfb_get_player_stats,
]
