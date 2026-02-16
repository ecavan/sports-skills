---
name: sports-news
description: |
  Sports news via RSS/Atom feeds and Google News. Fetch headlines, search by query, filter by date.

  Use when: user asks for recent news, headlines, transfer rumors, or articles about any sport. Good for "what's the latest on [team/player]" questions. Supports any Google News query and curated RSS feeds (BBC Sport, ESPN, The Athletic, Sky Sports).
  Don't use when: user asks for structured data like standings, scores, statistics, or xG — use football-data instead. Don't use for prediction market odds — use polymarket or kalshi. Don't use for F1 timing data — use fastf1. News results are text articles, not structured data.
triggers:
  - sports news
  - football news
  - transfer news
  - google news sports
  - rss feed
---

# Sports News

## Quick Start

```bash
npx skills add sports-skills
```

```python
from sports_skills import news

articles = news.fetch_items(google_news=True, query="Arsenal transfer news", limit=10)
feed = news.fetch_feed(url="https://feeds.bbci.co.uk/sport/football/rss.xml")
```

Or via CLI:
```bash
sports-skills news fetch_items --google_news --query="Arsenal transfer" --limit=5
sports-skills news fetch_feed --url="https://feeds.bbci.co.uk/sport/football/rss.xml"
```

## Commands

### fetch_feed
Fetch and parse a full RSS/Atom feed.
- `google_news` (bool, optional): Use Google News RSS. Default: false
- `query` (str): Search query (required if google_news=true)
- `url` (str): RSS feed URL (required if google_news=false)
- `language` (str, optional): Language code. Default: "en-US"
- `country` (str, optional): Country code. Default: "US"
- `after` (str, optional): Filter articles after date (YYYY-MM-DD)
- `before` (str, optional): Filter articles before date (YYYY-MM-DD)
- `sort_by_date` (bool, optional): Sort newest first. Default: false

### fetch_items
Fetch items from a feed, optionally limited by count.
- Same params as `fetch_feed`, plus:
- `limit` (int, optional): Max number of items to return

## Useful RSS Feeds

| Source | URL |
|--------|-----|
| BBC Sport Football | `https://feeds.bbci.co.uk/sport/football/rss.xml` |
| ESPN FC | `https://www.espn.com/espn/rss/soccer/news` |
| The Athletic | `https://theathletic.com/rss/` |
| Sky Sports Football | `https://www.skysports.com/rss/12040` |

## Google News Queries

Use `google_news=True` with `query` to search Google News:
- `"Arsenal transfer news"` — Arsenal transfer news
- `"Premier League results"` — latest PL results
- `"Champions League draw"` — CL draw coverage
- `"World Cup 2026"` — World Cup news
