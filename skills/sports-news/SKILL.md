---
name: sports-news
description: Sports news aggregation via RSS feeds and Google News. Fetch articles from any sports RSS feed or search Google News for sports topics. Filter by date range, language, and country. Use when the user asks about sports news, transfer rumors, match reports, press conferences, injury updates, or any sports journalism content. No API key required.
---

# Sports News

RSS and Atom feed aggregation for sports news. Supports any feed URL and Google News search queries. No API key required.

## Commands

### fetch_feed

Fetch a complete RSS/Atom feed with metadata and all entries.

```
Params:
  google_news (bool, optional, default: false) - Use Google News RSS
  query (string, required if google_news=true) - Google News search query
  url (string, required if google_news=false) - RSS feed URL
  language (string, optional, default: "en-US") - Language code for Google News
  country (string, optional, default: "US") - Country code for Google News
  after (string, optional) - Filter articles after date (YYYY-MM-DD)
  before (string, optional) - Filter articles before date (YYYY-MM-DD)
  sort_by_date (bool, optional, default: false) - Sort newest first
Returns: {
  title, subtitle, link, language, updated,
  entries: [{
    title, link, id, published, published_iso,
    author, summary, content, tags
  }]
}
```

### fetch_items

Fetch feed items with optional count limit and date filtering.

```
Params:
  (all params from fetch_feed, plus:)
  limit (int, optional) - Max number of items to return
Returns: {
  items: [...same structure as entries above...],
  count, query, url
}
```

## Google News Queries

When `google_news=true`, the connector builds a Google News RSS URL from the query. Useful queries for sports:

- `"Premier League transfer news"` - Transfer rumors and deals
- `"NFL injuries week 10"` - Injury reports
- `"Champions League results"` - Match results
- `"F1 race results 2026"` - Formula 1 news
- `"NBA free agency"` - Basketball transactions
- `"World Cup 2026"` - World Cup coverage

Combine with `after` and `before` date filters to narrow results.

## Popular Sports RSS Feeds

| Source | Feed URL | Coverage |
|--------|----------|----------|
| ESPN | `https://www.espn.com/espn/rss/news` | General sports |
| ESPN Soccer | `https://www.espn.com/espn/rss/soccer/news` | Football/soccer |
| ESPN NFL | `https://www.espn.com/espn/rss/nfl/news` | NFL |
| ESPN NBA | `https://www.espn.com/espn/rss/nba/news` | NBA |
| BBC Sport | `https://feeds.bbci.co.uk/sport/rss.xml` | UK sports |
| BBC Football | `https://feeds.bbci.co.uk/sport/football/rss.xml` | Football |
| The Athletic | `https://theathletic.com/rss/` | Multi-sport premium |
| Sky Sports | `https://www.skysports.com/rss/12040` | UK sports |
| Guardian Football | `https://www.theguardian.com/football/rss` | Football |

## Response Format

All commands return:

```json
{
  "status": true,
  "data": { ... },
  "message": "Error description (on failure only)"
}
```

## Usage Examples

Get latest sports news:
> "What's the latest Premier League news?"
> Uses: fetch_items with google_news=true, query="Premier League news", limit=10

Get transfer rumors:
> "Any transfer news from the last 3 days?"
> Uses: fetch_items with google_news=true, query="football transfer news", after="2026-02-12"

Read a specific feed:
> "Get the latest from BBC Sport"
> Uses: fetch_feed with url="https://feeds.bbci.co.uk/sport/rss.xml"

World Cup coverage:
> "Find World Cup 2026 news articles"
> Uses: fetch_items with google_news=true, query="World Cup 2026", sort_by_date=true
