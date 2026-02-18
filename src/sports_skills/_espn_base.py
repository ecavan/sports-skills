"""Shared ESPN HTTP infrastructure for US sports modules.

Provides caching, rate limiting, retry logic, and parameterized
ESPN API request functions. Used by nfl, nba, nhl, mlb, wnba modules.
"""

import gzip
import json
import logging
import time
import threading
import urllib.request
import urllib.error
import urllib.parse

logger = logging.getLogger("sports_skills._espn_base")


# ============================================================
# ESPN Status Map (common across all US sports)
# ============================================================

ESPN_STATUS_MAP = {
    "STATUS_SCHEDULED": "not_started",
    "STATUS_IN_PROGRESS": "live",
    "STATUS_HALFTIME": "halftime",
    "STATUS_FINAL": "closed",
    "STATUS_FULL_TIME": "closed",
    "STATUS_POSTPONED": "postponed",
    "STATUS_CANCELED": "cancelled",
    "STATUS_SUSPENDED": "suspended",
    "STATUS_END_PERIOD": "period_break",
    "STATUS_DELAYED": "delayed",
    "STATUS_RAIN_DELAY": "delayed",
    "STATUS_FIRST_HALF": "1st_half",
    "STATUS_SECOND_HALF": "2nd_half",
}


# ============================================================
# Module-Level Cache (TTL-based)
# ============================================================

_cache = {}
_cache_lock = threading.Lock()


def _cache_get(key):
    with _cache_lock:
        entry = _cache.get(key)
        if entry is None:
            return None
        value, expiry = entry
        if time.monotonic() > expiry:
            del _cache[key]
            return None
        return value


def _cache_set(key, value, ttl=300):
    with _cache_lock:
        if len(_cache) > 500:
            now = time.monotonic()
            expired = [k for k, (_, exp) in _cache.items() if now > exp]
            for k in expired:
                del _cache[k]
        _cache[key] = (value, time.monotonic() + ttl)


# ============================================================
# Rate Limiter (Token Bucket)
# ============================================================


class RateLimiter:
    def __init__(self, max_tokens=9, refill_rate=9.0 / 60.0):
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.refill_rate = refill_rate
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.max_tokens, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
            if self.tokens >= 1:
                self.tokens -= 1
                return
        time.sleep(max(0, (1 - self.tokens) / self.refill_rate))
        self.acquire()


_espn_rate_limiter = RateLimiter(max_tokens=2, refill_rate=2.0)


# ============================================================
# HTTP Helpers — Retry, Error Handling
# ============================================================

_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

_RETRYABLE_CODES = {429, 500, 502, 503, 504}

_MAX_RETRIES = 2
_RETRY_BASE_DELAY = 1.0
_RETRY_MAX_DELAY = 4.0


def _is_retryable(exc):
    """Check if an exception is worth retrying (transient failures only)."""
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in _RETRYABLE_CODES
    if isinstance(exc, (urllib.error.URLError, OSError, TimeoutError)):
        return True
    return False


def _http_fetch(
    url,
    headers=None,
    rate_limiter=None,
    timeout=30,
    max_retries=_MAX_RETRIES,
    decode_gzip=False,
):
    """Core HTTP fetch with retry + exponential backoff.

    Returns (data_bytes, None) on success or (None, error_dict) on failure.
    Only retries on transient errors (5xx, 429, timeouts, connection errors).
    Client errors (4xx except 429) fail immediately.
    """
    last_error = None
    for attempt in range(1 + max_retries):
        if rate_limiter:
            rate_limiter.acquire()
        req = urllib.request.Request(url)
        for key, value in (headers or {}).items():
            req.add_header(key, value)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                if decode_gzip and resp.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return raw, None
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode() if e.fp else ""
            except Exception:
                pass
            last_error = {"error": True, "status_code": e.code, "message": body}
            if not _is_retryable(e):
                logger.debug("HTTP %d (non-retryable) for %s", e.code, url)
                return None, last_error
            logger.debug(
                "HTTP %d (retryable, attempt %d/%d) for %s",
                e.code,
                attempt + 1,
                1 + max_retries,
                url,
            )
        except Exception as e:
            last_error = {"error": True, "message": str(e)}
            if not _is_retryable(e):
                logger.debug("Non-retryable error for %s: %s", url, e)
                return None, last_error
            logger.debug(
                "Retryable error (attempt %d/%d) for %s: %s",
                attempt + 1,
                1 + max_retries,
                url,
                e,
            )

        if attempt < max_retries:
            delay = min(_RETRY_BASE_DELAY * (2**attempt), _RETRY_MAX_DELAY)
            if isinstance(last_error, dict) and last_error.get("status_code") == 429:
                delay = min(delay * 2, _RETRY_MAX_DELAY * 2)
            time.sleep(delay)

    if max_retries > 0:
        logger.warning(
            "All %d attempts failed for %s: %s",
            1 + max_retries,
            url,
            last_error.get("message", ""),
        )
    else:
        logger.debug("Request failed for %s: %s", url, last_error.get("message", ""))
    return None, last_error


