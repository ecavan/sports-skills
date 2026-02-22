"""Textual TUI chat application for the sports agent.

Provides a polished terminal chat interface with:
- Streaming LLM responses (token-by-token)
- Tool call indicators
- ESC to quit, Ctrl+S to switch sport, Ctrl+M to switch model, Ctrl+B to toggle betting
"""

from __future__ import annotations

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Input, Static

from sports_skills.agent._agent import build_agent, stream_response
from sports_skills.agent._config import (
    MODELS,
    SPORT_LABELS,
    available_providers,
    load_config,
    model_display_name,
    save_config,
)


class ChatMessage(Static):
    """A single chat message widget."""

    pass


class ToolIndicator(Static):
    """Shows a tool call in progress."""

    DEFAULT_CSS = """
    ToolIndicator {
        color: $text-muted;
        padding: 0 2;
    }
    """


class SportsAgentApp(App):
    """Main sports agent chat application."""

    TITLE = "Sports Agent"

    CSS = """
    Screen {
        layout: vertical;
    }
    #status-bar {
        dock: top;
        height: 1;
        padding: 0 2;
        background: $primary;
        color: $text;
        text-style: bold;
    }
    #chat-log {
        height: 1fr;
        overflow-y: auto;
        padding: 1 2;
    }
    #user-input {
        dock: bottom;
        margin: 0 1;
    }
    .user-msg {
        padding: 0 2;
        margin: 1 0 0 0;
        color: $accent;
    }
    .assistant-msg {
        padding: 0 2;
        margin: 0 0 1 0;
    }
    .welcome-msg {
        padding: 1 2;
        color: $text-muted;
    }
    .system-msg {
        padding: 0 2;
        color: $success;
        text-style: italic;
    }
    """

    BINDINGS = [
        Binding("escape", "quit_app", "Quit", show=True),
        Binding("ctrl+s", "switch_sport", "Sport", show=True),
        Binding("ctrl+m", "switch_model", "Model", show=True),
        Binding("ctrl+b", "toggle_betting", "Betting", show=True),
    ]

    def __init__(
        self,
        sport: str,
        mode: str = "general",
        exchange: str | None = None,
    ) -> None:
        super().__init__()
        self.sport = sport
        self.mode = mode
        self.exchange = exchange
        self.agent = None
        self.history: list[tuple[str, str]] = []
        self._responding = False

    def compose(self) -> ComposeResult:
        yield Static(self._status_text(), id="status-bar")
        yield ScrollableContainer(id="chat-log")
        yield Input(placeholder=f"Ask about {SPORT_LABELS.get(self.sport, self.sport)}...", id="user-input")
        yield Footer()

    def on_mount(self) -> None:
        self._build_agent()
        chat_log = self.query_one("#chat-log")
        sport_name = SPORT_LABELS.get(self.sport, self.sport)
        mode_text = "betting analysis" if self.mode == "betting" else "scores, standings, and stats"
        welcome = f"Welcome! I'm focused on {sport_name} {mode_text}. Ask me anything."
        chat_log.mount(ChatMessage(welcome, classes="welcome-msg"))
        self.query_one("#user-input", Input).focus()

    def _status_text(self) -> str:
        config = load_config()
        model = model_display_name(config.get("model", "unknown"))
        sport_name = SPORT_LABELS.get(self.sport, self.sport)
        mode_text = " · Betting" if self.mode == "betting" else ""
        exchange_text = f" ({self.exchange.title()})" if self.exchange else ""
        return f"  Sports Agent  │  {sport_name}{mode_text}{exchange_text}  │  {model}"

    def _build_agent(self) -> None:
        config = load_config()
        self.agent = build_agent(config, self.sport, self.mode, self.exchange)
        self.history = []

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_text = event.value.strip()
        if not user_text:
            return
        event.input.clear()

        if self._responding:
            return

        # Handle slash commands
        if user_text.startswith("/"):
            await self._handle_slash(user_text)
            return

        # Add user message to chat
        chat_log = self.query_one("#chat-log")
        chat_log.mount(ChatMessage(f"[bold cyan]You:[/bold cyan] {user_text}", classes="user-msg"))

        # Stream the agent response
        self._stream_agent(user_text)

    @work(exclusive=True)
    async def _stream_agent(self, user_text: str) -> None:
        """Run the agent and stream tokens into the chat log."""
        self._responding = True
        chat_log = self.query_one("#chat-log")

        # Create placeholder for the assistant response
        response_widget = ChatMessage("", classes="assistant-msg")
        chat_log.mount(response_widget)

        full_response = ""

        try:
            async for event in stream_response(self.agent, user_text, self.history):
                etype = event["type"]

                if etype == "token":
                    full_response += event["content"]
                    response_widget.update(full_response)
                    chat_log.scroll_end(animate=False)

                elif etype == "tool_start":
                    indicator = ToolIndicator(f"  ▸ Calling {event['name']}...")
                    chat_log.mount(indicator, before=response_widget)
                    chat_log.scroll_end(animate=False)

                elif etype == "tool_end":
                    pass

                elif etype == "error":
                    response_widget.update(f"[red]Error: {event['message']}[/red]")

        except Exception as e:
            response_widget.update(f"[red]Error: {e}[/red]")

        # Save to history
        if full_response:
            self.history.append(("human", user_text))
            self.history.append(("assistant", full_response))

        self._responding = False
        chat_log.scroll_end(animate=False)

    async def _handle_slash(self, text: str) -> None:
        chat_log = self.query_one("#chat-log")
        cmd = text.lower().strip()

        if cmd in ("/help", "/h"):
            help_text = (
                "[bold]Commands:[/bold]\n"
                "  /help  — show this message\n"
                "  /clear — clear chat history\n"
                "  /config — show current config\n\n"
                "[bold]Shortcuts:[/bold]\n"
                "  ESC    — quit\n"
                "  Ctrl+S — switch sport\n"
                "  Ctrl+M — switch model\n"
                "  Ctrl+B — toggle betting mode"
            )
            chat_log.mount(ChatMessage(help_text, classes="welcome-msg"))
        elif cmd == "/clear":
            self.history = []
            chat_log.remove_children()
            chat_log.mount(ChatMessage("Chat cleared.", classes="welcome-msg"))
        elif cmd == "/config":
            config = load_config()
            info = (
                f"[bold]Sport:[/bold] {SPORT_LABELS.get(self.sport, self.sport)}\n"
                f"[bold]Mode:[/bold] {self.mode}\n"
                f"[bold]Exchange:[/bold] {self.exchange or 'None'}\n"
                f"[bold]Model:[/bold] {config.get('model', 'unknown')}"
            )
            chat_log.mount(ChatMessage(info, classes="welcome-msg"))
        else:
            chat_log.mount(ChatMessage(f"Unknown command: {cmd}. Type /help.", classes="welcome-msg"))

        chat_log.scroll_end(animate=False)

    def action_switch_sport(self) -> None:
        """Switch sport by relaunching the mode picker."""
        self.exit(result="switch")

    def action_switch_model(self) -> None:
        """Cycle to the next available model."""
        config = load_config()
        providers = available_providers(config)

        # Build flat list of available models
        all_models = []
        for provider in providers:
            for model_id, display in MODELS.get(provider, []):
                all_models.append((model_id, display))

        if len(all_models) < 2:
            return

        current = config.get("model", "")
        current_idx = next(
            (i for i, (mid, _) in enumerate(all_models) if mid == current),
            -1,
        )
        next_idx = (current_idx + 1) % len(all_models)

        new_model_id, new_display = all_models[next_idx]
        config["model"] = new_model_id
        save_config(config)

        self._build_agent()
        self.query_one("#status-bar", Static).update(self._status_text())

        chat_log = self.query_one("#chat-log")
        chat_log.mount(
            ChatMessage(f"Switched to [bold]{new_display}[/bold].", classes="system-msg")
        )
        chat_log.scroll_end(animate=False)

    def action_toggle_betting(self) -> None:
        """Toggle betting mode on/off."""
        if self.mode == "betting":
            self.mode = "general"
            self.exchange = None
        else:
            self.mode = "betting"

        # Save and rebuild
        config = load_config()
        config["last_mode"] = self.mode
        config["last_exchange"] = self.exchange
        save_config(config)

        self._build_agent()

        # Update UI
        self.query_one("#status-bar", Static).update(self._status_text())
        chat_log = self.query_one("#chat-log")
        chat_log.remove_children()
        mode_desc = "Betting mode enabled." if self.mode == "betting" else "General mode enabled."
        chat_log.mount(ChatMessage(mode_desc, classes="welcome-msg"))

    def action_quit_app(self) -> None:
        self.exit()
