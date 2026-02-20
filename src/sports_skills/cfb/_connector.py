"""College Football (CFB) data connector — ESPN public API.

Provides scores, standings, rosters, schedules, game summaries,
rankings (AP/Coaches polls), and news for NCAA Division I FBS football.
"""

import logging

from sports_skills._espn_base import (
    espn_request,
    espn_web_request,
    espn_summary,
    ESPN_STATUS_MAP,
)

logger = logging.getLogger("sports_skills.cfb")

SPORT_PATH = "football/college-football"

# CFB has 754+ FBS teams — default ESPN limit (50) is far too low.
_TEAMS_LIMIT = 1000


# ============================================================
# ESPN Response Normalizers
# ============================================================


def _normalize_event(espn_event):
    """Normalize an ESPN scoreboard event to a standard format."""
    comp = espn_event.get("competitions", [{}])[0]
    status_obj = comp.get("status", espn_event.get("status", {}))
    status_type = status_obj.get("type", {}).get("name", "")
    status_detail = status_obj.get("type", {}).get("shortDetail", "")

    competitors = []
    for c in comp.get("competitors", []):
        team = c.get("team", {})
        linescores = c.get("linescores", [])
        records = c.get("records", [])

        # College-specific: curatedRank (AP poll ranking, 99 = unranked)
        curated = c.get("curatedRank", {})
        rank = curated.get("current", 99)

        competitors.append({
            "team": {
                "id": str(team.get("id", "")),
                "name": team.get("displayName", ""),
                "abbreviation": team.get("abbreviation", ""),
                "logo": team.get("logo", ""),
                "conference_id": team.get("conferenceId", ""),
            },
            "home_away": c.get("homeAway", ""),
            "score": c.get("score", "0"),
            "period_scores": [int(p.get("value", 0)) for p in linescores],
            "record": records[0].get("summary", "") if records else "",
            "winner": c.get("winner", False),
            "rank": rank if rank != 99 else None,
        })

    odds = []
    for o in comp.get("odds", []):
        odds.append({
            "provider": o.get("provider", {}).get("name", ""),
            "details": o.get("details", ""),
            "over_under": o.get("overUnder", ""),
        })

    broadcasts = []
    for b in comp.get("broadcasts", []):
        for name in b.get("names", []):
            broadcasts.append(name)

    week_info = espn_event.get("week", {})

    # Conference competition metadata
    groups = comp.get("groups", {})

    return {
        "id": str(espn_event.get("id", "")),
        "name": espn_event.get("name", ""),
        "short_name": espn_event.get("shortName", ""),
        "status": ESPN_STATUS_MAP.get(status_type, status_type),
        "status_detail": status_detail,
        "start_time": comp.get("date", espn_event.get("date", "")),
        "venue": {
            "name": comp.get("venue", {}).get("fullName", ""),
            "city": comp.get("venue", {}).get("address", {}).get("city", ""),
            "state": comp.get("venue", {}).get("address", {}).get("state", ""),
        },
        "competitors": competitors,
        "odds": odds,
        "broadcasts": broadcasts,
        "week": week_info.get("number") if week_info else None,
        "conference": groups.get("name", "") if groups else "",
    }


def _normalize_standings_entries(standings_data):
    """Parse entries from an ESPN standings block."""
    entries = []
    for entry in standings_data.get("entries", []):
        team = entry.get("team", {})
        stats = {s["name"]: s.get("displayValue", s.get("value", ""))
                 for s in entry.get("stats", [])}
        entries.append({
            "team": {
                "id": str(team.get("id", "")),
                "name": team.get("displayName", ""),
                "abbreviation": team.get("abbreviation", ""),
                "logo": team.get("logos", [{}])[0].get("href", "") if team.get("logos") else "",
            },
            "wins": stats.get("wins", "0"),
            "losses": stats.get("losses", "0"),
            "win_pct": stats.get("winPercent", stats.get("winPct", "0")),
            "points_for": stats.get("pointsFor", "0"),
            "points_against": stats.get("pointsAgainst", "0"),
            "streak": stats.get("streak", ""),
            "conference_record": stats.get("conferenceRecord", stats.get("vs. Conf.", "")),
        })
    return entries


