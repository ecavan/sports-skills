# Testing the Sports Agent Locally

## Prerequisites

```bash
# Clone and checkout the branch
git checkout cloud-code-for-sports

# Create a virtual environment (if not already done)
python3 -m venv .venv
source .venv/bin/activate

# Install with agent dependencies
pip install -e ".[agent]"
```

## Run the Unit Tests

```bash
# Agent tool loading tests (42 tests)
pytest tests/test_agent_tools.py -v

# Full test suite
pytest tests/ -v
```

## Run the Agent

```bash
sports-agent
```

Or via module:

```bash
python -m sports_skills.agent
```

### First Launch (Setup Wizard)

On first run you'll see the setup wizard:

1. **Enter at least one API key** — Anthropic, OpenAI, or Google
2. **Select a model** — only models matching your provided keys will appear

Config is saved to `~/.config/sports-agent/config.json`.

### Mode Picker

After setup, you'll see the mode picker every launch:

1. **Pick a sport** — NFL, NBA, WNBA, NHL, MLB, College Football, College Basketball, Football (Soccer), Golf, Tennis, F1
2. **Pick a purpose** — General (scores, standings, stats) or Betting (adds odds focus)
3. **If Betting** — optionally add a prediction exchange (Polymarket or Kalshi)

### Chat

Once in chat:

- Type a question and press Enter
- Watch streaming responses with tool call indicators
- **Ctrl+S** — switch sport (reopens mode picker)
- **Ctrl+B** — toggle betting mode on/off
- **Ctrl+Q** — quit
- **/help** — show available commands
- **/clear** — clear chat history
- **/config** — show current configuration

## Testing with Specific Providers

### Anthropic

```
API Key: sk-ant-api03-...
Models: Claude Sonnet 4, Claude Opus 4
```

### OpenAI

```
API Key: sk-...
Models: GPT-4o, GPT-4o Mini
```

### Google

```
API Key: AIza...
Models: Gemini 2.0 Flash, Gemini 2.5 Pro
```

### OpenRouter

```
API Key: sk-or-v1-...
Models: Claude Sonnet 4, Claude Haiku, GPT-4o, Gemini 2.0 Flash (all via OpenRouter)
```

OpenRouter is natively supported. Enter your OpenRouter key during setup and
select any of the available models. OpenRouter routes through its own API
(`https://openrouter.ai/api/v1`) so you can access models from multiple
providers with a single key.

## Test Scenarios

### 1. Basic Score Check

```
Sport: NBA, Mode: General
Ask: "What are today's NBA scores?"
Expected: Calls nba_get_scoreboard, returns formatted scores
```

### 2. Team Lookup + Roster

```
Sport: NFL, Mode: General
Ask: "Show me the Eagles roster"
Expected: Calls nfl_get_teams (to find team ID), then nfl_get_team_roster
```

### 3. Betting Mode

```
Sport: NBA, Mode: Betting
Ask: "What are the best bets for tonight's games?"
Expected: Calls nba_get_scoreboard (for odds), nba_get_injuries, provides analysis
```

### 4. Betting + Polymarket

```
Sport: NFL, Mode: Betting, Exchange: Polymarket
Ask: "Are there any Super Bowl futures on Polymarket?"
Expected: Calls polymarket_search_markets or polymarket_get_sports_markets
```

### 5. Sport Switch

```
Start with NBA, ask a question, then Ctrl+S to switch to NHL
Expected: Mode picker reopens, agent rebuilds with NHL tools only
```

### 6. Soccer/Football

```
Sport: Football (Soccer), Mode: General
Ask: "Show me the Premier League standings"
Expected: Calls football_get_competitions, then football_get_season_standings
```

### 7. F1 (requires fastf1)

```
Sport: Formula 1, Mode: General
Ask: "Show me the 2025 championship standings"
Expected: Calls f1_get_championship_standings. If fastf1 is not installed,
returns a helpful error message instead of crashing.
```

## Resetting Config

To start fresh (re-run setup wizard):

```bash
rm ~/.config/sports-agent/config.json
sports-agent
```

## Lint

```bash
ruff check src/sports_skills/agent/
```
