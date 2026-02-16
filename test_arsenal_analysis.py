"""End-to-end Arsenal analysis — the same analysis that was done manually,
now using sports-skills Python API.

Tests: football, polymarket, kalshi, news modules working together.
"""

import json
import sys
import time

PASS = 0
FAIL = 0
RESULTS = {}


def section(name):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")


def check(label, result, required_keys=None, min_items=None, data_key=None):
    """Validate a result and track pass/fail."""
    global PASS, FAIL

    ok = True
    issues = []

    # Check status
    if not isinstance(result, dict):
        issues.append(f"Expected dict, got {type(result).__name__}")
        ok = False
    elif not result.get("status"):
        issues.append(f"status=False: {result.get('message', 'no message')}")
        ok = False
    else:
        data = result.get("data")
        if data is None and required_keys:
            issues.append("data is None")
            ok = False
        elif required_keys and isinstance(data, dict):
            for key in required_keys:
                if key not in data:
                    issues.append(f"missing key: {key}")
                    ok = False

        if min_items and data_key:
            items = data.get(data_key, []) if isinstance(data, dict) else data
            if isinstance(items, list) and len(items) < min_items:
                issues.append(f"expected >={min_items} items in '{data_key}', got {len(items)}")
                ok = False

    if ok:
        PASS += 1
        print(f"  [PASS] {label}")
    else:
        FAIL += 1
        print(f"  [FAIL] {label}: {'; '.join(issues)}")

    RESULTS[label] = {"ok": ok, "issues": issues}
    return result


# ============================================================
# 1. FOOTBALL — Arsenal season analysis
# ============================================================
section("1. FOOTBALL — Arsenal Season Analysis")

from sports_skills import football

# 1a. Current season detection
print("\n--- Current Season ---")
t0 = time.time()
season = check(
    "get_current_season(premier-league)",
    football.get_current_season(competition_id="premier-league"),
    required_keys=["competition", "season"],
)
print(f"  Time: {time.time()-t0:.1f}s")
if season.get("status"):
    s = season["data"]
    print(f"  Competition: {s['competition']['name']}")
    print(f"  Season: {s['season']['name']} ({s['season']['id']})")

# 1b. Premier League standings
print("\n--- PL Standings ---")
t0 = time.time()
standings = check(
    "get_season_standings(premier-league-2025)",
    football.get_season_standings(season_id="premier-league-2025"),
    required_keys=["standings"],
    min_items=1,
    data_key="standings",
)
print(f"  Time: {time.time()-t0:.1f}s")
if standings.get("status"):
    entries = standings["data"]["standings"][0].get("entries", [])
    arsenal = next((e for e in entries if "arsenal" in e.get("team", {}).get("name", "").lower()), None)
    if arsenal:
        print(f"  Arsenal: #{arsenal['position']} | {arsenal['points']}pts | W{arsenal['won']} D{arsenal['drawn']} L{arsenal['lost']} | GD {arsenal['goal_difference']}")
    # Show top 6
    for e in entries[:6]:
        t = e.get("team", {})
        print(f"    {e['position']:>2}. {t.get('name', '?'):20s} {e['points']:>3}pts  W{e['won']} D{e['drawn']} L{e['lost']}  GD{e['goal_difference']:>+3d}")

# 1c. Today's schedule
print("\n--- Today's Schedule ---")
t0 = time.time()
daily = check(
    "get_daily_schedule()",
    football.get_daily_schedule(),
    required_keys=["date", "events"],
)
print(f"  Time: {time.time()-t0:.1f}s")
if daily.get("status"):
    events = daily["data"]["events"]
    print(f"  Date: {daily['data']['date']}")
    print(f"  Total matches: {len(events)}")
    for e in events[:8]:
        comps = e.get("competitors", [])
        if len(comps) >= 2:
            home = comps[0]
            away = comps[1]
            comp = e.get("competition", {}).get("name", "?")
            print(f"    {home['team']['name']} vs {away['team']['name']} ({comp}) — {e['status']}")

