---
name: sports-news
description: |
  Sports news via RSS/Atom feeds and Google News. Fetch headlines, search by query, filter by date. Covers football news, transfer rumors, match reports, and any sport via Google News.

  Use when: user asks for recent news, headlines, transfer rumors, or articles about any sport. Good for "what's the latest on [team/player]" questions. Supports any Google News query and curated RSS feeds (BBC Sport, ESPN, The Athletic, Sky Sports).
  Don't use when: user asks for structured data like standings, scores, statistics, or xG — use football-data instead. Don't use for prediction market odds — use polymarket or kalshi. Don't use for F1 timing data — use fastf1. News results are text articles, not structured data.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# Sports News

## Setup

Before first use, check if the CLI is available:
```bash
which sports-skills || pip install sports-skills
```
If `pip install` fails with a Python version error, the package requires Python 3.10+. Find a compatible Python:
```bash
python3 --version  # check version
# If < 3.10, try: python3.12 -m pip install sports-skills
# On macOS with Homebrew: /opt/homebrew/bin/python3.12 -m pip install sports-skills
```
No API keys required.

## Quick Start

Prefer the CLI — it avoids Python import path issues:
```bash
sports-skills news fetch_items --google_news --query="Arsenal transfer" --limit=5
sports-skills news fetch_feed --url="https://feeds.bbci.co.uk/sport/football/rss.xml"
```

Python SDK (alternative):
```python
from sports_skills import news

articles = news.fetch_items(google_news=True, query="Arsenal transfer news", limit=10)
feed = news.fetch_feed(url="https://feeds.bbci.co.uk/sport/football/rss.xml")
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

## Examples

User: "What's the latest Arsenal transfer news?"
1. Call `fetch_items(google_news=True, query="Arsenal transfer news", limit=10)`
2. Present headlines with source, date, and links

User: "Show me BBC Sport football headlines"
1. Call `fetch_feed(url="https://feeds.bbci.co.uk/sport/football/rss.xml")`
2. Present feed title, last updated, and recent entries

User: "Any Champions League news from this week?"
1. Call `fetch_items(google_news=True, query="Champions League", after="2026-02-09", sort_by_date=True, limit=10)`
2. Present articles filtered to the last 7 days, sorted newest first

## Troubleshooting

- **`sports-skills` command not found**: Package not installed. Run `pip install sports-skills`. If pip fails with a Python version error, you need Python 3.10+ — see Setup section.
- **`ModuleNotFoundError: No module named 'sports_skills'`**: Same as above — install the package. Prefer the CLI over Python imports to avoid path issues.
- **No results from Google News**: Ensure `google_news=True` is set AND `query` is provided. Without `query`, Google News has nothing to search.
- **RSS feed returns error**: Some feeds may block automated requests or be temporarily down. Use Google News as a fallback.
- **Old articles appearing**: Use the `after` parameter (YYYY-MM-DD) to filter to recent articles. Combine with `sort_by_date=True`.
- **Non-English results**: Set `language` (e.g., "pt-BR") and `country` (e.g., "BR") for localized Google News results.