def _normalize_standings(espn_data):
    """Normalize ESPN standings with conference groups.

    Handles two ESPN response structures:
    - All conferences: children[] array with each conference
    - Single conference (group filter): root object IS the conference
    """
    groups = []

    # When filtered by group, the root object IS the conference (no children[])
    if not espn_data.get("children") and espn_data.get("standings"):
        conference_name = espn_data.get("name", espn_data.get("abbreviation", ""))
        entries = _normalize_standings_entries(espn_data["standings"])
        if entries:
            groups.append({
                "conference": conference_name,
                "division": "",
                "entries": entries,
            })
        return groups

    for child in espn_data.get("children", []):
        conference_name = child.get("name", child.get("abbreviation", ""))

        # Check for division sub-groups
        if child.get("children"):
            for division in child["children"]:
                division_name = division.get("name", "")
                standings = division.get("standings", {})
                entries = _normalize_standings_entries(standings)
                if entries:
                    groups.append({
                        "conference": conference_name,
                        "division": division_name,
                        "entries": entries,
                    })
        elif child.get("standings"):
            entries = _normalize_standings_entries(child["standings"])
            if entries:
                groups.append({
                    "conference": conference_name,
                    "division": "",
                    "entries": entries,
                })
    return groups


def _normalize_team(espn_team):
    """Normalize an ESPN team object."""
    team = espn_team.get("team", espn_team)
    logos = team.get("logos", [])
    return {
        "id": str(team.get("id", "")),
        "name": team.get("displayName", ""),
        "abbreviation": team.get("abbreviation", ""),
        "nickname": team.get("nickname", team.get("shortDisplayName", "")),
        "location": team.get("location", ""),
        "color": team.get("color", ""),
        "logo": logos[0].get("href", "") if logos else "",
        "is_active": team.get("isActive", True),
    }


def _normalize_roster(espn_data):
    """Normalize ESPN roster response (positional groups like NFL)."""
    athletes = []
    for group in espn_data.get("athletes", []):
        position_group = group.get("position", "")
        for item in group.get("items", []):
            athlete = item
            athletes.append({
                "id": str(athlete.get("id", "")),
                "name": athlete.get("displayName", athlete.get("fullName", "")),
                "jersey": athlete.get("jersey", ""),
                "position": athlete.get("position", {}).get("abbreviation", position_group),
                "age": athlete.get("age", ""),
                "height": athlete.get("displayHeight", ""),
                "weight": athlete.get("displayWeight", ""),
                "experience": athlete.get("experience", {}).get("years", ""),
                "status": athlete.get("status", {}).get("type", ""),
            })
    return athletes


def _normalize_game_summary(summary_data):
    """Normalize ESPN game summary with box score and scoring plays."""
    if not summary_data:
        return {"error": True, "message": "No summary data available"}

    header = summary_data.get("header", {})
    competitions = header.get("competitions", [{}])
    comp = competitions[0] if competitions else {}

    game_info = {
        "id": header.get("id", ""),
        "status": comp.get("status", {}).get("type", {}).get("name", ""),
        "status_detail": comp.get("status", {}).get("type", {}).get("shortDetail", ""),
        "venue": {
            "name": summary_data.get("gameInfo", {}).get("venue", {}).get("fullName", ""),
            "city": summary_data.get("gameInfo", {}).get("venue", {}).get("address", {}).get("city", ""),
        },
    }

    competitors = []
    for c in comp.get("competitors", []):
        team = c.get("team", [{}])
        if isinstance(team, list):
            team = team[0] if team else {}
        rank = c.get("rank", "")
        competitors.append({
            "team": {
                "id": str(team.get("id", "")),
                "name": team.get("displayName", team.get("location", "")),
                "abbreviation": team.get("abbreviation", ""),
                "logo": team.get("logo", ""),
            },
            "home_away": c.get("homeAway", ""),
            "score": c.get("score", "0"),
            "winner": c.get("winner", False),
            "record": c.get("record", ""),
            "rank": rank if rank else None,
            "linescores": [ls.get("displayValue", "0") for ls in c.get("linescores", [])],
        })

    # Box score
    boxscore = summary_data.get("boxscore", {})
    box_teams = []
    for bt in boxscore.get("teams", []):
        team = bt.get("team", {})
        stats_list = []
        for stat_group in bt.get("statistics", []):
            stat_name = stat_group.get("name", "")
            labels = stat_group.get("labels", [])
            athletes_stats = []
            for ath in stat_group.get("athletes", []):
                athlete = ath.get("athlete", {})
                athletes_stats.append({
                    "name": athlete.get("displayName", ""),
                    "position": athlete.get("position", {}).get("abbreviation", ""),
                    "stats": dict(zip(labels, ath.get("stats", []))),
                })
            totals = stat_group.get("totals", [])
            stats_list.append({
                "category": stat_name,
                "labels": labels,
                "athletes": athletes_stats,
                "totals": dict(zip(labels, totals)) if totals else {},
            })
        box_teams.append({
            "team": {
                "id": str(team.get("id", "")),
                "name": team.get("displayName", ""),
                "abbreviation": team.get("abbreviation", ""),
            },
            "statistics": stats_list,
        })

    # Scoring plays
    scoring_plays = []
    for sp in summary_data.get("scoringPlays", []):
        team = sp.get("team", {})
        scoring_plays.append({
            "period": sp.get("period", {}).get("number", ""),
            "clock": sp.get("clock", {}).get("displayValue", ""),
            "type": sp.get("type", {}).get("text", ""),
            "text": sp.get("text", ""),
            "team": {
                "id": str(team.get("id", "")),
                "name": team.get("displayName", team.get("name", "")),
                "abbreviation": team.get("abbreviation", ""),
            },
            "home_score": sp.get("homeScore", ""),
            "away_score": sp.get("awayScore", ""),
        })

    # Leaders
    leaders = []
    for leader_group in summary_data.get("leaders", []):
        team = leader_group.get("team", {})
        categories = []
        for cat in leader_group.get("leaders", []):
            top = cat.get("leaders", [{}])
            top_leader = top[0] if top else {}
            athlete = top_leader.get("athlete", {})
            categories.append({
                "category": cat.get("displayName", cat.get("name", "")),
                "leader": {
                    "name": athlete.get("displayName", ""),
                    "position": athlete.get("position", {}).get("abbreviation", ""),
                    "value": top_leader.get("displayValue", ""),
                },
            })
        leaders.append({
            "team": {
                "id": str(team.get("id", "")),
                "name": team.get("displayName", ""),
            },
            "categories": categories,
        })

    return {
        "game_info": game_info,
        "competitors": competitors,
        "boxscore": box_teams,
        "scoring_plays": scoring_plays,
        "leaders": leaders,
    }


