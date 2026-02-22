"""First-run setup wizard and mode picker for the sports agent.

Uses Textual for terminal UI screens:
- SetupWizard: API key entry + model selection (first run only)
- ModePicker: Sport + mode selection (every launch)
"""

from __future__ import annotations

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    RadioButton,
    RadioSet,
    Static,
)

from sports_skills.agent._config import (
    MODELS,
    SPORT_LABELS,
    SPORTS,
    load_config,
    save_config,
)

# ---------------------------------------------------------------------------
# Setup Wizard (first run) — API key + model
# ---------------------------------------------------------------------------


class ApiKeyScreen(Screen):
    """Screen for entering API keys."""

    CSS = """
    ApiKeyScreen {
        align: center middle;
    }
    #key-form {
        width: 70;
        height: auto;
        padding: 2 4;
        border: thick $accent;
        background: $surface;
    }
    .key-label {
        margin-top: 1;
    }
    .key-input {
        margin-bottom: 1;
    }
    #key-error {
        color: $error;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Vertical(id="key-form"):
            yield Static("Welcome to Sports Agent!", classes="title")
            yield Static("Enter at least one API key to get started.\n")
            yield Label("Anthropic API Key:", classes="key-label")
            yield Input(placeholder="sk-ant-...", id="key-anthropic", password=True, classes="key-input")
            yield Label("OpenAI API Key:", classes="key-label")
            yield Input(placeholder="sk-...", id="key-openai", password=True, classes="key-input")
            yield Label("Google API Key:", classes="key-label")
            yield Input(placeholder="AIza...", id="key-google", password=True, classes="key-input")
            yield Label("OpenRouter API Key:", classes="key-label")
            yield Input(placeholder="sk-or-v1-...", id="key-openrouter", password=True, classes="key-input")
            yield Static("", id="key-error")
            yield Button("Continue →", id="btn-keys", variant="primary")
        yield Footer()

    @on(Button.Pressed, "#btn-keys")
    def on_continue(self) -> None:
        anthropic = self.query_one("#key-anthropic", Input).value.strip()
        openai = self.query_one("#key-openai", Input).value.strip()
        google = self.query_one("#key-google", Input).value.strip()
        openrouter = self.query_one("#key-openrouter", Input).value.strip()

        if not any([anthropic, openai, google, openrouter]):
            self.query_one("#key-error", Static).update("Please enter at least one API key.")
            return

        api_keys = {}
        if anthropic:
            api_keys["anthropic"] = anthropic
        if openai:
            api_keys["openai"] = openai
        if google:
            api_keys["google"] = google
        if openrouter:
            api_keys["openrouter"] = openrouter

        self.app._api_keys = api_keys
        self.app.push_screen(ModelScreen())


class ModelScreen(Screen):
    """Screen for selecting the LLM model."""

    CSS = """
    ModelScreen {
        align: center middle;
    }
    #model-form {
        width: 70;
        height: auto;
        padding: 2 4;
        border: thick $accent;
        background: $surface;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Vertical(id="model-form"):
            yield Static("Select your AI model:\n")
            providers = list(self.app._api_keys.keys())
            with RadioSet(id="model-radios"):
                first = True
                for provider in providers:
                    models = MODELS.get(provider, [])
                    for model_id, display_name in models:
                        yield RadioButton(f"{display_name} ({provider})", value=first, name=model_id)
                        first = False
            yield Button("Continue →", id="btn-model", variant="primary")
        yield Footer()

    @on(Button.Pressed, "#btn-model")
    def on_continue(self) -> None:
        radio_set = self.query_one("#model-radios", RadioSet)
        if radio_set.pressed_button:
            model_id = radio_set.pressed_button.name
        else:
            # Default to first available
            providers = list(self.app._api_keys.keys())
            model_id = MODELS[providers[0]][0][0]

        config = load_config()
        config["api_keys"] = self.app._api_keys
        config["model"] = model_id
        save_config(config)

        self.app.exit(result="setup_complete")


class SetupWizard(App):
    """First-run setup wizard."""

    TITLE = "Sports Agent Setup"

    _api_keys: dict = {}

    def on_mount(self) -> None:
        self.push_screen(ApiKeyScreen())


