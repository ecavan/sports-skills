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
