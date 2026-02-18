"""sports-skills: Lightweight Python SDK for sports data."""

__version__ = "0.2.0"

from sports_skills import football, polymarket, kalshi, news, nfl, nba, wnba, nhl

# F1 is optional — requires fastf1 + pandas
try:
    from sports_skills import f1
except ImportError:
    f1 = None

__all__ = ["football", "f1", "polymarket", "kalshi", "news", "nfl", "nba", "wnba", "nhl"]
