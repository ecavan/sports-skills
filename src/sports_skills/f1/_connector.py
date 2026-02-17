import fastf1

import pandas as pd

fastf1.set_log_level('WARNING')


def _format_timedelta(td):
    """Convert pandas Timedelta to a clean time string like '1:42:06.304'."""
    if pd.isna(td) or td is None:
        return ""
    if isinstance(td, str):
        return td
    total_seconds = td.total_seconds()
    if total_seconds <= 0:
        return ""
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:06.3f}"
    elif minutes > 0:
        return f"{minutes}:{seconds:06.3f}"
    else:
        return f"{seconds:.3f}"


def _validate_event(year, event_name):
    """Validate that event_name matches an actual event. Returns the exact event name or raises ValueError."""
    schedule = fastf1.get_event_schedule(year)
    real_events = schedule[schedule['EventFormat'] != 'testing']
    exact = real_events[real_events['EventName'].str.lower() == event_name.lower()]
    if not exact.empty:
        return exact.iloc[0]['EventName']
    # Try substring match
    partial = real_events[real_events['EventName'].str.lower().str.contains(event_name.lower())]
    if len(partial) == 1:
        return partial.iloc[0]['EventName']
    # No valid match — list available events
    available = ', '.join(real_events['EventName'].tolist())
    raise ValueError(f"Event '{event_name}' not found in {year} calendar. Available events: {available}")


def get_session_data(request_data):
    try:
        params = request_data.get('params', {})

        year = params.get('session_year', 2019)
        event = params.get('session_name', 'Monza')
        session_type = params.get('session_type', 'Q')

        event = _validate_event(year, event)
        session = fastf1.get_session(year, event, session_type)

        session.load()

        result = {
            "session": str(session),
            "event_name": getattr(session.event, 'name', 'Unknown Event'),
            "event_date": str(getattr(session.event, 'date', 'Unknown Date')),
            "session_type": getattr(session, 'session_type', 'Unknown Session Type'),
            "track_name": getattr(session.event, 'circuit_name', 'Unknown Track')
        }

        return {"status": True, "data": result, "message": "Session data retrieved successfully"}

    except Exception as e:
        return {
            "status": False,
            "data": f"Error: {str(e)}",
            "message": "Error getting session data"
        }


def get_driver_info(request_data):
    """Get driver info by loading the last race session of the season and extracting from results."""
    try:
        params = request_data.get('params', {})

        year = params.get('year', 2023)
        driver = params.get('driver')

        # Get the schedule and find the last completed race
        schedule = fastf1.get_event_schedule(year)
        races = schedule[schedule['EventFormat'] != 'testing']

        # Load the last race to get driver info from results
        last_race = races.iloc[-1]['EventName']
        session = fastf1.get_session(year, last_race, 'R')
        session.load()
        results = session.results

        if driver:
            # Filter by driver code or name
            driver_upper = driver.upper()
            match = results[
                (results['Abbreviation'].str.upper() == driver_upper) |
                (results['FullName'].str.lower().str.contains(driver.lower()))
            ]
            if match.empty:
                return {"status": False, "data": None, "message": f"No information found for driver '{driver}' in {year}"}

            row = match.iloc[0]
            driver_data = {
                "driver_number": str(row.get('DriverNumber', '')),
                "driver_id": row.get('DriverId', ''),
                "driver_code": row.get('Abbreviation', ''),
                "first_name": row.get('FirstName', ''),
                "last_name": row.get('LastName', ''),
                "full_name": row.get('FullName', ''),
                "team_name": row.get('TeamName', ''),
                "team_color": row.get('TeamColor', ''),
                "headshot_url": row.get('HeadshotUrl', ''),
                "country_code": row.get('CountryCode', '')
            }
            return {"status": True, "data": [driver_data], "message": f"Driver information for {driver} in {year} retrieved successfully"}
        else:
            drivers_list = []
            for _, row in results.iterrows():
                drivers_list.append({
                    "driver_number": str(row.get('DriverNumber', '')),
                    "driver_id": row.get('DriverId', ''),
                    "driver_code": row.get('Abbreviation', ''),
                    "first_name": row.get('FirstName', ''),
                    "last_name": row.get('LastName', ''),
                    "full_name": row.get('FullName', ''),
                    "team_name": row.get('TeamName', ''),
                    "team_color": row.get('TeamColor', ''),
                    "headshot_url": row.get('HeadshotUrl', ''),
                    "country_code": row.get('CountryCode', '')
                })

            return {"status": True, "data": drivers_list, "message": f"Driver information for {year} retrieved successfully"}

    except Exception as e:
        return {
            "status": False,
            "data": f"Error: {str(e)}",
            "message": "Error getting driver information"
        }