# 1d. Arsenal team profile
print("\n--- Arsenal Team Profile ---")
t0 = time.time()
team = check(
    "get_team_profile(team_id=359)",
    football.get_team_profile(team_id="359", league_slug="premier-league"),
    required_keys=["team"],
)
print(f"  Time: {time.time()-t0:.1f}s")
if team.get("status"):
    t = team["data"]["team"]
    print(f"  Name: {t.get('name', '?')}")
    print(f"  Venue: {team['data'].get('venue', {}).get('name', '?')}")

# 1e. Missing players (injuries)
print("\n--- Arsenal Missing Players ---")
t0 = time.time()
missing = check(
    "get_missing_players(premier-league-2025)",
    football.get_missing_players(season_id="premier-league-2025"),
)
print(f"  Time: {time.time()-t0:.1f}s")
if missing.get("status"):
    teams = missing["data"].get("teams", [])
    arsenal_missing = next((t for t in teams if "arsenal" in t.get("team", {}).get("name", "").lower()), None)
    if arsenal_missing:
        players = arsenal_missing.get("players", [])
        print(f"  Arsenal missing/doubtful: {len(players)} players")
        for p in players[:5]:
            print(f"    - {p.get('name', '?')} ({p.get('status', '?')}): {p.get('news', '?')}")

# 1f. Season leaders
print("\n--- PL Season Leaders ---")
t0 = time.time()
leaders = check(
    "get_season_leaders(premier-league-2025)",
    football.get_season_leaders(season_id="premier-league-2025"),
    required_keys=["leaders"],
)
print(f"  Time: {time.time()-t0:.1f}s")
if leaders.get("status"):
    for l in leaders["data"]["leaders"][:5]:
        print(f"    {l.get('name', '?'):25s} {l.get('goals', '?'):>2} goals  ({l.get('team', {}).get('name', '?')})")


# ============================================================
# 2. POLYMARKET — Arsenal/Football prediction markets
# ============================================================
section("2. POLYMARKET — Sports Prediction Markets")

from sports_skills import polymarket

# 2a. Sports markets
print("\n--- Top Sports Markets ---")
t0 = time.time()
markets = check(
    "get_sports_markets(limit=10)",
    polymarket.get_sports_markets(limit=10),
    required_keys=["markets", "count"],
    min_items=1,
    data_key="markets",
)
print(f"  Time: {time.time()-t0:.1f}s")
if markets.get("status"):
    for m in markets["data"]["markets"][:5]:
        outcomes_str = " | ".join(
            f"{o['name']}: {o.get('price', '?')}" for o in m.get("outcomes", [])
        )
        print(f"    {m['question'][:60]:60s} [{outcomes_str}]")

# 2b. Search for Arsenal markets
print("\n--- Search: Arsenal Markets ---")
t0 = time.time()
arsenal_markets = check(
    "search_markets(query=arsenal)",
    polymarket.search_markets(query="arsenal", limit=10),
    required_keys=["markets"],
)
print(f"  Time: {time.time()-t0:.1f}s")
if arsenal_markets.get("status"):
    ams = arsenal_markets["data"]["markets"]
    print(f"  Found {len(ams)} Arsenal-related markets")
    for m in ams[:5]:
        outcomes_str = " | ".join(
            f"{o['name']}: {o.get('price', '?')}" for o in m.get("outcomes", [])
        )
        print(f"    {m['question'][:60]:60s} [{outcomes_str}]")

# 2c. Market types
print("\n--- Sports Market Types ---")
t0 = time.time()
types = check(
    "get_sports_market_types()",
    polymarket.get_sports_market_types(),
)
print(f"  Time: {time.time()-t0:.1f}s")


# ============================================================
# 3. KALSHI — Prediction market contracts
# ============================================================
section("3. KALSHI — Event Contracts")

from sports_skills import kalshi

