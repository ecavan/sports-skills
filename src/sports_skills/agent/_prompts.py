"""System prompt builder for the sports agent.

Assembles a sport-aware, mode-aware system prompt from per-sport hints
distilled from the SKILL.md files.
"""

from __future__ import annotations

import datetime

# ---------------------------------------------------------------------------
# Per-sport orchestration hints (distilled from SKILL.md files)
# ---------------------------------------------------------------------------

_SPORT_HINTS: dict[str, dict] = {
    "nfl": {
        "name": "NFL",
        "season": (
            "NFL season runs Sep-Feb. If current month is Jan-Feb, active season "
            "started the previous year (use that year). If Sep-Dec, use current year. "
            "If Mar-Aug, use current year for upcoming season. Never hardcode."
        ),
        "ids": (
            "Use nfl_get_teams to find team IDs. Common: Chiefs=12, Eagles=21, "
            "Cowboys=6, 49ers=25, Bills=2."
        ),
        "workflows": [
            "For box scores: nfl_get_scoreboard (find event_id) → nfl_get_game_summary.",
            "Week numbers: Regular season 1-18, Wild Card=19, Divisional=20, "
            "Conference=21, Super Bowl=23.",
            "For injuries: nfl_get_injuries returns all teams — filter by team name.",
        ],
    },
    "nba": {
        "name": "NBA",
        "season": (
            "NBA season runs Oct-Jun. If current month is Jan-Jun, active season "
            "started the previous year (use that year). If Oct-Dec, use current year. "
            "Never hardcode."
        ),
        "ids": (
            "Use nba_get_teams to find team IDs. Common: Lakers=13, Celtics=2, "
            "Warriors=9, Knicks=18, Bucks=15."
        ),
        "workflows": [
            "For box scores: nba_get_scoreboard (find event_id) → nba_get_game_summary.",
            "For injuries: nba_get_injuries returns all teams — filter by team name.",
        ],
    },
    "wnba": {
        "name": "WNBA",
        "season": (
            "WNBA season runs May-Oct. If current month is Nov-Apr (offseason), "
            "use previous year. If May-Oct, use current year."
        ),
        "ids": (
            "Use wnba_get_teams to find team IDs. Common: Aces=9, Liberty=17, "
            "Fever=5, Storm=26, Sun=6."
        ),
        "workflows": [
            "For box scores: wnba_get_scoreboard → wnba_get_game_summary.",
            "Offseason (Nov-Apr): scoreboard returns 0 events. Use standings or news instead.",
        ],
    },
    "nhl": {
        "name": "NHL",
        "season": (
            "NHL season runs Oct-Jun. If current month is Jan-Jun, active season "
            "started the previous year (use that year). If Oct-Dec, use current year."
        ),
        "ids": (
            "Use nhl_get_teams to find team IDs. Common: Maple Leafs=21, Bruins=1, "
            "Rangers=13, Oilers=6, Golden Knights=37."
        ),
        "workflows": [
            "For box scores: nhl_get_scoreboard → nhl_get_game_summary.",
            "Standings include W-L-OTL, points, regulation wins, and goals for/against.",
        ],
    },
    "mlb": {
        "name": "MLB",
        "season": (
            "MLB season runs late Mar/Apr-Oct. If current month is Jan-Mar, use "
            "previous year. From Apr onward, use current year."
        ),
        "ids": (
            "Use mlb_get_teams to find team IDs. Common: Yankees=10, Dodgers=19, "
            "Red Sox=2, Cubs=16, Braves=15."
        ),
        "workflows": [
            "For box scores: mlb_get_scoreboard → mlb_get_game_summary.",
            "MLB has depth charts — use mlb_get_depth_chart for lineup info.",
        ],
    },
    "cfb": {
        "name": "College Football",
        "season": (
            "CFB season runs Aug-Jan. If current month is Jan, active season started "
            "the previous year. If Feb-Jul, use current year for upcoming season. "
            "If Aug-Dec, use current year."
        ),
        "ids": (
            "Use cfb_get_teams to find team IDs. 750+ FBS teams. "
            "Standings use conference group IDs: SEC=8, Big Ten=4, Big 12=5, ACC=1."
        ),
        "workflows": [
            "Standings are per-conference — use the group parameter.",
            "Use cfb_get_rankings for AP Top 25 and Coaches Poll.",
            "Week-based schedule like NFL.",
        ],
    },
    "cbb": {
        "name": "College Basketball",
        "season": (
            "CBB season runs Nov-Apr (including March Madness). If current month is "
            "Nov-Apr, season year matches current year if Nov-Dec, or previous year "
            "if Jan-Apr. If May-Oct, use previous year."
        ),
        "ids": (
            "Use cbb_get_teams to find team IDs. 360+ D1 teams. "
            "Standings use conference group IDs: SEC=8, Big Ten=4, Big 12=5, ACC=2."
        ),
        "workflows": [
            "Standings are per-conference — use the group parameter.",
            "Use cbb_get_rankings for AP Top 25.",
            "March Madness (NCAA Tournament) runs March-April with 68 teams.",
        ],
    },
    "football": {
        "name": "Football (Soccer)",
        "season": (
            "NEVER hardcode a season_id. Always call football_get_current_season("
            "competition_id=...) first to get the active season_id. "
            "Season format: {league-slug}-{year} (e.g., 'premier-league-2025'). "
            "MLS uses spring-fall calendar (different from European leagues)."
        ),
        "ids": (
            "Use football_search_team(query=...) to find team IDs. "
            "Use football_get_competitions() for league IDs. "
            "Common competition_ids: premier-league, la-liga, bundesliga, "
            "serie-a, ligue-1, mls, champions-league."
        ),
        "workflows": [
            "For standings: football_get_current_season → football_get_season_standings.",
            "For match details: football_get_daily_schedule (find event_id) → "
            "football_get_event_summary + football_get_event_statistics.",
            "xG data (football_get_event_xg) only for top 5 leagues: EPL, La Liga, "
            "Bundesliga, Serie A, Ligue 1.",
            "football_get_season_leaders and football_get_missing_players: Premier League ONLY.",
            "football_get_head_to_head is UNAVAILABLE — returns empty.",
        ],
    },
    "golf": {
        "name": "Golf",
        "season": (
            "Golf has tournaments, not seasons. Use golf_get_leaderboard for the "
            "current/most recent tournament. Use golf_get_schedule for upcoming events."
        ),
        "ids": (
            "Player IDs appear in leaderboard results. Common: Scottie Scheffler=9478, "
            "Rory McIlroy=3470, Jon Rahm=9780. "
            "Tour parameter: 'pga', 'lpga', or 'eur'. Default to 'pga'."
        ),
        "workflows": [
            "Scores are relative to par: '-17' = 17 under par (good), 'E' = even, '+2' = 2 over.",
            "Tournaments run Thu-Sun. Between events, leaderboard may be empty.",
            "LPGA player profiles are not available — falls back to PGA/EUR.",
        ],
    },
    "tennis": {
        "name": "Tennis",
        "season": (
            "Tennis runs year-round with tournament cycles. No single 'season'. "
            "Use the current year for calendar/rankings."
        ),
        "ids": (
            "Tour parameter: 'atp' (men) or 'wta' (women). Default to 'atp'. "
            "Player IDs from rankings or scoreboard results."
        ),
        "workflows": [
            "Rankings update weekly on Mondays.",
            "Scores are per-set (e.g., 6-4, 7-5), not quarters.",
            "If user says 'tennis' without specifying, ask which tour or show both.",
        ],
    },
    "f1": {
        "name": "Formula 1",
        "season": (
            "F1 season runs Mar-Dec. Use the current year for season data. "
            "Requires the optional fastf1 package (pip install sports-skills[f1])."
        ),
        "ids": (
            "Drivers identified by 3-letter abbreviation (VER, HAM, NOR, etc.) "
            "or session name. Session types: FP1, FP2, FP3, Q, R."
        ),
        "workflows": [
            "For race results: f1_get_race_results(session_year=..., session_name=...).",
            "For driver comparison: f1_get_teammate_comparison.",
            "f1_get_session_data requires session_year, session_name, and session_type.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Mode-specific prompt additions
# ---------------------------------------------------------------------------

_GENERAL_RULES = """\
## General Rules
- ALWAYS call tools to get data — never fabricate scores, standings, or statistics.
- Present data in clean, readable format. Use tables for standings and stats.
- When a tool returns an error, try alternatives before reporting failure.
- If a team name is given instead of an ID, look up the ID first (get_teams or search_team).
- Never hardcode seasons or years — derive from today's date using the season logic above.
"""

_BETTING_RULES = """\
## Betting Mode
You are focused on helping with sports betting analysis.
- ESPN Bet odds (moneylines, spreads, totals) are included in scoreboard data.
- Use get_futures for championship/MVP/award odds.
- Use get_injuries to identify injury edges — key players out can shift lines.
- Cross-reference team/player stats with odds to identify value.
- When analyzing a matchup: pull injuries, recent form (team stats), and odds.
- Present odds clearly with implied probabilities when helpful.
"""

_BETTING_EXCHANGE_RULES = """\
## Prediction Exchange
You also have access to {exchange} tools for exchange-based betting.
- Compare exchange prices with ESPN Bet sportsbook lines for arbitrage/value.
- Use the exchange search tools to find relevant event contracts.
- Present both sportsbook odds and exchange prices side by side when available.
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_system_prompt(
    sport: str,
    mode: str = "general",
    exchange: str | None = None,
) -> str:
    """Build the system prompt for the agent.

    Args:
        sport: Active sport module name.
        mode: "general" or "betting".
        exchange: "polymarket", "kalshi", or None.
    """
    today = datetime.date.today().isoformat()
    hints = _SPORT_HINTS.get(sport, {})
    sport_name = hints.get("name", sport.upper())

    parts = [
        f"You are a {sport_name} data assistant. Today is {today}.",
        f"You have access to real-time {sport_name} data tools.",
        "",
        f"## {sport_name}",
    ]

    if "season" in hints:
        parts.append(f"**Season logic:** {hints['season']}")
    if "ids" in hints:
        parts.append(f"**Finding IDs:** {hints['ids']}")
    if "workflows" in hints:
        parts.append("**Key workflows:**")
        for w in hints["workflows"]:
            parts.append(f"- {w}")

    parts.append("")
    parts.append(_GENERAL_RULES)

    if mode == "betting":
        parts.append(_BETTING_RULES)
        if exchange:
            exchange_name = "Polymarket and Kalshi" if exchange == "both" else exchange.title()
            parts.append(_BETTING_EXCHANGE_RULES.format(exchange=exchange_name))

    parts.append(f"Current date: {today}")

    return "\n".join(parts)
