"""Smoke test: spin up hr_mcp_server.py and exercise its tools directly,
no Anthropic API key required. Run with: python test_server.py
"""

import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters, stdio_client

SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), "hr_mcp_server.py")


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=[SERVER_SCRIPT])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools available:")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description[:70]}")
            print()

            r = await session.call_tool("list_policies", {})
            print("list_policies() ->")
            print(" ", r.content[0].text)
            print()

            r = await session.call_tool("get_policy", {"policy_name": "remote work policy"})
            print("get_policy('remote work policy') ->")
            print(" ", r.content[0].text[:200], "...")
            print()

            r = await session.call_tool("search_faq", {"query": "vacation days"})
            print("search_faq('vacation days') ->")
            print(" ", r.content[0].text[:300])
            print()

            r = await session.call_tool("get_benefit", {"benefit_name": "401k"})
            print("get_benefit('401k') ->")
            print(" ", r.content[0].text[:200])
            print()

            r = await session.call_tool("search_hr_knowledge", {"query": "parental leave"})
            print("search_hr_knowledge('parental leave') ->")
            print(" ", r.content[0].text[:400])

    print("\nAll tool calls succeeded.")


if __name__ == "__main__":
    asyncio.run(main())