def get_team_info(request_data):
    """Get team info by loading the last race session of the season and extracting unique teams from results."""
    try:
        params = request_data.get('params', {})

        year = params.get('year', 2023)
        team = params.get('team')

        # Get the schedule and find the last completed race
        schedule = fastf1.get_event_schedule(year)
        races = schedule[schedule['EventFormat'] != 'testing']

        last_race = races.iloc[-1]['EventName']
        session = fastf1.get_session(year, last_race, 'R')
        session.load()
        results = session.results

        # Extract unique teams
        seen_teams = set()
        teams_list = []
        for _, row in results.iterrows():
            team_id = row.get('TeamId', '')
            if team_id in seen_teams:
                continue
            seen_teams.add(team_id)

            team_data = {
                "team_id": team_id,
                "team_name": row.get('TeamName', ''),
                "team_color": row.get('TeamColor', ''),
                "drivers": []
            }

            # Collect all drivers for this team
            team_drivers = results[results['TeamId'] == team_id]
            for _, d in team_drivers.iterrows():
                team_data["drivers"].append({
                    "driver_code": d.get('Abbreviation', ''),
                    "full_name": d.get('FullName', ''),
                    "driver_number": str(d.get('DriverNumber', ''))
                })

            teams_list.append(team_data)

        if team:
            team_lower = team.lower()
            match = [t for t in teams_list if team_lower in t['team_name'].lower() or team_lower in t['team_id'].lower()]
            if not match:
                available = ', '.join(t['team_name'] for t in teams_list)
                return {"status": False, "data": None, "message": f"No information found for team '{team}' in {year}. Available teams: {available}"}
            return {"status": True, "data": match, "message": f"Team information for {team} in {year} retrieved successfully"}

        return {"status": True, "data": teams_list, "message": f"Team information for {year} retrieved successfully"}

    except Exception as e:
        return {
            "status": False,
            "data": f"Error: {str(e)}",
            "message": "Error getting team information"
        }


def get_race_schedule(request_data):
    try:
        params = request_data.get('params', {})

        year = params.get('year', 2023)

        schedule = fastf1.get_event_schedule(year)
        events = []

        for _, row in schedule.iterrows():
            event_data = {
                "round_number": row.get('RoundNumber', ''),
                "country": row.get('Country', ''),
                "location": row.get('Location', ''),
                "event_name": row.get('EventName', ''),
                "circuit_name": row.get('CircuitName', ''),
                "event_date": str(row.get('EventDate', '')),
                "event_format": row.get('EventFormat', '')
            }
            events.append(event_data)

        return {"status": True, "data": events, "message": f"Race schedule for {year} retrieved successfully"}

    except Exception as e:
        return {
            "status": False,
            "data": f"Error: {str(e)}",
            "message": "Error getting race schedule"
        }


