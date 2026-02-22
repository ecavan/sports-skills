from __future__ import annotations

import json

from langchain_core.tools import tool


def _json(result: dict) -> str:
    return json.dumps(result, default=str, ensure_ascii=False)


@tool(parse_docstring=True)
def football_get_competitions() -> str:
    """List available football competitions with current season info."""
    from sports_skills import football

    return _json(football.get_competitions())


@tool(parse_docstring=True)
def football_get_competition_seasons(competition_id: str) -> str:
    """Get available seasons for a football competition.

    Args:
        competition_id: Competition identifier.
    """
    from sports_skills import football

    return _json(football.get_competition_seasons(competition_id=competition_id))


@tool(parse_docstring=True)
def football_get_current_season(competition_id: str) -> str:
    """Detect current season for a football competition.

    Args:
        competition_id: Competition identifier.
    """
    from sports_skills import football

    return _json(football.get_current_season(competition_id=competition_id))


@tool(parse_docstring=True)
def football_get_season_schedule(season_id: str) -> str:
    """Get full season match schedule.

    Args:
        season_id: Season identifier.
    """
    from sports_skills import football

    return _json(football.get_season_schedule(season_id=season_id))


@tool(parse_docstring=True)
def football_get_season_standings(season_id: str) -> str:
    """Get league table for a football season.

    Args:
        season_id: Season identifier.
    """
    from sports_skills import football

    return _json(football.get_season_standings(season_id=season_id))


@tool(parse_docstring=True)
def football_get_season_leaders(season_id: str) -> str:
    """Get top scorers and leaders for a football season.

    Args:
        season_id: Season identifier.
    """
    from sports_skills import football

    return _json(football.get_season_leaders(season_id=season_id))


@tool(parse_docstring=True)
def football_get_season_teams(season_id: str) -> str:
    """Get teams in a football season.

    Args:
        season_id: Season identifier.
    """
    from sports_skills import football

    return _json(football.get_season_teams(season_id=season_id))


@tool(parse_docstring=True)
def football_search_team(query: str, competition_id: str | None = None) -> str:
    """Search for a football team by name across all leagues.

    Args:
        query: Team name to search for.
        competition_id: Optional competition to narrow the search.
    """
    from sports_skills import football

    return _json(football.search_team(query=query, competition_id=competition_id))


@tool(parse_docstring=True)
def football_get_team_profile(team_id: str, league_slug: str | None = None) -> str:
    """Get football team profile with squad and roster.

    Args:
        team_id: Team identifier.
        league_slug: ESPN league slug (e.g. "eng.1" for Premier League).
    """
    from sports_skills import football

    return _json(football.get_team_profile(team_id=team_id, league_slug=league_slug))