def _normalize_rankings(espn_data):
    """Normalize ESPN rankings (AP Top 25, Coaches Poll, etc.)."""
    polls = []
    for ranking in espn_data.get("rankings", []):
        teams = []
        for entry in ranking.get("ranks", []):
            team = entry.get("team", {})
            teams.append({
                "rank": entry.get("current", ""),
                "previous_rank": entry.get("previous", ""),
                "trend": entry.get("trend", ""),
                "team": team.get("nickname", team.get("displayName", team.get("location", ""))),
                "team_id": str(team.get("id", "")),
                "abbreviation": team.get("abbreviation", ""),
                "logo": team.get("logo", ""),
                "record": entry.get("recordSummary", ""),
                "points": entry.get("points", ""),
                "first_place_votes": entry.get("firstPlaceVotes", 0),
            })
        polls.append({
            "name": ranking.get("name", ranking.get("shortName", "")),
            "short_name": ranking.get("shortName", ""),
            "type": ranking.get("type", ""),
            "teams": teams,
        })
    return polls


def _normalize_news(espn_data):
    """Normalize ESPN news response."""
    articles = []
    for article in espn_data.get("articles", []):
        articles.append({
            "headline": article.get("headline", ""),
            "description": article.get("description", ""),
            "published": article.get("published", ""),
            "type": article.get("type", ""),
            "premium": article.get("premium", False),
            "link": "",
            "images": [img.get("url", "") for img in article.get("images", [])[:1]],
        })
        links = article.get("links", {})
        web = links.get("web", {})
        if web.get("href"):
            articles[-1]["link"] = web["href"]
        elif links.get("api", {}).get("self", {}).get("href"):
            articles[-1]["link"] = links["api"]["self"]["href"]
    return articles


# ============================================================
# Command Functions
# ============================================================


def get_scoreboard(request_data):
    """Get live/recent college football scores."""
    params = request_data.get("params", {})
    date = params.get("date")
    week = params.get("week")
    group = params.get("group")
    limit = params.get("limit")

    espn_params = {}
    if date:
        espn_params["dates"] = date.replace("-", "")
    if week:
        espn_params["week"] = week
    if group:
        espn_params["groups"] = group
    if limit:
        espn_params["limit"] = limit

    data = espn_request(SPORT_PATH, "scoreboard", espn_params or None)
    if data.get("error"):
        return data

    events = [_normalize_event(e) for e in data.get("events", [])]
    season_info = data.get("season", {})
    week_info = data.get("week", {})

    return {
        "events": events,
        "season": {
            "year": season_info.get("year", ""),
            "type": season_info.get("type", ""),
        },
        "week": {
            "number": week_info.get("number", ""),
            "text": week_info.get("text", ""),
        },
        "count": len(events),
    }


