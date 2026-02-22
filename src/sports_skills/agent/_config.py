"""Config persistence for the sports agent.

Stores API keys, model preference, and last-used sport/mode settings
in ~/.config/sports-agent/config.json (XDG-compliant via platformdirs).
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

from platformdirs import user_config_dir

CONFIG_DIR = Path(user_config_dir("sports-agent"))
CONFIG_FILE = CONFIG_DIR / "config.json"

SPORTS = [
    "nfl", "nba", "wnba", "nhl", "mlb",
    "cfb", "cbb",
    "football", "golf", "tennis", "f1",
]

SPORT_LABELS = {
    "nfl": "NFL",
    "nba": "NBA",
    "wnba": "WNBA",
    "nhl": "NHL",
    "mlb": "MLB",
    "cfb": "College Football",
    "cbb": "College Basketball",
    "football": "Football (Soccer)",
    "golf": "Golf",
    "tennis": "Tennis",
    "f1": "Formula 1",
}

EXCHANGES = ["polymarket", "kalshi"]

MODELS = {
    "anthropic": [
        ("anthropic:claude-sonnet-4-20250514", "Claude Sonnet 4"),
        ("anthropic:claude-opus-4-0-20250514", "Claude Opus 4"),
    ],
    "openai": [
        ("openai:gpt-4o", "GPT-4o"),
        ("openai:gpt-4o-mini", "GPT-4o Mini"),
    ],
    "google": [
        ("google_genai:gemini-2.0-flash", "Gemini 2.0 Flash"),
        ("google_genai:gemini-2.5-pro", "Gemini 2.5 Pro"),
    ],
    "openrouter": [
        ("openrouter:mistralai/mistral-small-3.1-24b-instruct:free", "Mistral Small 3.1 24B (Free)"),
        ("openrouter:nvidia/nemotron-3-nano-30b-a3b:free", "Nemotron 3 Nano 30B (Free)"),
        ("openrouter:z-ai/glm-4.5-air:free", "GLM 4.5 Air (Free)"),
        ("openrouter:anthropic/claude-sonnet-4", "Claude Sonnet 4"),
        ("openrouter:anthropic/claude-haiku", "Claude Haiku"),
        ("openrouter:openai/gpt-4o", "GPT-4o"),
        ("openrouter:google/gemini-2.0-flash-001", "Gemini 2.0 Flash"),
    ],
}

PROVIDER_ENV_VARS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google": "GOOGLE_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}


def load_config() -> dict:
    """Load config from disk. Returns empty dict if not found."""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def save_config(config: dict) -> None:
    """Save config to disk with restricted permissions (owner-only)."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))
    os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)  # 0o600


def is_configured() -> bool:
    """Check if the agent has been set up (at least one API key)."""
    config = load_config()
    api_keys = config.get("api_keys", {})
    return any(api_keys.get(p) for p in PROVIDER_ENV_VARS)


def set_api_keys(config: dict) -> None:
    """Set API keys as environment variables for LangChain providers."""
    api_keys = config.get("api_keys", {})
    for provider, env_var in PROVIDER_ENV_VARS.items():
        key = api_keys.get(provider)
        if key:
            os.environ[env_var] = key


def available_providers(config: dict) -> list[str]:
    """Return providers that have API keys configured."""
    api_keys = config.get("api_keys", {})
    return [p for p in PROVIDER_ENV_VARS if api_keys.get(p)]


def model_display_name(model_id: str) -> str:
    """Return the human-readable display name for a model ID."""
    for provider_models in MODELS.values():
        for mid, display in provider_models:
            if mid == model_id:
                return display
    # Fallback: extract last meaningful part
    return model_id.split(":")[-1].split("/")[-1]
