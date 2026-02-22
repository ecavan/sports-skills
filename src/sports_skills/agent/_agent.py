"""LangGraph agent construction and streaming for the sports agent."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from sports_skills.agent._config import set_api_keys
from sports_skills.agent._prompts import build_system_prompt
from sports_skills.agent.tools import load_tools

if TYPE_CHECKING:
    from langgraph.graph.graph import CompiledGraph


def build_agent(
    config: dict,
    sport: str,
    mode: str = "general",
    exchange: str | None = None,
) -> CompiledGraph:
    """Build a LangGraph ReAct agent for the given sport and mode.

    Args:
        config: User config dict (api_keys, model, etc.).
        sport: Active sport module name.
        mode: "general" or "betting".
        exchange: "polymarket", "kalshi", or None.

    Returns:
        A compiled LangGraph agent ready for streaming.
    """
    from langchain.chat_models import init_chat_model
    from langgraph.prebuilt import create_react_agent

    # Set API keys in environment for LangChain providers
    set_api_keys(config)

    # Initialize LLM
    model_id = config.get("model", "anthropic:claude-sonnet-4-20250514")

    if model_id.startswith("openrouter:"):
        # OpenRouter uses OpenAI-compatible API with a custom base URL
        from langchain_openai import ChatOpenAI

        openrouter_model = model_id.removeprefix("openrouter:")
        api_key = config.get("api_keys", {}).get("openrouter", "")
        llm = ChatOpenAI(
            model=openrouter_model,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
    else:
        llm = init_chat_model(model_id)

    # Load tools for the selected sport + mode
    tools = load_tools(sport, mode, exchange)

    # Build system prompt
    system_prompt = build_system_prompt(sport, mode, exchange)

    # Create the ReAct agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt,
    )

    return agent


async def stream_response(
    agent: CompiledGraph,
    user_message: str,
    history: list,
) -> AsyncIterator[dict]:
    """Stream agent response events.

    Yields dicts with one of:
        {"type": "token", "content": "..."}
        {"type": "tool_start", "name": "..."}
        {"type": "tool_end", "name": "..."}
        {"type": "error", "message": "..."}

    Args:
        agent: The compiled LangGraph agent.
        user_message: The user's message text.
        history: List of previous (role, content) tuples for context.
    """
    messages = []
    for role, content in history:
        messages.append((role, content))
    messages.append(("human", user_message))

    try:
        async for event in agent.astream_events(
            {"messages": messages},
            version="v2",
        ):
            kind = event.get("event", "")

            if kind == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    yield {"type": "token", "content": chunk.content}

            elif kind == "on_tool_start":
                yield {"type": "tool_start", "name": event.get("name", "unknown")}

            elif kind == "on_tool_end":
                yield {"type": "tool_end", "name": event.get("name", "unknown")}

    except Exception as e:
        yield {"type": "error", "message": str(e)}