def get_standings(request_data):
    """Get college football standings by conference."""
    params = request_data.get("params", {})
    season = params.get("season")
    group = params.get("group")

    espn_params = {}
    if season:
        espn_params["season"] = season
    if group:
        espn_params["group"] = group

    data = espn_web_request(SPORT_PATH, "standings", espn_params or None)
    if data.get("error"):
        return data

    groups = _normalize_standings(data)
    return {
        "groups": groups,
        "season": data.get("season", {}).get("year", ""),
    }


def get_teams(request_data=None):
    """Get all FBS college football teams."""
    data = espn_request(SPORT_PATH, "teams", {"limit": _TEAMS_LIMIT})
    if data.get("error"):
        return data

    teams = []
    for sport in data.get("sports", []):
        for league in sport.get("leagues", []):
            for team_wrapper in league.get("teams", []):
                teams.append(_normalize_team(team_wrapper))

    return {"teams": teams, "count": len(teams)}


def get_team_roster(request_data):
    """Get roster for a college football team."""
    params = request_data.get("params", {})
    team_id = params.get("team_id")
    if not team_id:
        return {"error": True, "message": "team_id is required"}

    data = espn_request(SPORT_PATH, f"teams/{team_id}/roster")
    if data.get("error"):
        return data

    athletes = _normalize_roster(data)
    team_info = data.get("team", {})

    return {
        "team": {
            "id": str(team_info.get("id", team_id)),
            "name": team_info.get("displayName", ""),
            "abbreviation": team_info.get("abbreviation", ""),
        },
        "athletes": athletes,
        "count": len(athletes),
    }


def get_team_schedule(request_data):
    """Get schedule for a specific college football team."""
    params = request_data.get("params", {})
    team_id = params.get("team_id")
    season = params.get("season")
    if not team_id:
        return {"error": True, "message": "team_id is required"}

    espn_params = {}
    if season:
        espn_params["season"] = season

    resource = f"teams/{team_id}/schedule"
    data = espn_request(SPORT_PATH, resource, espn_params or None)
    if data.get("error"):
        return data

    events = [_normalize_event(event) for event in data.get("events", [])]

    team_info = data.get("team", {})
    return {
        "team": {
            "id": str(team_info.get("id", team_id)),
            "name": team_info.get("displayName", ""),
            "abbreviation": team_info.get("abbreviation", ""),
        },
        "events": events,
        "season": data.get("season", {}).get("year", ""),
        "count": len(events),
    }


def get_game_summary(request_data):
    """Get detailed game summary with box score."""
    params = request_data.get("params", {})
    event_id = params.get("event_id")
    if not event_id:
        return {"error": True, "message": "event_id is required"}

    data = espn_summary(SPORT_PATH, event_id)
    if not data:
        return {"error": True, "message": f"No summary data found for event {event_id}"}

    return _normalize_game_summary(data)


def get_rankings(request_data):
    """Get college football rankings (AP Top 25, Coaches Poll, CFP)."""
    params = request_data.get("params", {})
    season = params.get("season")
    week = params.get("week")

    espn_params = {}
    if season:
        espn_params["seasons"] = season
    if week:
        espn_params["weeks"] = week

    data = espn_request(SPORT_PATH, "rankings", espn_params or None)
    if data.get("error"):
        return data

    polls = _normalize_rankings(data)
    return {
        "polls": polls,
        "season": data.get("season", {}).get("year", ""),
        "week": data.get("week", ""),
    }


def get_news(request_data):
    """Get college football news articles."""
    params = request_data.get("params", {})
    team_id = params.get("team_id")

    resource = f"teams/{team_id}/news" if team_id else "news"
    data = espn_request(SPORT_PATH, resource)
    if data.get("error"):
        return data

    articles = _normalize_news(data)
    return {"articles": articles, "count": len(articles)}


def get_schedule(request_data):
    """Get college football schedule."""
    params = request_data.get("params", {})
    season = params.get("season")
    week = params.get("week")
    group = params.get("group")

    espn_params = {}
    if season:
        espn_params["dates"] = str(season)
    if week:
        espn_params["week"] = week
    if group:
        espn_params["groups"] = group

    data = espn_request(SPORT_PATH, "scoreboard", espn_params or None)
    if data.get("error"):
        return data

    events = [_normalize_event(e) for e in data.get("events", [])]
    season_info = data.get("season", {})
    week_info = data.get("week", {})

    return {
        "events": events,
        "season": {
            "year": season_info.get("year", ""),
            "type": season_info.get("type", ""),
        },
        "week": {
            "number": week_info.get("number", ""),
            "text": week_info.get("text", ""),
        },
        "count": len(events),
    }
