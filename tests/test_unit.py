"""Unit tests for pure data transformation and internal logic."""

import time
import urllib.error

from sports_skills._espn_base import (
    ESPN_STATUS_MAP,
    _cache_get,
    _cache_set,
    _is_retryable,
    normalize_odds,
)
from sports_skills._response import error, success, wrap

# ── normalize_odds ─────────────────────────────────────────────


class TestNormalizeOdds:
    """Tests for the shared ESPN odds normalizer."""

    def test_empty_list_returns_none(self):
        assert normalize_odds([]) is None

    def test_none_input_returns_none(self):
        assert normalize_odds(None) is None

    def test_two_way_moneyline(self):
        """Standard US sport odds — home/away only, no draw."""
        odds = [
            {
                "provider": {"name": "Draft Kings"},
                "details": "BOS -6.5",
                "overUnder": 220.5,
                "spread": 6.5,
                "moneyline": {
                    "home": {"close": {"odds": "-280"}},
                    "away": {"close": {"odds": "+220"}},
                },
                "pointSpread": {
                    "home": {"close": {"line": "-6.5", "odds": "-110"}},
                    "away": {"close": {"line": "+6.5", "odds": "-110"}},
                },
                "total": {
                    "over": {"close": {"line": "o220.5", "odds": "-110"}},
                    "under": {"close": {"line": "u220.5", "odds": "-110"}},
                },
                "homeTeamOdds": {"favorite": True},
                "awayTeamOdds": {},
            }
        ]
        result = normalize_odds(odds)

        assert result["provider"] == "Draft Kings"
        assert result["details"] == "BOS -6.5"
        assert result["over_under"] == 220.5
        assert result["favorite"] == "home"
        assert result["moneyline"]["home"] == "-280"
        assert result["moneyline"]["away"] == "+220"
        assert "draw" not in result["moneyline"]
        assert result["spread_line"]["home"]["line"] == "-6.5"
        assert result["total"]["over"]["line"] == "o220.5"

    def test_three_way_moneyline_soccer(self):
        """Soccer odds include draw in moneyline."""
        odds = [
            {
                "provider": {"name": "Draft Kings"},
                "details": "ATH -145",
                "overUnder": 2.5,
                "spread": "",
                "moneyline": {
                    "home": {"open": {"odds": "-170"}, "close": {"odds": "-145"}},
                    "away": {"open": {"odds": "+450"}, "close": {"odds": "+425"}},
                    "draw": {"open": {"odds": "+285"}, "close": {"odds": "+280"}},
                },
                "pointSpread": {},
                "total": {},
                "homeTeamOdds": {},
                "awayTeamOdds": {},
            }
        ]
        result = normalize_odds(odds)

        assert result["moneyline"]["home"] == "-145"
        assert result["moneyline"]["away"] == "+425"
        assert result["moneyline"]["draw"] == "+280"

    def test_opening_lines_included(self):
        """Opening lines should populate the 'open' sub-dict."""
        odds = [
            {
                "provider": {"name": "Draft Kings"},
                "details": "",
                "moneyline": {
                    "home": {"open": {"odds": "-250"}, "close": {"odds": "-280"}},
                    "away": {"open": {"odds": "+200"}, "close": {"odds": "+220"}},
                },
                "pointSpread": {
                    "home": {"open": {"line": "-6.0"}, "close": {"line": "-6.5"}},
                    "away": {"open": {"line": "+6.0"}, "close": {"line": "+6.5"}},
                },
                "total": {
                    "over": {"open": {"line": "o219.5"}, "close": {"line": "o220.5"}},
                    "under": {"close": {"line": "u220.5"}},
                },
                "homeTeamOdds": {},
                "awayTeamOdds": {},
            }
        ]
        result = normalize_odds(odds)

        assert result["open"]["moneyline"]["home"] == "-250"
        assert result["open"]["moneyline"]["away"] == "+200"
        assert result["open"]["spread"]["home"] == "-6.0"
        assert result["open"]["total"] == "o219.5"

    def test_opening_draw_lines(self):
        """Soccer opening lines should include draw when present."""
        odds = [
            {
                "provider": {"name": "Draft Kings"},
                "details": "",
                "moneyline": {
                    "home": {"open": {"odds": "-170"}, "close": {"odds": "-145"}},
                    "away": {"open": {"odds": "+450"}, "close": {"odds": "+425"}},
                    "draw": {"open": {"odds": "+285"}, "close": {"odds": "+280"}},
                },
                "pointSpread": {},
                "total": {},
                "homeTeamOdds": {},
                "awayTeamOdds": {},
            }
        ]
        result = normalize_odds(odds)

        assert result["open"]["moneyline"]["draw"] == "+285"

    def test_away_favorite(self):
        odds = [
            {
                "provider": {"name": "DK"},
                "details": "",
                "moneyline": {},
                "pointSpread": {},
                "total": {},
                "homeTeamOdds": {},
                "awayTeamOdds": {"favorite": True},
            }
        ]
        result = normalize_odds(odds)
        assert result["favorite"] == "away"

    def test_no_favorite(self):
        odds = [
            {
                "provider": {"name": "DK"},
                "details": "",
                "moneyline": {},
                "pointSpread": {},
                "total": {},
                "homeTeamOdds": {},
                "awayTeamOdds": {},
            }
        ]
        result = normalize_odds(odds)
        assert result["favorite"] is None

    def test_missing_nested_keys_default_empty(self):
        """Deeply nested missing keys should not raise — they default to empty strings."""
        odds = [{"provider": {}, "moneyline": {"home": {}}, "pointSpread": {}, "total": {}}]
        result = normalize_odds(odds)
        assert result["provider"] == ""
        assert result["moneyline"]["home"] == ""


