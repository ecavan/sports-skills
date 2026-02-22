from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def f1_get_session_data(
    session_year: int, session_name: str, session_type: str = "Q"
) -> str:
    """Get detailed F1 session data (qualifying, race, practice).

    Args:
        session_year: Year of the session.
        session_name: Event name (e.g., "Monza").
        session_type: Session type — "Q" (qualifying), "R" (race), "FP1", etc.
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(
        f1.get_session_data(
            session_year=session_year,
            session_name=session_name,
            session_type=session_type,
        )
    )


@tool(parse_docstring=True)
def f1_get_driver_info(year: int, driver: str | None = None) -> str:
    """Get F1 driver information for a season.

    Args:
        year: Season year.
        driver: Driver code or name (optional — omit for all drivers).
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_driver_info(year=year, driver=driver))


@tool(parse_docstring=True)
def f1_get_team_info(year: int, team: str | None = None) -> str:
    """Get F1 team information for a season.

    Args:
        year: Season year.
        team: Team name (optional — omit for all teams).
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_team_info(year=year, team=team))


@tool(parse_docstring=True)
def f1_get_race_schedule(year: int) -> str:
    """Get F1 race schedule for a season.

    Args:
        year: Season year.
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_race_schedule(year=year))


@tool(parse_docstring=True)
def f1_get_lap_data(
    year: int,
    event: str,
    session_type: str = "R",
    driver: str | None = None,
) -> str:
    """Get F1 lap-by-lap timing data.

    Args:
        year: Season year.
        event: Event name (e.g., "Monza").
        session_type: Session type — "R" (race), "Q", "FP1", etc.
        driver: Driver code (optional — omit for all drivers).
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(
        f1.get_lap_data(
            year=year, event=event, session_type=session_type, driver=driver
        )
    )


@tool(parse_docstring=True)
def f1_get_race_results(year: int, event: str) -> str:
    """Get F1 race results (positions, times, points).

    Args:
        year: Season year.
        event: Event name (e.g., "Monza").
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_race_results(year=year, event=event))


@tool(parse_docstring=True)
def f1_get_pit_stops(
    year: int, event: str | None = None, driver: str | None = None
) -> str:
    """Get F1 pit stop durations (PitIn to PitOut) for a race or full season.

    Args:
        year: Season year.
        event: Event name (optional — omit for full season).
        driver: Driver code (optional — omit for all drivers).
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_pit_stops(year=year, event=event, driver=driver))


@tool(parse_docstring=True)
def f1_get_speed_data(
    year: int, event: str | None = None, driver: str | None = None
) -> str:
    """Get F1 speed trap and intermediate speed data for a race or full season.

    Args:
        year: Season year.
        event: Event name (optional — omit for full season).
        driver: Driver code (optional — omit for all drivers).
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_speed_data(year=year, event=event, driver=driver))


@tool(parse_docstring=True)
def f1_get_championship_standings(year: int) -> str:
    """Get F1 driver and constructor championship standings aggregated from all race results.

    Args:
        year: Season year.
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_championship_standings(year=year))


@tool(parse_docstring=True)
def f1_get_season_stats(year: int) -> str:
    """Get aggregated F1 season stats: fastest laps, top speeds, points, wins, podiums per driver and team.

    Args:
        year: Season year.
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_season_stats(year=year))


@tool(parse_docstring=True)
def f1_get_team_comparison(
    year: int, team1: str, team2: str, event: str | None = None
) -> str:
    """Compare two F1 teams head-to-head: qualifying, race pace, sectors, points.

    Args:
        year: Season year.
        team1: First team name (e.g., "Red Bull").
        team2: Second team name (e.g., "McLaren").
        event: Event name (optional — omit for full season).
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(
        f1.get_team_comparison(year=year, team1=team1, team2=team2, event=event)
    )


@tool(parse_docstring=True)
def f1_get_teammate_comparison(
    year: int, team: str, event: str | None = None
) -> str:
    """Compare F1 teammates within the same team: qualifying H2H, race H2H, pace delta.

    Args:
        year: Season year.
        team: Team name (e.g., "McLaren").
        event: Event name (optional — omit for full season).
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_teammate_comparison(year=year, team=team, event=event))


@tool(parse_docstring=True)
def f1_get_tire_analysis(
    year: int, event: str | None = None, driver: str | None = None
) -> str:
    """F1 tire strategy and degradation analysis: compound usage, stint lengths, deg rates.

    Args:
        year: Season year.
        event: Event name (optional — omit for full season).
        driver: Driver code (optional — omit for all drivers).
    """
    try:
        from sports_skills import f1
    except ImportError:
        return _json({"error": "F1 module requires fastf1. Install with: pip install sports-skills[f1]"})

    return _json(f1.get_tire_analysis(year=year, event=event, driver=driver))


ALL_TOOLS = [
    f1_get_session_data,
    f1_get_driver_info,
    f1_get_team_info,
    f1_get_race_schedule,
    f1_get_lap_data,
    f1_get_race_results,
    f1_get_pit_stops,
    f1_get_speed_data,
    f1_get_championship_standings,
    f1_get_season_stats,
    f1_get_team_comparison,
    f1_get_teammate_comparison,
    f1_get_tire_analysis,
]