def get_lap_data(request_data):
    try:
        params = request_data.get('params', {})

        year = params.get('year', 2023)
        event = params.get('event', 'Monza')
        session_type = params.get('session_type', 'R')
        driver = params.get('driver')

        event = _validate_event(year, event)
        session = fastf1.get_session(year, event, session_type)
        session.load()

        if driver:
            laps = session.laps.pick_drivers(driver)
        else:
            laps = session.laps

        # Compute fastest valid lap for dynamic sanity threshold
        valid_times = laps['LapTime'].dropna()
        if not valid_times.empty:
            fastest_seconds = valid_times.min().total_seconds()
            max_reasonable = fastest_seconds * 1.5
        else:
            max_reasonable = 150  # fallback: 2.5 min

        laps_list = []
        for _, lap in laps.iterrows():
            lap_time = lap.get('LapTime')
            s1 = lap.get('Sector1Time')
            s2 = lap.get('Sector2Time')
            s3 = lap.get('Sector3Time')

            # Reconstruct lap time from sectors when missing (common in qualifying)
            is_accurate = True
            if pd.isna(lap_time) and pd.notna(s1) and pd.notna(s2) and pd.notna(s3):
                reconstructed = s1 + s2 + s3
                # Dynamic sanity check: reject if > 1.5x the fastest valid lap
                if reconstructed.total_seconds() <= max_reasonable:
                    lap_time = reconstructed
                    is_accurate = False

            lap_data = {
                "driver": lap.get('Driver', ''),
                "team": lap.get('Team', ''),
                "lap_number": lap.get('LapNumber', ''),
                "lap_time": _format_timedelta(lap_time),
                "is_accurate": is_accurate,
                "sector_1_time": _format_timedelta(s1),
                "sector_2_time": _format_timedelta(s2),
                "sector_3_time": _format_timedelta(s3),
                "compound": lap.get('Compound', ''),
                "tyre_life": lap.get('TyreLife', ''),
                "is_personal_best": bool(lap.get('IsPersonalBest', False)),
                "position": lap.get('Position', '')
            }
            laps_list.append(lap_data)

        return {"status": True, "data": laps_list, "message": "Lap data retrieved successfully"}

    except Exception as e:
        return {
            "status": False,
            "data": f"Error: {str(e)}",
            "message": "Error getting lap data"
        }


def _get_completed_races(year):
    """Get list of completed race event names for a season."""
    schedule = fastf1.get_event_schedule(year)
    races = schedule[schedule['EventFormat'] != 'testing']
    return races['EventName'].tolist()


def _load_session_cached(year, event):
    """Load a race session. FastF1 handles its own caching."""
    session = fastf1.get_session(year, event, 'R')
    session.load()
    return session


def get_pit_stops(request_data):
    """Get pit stop durations (PitIn → PitOut) for a race or full season."""
    try:
        params = request_data.get('params', {})
        year = int(params.get('year', 2025))
        event = params.get('event')
        driver = params.get('driver')

        if event:
            event = _validate_event(year, event)
            race_names = [event]
        else:
            race_names = _get_completed_races(year)

        all_pits = []
        for race_name in race_names:
            try:
                session = _load_session_cached(year, race_name)
                laps = session.laps.copy()

                for drv in laps['Driver'].unique():
                    if driver and drv.upper() != driver.upper():
                        continue
                    dl = laps[laps['Driver'] == drv].sort_values('LapNumber')
                    team = dl['Team'].iloc[0] if not dl.empty else ''

                    pit_in_laps = dl[dl['PitInTime'].notna()]
                    for _, pit_lap in pit_in_laps.iterrows():
                        pit_in_time = pit_lap['PitInTime']
                        lap_num = pit_lap['LapNumber']
                        next_lap = dl[dl['LapNumber'] == lap_num + 1]
                        if not next_lap.empty and pd.notna(next_lap.iloc[0]['PitOutTime']):
                            pit_out_time = next_lap.iloc[0]['PitOutTime']
                            duration = (pit_out_time - pit_in_time).total_seconds()
                            if 15 < duration < 60:
                                all_pits.append({
                                    'race': race_name,
                                    'team': team,
                                    'driver': drv,
                                    'lap': int(lap_num),
                                    'duration_seconds': round(duration, 3)
                                })
            except Exception:
                continue

        # Sort by duration
        all_pits.sort(key=lambda x: x['duration_seconds'])

        # Compute team averages
        team_stats = {}
        for p in all_pits:
            t = p['team']
            if t not in team_stats:
                team_stats[t] = {'durations': [], 'best': float('inf'), 'best_detail': None}
            team_stats[t]['durations'].append(p['duration_seconds'])
            if p['duration_seconds'] < team_stats[t]['best']:
                team_stats[t]['best'] = p['duration_seconds']
                team_stats[t]['best_detail'] = p

        team_summary = []
        for t, stats in sorted(team_stats.items(), key=lambda x: sum(x[1]['durations']) / len(x[1]['durations'])):
            avg = sum(stats['durations']) / len(stats['durations'])
            team_summary.append({
                'team': t,
                'average_seconds': round(avg, 3),
                'best_seconds': round(stats['best'], 3),
                'total_stops': len(stats['durations'])
            })

        return {
            "status": True,
            "data": {
                "pit_stops": all_pits,
                "team_summary": team_summary,
                "total_stops": len(all_pits)
            },
            "message": f"Pit stop data for {year}" + (f" {event}" if event else " (full season)") + " retrieved successfully"
        }

    except Exception as e:
        return {"status": False, "data": f"Error: {str(e)}", "message": "Error getting pit stop data"}


