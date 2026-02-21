"""College Basketball (CBB) data — scores, standings, rosters, schedules, rankings, and more.

Wraps ESPN public endpoints for NCAA Division I men's basketball. No API keys required. Zero config.
"""

from sports_skills._response import wrap
from sports_skills.cbb._connector import (
    get_game_summary as _get_game_summary,
)
from sports_skills.cbb._connector import (
    get_news as _get_news,
)
from sports_skills.cbb._connector import (
    get_play_by_play as _get_play_by_play,
)
from sports_skills.cbb._connector import (
    get_rankings as _get_rankings,
)
from sports_skills.cbb._connector import (
    get_schedule as _get_schedule,
)
from sports_skills.cbb._connector import (
    get_scoreboard as _get_scoreboard,
)
from sports_skills.cbb._connector import (
    get_standings as _get_standings,
)
from sports_skills.cbb._connector import (
    get_team_roster as _get_team_roster,
)
from sports_skills.cbb._connector import (
    get_team_schedule as _get_team_schedule,
)
from sports_skills.cbb._connector import (
    get_teams as _get_teams,
)
from sports_skills.cbb._connector import (
    get_win_probability as _get_win_probability,
)


def _params(**kwargs):
    """Build params dict, filtering out None values."""
    return {"params": {k: v for k, v in kwargs.items() if v is not None}}


def get_scoreboard(*, date: str | None = None, group: int | None = None, limit: int | None = None) -> dict:
    """Get live/recent college basketball scores.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        group: Conference group ID to filter by.
        limit: Max number of events to return.
    """
    return wrap(_get_scoreboard(_params(date=date, group=group, limit=limit)))


def get_standings(*, season: int | None = None, group: int | None = None) -> dict:
    """Get college basketball standings by conference.

    Args:
        season: Season year (e.g. 2025). Defaults to current.
        group: Conference ID to filter (e.g. 2=ACC, 7=Big 12, 8=Big East, 23=SEC).
    """
    return wrap(_get_standings(_params(season=season, group=group)))


def get_teams() -> dict:
    """Get all D1 men's college basketball teams."""
    return wrap(_get_teams(_params()))


def get_team_roster(*, team_id: str) -> dict:
    """Get full roster for a college basketball team.

    Args:
        team_id: ESPN team ID (e.g. "2250" for Duke).
    """
    return wrap(_get_team_roster(_params(team_id=team_id)))


def get_team_schedule(*, team_id: str, season: int | None = None) -> dict:
    """Get schedule for a specific college basketball team.

    Args:
        team_id: ESPN team ID.
        season: Season year. Defaults to current.
    """
    return wrap(_get_team_schedule(_params(team_id=team_id, season=season)))


def get_game_summary(*, event_id: str) -> dict:
    """Get detailed game summary with box score.

    Args:
        event_id: ESPN event ID.
    """
    return wrap(_get_game_summary(_params(event_id=event_id)))


def get_rankings(*, season: int | None = None, week: int | None = None) -> dict:
    """Get college basketball rankings (AP Top 25, Coaches Poll).

    Args:
        season: Season year. Defaults to current.
        week: Week number for historical rankings.
    """
    return wrap(_get_rankings(_params(season=season, week=week)))


def get_news(*, team_id: str | None = None) -> dict:
    """Get college basketball news articles.

    Args:
        team_id: Optional ESPN team ID to filter news by team.
    """
    return wrap(_get_news(_params(team_id=team_id)))


def get_schedule(*, date: str | None = None, season: int | None = None, group: int | None = None) -> dict:
    """Get college basketball schedule.

    Args:
        date: Date in YYYY-MM-DD format.
        season: Season year. Defaults to current.
        group: Conference group ID to filter by.
    """
    return wrap(_get_schedule(_params(date=date, season=season, group=group)))


def get_play_by_play(*, event_id: str) -> dict:
    """Get full play-by-play log for a college basketball game.

    Args:
        event_id: ESPN event ID.
    """
    return wrap(_get_play_by_play(_params(event_id=event_id)))


def get_win_probability(*, event_id: str) -> dict:
    """Get win probability timeline for a college basketball game.

    Args:
        event_id: ESPN event ID.
    """
    return wrap(_get_win_probability(_params(event_id=event_id)))
