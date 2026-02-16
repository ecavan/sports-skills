---
name: fastf1
description: |
  Formula 1 data — race schedules, results, lap timing, driver and team info. Powered by the FastF1 library.

  Use when: user asks about F1 race results, qualifying, lap times, driver stats, team info, or the F1 calendar.
  Don't use when: user asks about other motorsports (MotoGP, NASCAR, IndyCar, WEC, Formula E). Don't use for F1 betting odds or predictions — use kalshi or polymarket instead. Don't use for F1 news articles — use sports-news instead. Requires the [f1] extra: pip install sports-skills[f1].
triggers:
  - f1 schedule
  - f1 results
  - f1 lap data
  - formula 1
  - f1 driver
  - f1 team
---

# FastF1 — Formula 1 Data

## Quick Start

```bash
npx skills add sports-skills
pip install sports-skills[f1]  # F1 requires extra dependencies
```

```python
from sports_skills import f1

schedule = f1.get_race_schedule(year=2025)
results = f1.get_race_results(year=2025, event="Monza")
```

Or via CLI:
```bash
sports-skills f1 get_race_schedule --year=2025
sports-skills f1 get_race_results --year=2025 --event=Monza
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

## Dependencies

Requires `fastf1>=3.0` and `pandas>=2.0`. Install with:
```bash
pip install sports-skills[f1]
```