def get_speed_data(request_data):
    """Get speed trap and intermediate speed data for a race or full season."""
    try:
        params = request_data.get('params', {})
        year = int(params.get('year', 2025))
        event = params.get('event')
        driver = params.get('driver')

        if event:
            event = _validate_event(year, event)
            race_names = [event]
        else:
            race_names = _get_completed_races(year)

        speed_cols = {'SpeedST': 'speed_trap', 'SpeedFL': 'finish_line', 'SpeedI1': 'intermediate_1', 'SpeedI2': 'intermediate_2'}
        all_speeds = []

        for race_name in race_names:
            try:
                session = _load_session_cached(year, race_name)
                laps = session.laps.copy()

                if driver:
                    laps = laps[laps['Driver'].str.upper() == driver.upper()]

                for col, label in speed_cols.items():
                    if col not in laps.columns:
                        continue
                    valid = laps[laps[col].notna() & (laps[col] > 0)]
                    if valid.empty:
                        continue
                    idx = valid[col].idxmax()
                    row = valid.loc[idx]
                    all_speeds.append({
                        'race': race_name,
                        'driver': row['Driver'],
                        'team': row['Team'],
                        'speed_kmh': float(row[col]),
                        'trap': label,
                        'lap': int(row['LapNumber'])
                    })
            except Exception:
                continue

        all_speeds.sort(key=lambda x: x['speed_kmh'], reverse=True)

        # Team top speed summary (speed trap only)
        team_speeds = {}
        for s in all_speeds:
            if s['trap'] != 'speed_trap':
                continue
            t = s['team']
            if t not in team_speeds:
                team_speeds[t] = []
            team_speeds[t].append(s['speed_kmh'])

        team_summary = []
        for t, speeds in sorted(team_speeds.items(), key=lambda x: max(x[1]), reverse=True):
            team_summary.append({
                'team': t,
                'max_speed_kmh': max(speeds),
                'avg_speed_kmh': round(sum(speeds) / len(speeds), 1),
                'readings': len(speeds)
            })

        return {
            "status": True,
            "data": {
                "top_speeds": all_speeds[:50],
                "team_summary": team_summary
            },
            "message": f"Speed data for {year}" + (f" {event}" if event else " (full season)") + " retrieved successfully"
        }

    except Exception as e:
        return {"status": False, "data": f"Error: {str(e)}", "message": "Error getting speed data"}


