---
name: nba-data
description: |
  NBA data — scores, standings, rosters, schedules, game summaries, statistical leaders, and news.
  Use when: user asks about NBA scores, standings, team rosters, schedules, game box scores, or NBA news.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# NBA Data

Community NBA data skill. Uses publicly accessible ESPN endpoints. Data is sourced from ESPN and is subject to their terms of use.

## Installation

```bash
pip install sports-skills
```

## Commands

All commands are run via the `sports-skills` CLI:

```bash
sports-skills nba <command> [--param=value ...]
```

### get_scoreboard

Get live or recent NBA scores.

```bash
sports-skills nba get_scoreboard
sports-skills nba get_scoreboard --date=2026-02-18
```

**Parameters:**
- `--date` (optional): Date in YYYY-MM-DD format. Defaults to today.

### get_standings

Get NBA standings by conference.

```bash
sports-skills nba get_standings
sports-skills nba get_standings --season=2026
```

**Parameters:**
- `--season` (optional): Season year (e.g. 2026). Defaults to current season.

### get_teams

Get all 30 NBA teams with logos and basic info.

```bash
sports-skills nba get_teams
```

### get_team_roster

Get the full roster for an NBA team.

```bash
sports-skills nba get_team_roster --team_id=13
```

**Parameters:**
- `--team_id` (required): ESPN team ID.

### get_team_schedule

Get the schedule for a specific NBA team.

```bash
sports-skills nba get_team_schedule --team_id=13
sports-skills nba get_team_schedule --team_id=13 --season=2026
```

**Parameters:**
- `--team_id` (required): ESPN team ID.
- `--season` (optional): Season year. Defaults to current season.

### get_game_summary

Get a detailed game summary with box score, scoring plays, and leaders.

```bash
sports-skills nba get_game_summary --event_id=401584793
```

**Parameters:**
- `--event_id` (required): ESPN event ID.

### get_leaders

Get NBA statistical leaders (points, rebounds, assists, etc.).

```bash
sports-skills nba get_leaders
sports-skills nba get_leaders --season=2026
```

**Parameters:**
- `--season` (optional): Season year. Defaults to current season.

### get_news

Get NBA news articles, optionally filtered by team.

```bash
sports-skills nba get_news
sports-skills nba get_news --team_id=13
```

**Parameters:**
- `--team_id` (optional): ESPN team ID to filter news by team.

### get_schedule

Get NBA schedule for a specific date.

```bash
sports-skills nba get_schedule
sports-skills nba get_schedule --date=2026-02-18
```

**Parameters:**
- `--date` (optional): Date in YYYY-MM-DD format. Defaults to today.
- `--season` (optional): Season year. Defaults to current season.

## Common NBA Team IDs

| Team | ID | Team | ID |
|------|-----|------|-----|
| Atlanta Hawks | 1 | Memphis Grizzlies | 29 |
| Boston Celtics | 2 | Miami Heat | 14 |
| Brooklyn Nets | 17 | Milwaukee Bucks | 15 |
| Charlotte Hornets | 30 | Minnesota Timberwolves | 16 |
| Chicago Bulls | 4 | New Orleans Pelicans | 3 |
| Cleveland Cavaliers | 5 | New York Knicks | 18 |
| Dallas Mavericks | 6 | Oklahoma City Thunder | 25 |
| Denver Nuggets | 7 | Orlando Magic | 19 |
| Detroit Pistons | 8 | Philadelphia 76ers | 20 |
| Golden State Warriors | 9 | Phoenix Suns | 21 |
| Houston Rockets | 10 | Portland Trail Blazers | 22 |
| Indiana Pacers | 11 | Sacramento Kings | 23 |
| LA Clippers | 12 | San Antonio Spurs | 24 |
| Los Angeles Lakers | 13 | Toronto Raptors | 28 |
| Utah Jazz | 26 | Washington Wizards | 27 |

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
