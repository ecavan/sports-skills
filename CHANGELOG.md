# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-02-16

### Added
- HTTP retry with exponential backoff across all data sources (ESPN, Understat, FPL, Transfermarkt, football-data.org)
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