# ============================================================
# ESPN API Request Functions (parameterized by sport)
# ============================================================


def espn_request(sport_path, resource="scoreboard", params=None, max_retries=_MAX_RETRIES):
    """ESPN public site API request. Rate-limited and cached.

    Args:
        sport_path: e.g. "football/nfl", "basketball/nba", "hockey/nhl"
        resource: API resource, e.g. "scoreboard", "teams", "teams/12/roster"
        params: Optional query parameters dict.
        max_retries: Set to 0 for exploratory/probing requests.
    """
    cache_key = f"espn:{sport_path}:{resource}:{json.dumps(params or {}, sort_keys=True)}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached
    url = f"https://site.api.espn.com/apis/site/v2/sports/{sport_path}/{resource}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": _USER_AGENT}
    raw, err = _http_fetch(
        url, headers=headers, rate_limiter=_espn_rate_limiter, max_retries=max_retries
    )
    if err:
        return err
    try:
        data = json.loads(raw.decode())
        _cache_set(cache_key, data, ttl=120)
        return data
    except (json.JSONDecodeError, ValueError):
        return {"error": True, "message": "ESPN returned invalid JSON"}


def espn_web_request(sport_path, resource, params=None):
    """ESPN web API (standings, season lists). Different host from site API.

    Args:
        sport_path: e.g. "football/nfl", "basketball/nba"
        resource: API resource, e.g. "standings"
        params: Optional query parameters dict.
    """
    cache_key = f"espn_web:{sport_path}:{resource}:{json.dumps(params or {}, sort_keys=True)}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached
    url = f"https://site.web.api.espn.com/apis/v2/sports/{sport_path}/{resource}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": _USER_AGENT}
    raw, err = _http_fetch(url, headers=headers, rate_limiter=_espn_rate_limiter)
    if err:
        return err
    try:
        data = json.loads(raw.decode())
        _cache_set(cache_key, data, ttl=300)
        return data
    except (json.JSONDecodeError, ValueError):
        return {"error": True, "message": "ESPN web API returned invalid JSON"}


def espn_summary(sport_path, event_id, max_retries=_MAX_RETRIES):
    """ESPN game summary endpoint (box score, stats, play-by-play summary).

    Args:
        sport_path: e.g. "football/nfl", "basketball/nba"
        event_id: ESPN event ID.
        max_retries: Set to 0 for exploratory requests.

    Returns parsed JSON dict on success, None on failure.
    """
    if not event_id:
        return None
    cache_key = f"espn_summary:{sport_path}:{event_id}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached if cached else None
    url = (
        f"https://site.web.api.espn.com/apis/site/v2/sports/{sport_path}"
        f"/summary?event={event_id}"
    )
    headers = {"User-Agent": _USER_AGENT}
    raw, err = _http_fetch(
        url, headers=headers, rate_limiter=_espn_rate_limiter, max_retries=max_retries
    )
    if err:
        logger.debug(
            "ESPN summary failed for %s/%s: %s",
            sport_path,
            event_id,
            err.get("message", ""),
        )
        _cache_set(cache_key, {}, ttl=60)
        return None
    try:
        data = json.loads(raw.decode())
        _cache_set(cache_key, data, ttl=300)
        return data
    except (json.JSONDecodeError, ValueError):
        _cache_set(cache_key, {}, ttl=60)
        return None
