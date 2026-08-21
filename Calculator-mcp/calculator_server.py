"""
A simple MCP (Model Context Protocol) server that exposes calculator
tools: add, subtract, multiply, divide, power, and sqrt.

Run it directly for a quick manual test:
    python3 calculator_server.py

To use it with Claude Code or Claude Desktop, add it to your MCP config
(see README.md in this folder for the exact JSON snippet).
"""

import math

from mcp.server.mcpserver import MCPServer

# Create the MCP server. The name shows up in client UIs.
mcp = MCPServer("calculator")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together and return the sum."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a and return the difference."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the product."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b and return the quotient. Raises an error if b is 0."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raise base to the given exponent and return the result."""
    return math.pow(base, exponent)


@mcp.tool()
def sqrt(value: float) -> float:
    """Return the square root of a non-negative number."""
    if value < 0:
        raise ValueError("Cannot take the square root of a negative number.")
    return math.sqrt(value)


if __name__ == "__main__":
    # stdio transport is the standard way local MCP servers talk to clients
    # like Claude Code / Claude Desktop.
    mcp.run()