def get_championship_standings(request_data):
    """Get driver and constructor championship standings by aggregating all race results."""
    try:
        params = request_data.get('params', {})
        year = int(params.get('year', 2025))

        race_names = _get_completed_races(year)

        driver_points = {}
        driver_info = {}
        team_points = {}

        for race_name in race_names:
            try:
                session = _load_session_cached(year, race_name)
                results = session.results

                for _, row in results.iterrows():
                    drv = row.get('Abbreviation', '')
                    pts = float(row.get('Points', 0)) if pd.notna(row.get('Points')) else 0
                    pos = row.get('Position', 99)
                    pos = int(pos) if pd.notna(pos) else 99
                    team = row.get('TeamName', '')

                    if drv not in driver_points:
                        driver_points[drv] = 0
                        driver_info[drv] = {
                            'driver_code': drv,
                            'full_name': row.get('FullName', ''),
                            'team': team,
                            'wins': 0,
                            'podiums': 0,
                            'races': 0
                        }

                    driver_points[drv] += pts
                    driver_info[drv]['races'] += 1
                    if pos == 1:
                        driver_info[drv]['wins'] += 1
                    if pos <= 3:
                        driver_info[drv]['podiums'] += 1

                    if team not in team_points:
                        team_points[team] = 0
                    team_points[team] += pts
            except Exception:
                continue

        # Sort drivers by points
        driver_standings = []
        for i, (drv, pts) in enumerate(sorted(driver_points.items(), key=lambda x: x[1], reverse=True), 1):
            info = driver_info[drv]
            driver_standings.append({
                'position': i,
                'driver_code': drv,
                'full_name': info['full_name'],
                'team': info['team'],
                'points': pts,
                'wins': info['wins'],
                'podiums': info['podiums'],
                'races': info['races']
            })

        # Sort constructors by points
        constructor_standings = []
        for i, (team, pts) in enumerate(sorted(team_points.items(), key=lambda x: x[1], reverse=True), 1):
            constructor_standings.append({
                'position': i,
                'team': team,
                'points': pts
            })

        return {
            "status": True,
            "data": {
                "driver_standings": driver_standings,
                "constructor_standings": constructor_standings,
                "races_counted": len(race_names)
            },
            "message": f"Championship standings for {year} ({len(race_names)} races)"
        }

    except Exception as e:
        return {"status": False, "data": f"Error: {str(e)}", "message": "Error getting championship standings"}


