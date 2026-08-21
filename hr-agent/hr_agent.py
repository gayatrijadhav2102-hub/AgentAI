"""
HR Agent
========
A small CLI agent that answers employee HR questions by:
  1. Spawning hr_mcp_server.py as an MCP server (stdio transport)
  2. Exposing its tools to Claude via the Anthropic Messages API
  3. Running the standard tool-use loop until Claude has a final answer

Requires:
    pip install mcp anthropic

Set your API key first:
    export ANTHROPIC_API_KEY=sk-ant-...

Usage:
    python hr_agent.py                     # interactive chat
    python hr_agent.py "How much PTO do I get?"   # single question
"""

from __future__ import annotations

import asyncio
import os
import sys
from contextlib import AsyncExitStack

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters, stdio_client

MODEL = "claude-sonnet-4-6"
SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), "hr_mcp_server.py")

SYSTEM_PROMPT = (
    "You are an HR assistant for employees. Answer questions about company "
    "policies, benefits, and general HR topics using the tools available to "
    "you -- never guess or invent specifics like day counts, dollar amounts, "
    "or eligibility rules. If a question is about personal/sensitive matters "
    "(e.g. a specific pay dispute, harassment complaint, or medical "
    "situation), be empathetic but direct the employee to contact HR "
    "directly rather than trying to resolve it yourself. Keep answers "
    "concise and cite which policy/benefit the info comes from."
)


class HRAgent:
    """Wraps an MCP client session + Anthropic client into a chat loop."""

    def __init__(self) -> None:
        self.anthropic = Anthropic()  # reads ANTHROPIC_API_KEY from env
        self.session: ClientSession | None = None
        self.tools: list[dict] = []
        self._exit_stack = AsyncExitStack()

    async def connect(self) -> None:
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[SERVER_SCRIPT],
        )
        read_stream, write_stream = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.session = await self._exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self.session.initialize()

        listed = await self.session.list_tools()
        self.tools = [
            {
                "name": t.name,
                "description": t.description or "",
                "input_schema": t.inputSchema,
            }
            for t in listed.tools
        ]

    async def close(self) -> None:
        await self._exit_stack.aclose()

    async def ask(self, question: str, history: list[dict] | None = None) -> tuple[str, list[dict]]:
        """Answer one question, running the tool-use loop as needed.

        Returns (answer_text, updated_history) so callers can keep a
        multi-turn conversation going.
        """
        assert self.session is not None, "call connect() first"

        messages = list(history or [])
        messages.append({"role": "user", "content": question})

        while True:
            response = self.anthropic.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=self.tools,
                messages=messages,
            )

            if response.stop_reason != "tool_use":
                final_text = "".join(
                    block.text for block in response.content if block.type == "text"
                )
                messages.append({"role": "assistant", "content": response.content})
                return final_text, messages

            # Model wants to call one or more tools -- execute them via MCP.
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                result = await self.session.call_tool(block.name, block.input or {})
                result_text = "\n".join(
                    part.text for part in result.content if hasattr(part, "text")
                )
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_text,
                        "is_error": bool(result.isError),
                    }
                )

            messages.append({"role": "user", "content": tool_results})


async def run_single_question(question: str) -> None:
    agent = HRAgent()
    await agent.connect()
    try:
        answer, _ = await agent.ask(question)
        print(answer)
    finally:
        await agent.close()


async def run_interactive() -> None:
    agent = HRAgent()
    await agent.connect()
    print("HR Agent ready. Ask a question (or type 'exit').\n")
    history: list[dict] = []
    try:
        while True:
            try:
                question = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not question:
                continue
            if question.lower() in {"exit", "quit"}:
                break

            answer, history = await agent.ask(question, history)
            print(f"\nHR Agent: {answer}\n")
    finally:
        await agent.close()


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "ERROR: Set ANTHROPIC_API_KEY in your environment first.\n"
            "  export ANTHROPIC_API_KEY=sk-ant-...",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        asyncio.run(run_single_question(question))
    else:
        asyncio.run(run_interactive())


if __name__ == "__main__":
    main()
