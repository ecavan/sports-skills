# sports-skills.sh

Open-source agent skills for live sports data and prediction markets. Built for the [Agent Skills](https://agentskills.io/specification) spec. Works with Claude Code, Cursor, Copilot, Gemini CLI, and every major AI agent.

**Zero API keys. Zero signup. Just works.**

```bash
npx skills add machina-sports/sports-skills
```

---

## What This Is

A collection of agent skills that wrap **publicly available** sports data sources and APIs. These skills don't provide proprietary data — they give AI agents a structured interface to data that's already freely accessible on the web:

- **Football**: ESPN, Understat, FPL, Transfermarkt — 21 commands across 12 leagues
- **Formula 1**: FastF1 open-source library — sessions, lap data, race results
- **Prediction Markets**: Kalshi and Polymarket public APIs — markets, prices, order books
- **Sports News**: RSS feeds and Google News — any public feed

Each skill is a SKILL.md file that any compatible AI agent can load and use immediately. Data comes from third-party public sources and is subject to their respective terms of use.

> **Personal use only.** These open-source skills rely on third-party public APIs and are intended for personal, non-commercial use. For commercial or production workloads with licensed data, SLAs, and enterprise support, see [machina.gg](https://machina.gg).

---

## Available Skills

### Sports Data

| Skill | Sport | Commands | Data Sources |
|-------|-------|----------|-------------|
| `football-data` | Football | 21 | ESPN, FPL, Understat, Transfermarkt |
| `fastf1` | Formula 1 | 6 | FastF1 (free library) |
| `sports-news` | Multi-sport | 2 | Any RSS feed, Google News |

### Prediction Markets

| Skill | Platform | Commands | Coverage |
|-------|----------|----------|----------|
| `kalshi` | Kalshi | 12+ | Soccer, Basketball, Baseball, Tennis, NFL, Hockey |
| `polymarket` | Polymarket | 10 | NFL, NBA, MLB, Soccer, Tennis, Cricket, MMA, Esports |

### Football Data Coverage

| Competition | League | Live Scores | Standings | Player Stats | xG | Transfers |
|------------|--------|-------------|-----------|-------------|-----|-----------|
| Premier League | England | Yes | Yes | Yes | Yes | Yes |
| La Liga | Spain | Yes | Yes | Yes | Yes | Yes |
| Bundesliga | Germany | Yes | Yes | Yes | Yes | Yes |
| Serie A | Italy | Yes | Yes | Yes | Yes | Yes |
| Ligue 1 | France | Yes | Yes | Yes | Yes | Yes |
| Champions League | Europe | Yes | Yes | Yes | - | - |
| FIFA World Cup | International | Yes | Yes | Yes | - | - |
| Championship | England | Yes | Yes | Yes | - | Yes |
| Eredivisie | Netherlands | Yes | Yes | Yes | - | Yes |
| Primeira Liga | Portugal | Yes | Yes | Yes | - | Yes |
| Serie A Brazil | Brazil | Yes | Yes | Yes | - | Yes |
| European Championship | Europe | Yes | Yes | Yes | - | - |

---

## Quick Start

### Install a skill

```bash
npx skills add machina-sports/sports-skills
```

### Use with your AI agent

Once installed, your agent can call commands directly:

**Get today's matches:**
> "Show me all Premier League matches today"

**Check prediction market odds:**
> "What are the Polymarket odds for the Champions League final?"

**Get F1 race results:**
> "Show me the lap data from the last Monaco Grand Prix"

---

## Skills Reference

### football-data

Community football data skill. Aggregates publicly accessible web sources (ESPN, Understat, FPL, Transfermarkt). Data is sourced from these third-party sites and is subject to their respective terms of use.

**Commands:**

| Command | Description |
|---------|-------------|
| `get_competitions` | List all 12 supported competitions |
| `get_current_season` | Detect current season for a competition |
| `get_season_schedule` | All fixtures for a season |
| `get_daily_schedule` | All matches across competitions for a date |
| `get_season_standings` | League table (home/away/total) |
| `get_season_leaders` | Top scorers, assist leaders, card leaders |
| `get_season_teams` | All teams in a season |
| `search_team` | Fuzzy search for a team by name across all leagues |
| `get_team_profile` | Team info, crest, venue |
| `get_team_schedule` | Upcoming and recent matches for a team |
| `get_head_to_head` | H2H history between two teams (unavailable) |
| `get_event_summary` | Match summary with scores |
| `get_event_lineups` | Starting lineups and formations |
| `get_event_statistics` | Team-level match stats (possession, shots, passes) |
| `get_event_timeline` | Goals, cards, substitutions, VAR decisions |
| `get_event_xg` | Expected goals with shot maps |
| `get_event_players_statistics` | Individual player match stats |
| `get_missing_players` | Injured and suspended players |
| `get_player_profile` | Biography, career stats, market value |
| `get_season_transfers` | Transfer history |
| `get_competition_seasons` | Available seasons for a competition |

### fastf1

Formula 1 data via the [FastF1](https://github.com/theOehrly/Fast-F1) open-source library.

| Command | Description |
|---------|-------------|
| `get_session_data` | Session metadata (practice, qualifying, race) |
| `get_driver_info` | Driver details or full grid |
| `get_team_info` | Team details or all teams |
| `get_race_schedule` | Full calendar for a year |
| `get_lap_data` | Lap times, sectors, tire data |
| `get_race_results` | Final classification and fastest laps |

### kalshi

Kalshi's [official public API](https://trading-api.readme.io/reference/getmarkets). No API key needed for read-only market data.

| Command | Description |
|---------|-------------|
| `get_series_list` | All series filtered by sport tag |
| `get_series` | Single series details |
| `get_markets` | Markets with bid/ask/volume/open interest |
| `get_market` | Single market details |
| `get_events` | Events with pagination |
| `get_event` | Single event details |
| `get_trades` | Trade history |
| `get_market_candlesticks` | OHLCV price data (1min/1hr/1day) |
| `get_sports_filters` | Sports-specific filters and competitions |
| `get_exchange_status` | Exchange active/trading status |
| `get_exchange_schedule` | Exchange operating schedule |

### polymarket

Polymarket's official public APIs ([Gamma](https://gamma-api.polymarket.com) + [CLOB](https://docs.polymarket.com)). No API key needed for read-only data.

| Command | Description |
|---------|-------------|
| `get_sports_markets` | Active sports markets with type filtering |
| `get_sports_events` | Sports events by series/league |
| `get_series` | All series (NBA, NFL, MLB leagues) |
| `get_market_details` | Single market by ID or slug |
| `get_event_details` | Single event with nested markets |
| `get_market_prices` | Real-time midpoint, bid, ask from CLOB |
| `get_order_book` | Full order book with spread calculation |
| `get_sports_market_types` | 58+ market types (moneyline, spreads, totals, props) |
| `search_markets` | Full-text search across markets |
| `get_price_history` | Historical price data (1d, 1w, 1m, max) |
| `get_last_trade_price` | Most recent trade price |

### sports-news

RSS feed aggregation for sports news.

| Command | Description |
|---------|-------------|
| `fetch_feed` | Full feed with metadata and entries |
| `fetch_items` | Filtered items (date range, language, country) |

Supports any RSS/Atom feed URL and Google News queries.

---

## Architecture

```
sports-skills.sh
├── skills/                            # SKILL.md files (agent instructions)
│   ├── football-data/SKILL.md         # 21 commands, 12 leagues
│   ├── fastf1/SKILL.md               # F1 sessions, laps, results
│   ├── kalshi/SKILL.md               # Prediction markets (CFTC)
│   ├── polymarket/SKILL.md           # Prediction markets (crypto)
│   └── sports-news/SKILL.md          # RSS + Google News
├── src/sports_skills/                 # Python runtime (used by skills)
├── site/                              # Landing page (sports-skills.sh)
├── LICENSE
└── README.md
```

Each skill follows the [Agent Skills specification](https://agentskills.io/specification):

```yaml
---
name: football-data
description: |
  Football (soccer) data across 12 leagues — standings, schedules, match stats, xG, transfers, player profiles.
  Use when: user asks about football/soccer standings, fixtures, match stats, xG, lineups, transfers, or injury news.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# Football Data

Instructions for the AI agent...
```

---

## Compatibility

Works with every agent that supports the SKILL.md format:

- Claude Code
- OpenClaw (clawdbot / moltbot)
- Cursor
- GitHub Copilot
- VS Code Copilot
- Gemini CLI
- Windsurf
- OpenCode
- Kiro
- Roo
- Trae

---

## Coming Soon

Licensed data skills — coming soon via [Machina Sports](https://machina.gg):

| Provider | Coverage | Status |
|----------|----------|--------|
| Sportradar | 1,200+ competitions, real-time feeds | Coming Soon |
| Stats Perform (Opta) | Advanced analytics, event-level data | Coming Soon |
| API-Football | 900+ leagues, live scores, odds | Coming Soon |
| Data Sports Group | US sports, player props, projections | Coming Soon |

These will ship as additional skills that drop in alongside the open-source ones. Same interface, same JSON envelope — just licensed data underneath. Built for commercial and production use with proper data licensing, SLAs, and enterprise support.

For early access or enterprise needs, see [machina.gg](https://machina.gg).

---

## Contributing

We're actively expanding to cover more sports and data sources — and always looking for contributions. Whether it's a new sport, a new league, a better data source, or improvements to existing skills, PRs are welcome.

1. Fork the repo
2. Create a skill in `skills/<your-skill>/SKILL.md`
3. Follow the SKILL.md spec (YAML frontmatter + Markdown instructions)
4. Open a PR

See the existing SKILL.md files and the [Agent Skills spec](https://agentskills.io/specification) for format details.

---

## World Cup 2026

This project ships with World Cup 2026 coverage built in. The `football-data` skill includes FIFA World Cup as a supported competition. As the tournament approaches (June 2026), we'll add dedicated World Cup skills for bracket tracking, group stage analysis, and match predictions.

---

## Data Sources & Disclaimer

This project does not own, license, or redistribute any sports data. Each skill is a thin wrapper that accesses publicly available third-party sources on behalf of the user.

| Source | Access Method | Official API |
|--------|--------------|--------------|
| ESPN | Public web endpoints | No — undocumented, may change without notice |
| Understat | Public web data | No — community access, subject to their ToS |
| FPL | Public API | Semi-official — widely used by the community |
| Transfermarkt | Public web data | No — subject to their ToS |
| FastF1 | Open-source library | Yes — [FastF1](https://github.com/theOehrly/Fast-F1) (MIT) |
| Kalshi | Official public API | Yes — [Trade API v2](https://trading-api.readme.io) |
| Polymarket | Official public APIs | Yes — [Gamma](https://gamma-api.polymarket.com) + [CLOB](https://docs.polymarket.com) |
| RSS / Google News | Standard RSS protocol | Yes — RSS is designed for syndication |

**Important:**
- This project is intended for **personal, educational, and research use**.
- You are responsible for complying with each data source's terms of service.
- Data from unofficial sources (ESPN, Understat, Transfermarkt) may break without notice if those sites change their structure.
- For commercial or production use with properly licensed data, see [machina.gg](https://machina.gg).
- This project is not affiliated with or endorsed by any of the data sources listed above.

---

## Acknowledgments

This project is built on top of great open-source work and public APIs:

- **[ESPN](https://www.espn.com)** — for keeping their web endpoints accessible. The backbone of football scores, standings, schedules, lineups, match stats, and timelines across all 12 leagues.
- **[Fantasy Premier League](https://fantasy.premierleague.com)** — for their community API powering injury news, player stats, ownership data, and ICT index for Premier League players.
- **[Transfermarkt](https://www.transfermarkt.com)** — for player market values, transfer history, and the richest player data in football.
- **[Understat](https://understat.com)** — for xG data across the top 5 European leagues.
- **[FastF1](https://github.com/theOehrly/Fast-F1)** — the backbone of our Formula 1 skill. Thanks to theOehrly and contributors.
- **[feedparser](https://github.com/kurtmckee/feedparser)** — reliable RSS/Atom parsing for the news skill.
- **[Kalshi](https://kalshi.com)** and **[Polymarket](https://polymarket.com)** — for their public market data APIs.
- **[skills.sh](https://skills.sh)** — the open agent skills directory and CLI.
- **[Agent Skills](https://agentskills.io)** — the open spec that makes skills interoperable across agents.

---

## License

MIT — applies to the skill code and wrappers in this repository. Does not grant any rights to the underlying third-party data.

---

Built by [Machina Sports](https://machina.gg). The Operating System for sports AI.
