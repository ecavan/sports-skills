"""College Football (CFB) data — scores, standings, rosters, schedules, rankings, and more.

Wraps ESPN public endpoints. No API keys required. Zero config.
"""

from sports_skills._response import wrap
from sports_skills.cfb._connector import (
    get_scoreboard as _get_scoreboard,
    get_standings as _get_standings,
    get_teams as _get_teams,
    get_team_roster as _get_team_roster,
    get_team_schedule as _get_team_schedule,
    get_game_summary as _get_game_summary,
    get_rankings as _get_rankings,
    get_news as _get_news,
    get_schedule as _get_schedule,
)


def _params(**kwargs):
    """Build params dict, filtering out None values."""
    return {"params": {k: v for k, v in kwargs.items() if v is not None}}


def get_scoreboard(*, date: str | None = None, week: int | None = None, group: int | None = None, limit: int | None = None) -> dict:
    """Get live/recent college football scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        week: CFB week number.
        group: Conference group ID to filter by.
        limit: Max number of events to return.
    """
    return wrap(_get_scoreboard(_params(date=date, week=week, group=group, limit=limit)))


def get_standings(*, season: int | None = None, group: int | None = None) -> dict:
    """Get college football standings by conference.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
        group: Conference ID to filter (e.g. 1=ACC, 4=Big 12, 8=SEC, 9=Big Ten, 15=Pac-12).
    """
    return wrap(_get_standings(_params(season=season, group=group)))


def get_teams() -> dict:
    """Get all FBS college football teams."""
    return wrap(_get_teams(_params()))


def get_team_roster(*, team_id: str) -> dict:
    """Get full roster for a college football team.

    Args:
        team_id: ESPN team ID (e.g. "333" for Alabama).
    """
    return wrap(_get_team_roster(_params(team_id=team_id)))


def get_team_schedule(*, team_id: str, season: int | None = None) -> dict:
    """Get schedule for a specific college football team.

    Args:
        team_id: ESPN team ID.
        season: Season year. Defaults to current.
    """
    return wrap(_get_team_schedule(_params(team_id=team_id, season=season)))


def get_game_summary(*, event_id: str) -> dict:
    """Get detailed game summary with box score and scoring plays.

    Args:
        event_id: ESPN event ID.
    """
    return wrap(_get_game_summary(_params(event_id=event_id)))


def get_rankings(*, season: int | None = None, week: int | None = None) -> dict:
    """Get college football rankings (AP Top 25, Coaches Poll, CFP).

    Args:
        season: Season year. Defaults to current.
        week: Week number for historical rankings.
    """
    return wrap(_get_rankings(_params(season=season, week=week)))


def get_news(*, team_id: str | None = None) -> dict:
    """Get college football news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    return wrap(_get_news(_params(team_id=team_id)))


def get_schedule(*, season: int | None = None, week: int | None = None, group: int | None = None) -> dict:
    """Get college football schedule.

    Args:
        season: Season year. Defaults to current.
        week: CFB week number.
        group: Conference group ID to filter by.
    """
    return wrap(_get_schedule(_params(season=season, week=week, group=group)))
