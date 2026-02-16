# sports-skills.sh

Open-source agent skills for live sports data and prediction markets. Built for the [SKILL.md](https://github.com/anthropics/skill) spec. Works with Claude Code, Cursor, Copilot, Gemini CLI, and every major AI agent.

**Zero API keys. Zero signup. Just works.**

```bash
npx skills add sports-skills/football-data
```

---

## What This Is

A collection of free, production-grade data connectors that give AI agents access to:

- **Football**: 20 commands across 12 leagues (Premier League, La Liga, Champions League, World Cup, and more)
- **Formula 1**: Sessions, lap data, race results, driver and team info
- **Prediction Markets**: Kalshi and Polymarket sports markets, prices, order books
- **Sports News**: RSS feeds and Google News integration

Each connector is a SKILL.md file that any compatible AI agent can load and use immediately.

---

## Available Skills

### Sports Data

| Skill | Sport | Commands | Data Sources |
|-------|-------|----------|-------------|
| `football-data` | Football | 20 | ESPN, FPL, Understat, Transfermarkt |
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
npx skills add sports-skills/football-data
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

## Python SDK

Also available as a pip-installable Python package for programmatic use.

```bash
pip install sports-skills           # Football, Polymarket, Kalshi, News
pip install sports-skills[f1]       # + Formula 1 (fastf1 + pandas)
```

```python
from sports_skills import football, polymarket, kalshi, news

standings = football.get_season_standings(season_id="premier-league-2025")
matches = football.get_daily_schedule()
xg = football.get_event_xg(event_id="401234567")
player = football.get_player_profile(tm_player_id="433177")

markets = polymarket.get_sports_markets(limit=20)
articles = news.fetch_items(google_news=True, query="Arsenal transfer news", limit=10)
```

CLI included:

```bash
sports-skills football get_season_standings --season_id=premier-league-2025
sports-skills polymarket get_sports_markets --limit=20
sports-skills kalshi get_markets --series_ticker=KXNBA
sports-skills news fetch_items --google_news --query="Arsenal" --limit=5
sports-skills f1 get_race_schedule --year=2025
```

All commands output JSON with a consistent envelope: `{"status": true, "data": {...}, "message": ""}`.

---

## Skills Reference

### football-data

The most comprehensive open-source football data connector. Aggregates 4 sources (ESPN, Understat, FPL, Transfermarkt) with zero API keys required.

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
| `get_team_profile` | Squad roster, manager, venue |
| `get_team_schedule` | Upcoming and recent matches for a team |
| `get_head_to_head` | H2H history between two teams |
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

Full Formula 1 data via the FastF1 library.

| Command | Description |
|---------|-------------|
| `get_session_data` | Session metadata (practice, qualifying, race) |
| `get_driver_info` | Driver details or full grid |
| `get_team_info` | Team details or all teams |
| `get_race_schedule` | Full calendar for a year |
| `get_lap_data` | Lap times, sectors, tire data |
| `get_race_results` | Final classification and fastest laps |

### kalshi

Public endpoints from Kalshi prediction markets. No API key needed for market data.

| Command | Description |
|---------|-------------|
| `GetSeriesList` | All series filtered by sport tag |
| `GetSeries` | Single series details |
| `GetMarkets` | Markets with bid/ask/volume/open interest |
| `GetMarket` | Single market details |
| `GetEvents` | Events with pagination |
| `GetTrades` | Trade history |
| `GetMarketCandlesticks` | OHLCV price data (1min/1hr/1day) |
| `GetFiltersForSports` | Sports-specific filters and competitions |
| `GetExchangeStatus` | Exchange active/trading status |

### polymarket

Public endpoints from Polymarket (Gamma + CLOB APIs). No API key needed.

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
| `get_trades` | Recent trade history |

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
│   ├── football-data/SKILL.md         # 20 commands, 12 leagues
│   ├── fastf1/SKILL.md               # F1 sessions, laps, results
│   ├── kalshi/SKILL.md               # Prediction markets (CFTC)
│   ├── polymarket/SKILL.md           # Prediction markets (crypto)
│   └── sports-news/SKILL.md          # RSS + Google News
├── src/sports_skills/                 # Python SDK
│   ├── football/                      # ESPN, Understat, FPL, Transfermarkt
│   ├── f1/                            # FastF1 library
│   ├── polymarket/                    # Gamma + CLOB APIs
│   ├── kalshi/                        # Kalshi Trade API v2
│   ├── news/                          # RSS/Atom + Google News
│   └── cli.py                         # CLI entry point
├── pyproject.toml
├── site/                              # Landing page (sports-skills.sh)
├── LICENSE
└── README.md
```

Each skill follows the [SKILL.md specification](https://github.com/anthropics/skill):

```yaml
---
name: football-data
description: Live football data across 12 leagues. Scores, standings, stats, xG, transfers.
triggers:
  - football
  - soccer
  - premier league
  - match
  - standings
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

## Licensed Data (via Machina API)

Need Sportradar, Opta, or enterprise-grade data with SLAs?

The open-source skills cover free public data. For production workloads with licensed data providers, real-time feeds, and managed infrastructure, see [machina.gg](https://machina.gg).

| What You Get | Open Source (Free) | Machina API (Licensed) |
|-------------|-------------------|----------------------|
| Football data | ESPN, Understat, FPL, Transfermarkt | Sportradar, Opta/Stats Perform |
| Coverage | 12 leagues | 1,200+ competitions |
| Real-time latency | Best-effort | < 2s SLA |
| Prediction markets | Kalshi + Polymarket (public) | Full depth + analytics |
| Infrastructure | Self-managed | Managed, persistent, compliant |
| Support | Community | Enterprise SLAs |

---

## Contributing

We welcome contributions. Add a new sport, a new data source, or improve an existing skill.

1. Fork the repo
2. Create a skill in `skills/<your-skill>/SKILL.md`
3. Follow the SKILL.md spec (YAML frontmatter + Markdown instructions)
4. Open a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## World Cup 2026

This project ships with World Cup 2026 coverage built in. The `football-data` skill includes FIFA World Cup as a supported competition. As the tournament approaches (June 2026), we'll add dedicated World Cup skills for bracket tracking, group stage analysis, and match predictions.

---

## License

MIT

---

Built by [Machina Sports](https://machina.gg). The Operating System for sports AI.
