---
name: fastf1
description: Formula 1 race data including session info, driver and team details, race schedules, lap times with sector splits and tire data, and race results. Use when the user asks about F1 races, qualifying, practice sessions, lap times, driver standings, team info, or any Formula 1 data. Powered by the FastF1 library. No API key required.
---

# FastF1

Formula 1 data connector via the FastF1 Python library. Access session data, driver info, team info, race schedules, detailed lap data, and race results. No API key required.

## Commands

### get_session_data

Get metadata for a specific F1 session (practice, qualifying, sprint, race).

```
Params:
  session_year (int, optional, default: 2019) - Season year
  session_name (string, optional, default: "Monza") - Event name or round number
  session_type (string, optional, default: "Q") - Session type code
Returns: { session, event_name, event_date, session_type, track_name }
```

**Session type codes:** `FP1`, `FP2`, `FP3` (practice), `Q` (qualifying), `S` (sprint), `R` (race)

### get_driver_info

Get driver details for a season. Call without a driver parameter to get the full grid.

```
Params:
  year (int, optional, default: 2023) - Season year
  driver (string, optional) - Driver code (e.g. "VER", "HAM") or omit for all drivers
Returns (all): [{ driver_number, driver_id, driver_code, first_name, last_name, full_name, team_name }]
Returns (single): { driver_number, driver_id, driver_code, first_name, last_name, full_name, team_name }
```

### get_team_info

Get team/constructor details for a season.

```
Params:
  year (int, optional, default: 2023) - Season year
  team (string, optional) - Team name or omit for all teams
Returns (all): [{ team_id, team_name, nationality }]
Returns (single): { team_id, team_name, nationality }
```

### get_race_schedule

Get the full race calendar for a season.

```
Params:
  year (int, optional, default: 2023) - Season year
Returns: [{ round_number, country, location, event_name, circuit_name, event_date, event_format }]
```

**Event formats:** `conventional` (standard weekend), `sprint_qualifying`, `sprint_shootout`, `sprint_race`

### get_lap_data

Get detailed lap-by-lap data for a session. Includes sector times, tire compound, and tire life.

```
Params:
  year (int, optional, default: 2023) - Season year
  event (string, optional, default: "Monza") - Event name or round number
  session_type (string, optional, default: "R") - Session type code
  driver (string, optional) - Driver code to filter (omit for all drivers)
Returns: [{
  driver, team, lap_number, lap_time,
  sector_1_time, sector_2_time, sector_3_time,
  compound, tyre_life, is_personal_best, position
}]
```

### get_race_results

Get the final classification for a race event.

```
Params:
  year (int, required) - Season year
  event (string, optional, default: "Monza") - Event name or round number
Returns: [{
  position, driver_number, driver, team,
  grid_position, status, points, time,
  fastest_lap, fastest_lap_time
}]
```

## Response Format

All commands return:

```json
{
  "status": true,
  "data": { ... },
  "message": "Description of result"
}
```

On error: `{ "status": false, "data": "Error: ...", "message": "Error description" }`

## Usage Examples

Get the 2025 race calendar:
> "Show me the F1 2025 race schedule"
> Uses: get_race_schedule with year=2025

Get race results:
> "Who won the Monaco Grand Prix in 2024?"
> Uses: get_race_results with year=2024, event="Monaco"

Compare lap times:
> "Show me Verstappen's lap data from the Monza race"
> Uses: get_lap_data with driver="VER", event="Monza"

Get the current grid:
> "Who are all the F1 drivers this season?"
> Uses: get_driver_info with year=2026

Check qualifying:
> "What were the qualifying results at Silverstone?"
> Uses: get_session_data with session_name="Silverstone", session_type="Q"
