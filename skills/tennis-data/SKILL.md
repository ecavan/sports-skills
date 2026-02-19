---
name: tennis-data
description: |
  ATP and WTA tennis data via ESPN public endpoints — tournament scores, season calendars, player rankings, player profiles, and news. Zero config, no API keys.

  Use when: user asks about tennis scores, match results, tournament draws, ATP/WTA rankings, tennis player info, or tennis news.
  Don't use when: user asks about other sports. Don't use for live point-by-point data — scores update after each set/match.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# Tennis Data (ATP + WTA)

## Setup

Before first use, check if the CLI is available:
```bash
which sports-skills || pip install sports-skills
```
If `pip install` fails with a Python version error, the package requires Python 3.10+. Find a compatible Python:
```bash
python3 --version  # check version
# If < 3.10, try: python3.12 -m pip install sports-skills
# On macOS with Homebrew: /opt/homebrew/bin/python3.12 -m pip install sports-skills
```
No API keys required.

## Quick Start

Prefer the CLI — it avoids Python import path issues:
```bash
sports-skills tennis get_scoreboard --tour=atp
sports-skills tennis get_rankings --tour=wta
sports-skills tennis get_calendar --tour=atp --year=2026
```

## Important: Tennis is Not a Team Sport

Tennis data is fundamentally different from team sports (NFL, NBA, etc.):
- **Tournaments, not games**: Events are multi-day tournaments containing many matches.
- **Individual athletes**: Competitors are individual players (singles) or pairs (doubles), not teams.
- **Set-based scoring**: Scores are per-set game counts (e.g., 6-4, 7-5), not quarters.
- **Rankings, not standings**: Players have ATP/WTA ranking points, not team records.
- **No rosters or team schedules**: Tennis has no team-level commands.

## The `tour` Parameter

Most commands require `--tour=atp` or `--tour=wta`:
- **ATP**: Men's professional tennis tour
- **WTA**: Women's professional tennis tour

If the user doesn't specify, default to `atp` for men's tennis or `wta` for women's tennis. If the user just says "tennis" without specifying, ask which tour or show both by calling the command twice.

## Commands

### get_scoreboard
Get active tournaments with all current matches.
- `tour` (str, required): "atp" or "wta"
- `date` (str, optional): Date in YYYY-MM-DD format. Defaults to today.

Returns `tournaments[]` with tournament info and `draws[]` containing individual matches. Each draw represents a category (Men's Singles, Women's Doubles, etc.). Each match has `competitors[]` with player name, country, seed, set scores, and serving status.

### get_calendar
Get full season tournament calendar.
- `tour` (str, required): "atp" or "wta"
- `year` (int, optional): Season year. Defaults to current.

Returns `tournaments[]` with tournament-level info only (name, dates, venue, major flag). Does not include individual matches. Useful for answering "when is the Australian Open?" or "what tournaments are coming up?"

### get_rankings
Get current ATP or WTA rankings.
- `tour` (str, required): "atp" or "wta"
- `limit` (int, optional): Max ranked players to return. Defaults to 50.

Returns `rankings[]` with rank, previous_rank, name, points, and trend for each player. Rankings update weekly.

### get_player_info
Get individual player profile.
- `player_id` (str, required): ESPN athlete ID

Returns player details: name, country, birthplace, age, height, weight, playing hand (left/right), debut year, and ESPN profile link.

**Finding player IDs:** Player IDs appear in rankings results and match competitor data. You can also find them in ESPN tennis URLs (e.g., espn.com/tennis/player/_/id/3782/carlos-alcaraz → ID is 3782).

### get_news
Get tennis news articles.
- `tour` (str, required): "atp" or "wta"

Returns `articles[]` with headline, description, published date, and link.

## Common Player IDs

| Player | ID | Player | ID |
|--------|-----|--------|-----|
| Carlos Alcaraz | 3782 | Aryna Sabalenka | 3038 |
| Jannik Sinner | 3623 | Iga Swiatek | 3730 |
| Novak Djokovic | 296 | Coco Gauff | 3626 |
| Daniil Medvedev | 2383 | Elena Rybakina | 3126 |
| Taylor Fritz | 2946 | Jessica Pegula | 2113 |
| Casper Ruud | 2989 | Jasmine Paolini | 2615 |
| Stefanos Tsitsipas | 2869 | Paula Badosa | 2731 |
| Emma Navarro | 3785 | Anna Kalinskaya | 2977 |

**Tip:** Use `get_rankings` to find current player IDs and rankings.

## Reading Match Scores

Tennis scores are reported as set scores. Example response:
```json
{
  "competitors": [
    {"name": "Carlos Alcaraz", "seed": 1, "set_scores": [6, 3, 7], "winner": true},
    {"name": "Novak Djokovic", "seed": 2, "set_scores": [4, 6, 5], "winner": false}
  ],
  "result": "(1) Carlos Alcaraz (ESP) bt (2) Novak Djokovic (SRB) 6-4 3-6 7-5"
}
```
This means Alcaraz won 6-4, 3-6, 7-5 (won first set, lost second, won third).

## Understanding Tournament Draws

The `draws` array in scoreboard results contains match groupings:
- **Men's Singles** / **Women's Singles**: Individual matches
- **Men's Doubles** / **Women's Doubles**: Pairs matches

Each match has a `round` field: "Qualifying 1st Round", "Round 1", "Round of 16", "Quarterfinal", "Semifinal", "Final".

## Examples

**User: "What ATP matches are happening right now?"**
```bash
sports-skills tennis get_scoreboard --tour=atp
```

**User: "Show me the WTA rankings"**
```bash
sports-skills tennis get_rankings --tour=wta --limit=20
```

**User: "When is the French Open this year?"**
```bash
sports-skills tennis get_calendar --tour=atp --year=2026
```
Then search results for "Roland Garros" (the French Open's official name).

**User: "Tell me about Carlos Alcaraz"**
```bash
sports-skills tennis get_player_info --player_id=3782
```

**User: "What's the latest tennis news?"**
```bash
sports-skills tennis get_news --tour=atp
sports-skills tennis get_news --tour=wta
```

## Error Handling

When a command fails, **do not surface raw errors to the user**. Instead:
1. Catch silently and try alternatives
2. If rankings are empty, try a previous week (the command handles this automatically)
3. Only report failure with a clean message after exhausting alternatives

## Grand Slam Tournaments

| Tournament | Months | Surface | Location |
|-----------|--------|---------|----------|
| Australian Open | January | Hard | Melbourne, Australia |
| Roland Garros (French Open) | May-June | Clay | Paris, France |
| Wimbledon | June-July | Grass | London, England |
| US Open | August-September | Hard | New York, USA |

Grand Slams are marked with `"major": true` in the calendar.

## Troubleshooting

- **`sports-skills` command not found**: Run `pip install sports-skills`
- **No matches found**: Tennis tournaments run specific weeks; between events, `get_scoreboard` may return 0 matches. Use `get_calendar` to see upcoming events.
- **Rankings empty**: Rankings update weekly on Mondays. If the current week's rankings aren't available yet, the command automatically tries previous weeks.
- **Player not found**: Use `get_rankings` to find player IDs, or look up ESPN tennis URLs.
