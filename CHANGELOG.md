# Changelog

All notable changes to this project will be documented in this file.

## [0.6.0] - 2026-02-20

### ⚠️ Breaking Changes

- **`odds` field schema change** — The `odds` field in all ESPN scoreboard responses (NFL, NBA, WNBA, NHL, MLB, CBB, CFB) has changed from a **list of dicts** to a **single dict or `None`**.

  **Before (`0.5.x`):**
  ```python
  game["odds"]  # → [{"provider": "DraftKings", "details": "NE -6.5", "over_under": 220.5}]
  ```

  **After (`0.6.0`):**
  ```python
  game["odds"]  # → {"provider": "DraftKings", "details": "NE -6.5", "moneyline": {...}, "spread_line": {...}, "total": {...}, "open": {...}} or None
  ```

  **Migration:** Replace `game["odds"][0]["over_under"]` with `game["odds"]["over_under"]` (guard with `if game["odds"]`). ESPN only ever returns one provider (DraftKings), so the list wrapper was unnecessary abstraction.

### Added
- **Enriched ESPN odds parsing** across all 7 ESPN sport connectors (NFL, NBA, WNBA, NHL, MLB, CBB, CFB) via shared `normalize_odds()` in `_espn_base`
- Full DraftKings data now extracted: moneyline (home/away), spread with juice, total with juice, opening lines for line movement tracking, and favorite/underdog designation
- Three-way moneyline support for soccer (home/draw/away)
- `normalize_odds()` returns `None` when no odds are available (games in progress, final, or pre-odds)
- **CI infrastructure** — GitHub Actions workflow running lint and tests on PRs and pushes to main
- **ruff** linting (Python 3.10 target, line-length 120)
- **pytest** suite — 56 tests covering module imports, CLI registry, response envelope, cache, retry logic, and `normalize_odds` edge cases
- `py.typed` marker for PEP 561 compliance

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
