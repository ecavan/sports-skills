"""Tool loader for the sports agent.

Loads the right set of LangChain tools based on the user's
selected sport, mode, and exchange preference.
"""

from __future__ import annotations

import importlib


def _import_sport_tools(module_name: str) -> list:
    """Import ALL_TOOLS from a tool module by name."""
    try:
        mod = importlib.import_module(f"sports_skills.agent.tools.{module_name}")
        return list(mod.ALL_TOOLS)
    except ImportError:
        return []


def load_tools(
    sport: str,
    mode: str = "general",
    exchange: str | None = None,
) -> list:
    """Load LangChain tools for the selected sport and mode.

    Args:
        sport: Sport module name (e.g., "nba", "nfl", "football").
        mode: "general" or "betting".
        exchange: "polymarket", "kalshi", or None. Only used in betting mode.

    Returns:
        List of LangChain tool objects.
    """
    # Always load the sport's tools + news
    tools = _import_sport_tools(sport) + _import_sport_tools("news")

    # In betting mode, optionally add exchange tools
    if mode == "betting" and exchange:
        if exchange in ("polymarket", "both"):
            tools += _import_sport_tools("polymarket")
        if exchange in ("kalshi", "both"):
            tools += _import_sport_tools("kalshi")

    return tools
