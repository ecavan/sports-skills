"""Tests for the sports agent tool loading system."""

from __future__ import annotations

import pytest

from sports_skills.agent.tools import load_tools

# Expected tool counts per sport module
SPORT_TOOL_COUNTS = {
    "nfl": 17,
    "nba": 17,
    "wnba": 16,
    "nhl": 15,
    "mlb": 16,
    "cfb": 14,
    "cbb": 14,
    "football": 22,
    "golf": 6,
    "tennis": 5,
    "f1": 13,
}

NEWS_TOOL_COUNT = 2
POLYMARKET_TOOL_COUNT = 11
KALSHI_TOOL_COUNT = 11


@pytest.mark.parametrize("sport,expected_count", list(SPORT_TOOL_COUNTS.items()))
def test_sport_tools_load(sport: str, expected_count: int) -> None:
    """Each sport module loads the correct number of tools."""
    from sports_skills.agent.tools import _import_sport_tools

    tools = _import_sport_tools(sport)
    assert len(tools) == expected_count, (
        f"{sport}: expected {expected_count} tools, got {len(tools)}"
    )


def test_news_tools_load() -> None:
    from sports_skills.agent.tools import _import_sport_tools

    tools = _import_sport_tools("news")
    assert len(tools) == NEWS_TOOL_COUNT


def test_polymarket_tools_load() -> None:
    from sports_skills.agent.tools import _import_sport_tools

    tools = _import_sport_tools("polymarket")
    assert len(tools) == POLYMARKET_TOOL_COUNT


def test_kalshi_tools_load() -> None:
    from sports_skills.agent.tools import _import_sport_tools

    tools = _import_sport_tools("kalshi")
    assert len(tools) == KALSHI_TOOL_COUNT


@pytest.mark.parametrize("sport", list(SPORT_TOOL_COUNTS.keys()))
def test_load_tools_general_mode(sport: str) -> None:
    """General mode loads sport + news tools."""
    tools = load_tools(sport, mode="general")
    expected = SPORT_TOOL_COUNTS[sport] + NEWS_TOOL_COUNT
    assert len(tools) == expected, (
        f"{sport} general: expected {expected} tools, got {len(tools)}"
    )


@pytest.mark.parametrize("sport", list(SPORT_TOOL_COUNTS.keys()))
def test_load_tools_betting_no_exchange(sport: str) -> None:
    """Betting mode without exchange = same as general (sport + news)."""
    tools = load_tools(sport, mode="betting")
    expected = SPORT_TOOL_COUNTS[sport] + NEWS_TOOL_COUNT
    assert len(tools) == expected


def test_load_tools_betting_polymarket() -> None:
    """Betting + Polymarket loads sport + news + polymarket."""
    tools = load_tools("nba", mode="betting", exchange="polymarket")
    expected = SPORT_TOOL_COUNTS["nba"] + NEWS_TOOL_COUNT + POLYMARKET_TOOL_COUNT
    assert len(tools) == expected


def test_load_tools_betting_kalshi() -> None:
    """Betting + Kalshi loads sport + news + kalshi."""
    tools = load_tools("nba", mode="betting", exchange="kalshi")
    expected = SPORT_TOOL_COUNTS["nba"] + NEWS_TOOL_COUNT + KALSHI_TOOL_COUNT
    assert len(tools) == expected


def test_load_tools_betting_both_exchanges() -> None:
    """Betting + both exchanges loads sport + news + polymarket + kalshi."""
    tools = load_tools("nba", mode="betting", exchange="both")
    expected = (
        SPORT_TOOL_COUNTS["nba"]
        + NEWS_TOOL_COUNT
        + POLYMARKET_TOOL_COUNT
        + KALSHI_TOOL_COUNT
    )
    assert len(tools) == expected


def test_all_tools_have_names() -> None:
    """Every tool has a valid name attribute."""
    tools = load_tools("nfl", mode="betting", exchange="both")
    for t in tools:
        assert hasattr(t, "name"), f"Tool missing name: {t}"
        assert t.name, f"Tool has empty name: {t}"


def test_no_duplicate_tool_names() -> None:
    """No duplicate tool names within a full tool set."""
    tools = load_tools("nfl", mode="betting", exchange="both")
    names = [t.name for t in tools]
    assert len(names) == len(set(names)), (
        f"Duplicate tool names: {[n for n in names if names.count(n) > 1]}"
    )


def test_tool_names_prefixed() -> None:
    """Sport tools should be prefixed with sport name."""
    from sports_skills.agent.tools import _import_sport_tools

    for sport in SPORT_TOOL_COUNTS:
        tools = _import_sport_tools(sport)
        for t in tools:
            assert t.name.startswith(f"{sport}_"), (
                f"Tool {t.name} in {sport}.py should start with '{sport}_'"
            )
