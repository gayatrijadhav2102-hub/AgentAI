import os
import sys
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_community.tools import PythonREPLTool
from langgraph.prebuilt import create_react_agent
from langchain_experimental.tools import PythonREPLTool
from langchain.tools import tool

SYSTEM_PROMPT = """You  are helpful AI assitant with access to five tools:

1. **web_search** - search the internet for up-to-date information using DuckDuckGo.
2. **calculator** - Evaluate mathematical expression
3. **python_repl** - Execute Python code and return the output. Use this for tasks that need programming.
4. **get_current_datetime** - Get the current date and time in any timezone.
5. **convert_time** - convert a time from one timezone to another.

Guidelines:
- pick the most appropriate tools for each sub-task.
- For math, prefer the calculator, For complex logic or multi-step computation, use python_repl.
- Always explain your reasoning before and after using tools.
- If a tool call fails, try an alternative approach.
"""

searchtool = DuckDuckGoSearchRun(name="web_search")
python_repl = PythonREPLTool(name="python_repl")


@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result.

    This tool uses the `numexpr` library to safely compute arithmetic
    expressions such as addition, subtraction, multiplication, division,
    and other numeric operations.

    Args:
        expression (str): A valid mathematical expression as a string
                          (e.g., "2 + 3 * 5").

    Returns:
        str: The computed result in string format, or an error message
             if the evaluation fails.

    Example:
        calculator("10 / 2")
        -> "Result: 5.0"
    """

    try:
        import numexpr

        result = numexpr.evaluate(expression).item()
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


@tool
def convert_time(time_str: str, from_tz: str, to_tz: str) -> str:
    """
    Convert a time from one timezone to another.

    Args:
        time_str: Time in HH:MM (24-hour) format, e.g. "14:30"
        from_tz: Source IANA timezone, e.g. "US/Eastern"
        to_tz: Target IANA timezone, e.g. "Asia/Tokyo"

    Returns:
        str: Converted time in target timezone
    """
    from datetime import datetime
    from zoneinfo import ZoneInfo

    try:
        # Parse input time
        dt = datetime.strptime(time_str, "%H:%M")

        # Attach source timezone
        dt = dt.replace(tzinfo=ZoneInfo(from_tz))

        # Convert to target timezone
        converted = dt.astimezone(ZoneInfo(to_tz))

        return (
            f"{time_str} in {from_tz} is " f"{converted.strftime('%H:%M')} in {to_tz}"
        )

    except Exception as e:
        return f"Error: {e}"


@tool
def get_current_time(timezone: str) -> str:
    """
    Get the current date and time for a given timezone.

    Args:
        timezone: IANA timezone string (e.g., "Asia/Kolkata", "US/Eastern")

    Returns:
        str: Current date and time in the specified timezone
    """
    from datetime import datetime
    from zoneinfo import ZoneInfo

    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)

        return (
            f"Current time in {timezone}:\n"
            f"Date: {now.strftime('%Y-%m-%d (%A)')}\n"
            f"Time: {now.strftime('%H:%M:%S %Z')}"
        )

    except Exception as e:
        return f"Error: Invalid timezone '{timezone}' - {e}"


def create_agent():
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-40-mini")
    llm = ChatOpenAI(model=model, temperature=0.3, api_key=api_key)

    tools = [calculator, searchtool, convert_time, get_current_time, python_repl]

    agent = create_react_agent(model=llm, tools=tools, prompt=SYSTEM_PROMPT)

    return agent


def run_agent(agent, query: str) -> str:
    config = {"recursion_limit": 50}  # Prevents infinite loops in agent execution

    result = agent.invoke({"messages": [HumanMessage(content=query)]}, config=config)

    return result["messages"][-1].content


def run_demo():
    agent = create_agent()
    response = run_agent(agent, "what is the square root of 2 plus 2?")
    print(f"Agent:{response}")


if __name__ == "main":
    run_demo()
