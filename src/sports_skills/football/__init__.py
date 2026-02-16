"""Football data — standings, schedules, match stats, xG, transfers, and more.

Wraps the machina-football-data connector (ESPN, Understat, FPL, Transfermarkt).
No API keys required. Zero config.
"""

from sports_skills._response import wrap
from sports_skills.football._connector import (
    get_current_season as _get_current_season,
    get_competitions as _get_competitions,
    get_competition_seasons as _get_competition_seasons,
    get_season_schedule as _get_season_schedule,
    get_season_standings as _get_season_standings,
    get_season_leaders as _get_season_leaders,
    get_season_teams as _get_season_teams,
    get_team_profile as _get_team_profile,
    get_daily_schedule as _get_daily_schedule,
    get_event_summary as _get_event_summary,
    get_event_lineups as _get_event_lineups,
    get_event_statistics as _get_event_statistics,
    get_event_timeline as _get_event_timeline,
    get_team_schedule as _get_team_schedule,
    get_head_to_head as _get_head_to_head,
    get_event_xg as _get_event_xg,
    get_event_players_statistics as _get_event_players_statistics,
    get_missing_players as _get_missing_players,
    get_season_transfers as _get_season_transfers,
    get_player_profile as _get_player_profile,
)


def _params(**kwargs):
    """Build params dict, filtering out None values."""
    return {k: v for k, v in kwargs.items() if v is not None}


def get_current_season(*, competition_id: str) -> dict:
    """Detect current season for a competition."""
    return wrap(_get_current_season(_params(competition_id=competition_id)))


def get_competitions() -> dict:
    """List available competitions with current season info."""
    return wrap(_get_competitions(_params()))


def get_competition_seasons(*, competition_id: str) -> dict:
    """Get available seasons for a competition."""
    return wrap(_get_competition_seasons(_params(competition_id=competition_id)))


def get_season_schedule(*, season_id: str) -> dict:
    """Get full season match schedule."""
    return wrap(_get_season_schedule(_params(season_id=season_id)))


def get_season_standings(*, season_id: str) -> dict:
    """Get league table for a season."""
    return wrap(_get_season_standings(_params(season_id=season_id)))


def get_season_leaders(*, season_id: str) -> dict:
    """Get top scorers/leaders for a season."""
    return wrap(_get_season_leaders(_params(season_id=season_id)))


def get_season_teams(*, season_id: str) -> dict:
    """Get teams in a season."""
    return wrap(_get_season_teams(_params(season_id=season_id)))


def get_team_profile(*, team_id: str, league_slug: str | None = None) -> dict:
    """Get team profile with squad/roster."""
    return wrap(_get_team_profile(_params(team_id=team_id, league_slug=league_slug)))


def get_daily_schedule(*, date: str | None = None) -> dict:
    """Get all matches for a specific date across all leagues.

    Args:
        date: Date string in YYYY-MM-DD format. Defaults to today.
    """
    return wrap(_get_daily_schedule(_params(date=date)))


def get_event_summary(*, event_id: str) -> dict:
    """Get match summary with basic info and scores."""
    return wrap(_get_event_summary(_params(event_id=event_id)))


def get_event_lineups(*, event_id: str) -> dict:
    """Get match lineups."""
    return wrap(_get_event_lineups(_params(event_id=event_id)))


def get_event_statistics(*, event_id: str) -> dict:
    """Get match team statistics."""
    return wrap(_get_event_statistics(_params(event_id=event_id)))


def get_event_timeline(*, event_id: str) -> dict:
    """Get match timeline/key events."""
    return wrap(_get_event_timeline(_params(event_id=event_id)))


def get_team_schedule(*, team_id: str, league_slug: str | None = None, season_year: str | None = None) -> dict:
    """Get schedule for a specific team."""
    return wrap(_get_team_schedule(_params(team_id=team_id, league_slug=league_slug, season_year=season_year)))


def get_head_to_head(*, team_id: str, team_id_2: str) -> dict:
    """Get head-to-head history between two teams."""
    return wrap(_get_head_to_head(_params(team_id=team_id, team_id_2=team_id_2)))


def get_event_xg(*, event_id: str) -> dict:
    """Get expected goals (xG) data from Understat."""
    return wrap(_get_event_xg(_params(event_id=event_id)))


def get_event_players_statistics(*, event_id: str) -> dict:
    """Get player-level match statistics."""
    return wrap(_get_event_players_statistics(_params(event_id=event_id)))


def get_missing_players(*, season_id: str) -> dict:
    """Get injured/missing/doubtful players (PL only via FPL)."""
    return wrap(_get_missing_players(_params(season_id=season_id)))


def get_season_transfers(*, season_id: str, tm_player_ids: list[str] | None = None) -> dict:
    """Get season transfers via Transfermarkt."""
    return wrap(_get_season_transfers(_params(season_id=season_id, tm_player_ids=tm_player_ids)))


def get_player_profile(*, fpl_id: str | None = None, tm_player_id: str | None = None) -> dict:
    """Get player profile. At least one ID required.

    Args:
        fpl_id: FPL player ID (Premier League players only).
        tm_player_id: Transfermarkt player ID (any league).
    """
    return wrap(_get_player_profile(_params(fpl_id=fpl_id, tm_player_id=tm_player_id)))
