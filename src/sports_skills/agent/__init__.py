"""Sports Agent — a standalone terminal chat agent for sports data.

Install: pip install sports-skills[agent]
Run: sports-agent
"""

from __future__ import annotations


def main() -> None:
    """Entry point for the sports-agent command."""
    from sports_skills.agent._config import is_configured
    from sports_skills.agent._setup import run_mode_picker, run_setup_wizard

    # First-run setup if not configured
    if not is_configured():
        run_setup_wizard()

    # If still not configured after wizard (user cancelled), exit
    if not is_configured():
        return

    # Mode picker loop — allows switching sports via Ctrl+S
    while True:
        selection = run_mode_picker()
        if selection is None:
            break

        sport = selection["sport"]
        mode = selection["mode"]
        exchange = selection.get("exchange")

        # Launch the chat TUI
        from sports_skills.agent._tui import SportsAgentApp

        app = SportsAgentApp(sport=sport, mode=mode, exchange=exchange)
        result = app.run()

        # If user pressed Ctrl+S (switch), loop back to mode picker
        if result != "switch":
            break