@tool(parse_docstring=True)
def football_get_daily_schedule(date: str | None = None) -> str:
    """Get all football matches for a specific date across all leagues.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    from sports_skills import football

    return _json(football.get_daily_schedule(date=date))


@tool(parse_docstring=True)
def football_get_event_summary(event_id: str) -> str:
    """Get football match summary with basic info and scores.

    Args:
        event_id: Match event identifier.
    """
    from sports_skills import football

    return _json(football.get_event_summary(event_id=event_id))


@tool(parse_docstring=True)
def football_get_event_lineups(event_id: str) -> str:
    """Get football match lineups.

    Args:
        event_id: Match event identifier.
    """
    from sports_skills import football

    return _json(football.get_event_lineups(event_id=event_id))


@tool(parse_docstring=True)
def football_get_event_statistics(event_id: str) -> str:
    """Get football match team statistics.

    Args:
        event_id: Match event identifier.
    """
    from sports_skills import football

    return _json(football.get_event_statistics(event_id=event_id))


@tool(parse_docstring=True)
def football_get_event_timeline(event_id: str) -> str:
    """Get football match timeline and key events.

    Args:
        event_id: Match event identifier.
    """
    from sports_skills import football

    return _json(football.get_event_timeline(event_id=event_id))


@tool(parse_docstring=True)
def football_get_team_schedule(
    team_id: str,
    league_slug: str | None = None,
    season_year: str | None = None,
    competition_id: str | None = None,
) -> str:
    """Get schedule for a specific football team.

    Args:
        team_id: Team identifier.
        league_slug: ESPN league slug (e.g. "eng.1" for Premier League).
        season_year: Season year to filter by.
        competition_id: Competition to filter by.
    """
    from sports_skills import football

    return _json(
        football.get_team_schedule(
            team_id=team_id,
            league_slug=league_slug,
            season_year=season_year,
            competition_id=competition_id,
        )
    )


@tool(parse_docstring=True)
def football_get_head_to_head(team_id: str, team_id_2: str) -> str:
    """Get head-to-head history between two football teams.

    Args:
        team_id: First team identifier.
        team_id_2: Second team identifier.
    """
    from sports_skills import football

    return _json(football.get_head_to_head(team_id=team_id, team_id_2=team_id_2))


@tool(parse_docstring=True)
def football_get_event_xg(event_id: str) -> str:
    """Get expected goals (xG) data from Understat for a football match.

    Args:
        event_id: Match event identifier.
    """
    from sports_skills import football

    return _json(football.get_event_xg(event_id=event_id))


@tool(parse_docstring=True)
def football_get_event_players_statistics(event_id: str) -> str:
    """Get player-level match statistics for a football match.

    Args:
        event_id: Match event identifier.
    """
    from sports_skills import football

    return _json(football.get_event_players_statistics(event_id=event_id))


@tool(parse_docstring=True)
def football_get_missing_players(season_id: str) -> str:
    """Get injured, missing, and doubtful football players (PL only via FPL).

    Args:
        season_id: Season identifier.
    """
    from sports_skills import football

    return _json(football.get_missing_players(season_id=season_id))


@tool(parse_docstring=True)
def football_get_season_transfers(
    season_id: str, tm_player_ids: str | None = None
) -> str:
    """Get season transfers via Transfermarkt.

    Args:
        season_id: Season identifier.
        tm_player_ids: Comma-separated Transfermarkt player IDs.
    """
    from sports_skills import football

    ids = tm_player_ids.split(",") if tm_player_ids else None
    return _json(football.get_season_transfers(season_id=season_id, tm_player_ids=ids))


@tool(parse_docstring=True)
def football_get_player_profile(
    fpl_id: str | None = None, tm_player_id: str | None = None
) -> str:
    """Get football player profile. At least one ID required.

    Args:
        fpl_id: FPL player ID (Premier League players only).
        tm_player_id: Transfermarkt player ID (any league).
    """
    from sports_skills import football

    return _json(
        football.get_player_profile(fpl_id=fpl_id, tm_player_id=tm_player_id)
    )


@tool(parse_docstring=True)
def football_get_player_season_stats(
    player_id: str, league_slug: str | None = None
) -> str:
    """Get football player season gamelog with per-match stats.

    Returns appearances, goals, assists, shots, shots on target, fouls,
    offsides, and cards for each match in the current season.

    Args:
        player_id: ESPN athlete ID.
        league_slug: ESPN league slug (e.g. "eng.1" for Premier League, "esp.1" for La Liga). Defaults to "eng.1".
    """
    from sports_skills import football

    return _json(
        football.get_player_season_stats(
            player_id=player_id, league_slug=league_slug
        )
    )


ALL_TOOLS = [
    football_get_competitions,
    football_get_competition_seasons,
    football_get_current_season,
    football_get_season_schedule,
    football_get_season_standings,
    football_get_season_leaders,
    football_get_season_teams,
    football_search_team,
    football_get_team_profile,
    football_get_daily_schedule,
    football_get_event_summary,
    football_get_event_lineups,
    football_get_event_statistics,
    football_get_event_timeline,
    football_get_team_schedule,
    football_get_head_to_head,
    football_get_event_xg,
    football_get_event_players_statistics,
    football_get_missing_players,
    football_get_season_transfers,
    football_get_player_profile,
    football_get_player_season_stats,
]
