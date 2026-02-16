---
name: fastf1
description: |
  Formula 1 data — race schedules, results, lap timing, driver and team info. Powered by the FastF1 library. Covers F1 sessions, qualifying, practice, race results, sector times, tire strategy.

  Use when: user asks about F1 race results, qualifying, lap times, driver stats, team info, the F1 calendar, or Formula 1 data.
  Don't use when: user asks about other motorsports (MotoGP, NASCAR, IndyCar, WEC, Formula E). Don't use for F1 betting odds or predictions — use kalshi or polymarket instead. Don't use for F1 news articles — use sports-news instead.
license: MIT
compatibility: Requires Python 3.10+ with fastf1 and pandas (pip install sports-skills[f1])
metadata:
  author: machina-sports
  version: "0.1.0"
---

# FastF1 — Formula 1 Data

## Setup

F1 requires extra dependencies (fastf1 + pandas). Install with:
```bash
which sports-skills || pip install sports-skills[f1]
```
If already installed without F1 support, add the extra:
```bash
pip install sports-skills[f1]
```
If `pip install` fails with a Python version error, the package requires Python 3.10+. Find a compatible Python:
```bash
python3 --version  # check version
# If < 3.10, try: python3.12 -m pip install sports-skills[f1]
# On macOS with Homebrew: /opt/homebrew/bin/python3.12 -m pip install sports-skills[f1]
```
No API keys required.

## Quick Start

Prefer the CLI — it avoids Python import path issues:
```bash
sports-skills f1 get_race_schedule --year=2025
sports-skills f1 get_race_results --year=2025 --event=Monza
```

Python SDK (alternative):
```python
from sports_skills import f1

schedule = f1.get_race_schedule(year=2025)
results = f1.get_race_results(year=2025, event="Monza")
```

## Commands

### get_race_schedule
Get race schedule for a season.
- `year` (int, required): Season year

### get_race_results
Get race results (positions, times, points).
- `year` (int, required): Season year
- `event` (str, required): Event name (e.g., "Monza", "Silverstone")

### get_session_data
Get detailed session data (qualifying, race, practice).
- `session_year` (int, required): Year
- `session_name` (str, required): Event name
- `session_type` (str, optional): "Q" (qualifying), "R" (race), "FP1", etc. Default: "Q"

### get_driver_info
Get driver information for a season.
- `year` (int, required): Season year
- `driver` (str, optional): Driver code or name. Omit for all drivers.

### get_team_info
Get team information for a season.
- `year` (int, required): Season year
- `team` (str, optional): Team name. Omit for all teams.

### get_lap_data
Get lap-by-lap timing data.
- `year` (int, required): Season year
- `event` (str, required): Event name
- `session_type` (str, optional): Session type. Default: "R"
- `driver` (str, optional): Driver code. Omit for all drivers.

## Examples

User: "Show me the 2025 F1 calendar"
1. Call `get_race_schedule(year=2025)`
2. Present schedule with event names, dates, and circuits

User: "How did Verstappen do at Monza?"
1. Call `get_race_results(year=2025, event="Monza")` for final classification
2. Call `get_lap_data(year=2025, event="Monza", session_type="R", driver="VER")` for lap times
3. Present finishing position, gap to leader, fastest lap, and tire strategy

User: "Compare qualifying times at Silverstone"
1. Call `get_session_data(session_year=2025, session_name="Silverstone", session_type="Q")`
2. Call `get_lap_data(year=2025, event="Silverstone", session_type="Q")` for all drivers
3. Present Q1/Q2/Q3 times sorted by position

## Troubleshooting

- **`sports-skills` command not found**: Package not installed. Run `pip install sports-skills[f1]`. If pip fails with a Python version error, you need Python 3.10+ — see Setup section.
- **`ModuleNotFoundError: No module named 'sports_skills'`**: Same as above — install the package. Prefer the CLI over Python imports to avoid path issues.
- **ImportError on `from sports_skills import f1`**: F1 module requires extra dependencies beyond the base package. Run `pip install sports-skills[f1]` to add fastf1 + pandas.
- **No data for future events**: FastF1 only returns data for completed sessions. Future races appear in the schedule but have no session data.
- **Slow first request**: FastF1 downloads and caches session data locally. First call for a given session may take 10-30 seconds. Subsequent calls are fast.
- **Event name not found**: Use the exact event name from `get_race_schedule()`. Common circuit names like "Monza" or "Silverstone" usually work as aliases.