# ---------------------------------------------------------------------------
# Mode Picker (every launch)
# ---------------------------------------------------------------------------


class ModePickerScreen(Screen):
    """Screen for selecting sport, mode, and exchange."""

    CSS = """
    ModePickerScreen {
        align: center middle;
    }
    #picker-form {
        width: 80;
        height: auto;
        max-height: 90%;
        padding: 2 4;
        border: thick $accent;
        background: $surface;
    }
    .section-title {
        text-style: bold;
        margin-top: 1;
    }
    #sport-list {
        height: auto;
        max-height: 15;
    }
    #mode-radios {
        height: auto;
    }
    #exchange-section {
        height: auto;
    }
    .hidden {
        display: none;
    }
    """

    def compose(self) -> ComposeResult:
        config = load_config()
        last_sport = config.get("last_sport", "nba")
        last_mode = config.get("last_mode", "general")

        yield Header(show_clock=False)
        with VerticalScroll(id="picker-form"):
            yield Static("Sports Agent", classes="title")
            yield Static("")

            yield Label("Pick a sport:", classes="section-title")
            with RadioSet(id="sport-radios"):
                for sport_key in SPORTS:
                    label = SPORT_LABELS.get(sport_key, sport_key)
                    yield RadioButton(label, value=(sport_key == last_sport), name=sport_key)

            yield Label("Pick a purpose:", classes="section-title")
            with RadioSet(id="mode-radios"):
                yield RadioButton("General — scores, standings, stats, news", value=(last_mode == "general"), name="general")
                yield RadioButton("Betting — odds, futures, injury edges", value=(last_mode == "betting"), name="betting")

            with Vertical(id="exchange-section", classes="" if last_mode == "betting" else "hidden"):
                yield Label("Also use a prediction exchange?", classes="section-title")
                with RadioSet(id="exchange-radios"):
                    yield RadioButton("No — just ESPN Bet odds", value=True, name="none")
                    yield RadioButton("Polymarket", name="polymarket")
                    yield RadioButton("Kalshi", name="kalshi")

            yield Static("")
            yield Button("Start chatting →", id="btn-start", variant="primary")
        yield Footer()

    @on(RadioSet.Changed, "#mode-radios")
    def on_mode_changed(self, event: RadioSet.Changed) -> None:
        exchange_section = self.query_one("#exchange-section")
        if event.pressed.name == "betting":
            exchange_section.remove_class("hidden")
        else:
            exchange_section.add_class("hidden")

    @on(Button.Pressed, "#btn-start")
    def on_start(self) -> None:
        # Get selected sport
        sport_radios = self.query_one("#sport-radios", RadioSet)
        sport = "nba"
        if sport_radios.pressed_button:
            sport = sport_radios.pressed_button.name

        # Get selected mode
        mode_radios = self.query_one("#mode-radios", RadioSet)
        mode = "general"
        if mode_radios.pressed_button:
            mode = mode_radios.pressed_button.name

        # Get selected exchange (only if betting mode)
        exchange = None
        if mode == "betting":
            exchange_radios = self.query_one("#exchange-radios", RadioSet)
            if exchange_radios.pressed_button:
                ex = exchange_radios.pressed_button.name
                if ex != "none":
                    exchange = ex

        # Save last-used settings
        config = load_config()
        config["last_sport"] = sport
        config["last_mode"] = mode
        config["last_exchange"] = exchange
        save_config(config)

        self.app.exit(result={"sport": sport, "mode": mode, "exchange": exchange})


class ModePicker(App):
    """Mode picker app shown on every launch."""

    TITLE = "Sports Agent"

    def on_mount(self) -> None:
        self.push_screen(ModePickerScreen())


def run_setup_wizard() -> None:
    """Run the first-run setup wizard. Blocks until complete."""
    app = SetupWizard()
    app.run()


def run_mode_picker() -> dict | None:
    """Run the mode picker. Returns {sport, mode, exchange} or None if cancelled."""
    app = ModePicker()
    result = app.run()
    return result