# ── _response ──────────────────────────────────────────────────


class TestResponse:
    def test_success_envelope(self):
        r = success({"key": "val"}, message="ok")
        assert r == {"status": True, "data": {"key": "val"}, "message": "ok"}

    def test_error_envelope(self):
        r = error("broke", data={"debug": 1})
        assert r == {"status": False, "data": {"debug": 1}, "message": "broke"}

    def test_wrap_passthrough(self):
        """Already-formatted responses pass through unchanged."""
        envelope = {"status": True, "data": [1, 2], "message": ""}
        assert wrap(envelope) is envelope

    def test_wrap_error_dict(self):
        r = wrap({"error": True, "message": "timeout"})
        assert r["status"] is False
        assert r["message"] == "timeout"

    def test_wrap_plain_dict(self):
        r = wrap({"goals": 3})
        assert r["status"] is True
        assert r["data"] == {"goals": 3}

    def test_wrap_non_dict(self):
        r = wrap([1, 2, 3])
        assert r["status"] is True
        assert r["data"] == [1, 2, 3]


# ── Cache ──────────────────────────────────────────────────────


class TestCache:
    def test_set_and_get(self):
        _cache_set("test_key_1", "hello", ttl=60)
        assert _cache_get("test_key_1") == "hello"

    def test_miss_returns_none(self):
        assert _cache_get("nonexistent_key_xyz") is None

    def test_expired_entry_returns_none(self):
        _cache_set("test_key_expire", "val", ttl=0)
        time.sleep(0.01)
        assert _cache_get("test_key_expire") is None


# ── _is_retryable ─────────────────────────────────────────────


class TestIsRetryable:
    def test_429_is_retryable(self):
        exc = urllib.error.HTTPError("url", 429, "rate limited", {}, None)
        assert _is_retryable(exc) is True

    def test_500_is_retryable(self):
        exc = urllib.error.HTTPError("url", 500, "server error", {}, None)
        assert _is_retryable(exc) is True

    def test_404_is_not_retryable(self):
        exc = urllib.error.HTTPError("url", 404, "not found", {}, None)
        assert _is_retryable(exc) is False

    def test_timeout_is_retryable(self):
        assert _is_retryable(TimeoutError()) is True

    def test_os_error_is_retryable(self):
        assert _is_retryable(OSError("conn reset")) is True

    def test_value_error_is_not_retryable(self):
        assert _is_retryable(ValueError("bad")) is False


# ── ESPN_STATUS_MAP ────────────────────────────────────────────


class TestStatusMap:
    def test_scheduled_maps_to_not_started(self):
        assert ESPN_STATUS_MAP["STATUS_SCHEDULED"] == "not_started"

    def test_final_maps_to_closed(self):
        assert ESPN_STATUS_MAP["STATUS_FINAL"] == "closed"

    def test_in_progress_maps_to_live(self):
        assert ESPN_STATUS_MAP["STATUS_IN_PROGRESS"] == "live"


# ── CLI _parse_value ───────────────────────────────────────────


class TestParseValue:
    def test_int_param(self):
        from sports_skills.cli import _parse_value

        assert _parse_value("limit", "25") == 25
        assert _parse_value("season", "2024") == 2024

    def test_bool_param_string(self):
        from sports_skills.cli import _parse_value

        assert _parse_value("active", "true") is True
        assert _parse_value("active", "false") is False

    def test_bool_param_already_bool(self):
        from sports_skills.cli import _parse_value

        assert _parse_value("active", True) is True

    def test_list_param(self):
        from sports_skills.cli import _parse_value

        result = _parse_value("token_ids", "abc, def, ghi")
        assert result == ["abc", "def", "ghi"]

    def test_plain_string_passthrough(self):
        from sports_skills.cli import _parse_value

        assert _parse_value("team_id", "BOS") == "BOS"
