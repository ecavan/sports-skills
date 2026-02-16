---
name: football-data
description: Live football/soccer data across 12 leagues including Premier League, La Liga, Bundesliga, Serie A, Champions League, and FIFA World Cup. Provides match scores, standings, lineups, player statistics, expected goals (xG), transfers, and injuries. Use when the user asks about football matches, soccer scores, league tables, player stats, team info, or any football/soccer data. Zero API keys required.
---

# Football Data

Open-source football data connector aggregating 5 sources with intelligent fallback. Covers 12 major leagues and competitions. No API key required.

## Data Sources

| Source | Coverage | Auth |
|--------|----------|------|
| ESPN | Primary source for all 12 leagues. Live scores, lineups, stats. | None |
| football-data.org | Enrichment for match details, competitions, seasons. | Optional API key |
| Fantasy Premier League | Premier League only: injuries, xG/xA, form, ICT index, prices. | None |
| Understat | Top 5 European leagues: xG, xA, shot maps. | None |
| Transfermarkt | Market values, transfer history. | None |

ESPN is the primary fallback. All commands work with zero API keys.

## Supported Competitions

| Competition | Slug | Country |
|------------|------|---------|
| Premier League | `premier-league` | England |
| La Liga | `la-liga` | Spain |
| Bundesliga | `bundesliga` | Germany |
| Serie A | `serie-a` | Italy |
| Ligue 1 | `ligue-1` | France |
| Championship | `championship` | England |
| Eredivisie | `eredivisie` | Netherlands |
| Primeira Liga | `primeira-liga` | Portugal |
| Serie A Brazil | `serie-a-brazil` | Brazil |
| Champions League | `champions-league` | Europe |
| European Championship | `european-championship` | Europe |
| FIFA World Cup | `world-cup` | International |

## Commands

### Competition & Season

**get_competitions** - List all 12 supported competitions with current season info.

```
Params: none required
Optional: api_key (string) - football-data.org key for enrichment
Returns: { competitions: [...] }
```

**get_current_season** - Detect the current active season for a competition.

```
Params:
  competition_id (string, required) - Competition slug (e.g. "premier-league")
Returns: { competition: {...}, season: {...}, calendar_dates: int }
```

**get_competition_seasons** - Get all available seasons for a competition.

```
Params:
  competition_id (string, required)
Returns: { competition: {...}, seasons: [...] }
```

### Schedule & Results

**get_season_schedule** - Get all fixtures for a season (paginated).

```
Params:
  season_id (string, required)
Returns: { schedules: [...] }
```

**get_daily_schedule** - Get all matches across all competitions for a specific date.

```
Params:
  date (string, optional) - Format: YYYY-MM-DD. Defaults to today.
Returns: { date: string, events: [...] }
```

**get_team_schedule** - Get upcoming and recent matches for a specific team.

```
Params:
  team_id (string, required)
  league_slug (string, optional)
  season_year (string, optional)
Returns: { team: {...}, events: [...] }
```

### Standings & Leaders

**get_season_standings** - Get the league table with home/away/total groupings.

```
Params:
  season_id (string, required)
Returns: { standings: [{ name, type, entries: [...] }] }
```

**get_season_leaders** - Get top scorers, assist leaders, and card leaders.

```
Params:
  season_id (string, required)
Returns: { leaders: [{ player: {...}, goals: int, ... }] }
```

### Team Data

**get_season_teams** - Get all teams participating in a season.

```
Params:
  season_id (string, required)
Returns: { teams: [...] }
```

**get_team_profile** - Get team details including squad roster, manager, and venue.

```
Params:
  team_id (string, required)
  league_slug (string, optional) - Helps with FPL enrichment for PL teams
Returns: { team: {...}, players: [...], manager: {...}, venue: {...} }
```

**get_head_to_head** - Get head-to-head match history between two teams.

```
Params:
  team_id (string, required)
  team_id_2 (string, required)
Returns: { teams: [...], events: [...] }
Note: Requires football-data.org API key. No ESPN fallback for this command.
```

### Match/Event Data

**get_event_summary** - Get match summary with scores, teams, and venue.

```
Params:
  event_id (string, required)
  league_slug (string, optional)
Returns: { event: {...}, statistics: {...} }
```

**get_event_lineups** - Get starting lineups, formations, and substitutes.

```
Params:
  event_id (string, required)
Returns: { lineups: [{ team: {...}, formation: string, starting: [...], bench: [...] }] }
```

**get_event_statistics** - Get team-level match statistics (possession, shots, passes, etc.).

```
Params:
  event_id (string, required)
Returns: { teams: [{ team: {...}, statistics: {...}, qualifier: "home"|"away" }] }
```

**get_event_timeline** - Get all match events: goals, cards, substitutions, VAR decisions.

```
Params:
  event_id (string, required)
Returns: { timeline: [{ type, minute, player: {...}, team: {...} }] }
```

**get_event_xg** - Get expected goals (xG) data with shot maps.

```
Params:
  event_id (string, required)
Returns: { event_id, teams: [{ xg: float, ... }], shots: [...] }
Coverage: Premier League, La Liga, Bundesliga, Serie A, Ligue 1 only (via Understat).
```

**get_event_players_statistics** - Get individual player statistics for a match.

```
Params:
  event_id (string, required)
Returns: { event_id, teams: [{ players: [...], qualifier: "home"|"away" }] }
Player stats include: minutes, rating, goals, assists, shots, passes, tackles, interceptions, dribbles, duels.
```

### Player & Transfer Data

**get_player_profile** - Get player biography, career stats, market value, and transfer history.

```
Params (at least one required):
  player_id (string) - football-data.org player ID
  fpl_id (string) - Fantasy Premier League player ID
  tm_player_id (string) - Transfermarkt player ID
Returns: { player: {..., fpl_data: {...}, market_value: {...}, transfer_history: [...]} }
```

**get_missing_players** - Get injured and suspended players by team.

```
Params:
  season_id (string, required)
Returns: { season_id, teams: [{ team: {...}, players: [...] }] }
Coverage: Premier League only (via FPL).
```

**get_season_transfers** - Get player transfers for a season.

```
Params:
  tm_player_ids (list, required) - Transfermarkt player IDs (max 50)
  season_id (string, optional)
Returns: { season_id, transfers: [...] }
```

## Response Format

All commands return normalized JSON following IPTC Sport Schema conventions:

```json
{
  "status": true,
  "data": { ... },
  "message": "Description of result"
}
```

Match events include standardized status values: `not_started`, `live`, `halftime`, `1st_half`, `2nd_half`, `closed`, `postponed`, `suspended`, `cancelled`.

## Usage Examples

Get today's Premier League matches:
> "What Premier League matches are on today?"
> Uses: get_daily_schedule

Check the league standings:
> "Show me the current La Liga table"
> Uses: get_current_season (to find season_id) then get_season_standings

Get match details:
> "What happened in the Arsenal vs Chelsea match?"
> Uses: get_event_summary, get_event_statistics, get_event_timeline

Check xG data:
> "What was the xG for Liverpool's last match?"
> Uses: get_event_xg

Get player info:
> "Show me Haaland's stats and market value"
> Uses: get_player_profile
