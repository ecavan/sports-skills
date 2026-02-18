# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - 2026-02-18

### Added
- **NBA data** — 8 commands via ESPN: scoreboard, standings, teams, roster, schedule, game summary, leaders, news
- **WNBA data** — 8 commands via ESPN: scoreboard, standings, teams, roster, schedule, game summary, leaders, news
- **NFL data** — 9 commands via ESPN: scoreboard, standings, teams, roster, schedule, team schedule, game summary, leaders, news
- Season-aware statistical leaders for NBA and WNBA — auto-derives current season from system date, avoids offseason 404s
- Postseason support for NFL schedule and scoreboard (Wild Card through Super Bowl as weeks 19-23)

### Fixed
- NFL `get_teams` connector now accepts optional `request_data` arg — previously caused a positional arg error via CLI
- NBA `get_schedule` season/date param collision — `date` now takes priority over `season` (were writing to same ESPN param key)
- WNBA `get_leaders` offseason 404 — switched to season-scoped ESPN core API endpoint with regular season type

## [0.2.0] - 2026-02-16

### Added
- HTTP retry with exponential backoff across all data sources (ESPN, Understat, FPL, Transfermarkt)
- Smart retry classification: transient errors (5xx, 429, timeouts) retry up to 3 attempts; client errors (4xx) fail immediately
- Extra backoff for 429 rate-limit responses
- Structured logging via `logging` module for request failures
- Upcoming fixtures in `get_team_schedule` — ESPN's `fixture=true` param now fetched and merged with past results

### Fixed
- CLI errors now output JSON on stdout (for agents) alongside stderr text (for humans) — agents no longer see silent failures
- Standardized error dicts across all HTTP helpers (`{"error": True, "status_code": N, "message": "..."}`)
- League-probing requests (team schedule, team profile, event resolution) skip retries to avoid wasting 60+ requests on ESPN 500s for wrong team/league combos

## [0.1.0] - 2026-02-01

Initial release.

- Football data: 20 commands across 12 leagues (ESPN, FPL, Understat, Transfermarkt)
- Formula 1: 6 commands via FastF1
- Prediction markets: Kalshi (12 commands) and Polymarket (11 commands)
- Sports news: RSS/Atom feeds and Google News
- CLI (`sports-skills`) and Python SDK
