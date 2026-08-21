# Calculator MCP Server

A minimal MCP (Model Context Protocol) server that gives an AI client six
calculator tools: `add`, `subtract`, `multiply`, `divide`, `power`, `sqrt`.

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Test it runs

```bash
python3 calculator_server.py
```

It won't print anything and will just sit there — that's normal. MCP
servers speak over stdin/stdout to whatever client launches them, so you
won't see output when you run it standalone. Press `Ctrl+C` to stop it.

## 3. Connect it to Claude Code

Run this from your terminal (inside or outside a project — `--scope user`
makes it available everywhere):

```bash
claude mcp add calculator --scope user -- python3 /full/path/to/calculator_server.py
```

Replace `/full/path/to/calculator_server.py` with the actual path on your
machine. Then restart Claude Code (or run `/mcp` inside it) and you should
see `calculator` listed as a connected server. You can now ask Claude
things like "use the calculator tool to compute 47 * 89" and it will call
the real tool instead of doing the math itself.

## 4. Connect it to Claude Desktop (alternative)

Edit your Claude Desktop config file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python3",
      "args": ["/full/path/to/calculator_server.py"]
    }
  }
}
```

Restart Claude Desktop and the calculator tools will appear.

## Tools provided

| Tool     | Description                          |
|----------|---------------------------------------|
| add      | a + b                                 |
| subtract | a - b                                 |
| multiply | a * b                                 |
| divide   | a / b (errors on divide-by-zero)      |
| power    | base ** exponent                      |
| sqrt     | square root (errors on negative input)|
