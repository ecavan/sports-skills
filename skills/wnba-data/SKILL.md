---
name: wnba-data
description: |
  WNBA data — scores, standings, rosters, schedules, game summaries, statistical leaders, and news.
  Use when: user asks about WNBA scores, standings, team rosters, schedules, game box scores, or WNBA news.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# WNBA Data

Community WNBA data skill. Uses publicly accessible ESPN endpoints. Data is sourced from ESPN and is subject to their terms of use.

## Installation

```bash
pip install sports-skills
```

## Commands

All commands are run via the `sports-skills` CLI:

```bash
sports-skills wnba <command> [--param=value ...]
```

### get_scoreboard

Get live or recent WNBA scores.

```bash
sports-skills wnba get_scoreboard
sports-skills wnba get_scoreboard --date=2026-06-15
```

**Parameters:**
- `--date` (optional): Date in YYYY-MM-DD format. Defaults to today.

### get_standings

Get WNBA standings by conference.

```bash
sports-skills wnba get_standings
sports-skills wnba get_standings --season=2025
```

**Parameters:**
- `--season` (optional): Season year (e.g. 2025). Defaults to current season.

### get_teams

Get all WNBA teams with logos and basic info.

```bash
sports-skills wnba get_teams
```

### get_team_roster

Get the full roster for a WNBA team.

```bash
sports-skills wnba get_team_roster --team_id=14
```

**Parameters:**
- `--team_id` (required): ESPN team ID.

### get_team_schedule

Get the schedule for a specific WNBA team.

```bash
sports-skills wnba get_team_schedule --team_id=14
sports-skills wnba get_team_schedule --team_id=14 --season=2025
```

**Parameters:**
- `--team_id` (required): ESPN team ID.
- `--season` (optional): Season year. Defaults to current season.

### get_game_summary

Get a detailed game summary with box score, scoring plays, and leaders.

```bash
sports-skills wnba get_game_summary --event_id=401585432
```

**Parameters:**
- `--event_id` (required): ESPN event ID.

### get_leaders

Get WNBA statistical leaders (points, rebounds, assists, etc.).

```bash
sports-skills wnba get_leaders
sports-skills wnba get_leaders --season=2025
```

**Parameters:**
- `--season` (optional): Season year. Defaults to current season.

### get_news

Get WNBA news articles, optionally filtered by team.

```bash
sports-skills wnba get_news
sports-skills wnba get_news --team_id=14
```

**Parameters:**
- `--team_id` (optional): ESPN team ID to filter news by team.

### get_schedule

Get WNBA schedule for a specific date.

```bash
sports-skills wnba get_schedule
sports-skills wnba get_schedule --date=2026-06-15
```

**Parameters:**
- `--date` (optional): Date in YYYY-MM-DD format. Defaults to today.
- `--season` (optional): Season year. Defaults to current season.

## Common WNBA Team IDs

| Team | ID |
|------|-----|
| Atlanta Dream | 1 |
| Chicago Sky | 4 |
| Connecticut Sun | 5 |
| Dallas Wings | 16 |
| Golden State Valkyries | 20 |
| Indiana Fever | 3 |
| Las Vegas Aces | 14 |
| Los Angeles Sparks | 6 |
| Minnesota Lynx | 8 |
| New York Liberty | 9 |
| Phoenix Mercury | 11 |
| Seattle Storm | 12 |
| Washington Mystics | 15 |

## Data Source

All data comes from ESPN's public web endpoints. This skill does not use an official API and endpoints may change without notice. Intended for personal, educational, and research use.

## Error Handling

All commands return a JSON envelope:

```json
{
  "status": true,
  "data": { ... },
  "message": ""
}
```

On error:

```json
{
  "status": false,
  "data": null,
  "message": "Error description"
}
```