# 3a. Exchange status
print("\n--- Exchange Status ---")
t0 = time.time()
status = check(
    "get_exchange_status()",
    kalshi.get_exchange_status(),
    required_keys=["exchange_active", "trading_active"],
)
print(f"  Time: {time.time()-t0:.1f}s")
if status.get("status"):
    d = status["data"]
    print(f"  Exchange active: {d['exchange_active']}")
    print(f"  Trading active: {d['trading_active']}")

# 3b. Sports filters
print("\n--- Sports Filters ---")
t0 = time.time()
filters = check(
    "get_sports_filters()",
    kalshi.get_sports_filters(),
    required_keys=["filters_by_sports"],
)
print(f"  Time: {time.time()-t0:.1f}s")
if filters.get("status"):
    sports = list(filters["data"]["filters_by_sports"].keys())
    print(f"  Sports available: {', '.join(sports[:10])}")

# 3c. Series list
print("\n--- Series List ---")
t0 = time.time()
series = check(
    "get_series_list()",
    kalshi.get_series_list(),
    required_keys=["series"],
)
print(f"  Time: {time.time()-t0:.1f}s")
if series.get("status"):
    s_list = series["data"]["series"]
    print(f"  Total series: {len(s_list)}")
    # Find sports-related series
    sports_series = [s for s in s_list if any(kw in s.get("title", "").lower() for kw in ["nba", "nfl", "mlb", "nhl", "soccer", "premier", "football"])]
    for s in sports_series[:8]:
        print(f"    {s.get('ticker', '?'):20s} {s.get('title', '?')}")

# 3d. Get NBA markets as example
print("\n--- NBA Markets (example) ---")
t0 = time.time()
nba = check(
    "get_events(series_ticker=KXNBA, limit=5)",
    kalshi.get_events(series_ticker="KXNBA", limit=5, status="open"),
)
print(f"  Time: {time.time()-t0:.1f}s")
if nba.get("status"):
    for e in nba["data"]["events"][:5]:
        print(f"    {e.get('event_ticker', '?'):30s} {e.get('title', '?')[:50]}")


# ============================================================
# 4. NEWS — Arsenal news coverage
# ============================================================
section("4. NEWS — Arsenal Coverage")

from sports_skills import news

# 4a. Google News search
print("\n--- Google News: Arsenal ---")
t0 = time.time()
arsenal_news = check(
    "fetch_items(google_news, query=Arsenal, limit=5)",
    news.fetch_items(google_news=True, query="Arsenal transfer news", limit=5),
    required_keys=["items", "count"],
    min_items=1,
    data_key="items",
)
print(f"  Time: {time.time()-t0:.1f}s")
if arsenal_news.get("status"):
    for item in arsenal_news["data"]["items"][:5]:
        print(f"    [{item.get('published_iso', '?')[:10]}] {item['title'][:70]}")

# 4b. BBC Sport RSS
print("\n--- BBC Sport Football ---")
t0 = time.time()
bbc = check(
    "fetch_items(url=BBC Sport Football, limit=5)",
    news.fetch_items(url="https://feeds.bbci.co.uk/sport/football/rss.xml", limit=5, sort_by_date=True),
    required_keys=["items", "count"],
    min_items=1,
    data_key="items",
)
print(f"  Time: {time.time()-t0:.1f}s")
if bbc.get("status"):
    for item in bbc["data"]["items"][:5]:
        print(f"    [{item.get('published_iso', '?')[:10]}] {item['title'][:70]}")


# ============================================================
# SUMMARY
# ============================================================
section("TEST SUMMARY")

total = PASS + FAIL
print(f"\n  Passed: {PASS}/{total}")
print(f"  Failed: {FAIL}/{total}")

if FAIL > 0:
    print(f"\n  Failed tests:")
    for label, r in RESULTS.items():
        if not r["ok"]:
            print(f"    - {label}: {'; '.join(r['issues'])}")

print(f"\n{'='*60}")
if FAIL == 0:
    print("  ALL TESTS PASSED")
else:
    print(f"  {FAIL} TEST(S) FAILED")
print(f"{'='*60}\n")

sys.exit(1 if FAIL > 0 else 0)
