"""Formula 1 data — race schedules, results, lap data, driver/team info.

Requires optional dependencies: pip install sports-skills[f1]
"""

from sports_skills.f1._connector import (
    get_session_data as _get_session_data,
    get_driver_info as _get_driver_info,
    get_team_info as _get_team_info,
    get_race_schedule as _get_race_schedule,
    get_lap_data as _get_lap_data,
    get_race_results as _get_race_results,
)


def _req(**kwargs):
    """Build request_data dict from kwargs."""
    return {"params": {k: v for k, v in kwargs.items() if v is not None}}


def get_session_data(*, session_year: int, session_name: str, session_type: str = "Q") -> dict:
    """Get detailed session data (qualifying, race, practice).

    Args:
        session_year: Year of the session.
        session_name: Event name (e.g., "Monza").
        session_type: Session type — "Q" (qualifying), "R" (race), "FP1", etc.
    """
    return _get_session_data(_req(session_year=session_year, session_name=session_name, session_type=session_type))


def get_driver_info(*, year: int, driver: str | None = None) -> dict:
    """Get driver information for a season.

    Args:
        year: Season year.
        driver: Driver code or name (optional — omit for all drivers).
    """
    return _get_driver_info(_req(year=year, driver=driver))


def get_team_info(*, year: int, team: str | None = None) -> dict:
    """Get team information for a season.

    Args:
        year: Season year.
        team: Team name (optional — omit for all teams).
    """
    return _get_team_info(_req(year=year, team=team))


def get_race_schedule(*, year: int) -> dict:
    """Get race schedule for a season."""
    return _get_race_schedule(_req(year=year))


def get_lap_data(*, year: int, event: str, session_type: str = "R", driver: str | None = None) -> dict:
    """Get lap-by-lap timing data.

    Args:
        year: Season year.
        event: Event name (e.g., "Monza").
        session_type: Session type — "R" (race), "Q", "FP1", etc.
        driver: Driver code (optional — omit for all drivers).
    """
    return _get_lap_data(_req(year=year, event=event, session_type=session_type, driver=driver))


def get_race_results(*, year: int, event: str) -> dict:
    """Get race results (positions, times, points).

    Args:
        year: Season year.
        event: Event name (e.g., "Monza").
    """
    return _get_race_results(_req(year=year, event=event))
