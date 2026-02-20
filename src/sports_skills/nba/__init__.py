"""NBA data — scores, standings, rosters, schedules, game summaries, and more.

Wraps ESPN public endpoints. No API keys required. Zero config.
"""

from sports_skills._response import wrap
from sports_skills.nba._connector import (
    get_game_summary as _get_game_summary,
)
from sports_skills.nba._connector import (
    get_leaders as _get_leaders,
)
from sports_skills.nba._connector import (
    get_news as _get_news,
)
from sports_skills.nba._connector import (
    get_schedule as _get_schedule,
)
from sports_skills.nba._connector import (
    get_scoreboard as _get_scoreboard,
)
from sports_skills.nba._connector import (
    get_standings as _get_standings,
)
from sports_skills.nba._connector import (
    get_team_roster as _get_team_roster,
)
from sports_skills.nba._connector import (
    get_team_schedule as _get_team_schedule,
)
from sports_skills.nba._connector import (
    get_teams as _get_teams,
)


def _params(**kwargs):
    """Build params dict, filtering out None values."""
    return {"params": {k: v for k, v in kwargs.items() if v is not None}}


def get_scoreboard(*, date: str | None = None) -> dict:
    """Get live/recent NBA scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    return wrap(_get_scoreboard(_params(date=date)))


def get_standings(*, season: int | None = None) -> dict:
    """Get NBA standings by conference.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
    """
    return wrap(_get_standings(_params(season=season)))


def get_teams() -> dict:
    """Get all 30 NBA teams."""
    return wrap(_get_teams(_params()))


def get_team_roster(*, team_id: str) -> dict:
    """Get full roster for an NBA team.

    Args:
        team_id: ESPN team ID (e.g. "13" for Los Angeles Lakers).
    """
    return wrap(_get_team_roster(_params(team_id=team_id)))


def get_team_schedule(*, team_id: str, season: int | None = None) -> dict:
    """Get schedule for a specific NBA team.

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


def get_leaders(*, season: int | None = None) -> dict:
    """Get NBA statistical leaders (points, rebounds, assists, etc.).

    Args:
        season: Season year. Defaults to current.
    """
    return wrap(_get_leaders(_params(season=season)))


def get_news(*, team_id: str | None = None) -> dict:
    """Get NBA news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    return wrap(_get_news(_params(team_id=team_id)))


def get_schedule(*, date: str | None = None, season: int | None = None) -> dict:
    """Get NBA schedule.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        season: Season year. Defaults to current.
    """
    return wrap(_get_schedule(_params(date=date, season=season)))