def get_season_stats(request_data):
    """Get aggregated season stats: fastest laps, top speeds, points, wins per driver/team."""
    try:
        params = request_data.get('params', {})
        year = int(params.get('year', 2025))

        race_names = _get_completed_races(year)

        driver_stats = {}
        team_fastest_laps = {}

        for race_name in race_names:
            try:
                session = _load_session_cached(year, race_name)
                results = session.results
                laps = session.laps

                # Results-based stats
                for _, row in results.iterrows():
                    drv = row.get('Abbreviation', '')
                    team = row.get('TeamName', '')
                    pts = float(row.get('Points', 0)) if pd.notna(row.get('Points')) else 0
                    pos = int(row.get('Position', 99)) if pd.notna(row.get('Position')) else 99
                    grid = int(row.get('GridPosition', 99)) if pd.notna(row.get('GridPosition')) else 99

                    if drv not in driver_stats:
                        driver_stats[drv] = {
                            'driver_code': drv,
                            'full_name': row.get('FullName', ''),
                            'team': team,
                            'points': 0, 'wins': 0, 'podiums': 0, 'poles': 0,
                            'dnfs': 0, 'races': 0, 'best_finish': 99,
                            'fastest_lap_time': None, 'fastest_lap_race': '',
                            'top_speed_kmh': 0, 'top_speed_race': '',
                            'positions_gained': 0
                        }

                    ds = driver_stats[drv]
                    ds['points'] += pts
                    ds['races'] += 1
                    if pos == 1:
                        ds['wins'] += 1
                    if pos <= 3:
                        ds['podiums'] += 1
                    if grid == 1:
                        ds['poles'] += 1
                    if row.get('Status', '') not in ('Finished', '+1 Lap', '+2 Laps', '+3 Laps'):
                        ds['dnfs'] += 1
                    if pos < ds['best_finish']:
                        ds['best_finish'] = pos
                    ds['positions_gained'] += (grid - pos)

                # Lap-based stats (fastest laps, top speeds)
                valid_laps = laps[laps['LapTime'].notna() & laps['IsAccurate']]
                if not valid_laps.empty:
                    # Race fastest lap
                    fastest_idx = valid_laps['LapTime'].idxmin()
                    fl = valid_laps.loc[fastest_idx]
                    fl_team = fl['Team']
                    if fl_team not in team_fastest_laps:
                        team_fastest_laps[fl_team] = 0
                    team_fastest_laps[fl_team] += 1

                    # Per-driver fastest lap
                    for drv in valid_laps['Driver'].unique():
                        drv_laps = valid_laps[valid_laps['Driver'] == drv]
                        best_lap = drv_laps['LapTime'].min()
                        if drv in driver_stats:
                            if driver_stats[drv]['fastest_lap_time'] is None or best_lap < driver_stats[drv]['fastest_lap_time']:
                                driver_stats[drv]['fastest_lap_time'] = best_lap
                                driver_stats[drv]['fastest_lap_race'] = race_name

                # Speed trap data
                if 'SpeedST' in laps.columns:
                    for drv in laps['Driver'].unique():
                        drv_laps = laps[(laps['Driver'] == drv) & (laps['SpeedST'].notna()) & (laps['SpeedST'] > 0)]
                        if not drv_laps.empty:
                            max_speed = drv_laps['SpeedST'].max()
                            if drv in driver_stats and max_speed > driver_stats[drv]['top_speed_kmh']:
                                driver_stats[drv]['top_speed_kmh'] = float(max_speed)
                                driver_stats[drv]['top_speed_race'] = race_name

            except Exception:
                continue

        # Format output
        driver_list = []
        for drv, ds in sorted(driver_stats.items(), key=lambda x: x[1]['points'], reverse=True):
            entry = dict(ds)
            entry['fastest_lap_time'] = _format_timedelta(entry['fastest_lap_time'])
            entry['top_speed_kmh'] = round(entry['top_speed_kmh'], 1)
            entry['avg_positions_gained'] = round(entry['positions_gained'] / max(entry['races'], 1), 1)
            del entry['positions_gained']
            driver_list.append(entry)

        team_fl_list = [{'team': t, 'fastest_laps': c} for t, c in sorted(team_fastest_laps.items(), key=lambda x: x[1], reverse=True)]

        return {
            "status": True,
            "data": {
                "drivers": driver_list,
                "team_fastest_laps": team_fl_list,
                "races_counted": len(race_names)
            },
            "message": f"Season stats for {year} ({len(race_names)} races)"
        }

    except Exception as e:
        return {"status": False, "data": f"Error: {str(e)}", "message": "Error getting season stats"}


def get_race_results(request_data):
    try:
        params = request_data.get('params', {})

        year = int(params.get('year', 2023))
        event = params.get('event', 'Monza')

        event = _validate_event(year, event)
        session = fastf1.get_session(year, event, 'R')
        session.load()

        results = session.results

        # Find who set the fastest lap (lowest FastestLapTime)
        fastest_lap_driver = None
        if 'FastestLapTime' in results.columns:
            valid_times = results[results['FastestLapTime'].notna() & (results['FastestLapTime'] > pd.Timedelta(0))]
            if not valid_times.empty:
                fastest_idx = valid_times['FastestLapTime'].idxmin()
                fastest_lap_driver = results.loc[fastest_idx, 'Abbreviation']

        results_list = []
        for _, result in results.iterrows():
            driver_abbr = result.get('Abbreviation', '')
            result_data = {
                "position": result.get('Position', ''),
                "driver_number": result.get('DriverNumber', ''),
                "driver": driver_abbr,
                "full_name": result.get('FullName', ''),
                "team": result.get('TeamName', ''),
                "grid_position": result.get('GridPosition', ''),
                "status": result.get('Status', ''),
                "points": result.get('Points', ''),
                "time": _format_timedelta(result.get('Time')),
                "fastest_lap": driver_abbr == fastest_lap_driver,
                "fastest_lap_time": _format_timedelta(result.get('FastestLapTime'))
            }
            results_list.append(result_data)

        return {"status": True, "data": results_list, "message": f"Race results for {event} {year} retrieved successfully"}

    except Exception as e:
        return {
            "status": False,
            "data": f"Error: {str(e)}",
            "message": "Error getting race results"
        }
